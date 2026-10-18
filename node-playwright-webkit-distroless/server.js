const http = require('http'); // Loads the http module
const url = require('url'); // Parse the HTTP URL
const {webkit} = require('playwright'); // Get Webkit headless browser

const port = 8080; // Use port 8080 by default

const requestListener = function (request, response) {

    // Get information object of request URL
    const parsedURL = url.parse(request.url, true);

    // Check for `page` GET variable
    if (parsedURL.pathname === '/' && parsedURL.query.page) {
        remote = parsedURL.query.page;

        // Anonymous function to call Playwright
        (async () => {
            try {
                const browser = await webkit.launch({headless: true});
                const page = await browser.newPage();
                await page.goto(remote);
                const buffer = await page.screenshot();

                await browser.close();

                // Tell the browser everything is OK (Status code 200), and the data is PNG
                response.writeHead(200, {
                    'Content-Type': 'image/png'
                });

                // Write image buffer to the body of the response
                response.write(buffer, 'binary');
                response.end();
            } catch(err) {
                // In case of error, send a text message
                response.writeHead(200, {
                    'Content-Type': 'text/plain'
                });

                // Write the error text to the body of the response
                response.write('Error' + err + '.\n');
                response.end();
            }
        })()

        return;
    }

    // If no HTTP GET variable, tell the browser everything is OK (Status code 200), and the data is in plain text
    response.writeHead(200, {
        'Content-Type': 'text/plain'
    });

    // Write a simple text to the body of the page
    response.write('Nothing to do.\n');
    response.end();

}

// Fire up server, show banner message and wait for connections
const server = http.createServer(requestListener);
server.listen(port, () => {
    console.log('Server is running on port ' + port);
});
