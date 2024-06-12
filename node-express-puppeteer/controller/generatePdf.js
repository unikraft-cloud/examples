const puppeteer = require("puppeteer");

const generatePdf = async (type, payload) => {
  // Browser actions & buffer creator
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"], // SEE BELOW WARNING!!!
  });

  if (type === 'url') {
    const page = await browser.newPage();
    await page.goto(payload);
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
