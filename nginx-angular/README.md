# Angular

[Angular](https://angular.dev/) is a platform for building mobile and desktop web applications. It provides a comprehensive solution for building single-page applications (SPAs) with a focus on performance, scalability, and maintainability.

## Deployment

This example uses a [`compose.yaml`](compose.yaml) file to define the Angular application.

To run Angular on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli). Make sure you have an active account on Unikraft Cloud (UKC) and that you have authenticated your CLI with your UKC account.

```console
export UKC_TOKEN=<your-unikraft-cloud-access-token>
export UKC_METRO=fra0
```

Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud compose up
```

This will create an instance with the name of the service defined in [`compose.yaml`](compose.yaml) (`web`), prefixed by the current working directory [`nginx-angular`](./).
You can retrieve the FQDN (Fully Qualified Domain Name) of the instance using:

```console
kraft cloud instance get nginx-angular-web
```

You can then access it at port 443 using HTTPS.

## Learn more

- [Angular's Documentation](https://angular.dev/overview)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
- [Deploying with Compose Files](https://unikraft.cloud/docs/guides/features/compose/)
