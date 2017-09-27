# Helm chart for [wasabi A/B Testing Platform](https://github.com/intuit/wasabi).

Wasabi UI requires the publicly reachable IP- address of its wasabi host.
The current solution is a static IP- address for wasabi's service.

## Setup static IP

1. Allocate static ip: `gcloud compute addresses create wasabi-host --region europe-west1`
2. Show allocated ip: `gcloud compute addresses list`

## Install Helm chart with your own static ip

There are two different ways:

* change the `wasabi.host` value in `values.yaml` and use `helm install helm-wasabi` or
* use directly `helm install --set wasabi.host=<static-ip>  helm-wasabi`

## Credentials

Default username and password are **admin/admin**