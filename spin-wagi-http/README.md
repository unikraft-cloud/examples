# Spin Wagi HTTP example

This example is derived from [Spin's `spin-wagi-http` example](https://github.com/fermyon/spin/tree/v2.1.0/examples/spin-wagi-http) and shows how to run a Spin application serving routes from two programs written in different languages (Rust and C++) using both the Spin executor and the Wagi executor on KraftCloud.

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, simply invoke:

```
kraft cloud deploy -p 443:3000 -M 2048 .
```

Then `curl` the hello route:

```
$ curl -i https://little-bird-4f8zuwj5.fra0.kraft.cloud/hello
HTTP/1.1 200 OK
content-type: application/text
content-length: 7
date: Thu, 10 Mar 2022 21:38:34 GMT

Hello
```

And `curl` the goodbye route:

```
$ curl -i https://little-bird-4f8zuwj5.fra0.kraft.cloud/goodbye
HTTP/1.1 200 OK
foo: bar
content-length: 7
date: Thu, 10 Mar 2022 21:38:58 GMT

Goodbye
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
