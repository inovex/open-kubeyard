#!/bin/bash
if [ -z $ZEPPELIN_NOTEBOOK_S3_BUCKET ];
then 
  echo "use local notebook storage"
    cat <<< '
<property>
  <name>zeppelin.notebook.storage</name>
  <value>org.apache.zeppelin.notebook.repo.VFSNotebookRepo</value>
  <description>notebook persistence layer implementation</description>
</property>
</configuration>
    ' >> $ZEPPELIN_CONF_DIR/zeppelin-site.xml
else 
  echo "use AWS notebook storage"
    cat <<< '
<property>
  <name>zeppelin.notebook.s3.endpoint</name>
  <value>s3.amazonaws.com</value>
  <description>endpoint for s3 bucket</description>
</property>

<property>
  <name>zeppelin.notebook.storage</name>
  <value>org.apache.zeppelin.notebook.repo.S3NotebookRepo</value>
  <description>notebook persistence layer implementation</description>
</property>
</configuration>
    ' >> $ZEPPELIN_CONF_DIR/zeppelin-site.xml
fi

./bin/zeppelin.sh