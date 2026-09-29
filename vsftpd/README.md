# vsftpd

This guide explains how to create and deploy a [vsftpd](https://security.appspot.com/vsftpd.html) app, to secure access to the files of your VM.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/vsftpd` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/vsftpd/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft volume create --set metro=fra --set name=vsftpd-workspace --set size=1G

unikraft build . --output <my-org>/vsftpd:latest
unikraft run --metro fra \
  -m 1G \
  -p 20:20/tls \
  -p 21:21/tls \
  -p 222:22/tls \
  -p 990:990/tls \
  -p 10100:10100/tls \
  --scale-to-zero policy=on,cooldown-time=40000,stateful=true \
  --volume vsftpd-workspace:/root \
  --image <my-org>/vsftpd:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         vsftpd
uuid:         186a46a0-7c89-4bfd-83a8-649bcc60a96e
state:        starting
image:        <my-org>/vsftpd
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       4814b43a-c1d3-48f0-ef3e-9dba8bcaba25
  name:       broken-orangutan-jypu2z53
  domains:
  - fqdn:     broken-orangutan-jypu2z53.fra.unikraft.app
networks:
- uuid:       6adc6c29-5c9b-e472-70ff-fc3f3816d5a2
  private-ip: 10.0.0.109
  mac:        12:b0:17:ff:e4:c7
timestamps:
  created:    just now
```

This will create a volume for data persistence, and mount it at `/root` inside the VM.

In this case, the instance name is `vsftpd` and the address is `https://broken-orangutan-jypu2z53.fra.unikraft.app`.
The name was preset, but the address is different for each run.

**Note**: The `root` password defaults to `rootpass`.
Don't forget to change it inside the `Dockerfile` and update the commands below.

You can access the FTP server using a client like `lftp`:

```bash
lftp -u root,rootpass ftps://broken-orangutan-jypu2z53.fra.unikraft.app:21
lftp root@broken-orangutan-jypu2z53.fra.unikraft.app:~> ls
```

You can list information about the volume by running:

```bash title="unikraft"
unikraft volumes list
```

```ansi title="unikraft"
METRO  NAME              STATE    SIZE    CREATED
fra    vsftpd-workspace  mounted  1.0GiB  9 minutes ago
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME    STATE    IMAGE            ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    vsftpd  standby  <my-org>/vsftpd        1.0GiB  1      broken-orangutan-jypu2z53.fra.unikraf…  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete vsftpd
```

The volume isn't removed by default, so you can recreate the instance and still have access to your old data.
Remove it using:

```bash title="unikraft"
unikraft volume delete vsftpd-workspace
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
