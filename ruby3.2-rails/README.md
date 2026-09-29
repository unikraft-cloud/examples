# Ruby on Rails

This guide explains how to create and deploy a [Ruby on Rails](https://rubyonrails.org/) app.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/ruby3.2-rails/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/ruby3.2-rails/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/ruby32-rails:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  -e GEM_HOME=/usr/local/bundle \
  -e BUNDLE_APP_CONFIG=/usr/local/bundle \
  --image <my-org>/ruby32-rails:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         ruby32-rails-apa93
uuid:         2f85b9db-94f8-45d2-8e38-ed9b56cb8695
state:        starting
image:        <my-org>/ruby32-rails
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       42265dab-df44-6d66-0075-fc07455178c8
  name:       aged-waterfall-qraz0s7d
  domains:
  - fqdn:     aged-waterfall-qraz0s7d.fra.unikraft.app
networks:
- uuid:       7ae3414b-1d87-c831-d26a-506a4cf9ac71
  private-ip: 10.0.3.3
  mac:        12:b0:39:3e:b5:36
timestamps:
  created:    just now
```

In this case, the instance name is `ruby32-rails-apa93` and the address is `https://aged-waterfall-qraz0s7d.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Python-based HTTP web server:

```bash
curl https://aged-waterfall-qraz0s7d.fra.unikraft.app/hello
```

```text
[...]
  <body>
    <h1>Hello World</h1>
Hello, World!

  </body>
[...]
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                STATE    IMAGE                  ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    ruby32-rails-apa93  running  <my-org>/ruby32-rails        1.0GiB  1      aged-waterfall-qraz0s7d.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete ruby32-rails-apa93
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `app/` and `config/`: the contents to update the Rails setup
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The `app/` and `config/` directories contain files that are to overwrite generated Rails files:

```bash
tree app/ config/
```

```text
app/
|-- controllers/
|   `-- hello_controller.rb
`-- views/
    `-- hello/
        `-- index.html.erb
config/
|-- environments/
|   `-- development.rb
`-- routes.rb
```

These files add the configuration (controller, view, route) to print the `Hello, World!` message in Rails.
They overwrite the generated Rails configuration to provide the app setup.
Update these files, and other files, with required contents for your own app.

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/ruby", "/app/bin/rails", "server", "-b", "0.0.0.0"]`: Use `/usr/bin/ruby /app/bin/rails server -b 0.0.0.0` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* The `RUN` lines install Rails and generate the default app setup for a `hello` app.

* `COPY . /app/`: Copies the local files (from `app/` and `config/`) to the app, overwriting generated contents to provide the user-specified app.

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY --from=build /app /app`: Copy the app directory to the filesystem.

The following options are available for customizing the app:

* If you only update the implementation in the `app/` or `config/` directories, or adding new directories or files to overwrite Rails generated files, you don't need to make any other changes.

* If changing the app name, change the `hello` name in `RUN rails generate controller hello` to a new one.
  The file names in the `app/` and `config/` directories have to be similarly updated.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
