const puppeteer = require("puppeteer");
const { URL } = require("url");

const ALLOWED_PROTOCOLS = ["http:", "https:"];

function validateUrl(input) {
  let parsed;
  try {
    parsed = new URL(input);
  } catch {
    throw new Error("Invalid URL");
  }
  if (!ALLOWED_PROTOCOLS.includes(parsed.protocol)) {
    throw new Error("Only http and https URLs are allowed");
  }
  // Block private/internal IPs to prevent SSRF
  const hostname = parsed.hostname;
  if (
    hostname === "localhost" ||
    hostname === "127.0.0.1" ||
    hostname === "::1" ||
    hostname === "0.0.0.0" ||
    hostname.endsWith(".local") ||
    hostname.startsWith("10.") ||
    hostname.startsWith("192.168.") ||
    /^172\.(1[6-9]|2\d|3[0-1])\./.test(hostname) ||
    hostname === "[::1]" ||
    hostname.startsWith("169.254.")
  ) {
    throw new Error("URLs pointing to internal addresses are not allowed");
  }
  return parsed.href;
}

const generatePdf = async (type, payload) => {
  // Browser actions & buffer creator
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"], // SEE BELOW WARNING!!!
  });

  if (type === 'url') {
    const safeUrl = validateUrl(payload);
    const page = await browser.newPage();
    await page.goto(safeUrl);
    const pdf = await page.pdf();
    await browser.close();
    // Return Buffer
    return pdf;
  }

  if (type === 'base64') {
    const page = await browser.newPage();
    await page.goto(`data:text/html;base64,${payload}`);
    const pdf = await page.pdf();
    await browser.close();
    // Return Buffer
    return pdf;
  }

};

/******************** WARNING ********************* WARNING ********************* WARNING *********************

 If you absolutely trust the content you open in Chrome, you can launch Chrome with the --no-sandbox argument...
 Running without a sandbox is strongly discouraged. Consider configuring a sandbox instead!!!

 More Info Here: https://github.com/GoogleChrome/puppeteer/blob/master/docs/troubleshooting.md

******************** WARNING ********************* WARNING ********************* WARNING *********************/

module.exports = generatePdf;
