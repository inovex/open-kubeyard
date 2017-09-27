#!/bin/bash
if [[ -z $JUPYTER_NOTEBOOK_GCS_PROJECT_ID || -z $JUPYTER_NOTEBOOK_GCS_KEYFILE || -z $JUPYTER_NOTEBOOK_GCS_BUCKET_PATH ]];
then 
  echo "use local notebook storage"
else 
  echo "use GCS notebook storage"

    cat <<< '
c.NotebookApp.contents_manager_class = "jgscm.GoogleStorageContentManager"
c.GoogleStorageContentManager.project = "'"$JUPYTER_NOTEBOOK_GCS_PROJECT_ID"'"
c.GoogleStorageContentManager.keyfile = "/usr/jupyter/'$JUPYTER_NOTEBOOK_GCS_KEYFILE'"
c.GoogleStorageContentManager.default_path = "'"$JUPYTER_NOTEBOOK_GCS_BUCKET_PATH"'"
    ' >> ~/.jupyter/jupyter_notebook_config.py
fi

/usr/local/bin/start-notebook.sh