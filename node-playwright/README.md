# Playwright with Node.js on Unikraft Cloud

[Playwright](https://playwright.dev/) is a framework for web testing and Automation.

To run Playwright with Node.js on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy -M 4096 -p 443:8080 .
```

The command will deploy the files in the current directory.
It results in the creation of a remote web-based service for creating PNG screenshots of remote pages.

Use the `?page=<REMOTE_URL>` to point the service to the remote page to screenshot.
Query the service using commands such as:

```console
curl https://<NAME>.<METRO>.kraft.host/?page=https://google.com -o ss-google.png
curl https://<NAME>.<METRO>.kraft.host/?page=https://bing.com -o ss-bing.png
```

## Learn more

- [Playwright's Documentation](https://playwright.dev/docs/intro)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
