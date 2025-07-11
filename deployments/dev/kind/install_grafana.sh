#!/bin/bash

helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install --create-namespace --wait grafana grafana/grafana --namespace=monitoring --values manifests/grafana-values.yaml