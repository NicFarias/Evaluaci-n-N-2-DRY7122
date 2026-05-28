#!/bin/bash
echo "FROM python:3.9-alpine" > Dockerfile
echo "RUN mkdir /app" >> Dockerfile
echo "WORKDIR /app" >> Dockerfile
echo "RUN echo '<h1>Evaluacion 2 Operativa en puerto 9999</h1>' > index.html" >> Dockerfile
echo "EXPOSE 8080" >> Dockerfile
echo "CMD ["python", "-m", "http.server", "8080"]" >> Dockerfile

docker build -t sample-app .
docker rm -f sample-app-container || true
docker run -t -d -p 9999:8080 --name sample-app-container sample-app
