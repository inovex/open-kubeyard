druid.service=druid/overlord
druid.host={{ tuple (print (include "name" .) "-overlord") . | include "fqdn" }}
druid.port={{ default "8090" .Values.overlord.port }}

druid.indexer.queue.startDelay=PT30S

druid.indexer.runner.type=remote
druid.indexer.storage.type=metadata
