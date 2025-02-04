# Node 21 WebSocket Server

[WebSocket](https://en.wikipedia.org/wiki/WebSocket) is a bidirectional communication protocol over TCP, compatible with HTTP.
This example builds an echo-reply WebSocket server in [Node](https://nodejs.org/en).

To run the Node WebSocket server on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 -M 1Gi .
```

The command will build the files in the current directory.

After deploying, you can query the service with a WebSocket client, such as [`wscat`](https://github.com/websockets/wscat).
Install `wscat` with `npm`:

```console
npm install -g wscat
```

Then query the WebSocket server deployed on Unikraft Cloud, using its URL:

```console
wscat --connect wss://<NAME>.<METRO>.kraft.host
```

Then enter messages, that will be replied by the server.

## Learn more

- [WebSocket documentation](https://nextjs.org/docs)
- [ws: A Node.js WebSocket library](https://github.com/websockets/ws)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
