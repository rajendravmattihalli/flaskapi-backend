# flaskapi-backend
flaskapi-backend web application

<img width="618" height="199" alt="Screenshot 2025-10-19 at 1 18 49 PM" src="https://github.com/user-attachments/assets/46609616-05fa-4d65-ae11-ea88aa590e6c" />


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

```
├── observability
│   └── flaskapi-backend-servicemonitor.yml
```
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

```
flaskapi-backend % minikube kubectl -- logs flaskapi-backend-86bc48cf7c-ggz5k -n webapp
 * Serving Flask app '/app/app.py'
 * Debug mode: off
{"level": "INFO", "service": "flaskapi-backend", "message": "GET / 200 0.0008s", "logger": "flaskapi", "time": "2025-10-19 07:28:42,968"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /favicon.ico 500 0.0011s", "logger": "flaskapi", "time": "2025-10-19 07:28:43,071"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /metrics 200 0.0031s", "logger": "flaskapi", "time": "2025-10-19 07:28:47,538"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /favicon.ico 500 0.0002s", "logger": "flaskapi", "time": "2025-10-19 07:28:47,605"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /api 200 0.0003s", "logger": "flaskapi", "time": "2025-10-19 07:28:52,051"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /favicon.ico 500 0.0003s", "logger": "flaskapi", "time": "2025-10-19 07:28:52,100"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /status 500 0.0002s", "logger": "flaskapi", "time": "2025-10-19 07:29:00,933"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /favicon.ico 500 0.0002s", "logger": "flaskapi", "time": "2025-10-19 07:29:00,971"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /health 200 0.0001s", "logger": "flaskapi", "time": "2025-10-19 07:29:06,295"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /favicon.ico 500 0.0002s", "logger": "flaskapi", "time": "2025-10-19 07:29:06,339"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /api 200 0.0009s", "logger": "flaskapi", "time": "2025-10-19 07:33:23,401"}
{"level": "INFO", "service": "flaskapi-backend", "message": "GET /api 200 0.0003s", "logger": "flaskapi", "time": "2025-10-19 07:33:47,386"}
```


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
**Prerequisite**
1. OIDC provider
2. IAM role - Githubactions
3. Permission to ECR policy
4. Change <ACCOUNT_ID> - cibuild-ecr/trust-policy.json
5. create a GITHUB secret - AWS_ACCOUNT_ID 

**OIDC provider**
```
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

**IAM role - GithubActions**
```
aws iam create-role \
  --role-name GitHubActionsECRRole \
  --assume-role-policy-document trust-policy.json
```

**Permission to ECR policy**
```
aws iam put-role-policy \
  --role-name GitHubActionsECRRole \
  --policy-name ECRPushPolicy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage"
        ],
        "Resource": "*"
      }
    ]
  }'

```


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
