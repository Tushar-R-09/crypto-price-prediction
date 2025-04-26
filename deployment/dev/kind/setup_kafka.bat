@echo off
REM 1. Create a namespace called 'kafka'
kubectl create namespace kafka

REM 2. Download and apply Strimzi manifests to set up the Kafka operator
kubectl create -f "https://strimzi.io/install/latest?namespace=kafka" -n kafka

REM 3. Deploy the Kafka cluster from your local YAML file
kubectl apply -f .\manifest\kafka-e11b.yaml

pause
