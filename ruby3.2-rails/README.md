# Ruby on Rails

This guide explains how to create and deploy a [Ruby on Rails](https://rubyonrails.org/) app.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/ruby3.2-rails/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/ruby3.2-rails/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud deploy -M 1024 -p 443:3000 -e GEM_HOME=/usr/local/bundle -e BUNDLE_APP_CONFIG=/usr/local/bundle .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: ruby32-rails-apa93
 ├────────── uuid: 2f85b9db-94f8-45d2-8e38-ed9b56cb8695
 ├───────── state: running
 ├─────────── url: https://aged-waterfall-qraz0s7d.fra.unikraft.app
 ├───────── image: ruby32-rails@sha256:fdd46011408fdee05644665ad59b24115737e3fdb352169ec2f3f16a45d4f31d
 ├───── boot time: 577.34 ms
 ├──────── memory: 1024 MiB
 ├─────── service: aged-waterfall-qraz0s7d
 ├── private fqdn: ruby32-rails-apa93.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/ruby /app/bin/rails server -b 0.0.0.0
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

```bash
kraft cloud instance list
```
```ansi
NAME                FQDN                                      STATE    STATUS         IMAGE                                   MEMORY   VCPUS  ARGS                                            BOOT TIME
ruby32-rails-apa93  aged-waterfall-qraz0s7d.fra.unikraft.app  running  2 minutes ago  ruby32-rails@sha256:fdd46011408fdee...  1.0 GiB  1      /usr/bin/ruby /app/bin/rails server -b 0.0.0.0  577.34 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove ruby32-rails-apa93
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

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: ruby:3.2`: The Unikraft runtime kernel to use is Ruby 3.2.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

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

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
