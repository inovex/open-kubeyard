{{/* vim: set filetype=mustache: */}}
{{/*
Define fqan of the datanode component.
*/}}
{{- define "hdfs-datanode-fqan" -}}
{{- tuple (default "hdfs-datanode" .Values.hdfs.datanode.name) . | include "fqan" -}}
{{- end -}}

{{/*
Define fqdn of the datanode component.
*/}}
{{- define "hdfs-datanode-fqdn" -}}
{{- tuple (default "hdfs-datanode" .Values.hdfs.datanode.name) . | include "fqdn" -}}
{{- end -}}

{{/*
Define fqan of the namenode component.
*/}}
{{- define "hdfs-namenode-fqan" -}}
{{- tuple (default "hdfs-namenode" .Values.hdfs.namenode.name) . | include "fqan" -}}
{{- end -}}

{{/*
Define fqdn of the namenode component.
*/}}
{{- define "hdfs-namenode-fqdn" -}}
{{- tuple (default "hdfs-namenode" .Values.hdfs.namenode.name) . | include "fqdn" -}}
{{- end -}}
