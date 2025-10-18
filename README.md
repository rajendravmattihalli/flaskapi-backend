# flaskapi-backend
flaskapi backend CI - CD integration - job

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




