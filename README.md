# kubeyard

Kubeyard is a collection of docker images, helm charts and other software, that allows for a fast and versatile deployment of applications on kubernetes. The project is structured into three components.

- apps contains complete applications for end user usage composed of multiple atomic components.
- docker contains all the atomic docker project components with their respective Dockerfile and image.
- helm contains all the atomic Helm projects with their respective Helm charts.

## Installation

- Install docker
- Install gcloud
- Install kubectl using gcloud
- Install helm
- Install ruby gems
- Clone the repository
- Setup a private registry for the container you want to use.
- Start the cluster using ```rake kubeyard:init```
- Install components using **helm**
