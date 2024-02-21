# Spring Boot on KraftCloud

[Spring Boot](https://spring.io/projects/spring-boot) is an extension of the Spring plaform for Java that simplifies the creation of Spring applicaitons.

This repository provides the [quickstart example of Spring Boot](https://spring.io/quickstart) over Unikraft. This implements a "Hello World!" endpoint which a browser can connect to.

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

To deploy this application on KraftCloud, invoke:

```console
kraft cloud deploy -M 1024 -p 443:8080 .
```

The command will build and deploy `DemoApplication.java`. Feel free to modify and redeploy!

## Learn more

- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
