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