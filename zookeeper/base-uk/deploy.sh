#!/bin/bash

#kraft cloud deploy -e CLASSPATH="/apache-zookeeper-3.7.2-bin/bin/../zookeeper-server/target/classes:/apache-zookeeper-3.7.2-bin/bin/../build/classes:/apache-zookeeper-3.7.2-bin/bin/../zookeeper-server/target/lib/*.jar:/apache-zookeeper-3.7.2-bin/bin/../build/lib/*.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/zookeeper-prometheus-metrics-3.7.2.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/zookeeper-jute-3.7.2.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/zookeeper-3.7.2.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/snappy-java-1.1.10.5.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/slf4j-reload4j-1.7.35.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/slf4j-api-1.7.35.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/simpleclient_servlet-0.9.0.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/simpleclient_hotspot-0.9.0.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/simpleclient_common-0.9.0.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/simpleclient-0.9.0.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/reload4j-1.2.22.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-transport-native-unix-common-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-transport-native-epoll-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-transport-classes-epoll-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-transport-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-resolver-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-handler-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-common-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-codec-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/netty-buffer-4.1.94.Final.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/metrics-core-4.1.12.1.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jline-2.14.6.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jetty-util-ajax-9.4.52.v20230823.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jetty-util-9.4.52.v20230823.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jetty-servlet-9.4.52.v20230823.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jetty-server-9.4.52.v20230823.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jetty-security-9.4.52.v20230823.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jetty-io-9.4.52.v20230823.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jetty-http-9.4.52.v20230823.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/javax.servlet-api-3.1.0.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jackson-databind-2.15.2.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jackson-core-2.15.2.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/jackson-annotations-2.15.2.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/commons-cli-1.5.0.jar:/apache-zookeeper-3.7.2-bin/bin/../lib/audience-annotations-0.12.0.jar:/apache-zookeeper-3.7.2-bin/bin/../zookeeper-*.jar:/apache-zookeeper-3.7.2-bin/bin/../zookeeper-server/src/main/resources/lib/*.jar:/conf:" -p 2181:2181/tls -p 2888:2888/tls -p 3888:3888/tls -p 8080:8080/tls -M 1024 .

kraft cloud deploy -p 2181:2181/tls -p 2888:2888/tls -p 3888:3888/tls -p 8080:8080/tls -M 1024 .