#!/bin/bash
set -e

echo "TEST"

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${JAVA_HOME}/jre/lib/amd64/server
#source ${HADOOP_HOME}/libexec/hadoop-config.sh
export CLASSPATH=$(/opt/hadoop/bin/hadoop classpath --glob) 




cd /opt/tensorflow
echo "START: $@"

echo "which: $(which python3)"
echo $(ls -al ./)
echo "pwd: $(pwd)"
echo "find: $(find / -name "libjvm.so")"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
echo "HADOOP_HDFS_HOME: $HADOOP_HDFS_HOME"
echo "HADOOP_HOME: $HADOOP_HOME"
echo "CLASSPATH: $CLASSPATH"

exec "$@"