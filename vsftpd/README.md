# Very Secure FTP Daemon

This guide explains how to create and deploy a [vsftpd](https://security.appspot.com/vsftpd.html) app, to secure access to the files of your VM.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/vsftpd` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/vsftpd/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following commands to deploy the app on Unikraft Cloud:

```bash
kraft cloud volume create \
    --name vsftpd-workspace \
    --size 1Gi

kraft cloud deploy \
    --scale-to-zero on \
    --scale-to-zero-stateful \
    --scale-to-zero-cooldown 3s \
    --name vsftpd \
    -M 1024Mi \
    -p 20:20/tls \
    -p 21:21/tls \
    -p 222:22/tls \
    -p 990:990/tls \
    -p 10100:10100/tls \
    -v "vsftpd-workspace":/root \
    .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├─────── name: vsftpd
 ├─────── uuid: 186a46a0-7c89-4bfd-83a8-649bcc60a96e
 ├────── metro: https://api.fra.unikraft.cloud/v1
 ├────── state: starting
 ├───── domain: broken-orangutan-jypu2z53.fra.unikraft.app
 ├────── image: vsftpd@sha256:31aad1619c31f499b11f1bef8fead6e6df76f235a57add011e5e414a3f51ee64 
 ├───── memory: 1024 MiB
 ├──── service: broken-orangutan-jypu2z53
 ├─ private ip: 10.0.0.109
 └─────── args: /wrapper.sh
```

This will create a volume for data persistence, and mount it at `/root` inside the VM.

In this case, the instance name is `vsftpd` and the address is `https://broken-orangutan-jypu2z53.fra.unikraft.app`.
The name was preset, but the address is different for each run.

**Note**: The password for the `root` user is set to `rootpass`. Do not forget to change it inside the `Dockerfile` and update the commands below.

You can access the FTP server using a client like `lftp`:

```bash
lftp -u root,rootpass ftps://broken-orangutan-jypu2z53.fra.unikraft.app:21
lftp root@broken-orangutan-jypu2z53.fra.unikraft.app:~> ls
```

You can list information about the volume by running:

```bash
kraft cloud volume list
```

```text
NAME              CREATED AT     SIZE     ATTACHED TO  MOUNTED BY  STATE    PERSISTENT
vsftpd-workspace  9 minutes ago  1.0 GiB  vsftpd       vsftpd      mounted  true
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME    FQDN                                        STATE    STATUS   IMAGE                                        MEMORY   VCPUS  ARGS         BOOT TIME
vsftpd  broken-orangutan-jypu2z53.fra.unikraft.app  standby  standby  vsftpd@sha256:3c448f1e1596a2f017871aa9a7...  1.0 GiB  1      /wrapper.sh  7.19 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove vsftpd
```

The volume is not removed by default, so you can recreate the instance and still have access to your old data. Remove it using:

```bash
kraft cloud volume remove vsftpd-workspace
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
