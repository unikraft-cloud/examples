import { createRequestHandler } from "@react-router/express";
import compression from "compression";
import express from "express";
import morgan from "morgan";

const app = express();

app.use(compression());

// http://expressjs.com/en/advanced/best-practice-security.html#at-a-minimum-disable-x-powered-by-header
app.disable("x-powered-by");

// Assets with fingerprinted filenames can be cached forever.
app.use(
  "/assets",
  express.static("build/client/assets", { immutable: true, maxAge: "1y" })
);

// Everything else (like favicon.ico) is cached for an hour.
app.use(express.static("build/client", { maxAge: "1h" }));

app.use(morgan("tiny"));

app.all(
  "/{*splat}",
  createRequestHandler({
    build: () => import("./build/server/index.js"),
  })
);

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Express server listening at http://localhost:${port}`);
});

