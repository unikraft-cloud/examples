import http from "node:http";
import fs from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { pathToFileURL } from "node:url";

const templatePath: string = "/uk/libukp/template_instance";
const compiledRomPath: string = "/run/rom.compiled.mjs";

let romHandler: () => string;

function resolveRomSource(): { path: string; isTypeScript: boolean } {
  const tsPath = "/rom/rom.ts";
  if (fs.existsSync(tsPath)) {
    return { path: tsPath, isTypeScript: true };
  }

  const jsPath = "/rom/rom.js";
  if (fs.existsSync(jsPath)) {
    return { path: jsPath, isTypeScript: false };
  }

  throw new Error("No ROM module found at /rom/rom.ts or /rom/rom.js");
}

function compileTypeScript(sourcePath: string): string {
  const tsSource: string = fs.readFileSync(sourcePath, "utf-8");
  const jsSource: string = stripTypeScriptTypes(tsSource, {
    mode: "strip",
    sourceUrl: sourcePath,
  });
  fs.writeFileSync(compiledRomPath, jsSource, "utf-8");
  console.log(`compiled ${sourcePath} -> ${compiledRomPath}`);
  return compiledRomPath;
}

async function loadRomModule(): Promise<void> {
  const { path: romPath, isTypeScript } = resolveRomSource();

  const modulePath: string = isTypeScript
    ? compileTypeScript(romPath)
    : romPath;

  const romModule = await import(pathToFileURL(modulePath).href);
  romHandler = romModule.handler;
  console.log(`loaded ROM module from ${romPath}`);
}

function writeTemplateFlag(): void {
  fs.writeFileSync(templatePath, "1", { encoding: "utf-8" });
}

function parseArgs(): { host: string; port: number } {
  const args: string[] = process.argv.slice(2);
  let host: string = "0.0.0.0";
  let port: number = 8080;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--host" && i + 1 < args.length) {
      host = args[++i];
    } else if (args[i] === "--port" && i + 1 < args.length) {
      port = parseInt(args[++i], 10);
    }
  }

  return { host, port };
}

async function main(): Promise<void> {
  const { host, port } = parseArgs();

  const server = http.createServer((req, res) => {
    if (req.method === "GET") {
      res.writeHead(200, { "Content-Type": "text/plain" });
      const msg: string = romHandler();
      res.end(msg);
    } else {
      res.writeHead(405, { "Content-Type": "text/plain" });
      res.end("Method Not Allowed\n");
    }
  });

  // Initiate template creation right before loading the ROM module
  console.log("writing template flag");
  writeTemplateFlag();

  await loadRomModule();

  server.listen(port, host, () => {
    console.log(`starting server at ${host}:${port}`);
  });
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`failed to start server: ${message}`);
  process.exit(1);
});
