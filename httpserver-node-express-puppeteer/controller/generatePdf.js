const puppeteer = require("puppeteer");
const { URL } = require("url");
const dns = require("dns");
const { promisify } = require("util");
const net = require("net");

const dnsLookup = promisify(dns.lookup);

// Allowlist of hostnames that can be requested.
// Configure via the ALLOWED_HOSTNAMES environment variable (comma-separated).
const ALLOWED_HOSTNAMES = new Set(
  (process.env.ALLOWED_HOSTNAMES || "example.com,www.example.com")
    .split(",")
    .map((h) => h.trim().toLowerCase())
    .filter(Boolean)
);

// Check if an IP address is private/internal
function isPrivateIP(ip) {
  // IPv4 private ranges and special addresses
  const parts = ip.split('.').map(Number);
  if (parts.length === 4) {
    if (parts[0] === 10) return true;                                    // 10.0.0.0/8
    if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true; // 172.16.0.0/12
    if (parts[0] === 192 && parts[1] === 168) return true;              // 192.168.0.0/16
    if (parts[0] === 127) return true;                                    // 127.0.0.0/8
    if (parts[0] === 169 && parts[1] === 254) return true;              // 169.254.0.0/16 (link-local/cloud metadata)
    if (parts[0] === 0) return true;                                      // 0.0.0.0/8
  }
  // IPv6 loopback and private
  if (net.isIPv6(ip)) {
    if (ip === '::1') return true;
    if (ip.startsWith('fc') || ip.startsWith('fd')) return true;          // ULA
    if (ip.startsWith('fe80')) return true;                               // link-local
  }
  return false;
}

// Validate that a URL is safe for server-side requests
async function validateUrl(urlString) {
  let parsed;
  try {
    parsed = new URL(urlString);
  } catch {
    throw new Error("Invalid URL");
  }

  // Only allow http and https schemes
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    throw new Error("Only http and https URLs are allowed");
  }

  // Enforce hostname allowlist so user input cannot select arbitrary destinations
  const hostname = parsed.hostname.toLowerCase();
  if (!ALLOWED_HOSTNAMES.has(hostname)) {
    throw new Error("Hostname is not allowed");
  }

  // Resolve hostname and check for private IPs
  if (net.isIP(hostname)) {
    if (isPrivateIP(hostname)) {
      throw new Error("Requests to private/internal addresses are not allowed");
    }
  } else {
    const { address } = await dnsLookup(hostname);
    if (isPrivateIP(address)) {
      throw new Error("Requests to private/internal addresses are not allowed");
    }
  }

  return parsed.href;
}

const generatePdf = async (type, payload) => {
  // Browser actions & buffer creator
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"], // SEE BELOW WARNING!!!
  });

  if (type === 'url') {
    const safeUrl = await validateUrl(payload);
    const safeTarget = new URL(safeUrl);
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', (request) => {
      try {
        const requestUrl = new URL(request.url());
        const isHttp = requestUrl.protocol === 'http:' || requestUrl.protocol === 'https:';
        const sameHost = requestUrl.hostname.toLowerCase() === safeTarget.hostname.toLowerCase();
        if (isHttp && sameHost) {
          request.continue();
        } else {
          request.abort();
        }
      } catch {
        request.abort();
      }
    });
    await page.goto(safeUrl);
    const pdf = await page.pdf();
    await browser.close();
    // Return Buffer
    return pdf;
  }

  if (type === 'base64') {
    const page = await browser.newPage();
    // Block all network requests to prevent SSRF via embedded HTML content
    await page.setRequestInterception(true);
    page.on('request', (request) => {
      if (request.url().startsWith('data:')) {
        request.continue();
      } else {
        request.abort();
      }
    });
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
