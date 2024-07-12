# Example for app scale-to-zero integration

This application provides an example of how to use the [Application Support for Scale-To-Zero](https://unikraft.cloud/docs/api/v1/instances/#application-support-for-scale-to-zero) feature. 

To run this example on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --scale-to-zero=idle --metro fra0 -p 443:8080 -M 512 .
```

Alternatively, you can expose the application with the non-HTTP mode by using a different port:

```console
kraft cloud deploy --scale-to-zero=idle --metro fra0 -p 8080:8080/tls -M 512 .
```

This mode allows you to use more advanced HTTP features such as [Server-Sent-Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events).

After deploying, you can interact with the following endpoints:

| Endpoint | Description | Curl Example |
| -------- | ----------- | ------------ |
| `GET` `<URL>/` | Get the current content of the `scale_to_zero_disable` file | `curl https://<FQDN>/` |
| `POST` `<URL>/set/<number>` | Set the count of disable requests to `<number>` | `curl -XPOST https://<FQDN>/set/10` |
| `POST` `<URL>/add` | Increment the count by one | `curl -XPOST https://<FQDN>/add` |
| `POST` `<URL>/add/<number>` | Increment the count by `<number>` | `curl -XPOST https://<FQDN>/add/2` |
| `POST` `<URL>/sub` | Decrement the count by one | `curl -XPOST https://<FQDN>/sub` |
| `POST` `<URL>/sub/<number>` | Decrement the count by `<number>` | `curl -XPOST https://<FQDN>/sub/2` |
| `GET` `<URL>/sse/<interval>` | Get periodic server side events every `<interval>` seconds (Only works for a non-HTTP handler port) | `curl https://<FQDN>/sse/1` |

## Learn more

- [Unikraft Cloud's Scale-To-Zero Documentation](https://unikraft.cloud/docs/api/v1/instances/#scale-to-zero)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
