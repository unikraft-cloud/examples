import { PuppeteerCrawler, Request, Configuration } from 'crawlee';

// Create configuration.
//const config = new Configuration({disableBrowserSandbox: true, headless: true, chromeExecutablePath: '/home/razvan/orgs/unikraft-io/examples/puppeteer-scraper/chrome/linux-128.0.6613.119/chrome-linux64/chrome'});
const config = new Configuration({disableBrowserSandbox: true, headless: true});

const crawler = new PuppeteerCrawler({
    async requestHandler({ request, page, enqueueLinks }) {
        const title = await page.title();
        console.log(`Title of ${request.url}: ${title}`);

        await enqueueLinks({
            pseudoUrls: ['https://www.iana.org/[.*]'],
        });
    },
    maxRequestsPerCrawl: 10,
}, config);

await crawler.run(['https://www.iana.org/']);
