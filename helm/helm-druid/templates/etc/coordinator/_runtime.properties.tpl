druid.service=druid/coordinator
druid.host={{ tuple (print (include "name" .) "-coordinator") . | include "fqdn" }}
druid.port={{ default "8081" .Values.coordinator.port }}

druid.coordinator.startDelay=PT30S
druid.coordinator.period=PT30S
