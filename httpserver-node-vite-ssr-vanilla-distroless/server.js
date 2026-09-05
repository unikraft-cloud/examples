import fs from 'node:fs/promises'
import express from 'express'
import rateLimit from 'express-rate-limit'

// Constants
const isProduction = process.env.NODE_ENV === 'production'
const port = process.env.PORT || 8080
const base = process.env.BASE || '/'

// Cached production assets
const templateHtml = isProduction
  ? await fs.readFile('./dist/client/index.html', 'utf-8')
  : ''

// Create http server
const app = express()

// Rate limiting middlewares
app.set('trust proxy', 1)
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
  message: "Too many requests, please try again later.",
  validate: {
    trustProxy: false, // This should not be used in production !! (check out https://express-rate-limit.mintlify.app/guides/troubleshooting-proxy-issues)
  },
});
app.use(limiter)

// Add Vite or respective production middlewares
/** @type {import('vite').ViteDevServer | undefined} */
let vite
if (!isProduction) {
  const { createServer } = await import('vite')
  vite = await createServer({
    server: {
      middlewareMode: true,

      // Setting server.allowedHosts to true allows any website to send requests
      // to your dev server through DNS rebinding attacks, allowing them to
      // download your source code and content. We recommend always using an
      // explicit list of allowed hosts.
      //
      // See GHSA-vg6x-rcgg-rjx6 for more details[0].
      //
      // [0]: https://vite.dev/config/server-options.html#server-allowedhosts
      allowedHosts: true
    },
    appType: 'custom',
    base,
  })
  app.use(vite.middlewares)
} else {
  const compression = (await import('compression')).default
  const sirv = (await import('sirv')).default
  app.use(compression())
  app.use(base, sirv('./dist/client', { extensions: [] }))
}

// Serve HTML
app.use('*all', async (req, res) => {
  try {
    const url = req.originalUrl.replace(base, '')

    /** @type {string} */
    let template
    /** @type {import('./src/entry-server.js').render} */
    let render
    if (!isProduction) {
      // Always read fresh template in development
      template = await fs.readFile('./index.html', 'utf-8')
      template = await vite.transformIndexHtml(url, template)
      render = (await vite.ssrLoadModule('/src/entry-server.js')).render
    } else {
      template = templateHtml
      render = (await import('./dist/server/entry-server.js')).render
    }

    const rendered = await render(url)

    const html = template
      .replace(`<!--app-head-->`, rendered.head ?? '')
      .replace(`<!--app-html-->`, rendered.html ?? '')

    res.status(200).set({ 'Content-Type': 'text/html' }).send(html)
  } catch (e) {
    vite?.ssrFixStacktrace(e)
    console.log(e.stack)
    res.status(500).end('An internal server error occurred.')
  }
})

// Start http server
app.listen(port, () => {
  console.log(`Server started at http://0.0.0.0:${port}`)
})
