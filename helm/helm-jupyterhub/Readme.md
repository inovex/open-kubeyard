# Deploy JupyterHub without OAuth

1) Create cluster with ```--scopes "https://www.googleapis.com/auth/projecthosting,storage-rw,bigquery"```

2) Deploy NFS

```helm install helm-nfs```

3) Replace ```FILER_IP``` in ```helm-jupyterhub/values.yaml``` with actual IP-Address of the NFS-Server.

4) Deploy JupyterHub

```helm install helm-jupyterhub```

5) Compute SSL key and certificate

```openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/tls.key -out /tmp/tls.crt -subj "/CN=jhub/O=xip.io"```

```openssl dhparam -out /tmp/dhparam.pem 2048```

```gcloud compute ssl-certificates create  kubeyard-cert --certificate /tmp/tls.crt --private-key /tmp/tls.key```

6) Create Secret in Kubernetes cluster

```kubectl create secret generic jhub-tls --from-file=/tmp/tls.crt --from-file=/tmp/tls.key --from-file=/tmp/dhparam.pem --namespace kubeyard```

7) Create Configmap

```kubectl create configmap  jhub-nginx-conf --from-file=proxy/nginx.conf --namespace kubeyard```

8) Set NGINX Service to a Static IP

Go to nginx-proxy.yaml and replace <STATIC_IP>

9) Create NGINX proxy

```kubectl create -f proxy/nginx-proxy.yaml```

Note: The nginx proxy image can be found in the proxy folder of this project. It is pushed to the registry with the tag ```proxy```. Build and push via:

```sh
docker build --tag registry.inovex.de:4567/inovex-kubeyard/docker-jupyterhub:proxy proxy\

docker push registry.inovex.de:4567/inovex-kubeyard/docker-jupyterhub:proxy\
```

10) Default login is for testing purpose: ```admin``` / ```jhub123```. Every newly created user also gets the password ```jhub123``` by default.


The templates are in part based on (https://github.com/GoogleCloudPlatform/gke-jupyter-classroom/tree/master/jupyterhub/custom_manifests) which is published under the Apache 2.0 License. A copy of the license can be acquired under http://www.apache.org/licenses/ .
