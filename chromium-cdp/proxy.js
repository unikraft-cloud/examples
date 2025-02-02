const {chromium} = require('playwright');
var http = require('http');
var httpProxy = require('http-proxy');
var modifyResponse = require('node-http-proxy-json');

const port = 8080; // Use port 8080 by default
const cdp_host = '127.0.0.1';
const cdp_port = 9222;

//
// Launch Chromium browser with CDP enabled.
//
chromium.launch({headless: true, args: [`--remote-debugging-port=${cdp_port}`]})

//
// Set up our server to proxy standard HTTP requests.
//
var proxy = new httpProxy.createProxyServer({
    target: {
        host: cdp_host,
        port: cdp_port
    }
});
var proxyServer = http.createServer(function (req, res) {
    req.headers['host'] = `${cdp_host}:${cdp_port}`;
    proxy.web(req, res);
});

//
// Listen for the `proxyRes` event on `proxy`.
// Update WebSocket URL in JSON response from Chrome CDP.
//
proxy.on('proxyRes', function (proxyRes, req, res) {
    if (res.req.url.startsWith("/json")) {
        const isHost = (element) => element == 'Host';
        host = res.req.rawHeaders[res.req.rawHeaders.findIndex(isHost)+1];

        modifyResponse(res, proxyRes, function (body) {
            if (body) {
                body.webSocketDebuggerUrl = body.webSocketDebuggerUrl.replace(`${cdp_host}:${cdp_port}`, host);
                body.webSocketDebuggerUrl = body.webSocketDebuggerUrl.replace("ws://", "wss://");
            }
            return body; // return value can be a promise
        });

        res.setHeader('Host', host);
    }
});

//
// Listen to the `upgrade` event and proxy the
// WebSocket requests as well.
//
proxyServer.on('upgrade', function (req, socket, head) {
    proxy.ws(req, socket, head);
});

proxyServer.listen(port, () => {
    console.log('Server is running on port ' + port);
});
