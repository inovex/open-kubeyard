# Setup realtime clickstream-app

## Prerequisites
1. Generate ssh key for sshd Deamon

    ```sh
    ssh-keygen -t rsa -b 4096 -C "<your-comment>"
    ```
2. Place public-key in `values.yaml`

```yaml
helm-sshd:
  pubkey: <your key>
```

## Install App

1. Run `helm install clickstream`
2. Wait for all Pods to start
3. [Init](##Init)

## Access
1. Install Proxy Plugin (https://getfoxyproxy.org/)
2. Configure Foxy Proxy to whitelist all urls with `*.kubeyard` to connect via SocksProxy to `localhost:8157`
3. Open ssh tunnel to cluster

    ```
    ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -N -D 8157 ssh-user@<IP SSH Endpoint>
    ```
4. You should be able to connect to services, for example `http://<release-name>-superset.<namespace>:8088`



## Init
1. Druid uses HDFS for deep storage. You have to create the `/druid` folder before druid can use it:
    * Log in to the hdfs-namenode pod `kubectl exec <namenode-pod> --namespace=<namespace> -it /bin/bash`
    * Execute `hdfs dfs -mkdir /druid && hdfs dfs -chown druid /druid`
2. Before you can login into superset, you first have to initialize it:
    * Log in to the superset pod `kubectl exec <superset-pod> --namespace=<namespace> -it /bin/sh`
    * Run `superset-init`
    * Follow instructions
3. Metabase is available at `<helm-release>-metabase.<namespace>:3000` For setup follow instructions (You need to get [access](##Access) to the cluster first)

## Configure Superset UI

### Add druid cluster as source
Go to the 'Sources' tab, open 'Druid Clusters', and add a new record as follows:

| Key                  |  Value                                      |
| -------------------- |:-------------------------------------------:|
| Cluster              | druid-cluster                               |
| Coordinator Host     | [helm-release]-druid-coordinator            |
| Coordinator Port     | 8081                                        |
| Broker Host          | [helm-release]-druid-broker                 |
| Broker Port          | 8082                                        |

Hit Save.

### Add divolte as source
Go to the 'Sources' tab, open 'Druid Datasources', and add a new record as follows:

| Key                  |  Value                                      |
| -------------------- |:-------------------------------------------:|
| Datasource Name      | divolte                                     |
| Cluster              | druid-cluster                               |
| Owner                | max mustermann                              |

Hit Save.

### Push events
Go to the divolte service and push new events through the button. This will trigger an index job which you can observe at the druid-overlod if you have an open proxy to the pods though the sshd pod.
Wait until this indexing job is done (this could take a while!).

### Refresh superset metadata
Go to the 'Sources' tab and hit 'Refresh Druid Metadata'.

### View events
Open [http://<SUPERSET-SERVICE>/superset/explore/druid/1/](http://<SUPERSET-SERVICE>/superset/explore/druid/1/) to view the data and save it as a Dashboard.
