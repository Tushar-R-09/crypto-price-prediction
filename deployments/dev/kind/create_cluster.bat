@echo off
REM Deleting the cluster
echo Deleting the cluster...
kind delete cluster --name rwml-34fa

REM Deleting the docker network
echo Deleting the docker network...
docker network rm rwml-34fa-network

REM Creating the docker network
echo Creating the docker network...
docker network create --subnet 172.100.0.0/16 rwml-34fa-network

REM Creating the cluster
echo Creating the cluster...
set KIND_EXPERIMENTAL_DOCKER_NETWORK=rwml-34fa-network
kind create cluster --config ./kind-with-portmapping.yaml

echo Script finished.
pause
