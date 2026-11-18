# Persistent Volumes on Unikraft Cloud

This guide demonstrates how to provision, attach, inspect and manage persistent block storage volumes for Unikraft Cloud instances.
This allows applications like databases or file servers to retain state across restarts and re-deployments.

What you’ll learn:
- Create a persistent volume;
- List active and unattached volumes;
- Deploy an instance with a mounted volume;
- Inspect volume status and metrics;
- Import data into volumes;
- Detach and delete persistent volumes;

For this tutorial, we will be using the Kraft/Unikraft CLI and direct HTTP requests using the Unikraft Cloud Platform API.

Contents of the current directory:
- `app_storage.c`: Simple application written in C that reads, writes and logs persistent data to /data.
- `Dockerfile`: builds the application binary.
- `Kraftfile`: used for building and packaging the Unikernel.
- `ukc.config`: necessary for using Kraft CLI, you must give your own values to the `UKC_USER`, `UKC_METRO` and `UKC_TOKEN` variables.
It can also come in handy even if you're using the Unikraft CLI.
- `README.md`: documentation
- api/: directory with helper scripts for API calls to Unikraft Cloud.


## Setup

You must make sure that you have Kraft or Unikraft CLI, Docker and an active Unikraft Cloud account, including an API token.
Once you’ve entered your credentials into `ukc.config`, enter the following command:

	source ukc.config

## Starting

#### Kraft CLI:

```console
source ukc.config

# 1. Create a 9MB persistent volume
kraft cloud volume create --size 9M --name storage-vol-01

# 2. Build before package
kraft build --plat kraftcloud --arch x86_64

# 3. Package and push the application image
kraft pkg --plat kraftcloud --arch x86_64 --name index.unikraft.io/"$UKC_USER"/storage-app:latest .
kraft pkg push index.unikraft.io/"$UKC_USER"/storage-app:latest

# 4. Deploy instance with volume attached at /data
kraft cloud instance create \
--memory 256M \
--volume storage-vol-01:/data \
--name storage-demo \
index.unikraft.io/"$UKC_USER"/storage-app:latest

# 5. Start instance and check persistent logs
kraft cloud instance start storage-demo
kraft cloud instance logs storage-demo

# 6. Cleanup
kraft cloud instance stop storage-demo
kraft cloud instance delete storage-demo
kraft cloud volume delete storage-vol-01
```	

#### Unikraft CLI:

```console
unikraft login

# 1. Create a 9MiB persistent volume
unikraft volumes create --name storage-vol-01 --size 9M --metro was

# 2. Build and publish the application image
unikraft build . --no-cache --output "$UKC_USER"/storage-app:latest

# 3. Deploy instance with volume attached at /data
unikraft instances create --name storage-demo --metro was --memory 256MiB --volume storage-vol-01:/data --image "$UKC_USER"/storage-app:latest --autostart

# 4. Check persistent logs
unikraft instances logs storage-demo

# 5. Cleanup
unikraft instances stop storage-demo
unikraft instances delete storage-demo
unikraft volumes delete storage-vol-01 --force
```

## Using Unikraft Cloud API

```console
./api/create-volume.sh
./api/list-volumes.sh
./api/attach-volume-deploy.sh
./api/get-volume-info.sh
./api/delete-volume.sh
```

## CLI Guide

### Create a persistent volume

For this example, we will create a volume of 9MB:

#### Kraft:

```console
kraft cloud volume create --size 9M storage-vol-01
```

#### Unikraft:

```console
unikraft volumes create --name storage-vol-01 --size 9M --metro was
```

### List Volumes

This command will list all persistent volumes on your account:

#### Kraft:

```console
kraft cloud volume list
```

#### Unikraft:

```console
unikraft volumes list
```

### Deploy Instance with Mounted Volume:

Attach the volume during instance creation using the --volume flag with the syntax: `VOLUME_NAME:MOUNT_PATH`

#### Kraft:

Read and Write Mount:

```console
kraft cloud instance create \
--memory 256M \
--volume storage-vol-01:/data \
--name storage-demo \
index.unikraft.io/"$UKC_USER"/storage-app:latest
```
Read Only Mount:

```console
kraft cloud instance create \
--memory 256M \
--volume storage-vol-01:/data:ro \
--name storage-demo-ro \
index.unikraft.io/"$UKC_USER"/storage-app:latest
```

#### Unikraft:

Read and Write Mount:

```console
unikraft instances create --name storage-demo --metro was --memory 256MiB --volume storage-vol-01:/data --image dan-andrei-simionescu/storage-app:latest --autostart
```

Read Only Mount:

```console
unikraft instances create --name storage-demo --metro was --memory 256MiB --volume storage-vol-01:/data:ro --image dan-andrei-simionescu/storage-app:latest --autostart
```

### Inspect Volume Details

To view detailed state, attachment details and health metrics:

#### Kraft:

```console
kraft cloud volume get storage-vol-01
```

#### Unikraft:

```console
unikraft volumes get storage-vol-01
```

### Detach and Delete Volumes

Be careful, volumes attached to active or stopped instances cannot be deleted directly, you must remove the instance first or explicitly detach the volume:

#### Kraft:

```console
kraft cloud instance delete storage-demo
```

or

```console
kraft cloud volume delete storage-vol-01
```

#### Unikraft:

```console
unikraft instances delete storage-demo
```

or

```console
unikraft volumes delete storage-vol-01 --force
```
