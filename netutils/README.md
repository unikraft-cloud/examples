# Netutils Example image

This image contains a minimal user space environment based on Alpine Linux.
A SSH server is launched and a couple of essential networking tools such as
`nslookup`, `ping`, `traceroute`, `ip`, `socat`, and `tcpdump` are preloaded.

To run this example on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy
```

Alternatively, you can deploy the image accepting your public key by handing it over the `PUBKEY`
environment variable, for example:

```console
kraft cloud deploy  -e PUBKEY="$( cat $HOME/.ssh/id_rsa.pub )"
```

After deploying, you can connect to the console via SSH through a tunnel.
Run the command below:

```console
kraft cloud tunnel 2222:<instance-name>:22
```

Then connect to the instance via SSH using (default password is `unikraft`):

```console
ssh root@localhost -p 2222
```

## Learn more

- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
