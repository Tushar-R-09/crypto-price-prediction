@echo off
REM Set KUBECONFIG permanently for the current user
setx KUBECONFIG "C:\Users\LENOVO\.kube\config-rwl-dev"

echo KUBECONFIG environment variable has been set permanently to C:\Users\LENOVO\.kube\config-rwl-dev
