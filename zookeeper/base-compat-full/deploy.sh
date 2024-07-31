#!/bin/bash

kraft cloud deploy -p 2181:2181/tls -p 2888:2888/tls -p 3888:3888/tls -p 8080:8080/tls -M 1024 .
