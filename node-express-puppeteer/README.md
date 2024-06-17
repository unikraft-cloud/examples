# Node Express Puppeteer Puppeteer

[Puppeteer](https://pptr.dev/) is a Node.js library which provides a high-level API to control browsers, including the option to run them headless (no UI).

To run Puppeteer on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 4096 .
```

The command will deploy the files in the current directory.
The application and the landing page are part of [this repository](https://github.com/christopher-talke/node-express-puppeteer-pdf-example).
It uses the [ExpressJS framework](https://expressjs.com/).

It results in the creation of a remote web-based service for generating PDF files from browsers.
Use a browser to access the URL shown by the command above.
And then use the interface to generate PDF files.

## Learn more

- [Puppeteer's Documentation](is a Node.js library which provides a high-level API to control)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
