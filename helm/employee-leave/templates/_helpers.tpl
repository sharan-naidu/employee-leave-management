{{- define "employee-leave.name" -}}
employee-leave
{{- end }}

{{- define "employee-leave.fullname" -}}
employee-leave-app
{{- end }}

{{- define "employee-leave.labels" -}}
app.kubernetes.io/name: {{ include "employee-leave.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
