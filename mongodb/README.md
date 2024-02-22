# MongoDB

This examples demonstrates how to use [MongoDB](https://www.mongodb.com), a source-available, cross-platform, document-oriented database program.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 27017:27017/tls -M 1024 .
```

To connect, you first need to create a tunnel to the remote server (save the returned PID):
```console
socat tcp-listen:27017,bind=127.0.0.1,fork,reuseaddr openssl:solitary-breeze-ou8bygcn.dal0.kraft.cloud:27017 &
```

Then you can use the `mongo` client to connect to the server:
```console
mongosh mongodb://localhost
```

To disconnect, simply kill the `socat` process:
```console
kill -9 <PID>
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
