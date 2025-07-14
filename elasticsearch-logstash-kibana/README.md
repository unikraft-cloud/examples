# ELK stack

The ELK stack (Elasticsearch, Logstash, Kibana) is a powerful set of tools for searching, analyzing, and visualizing log data in real-time.

**Credits**: This example is based on this [ELK Stack Docker Compose example](https://github.com/docker/awesome-compose/tree/master/elasticsearch-logstash-kibana).

## Deployment

**Disclaimer**: The instances reserve more than 2GB of RAM, so you might need to get your Unikraft Cloud account quota increased to run this example.

This example uses a [`compose.yaml`](compose.yaml) file to define the services required for the ELK stack. The file specifies the following services:

- **Elasticsearch**: The search and analytics engine.
- **Logstash**: The data processing pipeline that ingests data from various sources, transforms it, and sends it to Elasticsearch.
- **Kibana**: The visualization layer that provides a web interface to interact with the data stored in Elasticsearch.
- **Metricbeat**: A lightweight shipper for metrics that can be used to collect and send system and service metrics to Elasticsearch.

To run the ELK stack on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli). Make sure you have an active account on Unikraft Cloud (UKC) and that you have authenticated your CLI with your UKC account.

```console
export UKC_TOKEN=<your-unikraft-cloud-access-token>
export UKC_METRO=fra0
```

Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud compose up
```

This will create an instance with the name of the service defined in [`compose.yaml`](compose.yaml) (`web`), prefixed by the current working directory [`elasticsearch-logstash-kibana`](./).
You can retrieve the FQDN (Fully Qualified Domain Name) of the instance using:

```console
kraft cloud instance get elasticsearch-logstash-kibana-web
```

You can then access it at port 443 using HTTPS.

## Next steps

Once the ELK stack is running, you can start sending logs to Logstash and visualizing them in Kibana. You can add [Filebeat](https://www.elastic.co/beats/filebeat)
to ship logs from your applications to Logstash.

This deployment is **NOT** production-ready, as it does not include any security features, such as TLS encryption or authentication.
Some features in Kibana might not be available because of this. You can find more information [here](https://www.elastic.co/docs/reference/kibana/configuration-reference/security-settings).

## Learn more

- [Elasticsearch's Documentation](https://www.elastic.co/docs/solutions/search)
- [Logstash's Documentation](https://www.elastic.co/docs/reference/logstash)
- [Kibana's Documentation](https://www.elastic.co/docs/reference/kibana)
- [Metricbeat's Documentation](https://www.elastic.co/docs/reference/beats/metricbeat)
- [Getting started with the Elastic Stack and Docker Compose](https://www.elastic.co/blog/getting-started-with-the-elastic-stack-and-docker-compose)
- [Awesome Compose](https://github.com/docker/awesome-compose)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
- [Deploying with Compose Files](https://unikraft.cloud/docs/guides/features/compose/)
