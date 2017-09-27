#!/bin/bash

ulimit -l unlimited


chown elastic:elastic /es-data
envsubst < /opt/elasticsearch/config/elasticsearch.yml > /opt/elasticsearch/config/elasticsearch.yml
envsubst < /opt/elasticsearch/config/jvm.options > /opt/elasticsearch/config/jvm.options

chown elastic:elastic /opt/elasticsearch/config/jvm.options

su - elastic -c '/opt/elasticsearch/bin/elasticsearch'
