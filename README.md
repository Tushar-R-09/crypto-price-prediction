### Install python 3.12 with uv
```
uv python install 3.12

```

### Create a python environment with python 3.12

```
uv venv --python=3.12

```
This command will create a .venv folder for environment.

### Activate your environment

```
 .venv\Scripts\activate

```

### Add pyproject.toml

```
uv init

```

### To make whole software as library

```
uv init trades --lib

```

### Install Kafka in kubernetes cluster

```
deployment\dev\kind\setup_kafka.bat

```

### Install kafka UI

```
deployment\dev\kind\install_kafka_ui.bat

```
### Do port forwarding to access kafka fromm local 

```
kubectl -n kafka port-forward svc/kafka-ui 8182:8080

```

### Power shell Command to check from windows which port is working

```
Test-NetConnection -ComputerName 127.0.0.1 -Port 31235
```

### To get cluster name
 ```
 kind get clusters
 ```
 ### TO push an image to kind cluster locally
 ```
 kind load docker-image trades:dev --name rwml-34fa
 ```

 ### Switching the branch on git along with copying file
 ```
 git checkout <branch_name> -- <path to file>
 ```

 ### To list all deployments in kubernetes
 ```
 kubectl get deployments -A
 ```

 ### To get into a container
 ```
 docker exec -it <name_of_container> /bin/bash

 kubectl exec -it -n <namespace> <pod-name> -- /bin/bash
 ```

 ### Adding trades as a package
Run this from root directory of project
 ```
 uv add trades
```
This will add trades as a importable package as it is already mentioned in workspace

### Install ruff and pre-commit using uv
```
uv tool install ruff@latest
uv tool install pre-commit@latest

```

### Install pre-commit 
It is a one time thing to activate the hook
```
pre-commit install

```

### Install direnv

First install scoop

1. Open powershell as admin permission

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
2. Open powershell as non admin
```
iwr -useb get.scoop.sh | iex
```
3. Install direnv with scoop
```
scoop install direnv
```

### Challenges
1. Make docker images lighter in weight by breaking them up
2. Make a single docker file for all services passing service name as a parameter from the make file.
3. Read about kafka_topic, kafka_partition, kafka_replication, message keys.
4. How to use kafka registry to make messages have correct formating.
5. Port forwarding using K9s (shift+f from services)
6. How to decide to which external port to map to ? (Rules to map)
7. Remove ta-lib from workspace level and move it to technical_indicator service
8. load parameters like sma_7, sma_14, sma_21, sma_60 through a yaml file
9. Put candles.json in a config map so that we can load dashboard the moment we install grafana instead of manually regenerating it up.

### Make kubernetes cluster on digital ocean
1. Install doctl
2. Authenticate yourself
```
doctl auth init
```
3. create cluster
```
doctl kubernetes cluster create my-k8s-cluster --region nyc1 --version latest --size s-2vcpu-4gb --count 1 && doctl kubernetes cluster kubeconfig save my-k8s-cluster && kubectl get nodes && k9s
```

4. listing all the clusters
```
kubectl config get-contexts
```

5. Regenerate kind config 
```
kind get kubeconfig > C:\Users\LENOVO\.kube\config
```
6. Generate prod config file
```
doctl kubernetes cluster kubeconfig show <cluster-name> > %USERPROFILE%\.kube\config-rwl-prod

```

### Deploy candles and trades service to prod cluster 

```
Make deploy-for-dev service=trades/candles
```
### Bump the prod cluster with different docker image

```
kubectl set image deployment/trades -n rwml trades=ghcr.io/tushar-r-09/candles:0.1.3-beta.20250517164825
```

### Kubectl events log
```
kubectl get events -A -w
```

### Tools to monitor kubernetes
1. Prometheus = to monitor metrics
2. Graphanna
3. logz.io
4. kibana
5. Ingress = Make service to accept outside traffic (Using Nginx and load balancer etc)
6. Helm : pip for kubernetes

### Tools for orchestration python pipeline

1. Zenml
2. Flyte

## Install Rising wave

```
helm repo add risingwavelabs https://risingwavelabs.github.io/helm-charts/ --force-update
helm repo update
helm upgrade --install --create-namespace --wait risingwave risingwavelabs/risingwave --namespace=risingwave -f manifests/risingwave-values.yaml 
```

### Make bash script executable
```
chmod 755 install_risingwave.sh 
./install_risingwave.sh 
```

### Postgreesql command
```
psql -h localhost -p 4567 -d dev -U root
```