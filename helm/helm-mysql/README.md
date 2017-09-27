# Helm chart for MySQL

This chart needs a ConfigMap, named `mysql-config-map`, with additional configurations, which has to be provided.

If you don`t need special configurations you can use the following empty one:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mysql-config-map
  namespace: {{ .Values.image.namespace }}
  labels:
    app: {{ template "fullname" . }}
    chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
    release: "{{ .Release.Name }}"
    heritage: "{{ .Release.Service }}"
data:
```