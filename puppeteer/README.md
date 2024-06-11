# Puppeteer

[Puppeteer](https://pptr.dev/) is a Node.js library which provides a high-level API to control browsers, including the option to run them headless (no UI).

To run Puppeteer on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 4096 .
```

The command will deploy the files in the current directory.
It will run the `pdf.js` example.
Note that this example won't give you access the generated PDF file.
To be able to extract the result, you will have to create a service-like implementation on top of the Puppeteer API that can be queried remotely.

To check it worked, use:

```console
kraft cloud inst logs $(kraft cloud inst ls | grep puppeteer | cut -d ' ' -f 1)
```

## Learn more

- [Puppeteer's Documentation](is a Node.js library which provides a high-level API to control)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
