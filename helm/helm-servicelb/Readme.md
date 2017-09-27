# Service Loadbalancer

Helm chart for [service-loadbalancer](https://github.com/kubernetes/contrib/tree/master/service-loadbalancer).
Published under the Apache 2.0 license http://www.apache.org/licenses/ .

This way you can provide a HA-Proxy powered LoadBalancer from within a pod instead of the Google- or AWS-Loadbalancers.

It is able to handle:

* HTTP Connections
* TCP Connections
* HTTPs Connections

Please check the notes.txt for deployment tips.

## Setup

Annotate all pods which should use SSL with:

``` sh
  annotations:
    serviceloadbalancer/lb.sslTerm: "true"
```

``` sh
# Install Chart
helm install ./service-loadbalancer -n svclb --namespace test --debug
```

``` sh
# Label Node
node=`kubectl get nodes -o json | jq -r '.items[0].metadata.name'`; kubectl label node $node role=loadbalancer
```

Don't forget to set your ssl key in the ```values.yaml```
