@echo off

REM 1. Check if the 'kafka' namespace exists, delete it if it does
kubectl get namespace kafka >nul 2>nul
if %errorlevel% equ 0 (
    echo Namespace "kafka" exists, deleting it...
    kubectl delete namespace kafka
) else (
    echo Namespace "kafka" does not exist.
)

REM 2. Recreate the 'kafka' namespace
kubectl create namespace kafka

REM 3. Download and apply Strimzi manifests to set up the Kafka operator
kubectl apply -f "https://strimzi.io/install/latest?namespace=kafka" -n kafka

REM 4. Deploy the Kafka cluster from your local YAML file
kubectl apply -f .\manifest\kafka-e11b.yaml

pause
