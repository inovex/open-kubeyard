druid.service=druid/broker
druid.host={{ tuple (print (include "name" .) "-broker") . | include "fqdn" }}
druid.port={{ default "8082" .Values.broker.port }}

# HTTP server threads
druid.broker.http.numConnections=5
druid.server.http.numThreads=25

# Processing threads and buffers
druid.processing.buffer.sizeBytes=536870912
druid.processing.numThreads=7

# Query cache
druid.broker.cache.useCache=true
druid.broker.cache.populateCache=true
druid.cache.type=local
druid.cache.sizeInBytes=2000000000
