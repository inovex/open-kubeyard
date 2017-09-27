# Jupyter datascience notebook

Github: [jupyter/docker-stacks](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook)

Authentication via a randomly generated token which could be found in the startup log of the pod.

## Docker Registry Image handling
The default location for the image is "registry.inovex.de:4567/inovex-kubeyard/docker-jupyter". 
Because of the performance bottleneck you could use the Google Registry from your project.
Therefore you have to build and push it manually:
```sh
docker build -t eu.gcr.io/<project-id>/docker-jupyter:latest . 

# Switch gcloud cli to the project

gcloud docker -- push eu.gcr.io/<project-id>/docker-jupyter:latest
```

Now you have to adapt/change the image paths in the helm values.yaml for the deployment of the notebook.

If you like to use the given utils you also have to adapt the container-image paths.
