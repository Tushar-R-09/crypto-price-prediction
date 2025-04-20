# real-time-ml-system-cohort-4

### Table of contents

- [Some general information](#some-general-information)
- [Before the course starts](#before-the-course-starts)
- [Lessons](#lessons)

## Some general information

- [What's new in this cohort?](https://www.realworldml.net/products/building-a-real-time-ml-system-together-cohort-4/categories/2157289689/posts/2186077943)
- [Calendar](https://www.realworldml.net/products/communities/buildingrealtimemlsystemsforproduction/meetups)
- [How to share problems and issues you face during the course?](https://www.realworldml.net/products/building-a-real-time-ml-system-together-cohort-4/categories/2157289689/posts/2186535362)

## Before the course starts

- [How to setup your development environment](lessons/00_how_to_setup_your_development_environment.md)
- [How to create a local Kubernetes cluster](lessons/01_create_local_kubernetes_cluster.md)

## Commands
 - chmod 600 ~/.ssh/id_rsa : To restrict permission to ssh keys
 - uv init <project-name> : The uv project creation
 - uv init trades --lib : To add a package in workspace # All the dependencies will be synced in one place

 ## Install kkubectl in dev container
  VERSION="v1.29.4"
  curl -LO "https://dl.k8s.io/release/${VERSION}/bin/linux/amd64/kubectl"
  chmod +x kubectl
  mv kubectl /usr/local/bin/
  kubectl version --client

## Install k9s 
    curl -Lo k9s.tar.gz https://github.com/derailed/k9s/releases/latest/download/k9s_Linux_amd64.tar.gz
    tar -xzf k9s.tar.gz
    chmod +x k9s
    sudo mv k9s /usr/local/bin/

## Type inside k9s
    -Type ":"
    - Start typing
    svc (For kubernetes services)

## port forwarding for kafka ui
kubectl -n kafka port-forward svc/kafka-ui 8182:8080




## Lessons