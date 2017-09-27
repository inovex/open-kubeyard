# INES - Inovex Enterprise Search

INES is a Spring Boot + Angular application. This project is divided into backend and frontend.

## Angular Frontend

The frontend is based on Angular

## Spring Boot Backend

Run the application with ```mvn spring-boot:run```

## Getting Started

1) Clone this project

2) Within the frontend folder run ```ng build```

3) Withing the backend folder run ```mvn package && java -jar target/backend-0.0.1-SNAPSHOT.jar``` to build and start the application

## Run as Docker Container

The backend folder has a Dockerfile. If you built the application already you can run ```docker build -t ines:latest backend``` to build the image. Afterwards you can start the container by executing ```docker run -p 8080:8080 -t ines:latest```

## Deploy to Kubernetes

Simply run ```helm install ines```

## Push new version (TODO: CI Pipeline)

To deploy to new version of INES you have to build and push a new image to the container registry.

1) Build: ```docker build -t registry.yourdomain:4567/kubeyard/ines:latest backend```

2) Push: ```docker push registry.yourdomain.de:4567/kubeyard/ines:latest```
