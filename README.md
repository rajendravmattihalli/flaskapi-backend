# flaskapi-backend
<ins> **flaskapi-backend application - contents** </ins>

> 1. Multistage Docker build
> 2. Observability
> 3. Kubernetes manifest 
> 4. CI Integration
> 5. ArgoCD Integartion
> 6. Sandbox Testing

## Docker Build - Multistage

Folder structure

```
├── docker-multistage
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
```

**Prerequisite**
> Docker

**Manual Build**
> docker build -t flaskapi-backend:latest .
> docker run --name flaskapi-backend -d -p 5001:5001 flaskapi-backend:latest

## Observability
**Prometheus Instrumentation**
<ins> **RED Metrics** </ins>
1. Request count
2. Error count
3. Duration Latency

ScrapeEndpoint = /metrics 
ScrapeEndpointPort = 5001
<img width="1087" height="895" alt="Screenshot 2025-10-19 at 2 00 34 AM" src="https://github.com/user-attachments/assets/359d6e25-d934-489e-863a-2eceb4a5a6a4" />

<ins> **Prometheus Operator Installation** </ins>
**Prerequisite**
1. Kubernetes
2. Helm
3. Kubectl

**Installation**
1. Add repository for helm charts for prometheus-operator deployment
> helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
2. Helm repo update
> helm repo update
3. Create monitoring namespace
> kubectl create namespace monitoring
4. Servicemonitor kubernetes manifest definition for flaskapi-backend application
> kubectl apply -f flaskapi-backend-servicemonitor.yml
<img width="1678" height="442" alt="Screenshot 2025-10-19 at 1 54 33 AM" src="https://github.com/user-attachments/assets/3062f8ba-31fc-40b6-a7bb-870fa33555fa" />


**Logging Instrumentation**
1. INFO and ERROR Log
2. stdout/stderr - container
3. Json format



## Kubernetes Manifest
Manifest for deployment on kuberenetes

Folder Structure
```
├── kubernetes
│   ├── flaskapi-backend-deployment.yml
│   ├── flaskapi-backend-service.yml
│   └── namespace.yml
```
**Kubernetes Deployment**
1. Create namespace if not exists
> kubectl create -f namespace.yml
2. Create - Deployment for flaskapi-backend -n webapp
> kubectl create -f flaskapi-backend-deployment.yml
3. Create - Service for flaskapi-backend
> kubectl create -f flaskapi-backend-service.yml -n webapp

## CI Integration


## ArgoCD integration
flaskapi-backend app ArgoCD integration steps listed below.

Folder structure 
```
.
├── argo-cd
│   ├── application.yaml
│   └── project.yaml
├── kubernetes
│   ├── flaskapi-backend-deployment.yml
│   ├── flaskapi-backend-service.yml
│   └── namespace.yml
└── README.md
```

<ins> **Steps for ArgoCD integration** </ins>
**Prerequisite**
> Kubernetes cluster setup running (minikube or cloud)

**MiniKube Setup**
1. create a namespace - argocd
> minikube kubectl -- create namespace argocd
2. create a arogcd deployment 
> minikube kubectl -- apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
3. validate if the pods running in argocd namespace
> minikube kubectl -- get pods -n argocd
4. Acess the argocd admin page on host box
> minikube kubectl -- port-forward service/argocd-server -n argocd 8080:443
5. Fetch the password for web login
> minikube kubectl -- -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
6. Create - Repository - flaskapi-backend using admin page - repository url = https://github.com/rajendravmattihalli/flaskapi-backend.git 
> <img width="1290" height="317" alt="Screenshot 2025-10-18 at 4 32 27 PM" src="https://github.com/user-attachments/assets/79974624-4d50-4be4-a559-a4db69a78d0d" />
8. Create - Project - flaskapi-backend
> minikube kubectl -- apply -f argo-cd/project.yaml
9. Create - Application - flaskapi-backend
> minikube kubectl -- apply -f argo-cd/application.yaml
10. Final validate the sync status - under application
> <img width="1675" height="902" alt="Screenshot 2025-10-18 at 4 03 56 PM" src="https://github.com/user-attachments/assets/27a1f5b3-c60c-4c70-bdce-5ceee0458509" />



## Sandbox Testing
