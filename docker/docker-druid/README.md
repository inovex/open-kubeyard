# docker-druid

This image can be used to launch a single node type of a [druid](http://druid.io/) cluster.

Current druid version: 0.9.2

## Usage
You have to overwrite the default command with `druid start <node>`
Example:
```
docker run registry/druid druid start coordinator
```

To adjust the runtime config, copy the [druid conf directory](https://github.com/druid-io/druid/tree/druid-0.9.2/examples/conf/druid) and mount it to `/opt/druid/conf/druid/`.
