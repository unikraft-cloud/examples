# Flask with MongoDB

[Flask](https://flask.palletsprojects.com/en/stable/) is a lightweight WSGI web application framework in Python, and [MongoDB](https://www.mongodb.com/) is a NoSQL database that stores data in JSON-like documents.
This example deploys three services on Unikraft Cloud: NGINX (reverse proxy), Flask (backend), and MongoDB (database).

**Credits**: This example is based on this [Awesome Compose example](https://github.com/docker/awesome-compose/tree/master/nginx-flask-mongo).

## Deployment

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/nginx-flask-mongo` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/nginx-flask-mongo/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## MongoDB

Create a volume for MongoDB data persistence:

```bash title="unikraft"
unikraft volume create --metro fra --name mongo-data --size 1G
```

You can list the created volume by running:

```bash title="unikraft"
unikraft volume list
```

```ansi title="unikraft"
METRO  NAME        STATE      SIZE  CREATED
fra    mongo-data  available  1GiB  just now
```

First, deploy the MongoDB instance.
MongoDB is an internal service (not publicly accessible), reached via the `mongo.internal` domain:

```bash title="unikraft"
unikraft build ./mongo --output <my-org>/mongo:latest
unikraft run --metro fra \
  -m 1024M \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --domain mongo.internal \
  --volume mongo-data:/data/db \
  --image <my-org>/mongo:latest
```

The output shows the MongoDB instance details:

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

## Flask

Next, deploy the Flask backend.
It connects to MongoDB using the `MONGO_SERVER_URL` environment variable and is reached internally via `backend.internal`:

```bash title="unikraft"
unikraft build ./flask --output <my-org>/flask:latest
unikraft run --metro fra \
  -m 1024M \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --domain backend.internal \
  --env FLASK_SERVER_PORT=9091 \
  --env MONGO_SERVER_URL=mongo.internal:27017 \
  --image <my-org>/flask:latest
```

The output shows the Flask instance details:

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

## NGINX

Finally, deploy NGINX as the public-facing reverse proxy.
It forwards requests to the Flask backend at `backend.internal:9091` by default.
To use a different backend domain, set the `BACKEND_HOST` environment variable to the same value you pass as the Flask domain.

```bash title="unikraft"
unikraft build ./nginx --output <my-org>/nginx:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:80/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  -e BACKEND_HOST=backend.internal \
  --image <my-org>/nginx:latest
```

The output shows the NGINX instance details including its public FQDN:

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

You can list all deployed instances with:

```bash title="unikraft"
unikraft instances list
```

```text title="unikraft"
METRO  NAME         STATE    IMAGE           MEMORY  VCPUS  FQDN                                   CREATED
fra    nginx-jnpwi  standby  <my-org>/nginx  512MiB  1      snowy-river-gotjeojl.fra.unikraft.app  11 minutes ago
fra    flask-9a68z  standby  <my-org>/flask  1GiB    1      backend.internal                       12 minutes ago
fra    mongo-o3qhq  standby  <my-org>/mongo  1GiB    1      mongo.internal                         14 minutes ago
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

```bash title="unikraft"
unikraft instances delete mongo-o3qhq flask-9a68z nginx-jnpwi
unikraft volume delete mongo-data
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Awesome Compose](https://github.com/docker/awesome-compose)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
