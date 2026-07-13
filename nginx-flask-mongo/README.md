# Flask with MongoDB

[Flask](https://flask.palletsprojects.com/en/stable/) is a lightweight WSGI web application framework in Python, and [MongoDB](https://www.mongodb.com/) is a NoSQL database that stores data in JSON-like documents.
This example deploys three services on Unikraft Cloud: NGINX (reverse proxy), Flask (backend), and MongoDB (database).

**Credits**: This example is based on this [Awesome Compose example](https://github.com/docker/awesome-compose/tree/master/nginx-flask-mongo).

## Deployment

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/nginx-flask-mongo` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/nginx-flask-mongo/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft login
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

## MongoDB

Create a volume for MongoDB data persistence:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --metro fra --name mongo-data --size 1G
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name mongo-data --size 1Gi
```

You can list the created volume by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume list
```

```ansi title="unikraft"
METRO  NAME        STATE      SIZE  CREATED
fra    mongo-data  available  1GiB  just now
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume list
```

```ansi title="kraft"
NAME        CREATED AT  SIZE     ATTACHED TO  MOUNTED BY  STATE      PERSISTENT
mongo-data  now         1.0 GiB                           available  true
```

First, deploy the MongoDB instance.
MongoDB is an internal service (not publicly accessible), reached via the `mongo.internal` domain:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./mongo --output <my-org>/mongo:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -m 1024M --image <my-org>/mongo:latest --domain mongo.internal --volume mongo-data:/data/db
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -M 1024Mi --domain mongo.internal --volume mongo-data:/data/db ./mongo
```

The output shows the MongoDB instance details:

**Using the unikraft CLI (Recommended)**
```text title="unikraft"
metro:           fra
name:            mongo-o3qhq
uuid:            90158c53-6654-4e73-bad1-1d6ab4452001
state:           starting
image:           <my-org>/mongo
resources:
  memory:        1GiB
  vcpus:         1
service:
  name:          restless-glade-l8pu2mf0
  uuid:          77a04441-2479-433a-b468-32f23e475f58
  domains:
  - fqdn:        mongo.internal
volumes:
- name:          mongo-data
  uuid:          9c7723f3-7e1f-4e06-afe6-c811240faf5a
  at:            /data/db
networks:
- uuid:          4f891227-d381-42f4-88a4-25a97b95a9e3
  private-ip:    10.0.15.21
  mac:           12:b0:0a:00:0f:15
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        idle
  stateful:      true
  cooldown-time: 1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: mongo-o3qhq
 ├───────── uuid: 90158c53-6654-4e73-bad1-1d6ab4452001
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: mongo.internal
 ├──────── image: oci://unikraft.io/<my-org>/mongo@sha256:68894454735e0e5b07d61aad19b1c03355f415ec33c050daeaa419d931962657
 ├─────── memory: 1024 MiB
 ├────── service: restless-glade-l8pu2mf0
 ├─ private fqdn: mongo-o3qhq.internal
 └─── private ip: 10.0.15.21
```

## Flask

Next, deploy the Flask backend.
It connects to MongoDB using the `MONGO_SERVER_URL` environment variable and is reached internally via `backend.internal`.
If you change this domain, set `BACKEND_HOST` on the NGINX instance to the same value.

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./flask --output <my-org>/flask:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -m 1024M --image <my-org>/flask:latest --domain backend.internal --env FLASK_SERVER_PORT=9091 --env MONGO_SERVER_URL=mongo.internal:27017
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -M 1024Mi --domain backend.internal --env FLASK_SERVER_PORT=9091 --env MONGO_SERVER_URL=mongo.internal:27017 ./flask
```

The output shows the Flask instance details:

**Using the unikraft CLI (Recommended)**
```text title="unikraft"
metro:                 fra
name:                  flask-9a68z
uuid:                  bb6d91f7-0714-45e5-b14a-ec82a5dac36e
state:                 starting
image:                 <my-org>/flask
runtime:
  env:
    FLASK_SERVER_PORT: 9091
    MONGO_SERVER_URL:  mongo.internal:27017
resources:
  memory:              1GiB
  vcpus:               1
service:
  name:                broken-bird-8isa6q21
  uuid:                cd9fe757-784a-49d4-8936-1b6859b3a72d
  domains:
  - fqdn:              backend.internal
networks:
- uuid:                2da7f679-7067-4fb5-908b-853607d383f2
  private-ip:          10.0.17.97
  mac:                 12:b0:0a:00:11:61
timestamps:
  created:             just now
scale-to-zero:
  enabled:             true
  policy:              on
  cooldown-time:       1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: flask-9a68z
 ├───────── uuid: bb6d91f7-0714-45e5-b14a-ec82a5dac36e
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: backend.internal
 ├──────── image: oci://unikraft.io/<my-org>/flask@sha256:f23b3368cd777acae68ad8f35713a4cf55f901d6c266017bf6f0679ffc7a8172
 ├─────── memory: 1024 MiB
 ├────── service: broken-bird-8isa6q21
 ├─ private fqdn: flask-9a68z.internal
 └─── private ip: 10.0.17.97
```

## NGINX

Finally, deploy NGINX as the public-facing reverse proxy.
It forwards requests to the Flask backend at `backend.internal:9091` by default.
The backend domain can be changed with the `BACKEND_HOST` environment variable;
if you use a different value, make sure it matches the domain you assign to the
Flask instance.

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./nginx --output <my-org>/nginx:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:80/tls+http -m 512M --image <my-org>/nginx:latest -e BACKEND_HOST=backend.internal
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:80/tls+http -M 512Mi --env BACKEND_HOST=backend.internal ./nginx
```

The output shows the NGINX instance details including its public FQDN:

**Using the unikraft CLI (Recommended)**
```text title="unikraft"
metro:           fra
name:            nginx-jnpwi
uuid:            57f64e99-bd06-46fd-98f4-26b64751623e
state:           starting
image:           <my-org>/nginx
resources:
  memory:        512MiB
  vcpus:         1
service:
  name:          snowy-river-gotjeojl
  uuid:          287ee3b8-43bc-47d1-a88e-4d6c72d2d682
  domains:
  - fqdn:        snowy-river-gotjeojl.fra.unikraft.app
networks:
- uuid:          107e4a03-e285-4d1d-84cb-24f86d7af875
  private-ip:    10.0.14.201
  mac:           12:b0:0a:00:0e:c9
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        on
  cooldown-time: 1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: nginx-jnpwi
 ├───────── uuid: 57f64e99-bd06-46fd-98f4-26b64751623e
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://snowy-river-gotjeojl.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/nginx@sha256:8cff54392eeead80bafe33538866b04bfd076f2052d65cb3751a938a22368bc0
 ├─────── memory: 512 MiB
 ├────── service: snowy-river-gotjeojl
 ├─ private fqdn: nginx-jnpwi.internal
 └─── private ip: 10.0.14.201
```

You can list all deployed instances with:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```text title="unikraft"
METRO  NAME         STATE    IMAGE           MEMORY  VCPUS  FQDN                                   CREATED
fra    nginx-jnpwi  standby  <my-org>/nginx  512MiB  1      snowy-river-gotjeojl.fra.unikraft.app  11 minutes ago
fra    flask-9a68z  standby  <my-org>/flask  1GiB    1      backend.internal                       12 minutes ago
fra    mongo-o3qhq  standby  <my-org>/mongo  1GiB    1      mongo.internal                         14 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME         FQDN                                   STATE    STATUS       IMAGE                                         MEMORY   VCPUS  ARGS  BOOT TIME
nginx-jnpwi  snowy-river-gotjeojl.fra.unikraft.app  standby  standby      oci://unikraft.io/<my-org>/nginx@sha256:...   512 MiB  1            83.87 ms
flask-9a68z  backend.internal                       running  since 2mins  oci://unikraft.io/<my-org>/flask@sha256:...   1.0 GiB  1            1916.54 ms
mongo-o3qhq  mongo.internal                         running  since 5mins  oci://unikraft.io/<my-org>/mongo@sha256:...   1.0 GiB  1            2776.86 ms
```

## Test the deployment

The FQDN of the NGINX instance can be found in the `FQDN` column of the `unikraft instances list` output above.
Use `curl` to query it (replace with your actual FQDN):

```bash
curl https://<FQDN>
```

```text
Hello from the MongoDB client!
```

## Clean up

When done, remove the instances and volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete mongo-o3qhq flask-9a68z nginx-jnpwi
unikraft volume delete mongo-data
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove mongo-o3qhq flask-9a68z nginx-jnpwi
kraft cloud volume remove mongo-data
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft --help
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Awesome Compose](https://github.com/docker/awesome-compose)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
