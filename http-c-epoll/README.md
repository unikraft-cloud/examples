# Simple epoll-based Echo Reply C Server

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, simply invoke:

```console
kraft cloud deploy -p 42424:42424/tls .
```

To use the application, connect to the remote URL (provided by the above command):

```console
openssl s_client -connect <url>:42424
```

Replace `<url>` with the URL provided by the `kraft cloud deploy` command.
Send out messages to be replied by the epoll-based server.

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
