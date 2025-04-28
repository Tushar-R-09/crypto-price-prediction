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