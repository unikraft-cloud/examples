FROM grafana/grafana:12.0.2

COPY datasource.yml /etc/grafana/provisioning/datasources/

COPY env.txt /env.txt

COPY --chmod=0755 wrapper.sh /wrapper.sh
