# MongoDB

[MongoDB](https://www.mongodb.com) is a source-available, cross-platform, document-oriented database program.

To run MongoDB on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 27017:27017/tls -M 1024 .
```

To connect, you first need to create a tunnel to the remote server (save the returned PID):

```console
socat tcp-listen:27017,bind=127.0.0.1,fork,reuseaddr openssl:<NAME>.<METRO>.kraft.cloud:27017 &
```

Then you can use the `mongo` client to connect to the server:

```console
mongosh mongodb://localhost
```

To stop the `socat` process, run:

```console
kill -9 <PID>
```

## Learn more

- [MongoDB's Documentation](https://www.mongodb.com/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
