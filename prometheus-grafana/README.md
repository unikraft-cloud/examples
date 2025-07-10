# Prometheus and Grafana

[Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/) are two of the most popular open-source tools for monitoring and observability.
Prometheus is a powerful time-series database and monitoring system, while Grafana is a visualization tool
that allows you to create beautiful dashboards and graphs from your data. They are often used together to provide
a complete monitoring solution.

## Building

Because of quota limitations, you might not be able to instantiate VMs with more than 2G of RAM. Grafana's image is pretty
heavy, and using the traditional `initrd` approach will not work because of the size of the image. Thus, we will
create an `erofs` filesystem image from the Docker image, to bypass the memory consumption of unpacking into RAM on startup.
This approach will be automated in the near future, but for now, you can follow these steps to create the `erofs` filesystem image:

1. **Navigate to the image directory**

   ```bash
   cd grafana/image
   ```

2. **Extract the original image env**

    ```bash
    ./extract-env.sh
    ```

    This will create a `env.txt` file containing the environment variables from the original Docker image.

3. **Build the Docker image**

   ```bash
   docker build -t grafana-with-wrapper .
   ```

   The resulting image will contain a `wrapper.sh` script that will inject the necessary environment variables embedded into the original image and run the original entrypoint.

4. **Export the container filesystem**

   ```bash
   docker create --name temp-grafana grafana-with-wrapper
   docker export -o rootfs.tar temp-grafana
   docker rm temp-grafana
   ```

5. **Create the erofs filesystem image**

   ```bash
   mkdir rootfs
   tar -xvf rootfs.tar -C rootfs
   mkfs.erofs --all-root -d2 -E noinline_data rootfs.erofs ./rootfs
   ```

6. **Clean up temporary files**

   ```bash
   rm -rf rootfs/ rootfs.tar
   cd ../..
   ```

## Deployment

This example uses a [`compose.yaml`](compose.yaml) file to define the Grafana and Prometheus services.

To run it on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli). Make sure you have an active account on Unikraft Cloud (UKC) and that you have authenticated your CLI with your UKC account.

```bash
export UKC_TOKEN=<your-unikraft-cloud-access-token>
export UKC_METRO=fra0
```

Then `cd` into [this](.) directory, and invoke:

```bash
kraft cloud compose up
```

## Volumes

This deployment creates volumes for data persistence: `prometheus-grafana-prom-data` and `prometheus-grafana-grafana-data`.
Upon bringing down the services (e.g., `kraft cloud compose down`), these volumes will persist, allowing you to bring the services back up without losing data.
To remove the volumes, you can use:

```bash
kraft cloud volume rm prometheus-grafana-prom-data prometheus-grafana-grafana-data
```

## Learn more

- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Awesome Compose](https://github.com/docker/awesome-compose)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
- [Deploying with Compose Files](https://unikraft.cloud/docs/guides/features/compose/)
- [Creating tunnels](https://unikraft.cloud/docs/guides/features/tunnel/)
