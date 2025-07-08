# Gitea with PostgreSQL

[Gitea](https://about.gitea.com/) is a lightweight, self-hosted Git service that provides a web interface for managing Git repositories. It is often used as an alternative to GitHub or GitLab for hosting code repositories. In this example, [PostgreSQL](https://www.postgresql.org/) is used as the database backend for Gitea.

**Credits**: This example is based on this [Gitea Docker Compose example](https://github.com/docker/awesome-compose/tree/master/gitea-postgres).

## Deployment

This example uses a [`compose.yaml`](compose.yaml) file to define the Gitea and PostgreSQL services.

To run them on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli). Make sure you have an active account on Unikraft Cloud (UKC) and that you have authenticated your CLI with your UKC account.

```console
export UKC_TOKEN=<your-unikraft-cloud-access-token>
export UKC_METRO=fra0
```

Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud compose up
```

This will create two instance with the names of respective compose [`compose.yaml`](compose.yaml) services, prefixed by the current working directory [`gitea-postgres`](./).
You can retrieve the FQDN (Fully Qualified Domain Name) of the Gitea instance using:

```console
kraft cloud instance get gitea-postgres-gitea
```

You can then access it at port 443 using HTTPS.

## Volumes

This deployment creates two volumes for data persistence: `gitea-postgres-git-data` for Gitea and `gitea-postgres-db-data` for PostgreSQL.
Upon bringing down the services (e.g., `kraft cloud compose down`), these volumes will persist, allowing you to bring the services back up without losing data.
To remove the volumes, you can use:

```console
kraft cloud volume rm gitea-postgres-git-data gitea-postgres-db-data
```

## SSH

If you want to enable SSH access to the Gitea instance, you need to open up a port for SSH in the `compose.yaml` file:

```yaml
ports:
  ...
  - "2222:22"
```

## Custom Domain Name

Each time you deploy this example, it will create a new instance with a unique FQDN. This might be problematic if you
want to reuse the Gitea volume across deployments because the certificates are tied to the FQDN.
To use a custom domain name, you can specify the `domainname` field in the `compose.yaml` file:

```yaml
services:
  gitea:
    ...
    domainname: <your-domain-name>
```

More info [here](https://unikraft.cloud/docs/guides/features/edns/).

## Learn more

- [Gitea's Documentation](https://docs.gitea.com/)
- [PostgreSQL's Documentation](https://www.postgresql.org/docs/)
- [Awesome Compose](https://github.com/docker/awesome-compose)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
- [Deploying with Compose Files](https://unikraft.cloud/docs/guides/features/compose/)
