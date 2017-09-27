{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "name" -}}
{{- default .Chart.Name .Values.name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a fully qualified app name truncated to 63 characters.
*/}}
{{- define "fqan" -}}
{{- $name := index . 0 -}}
{{- $context := index . 1 -}}
{{- $releaseName := $context.Release.Name | trunc 20 -}}
{{- $name := $name -}}
{{- printf "%s-%s" $releaseName $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the fully qualified app name for this app.
*/}}
{{- define "fullname" -}}
{{- tuple (include "name" .) . | include "fqan" -}}
{{- end -}}

{{/*
Create an fqdn for an app <release>-<name>.<namespace>.
*/}}
{{- define "fqdn" -}}
{{- $name := index . 0 -}}
{{- $context := index . 1 -}}
{{- $hostname := tuple $name $context | include "fqan" -}}
{{- $domainname := $context.Release.Namespace -}}
{{- printf "%s.%s" $hostname $domainname -}}
{{- end -}}
