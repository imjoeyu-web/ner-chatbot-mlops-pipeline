# NER Chatbot MLOps Pipeline 🚀

Container-native MLOps pipeline for NER chatbot using Kubeflow, Docker, and GCP

## 📌 프로젝트 개요

챗봇에서 활용하는 **개체명 인식(NER)** 모델을 위한 컨테이너 네이티브 MLOps 파이프라인 구축 실습입니다.
모델 학습부터 배포까지의 전체 과정을 Docker 컨테이너로 패키징하고 Kubeflow 파이프라인으로 자동화합니다.

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| 컨테이너 | Docker, Kubernetes, Minikube |
| ML 파이프라인 | Kubeflow |
| 클라우드 | GCP (Cloud Storage, Artifact Registry, Service Account) |
| 인프라 | Terraform |
| 모델 | Bidirectional LSTM (NER) |

## 📁 프로젝트 구조

```
ch07/
├── named_entity_recognition/
│   └── named_entity_recognition/
│       ├── components/
│       │   ├── preprocess/       # 전처리 컨테이너
│       │   │   ├── Dockerfile
│       │   │   ├── build_image.sh
│       │   │   ├── component.yaml
│       │   │   └── src/
│       │   ├── train/            # 학습 컨테이너
│       │   │   ├── Dockerfile
│       │   │   ├── build_image.sh
│       │   │   ├── component.yaml
│       │   │   └── src/
│       │   └── deploy/           # 배포 컨테이너
│       │       ├── Dockerfile
│       │       ├── build_image.sh
│       │       ├── component.yaml
│       │       └── src/
│       └── documentation/
│           └── Pipeline.ipynb    # 파이프라인 코드
└── terraform/
    └── terraform/
        └── morise-kubeflow/
            ├── gcs/              # GCS 버킷 생성
            ├── gar/              # Artifact Registry 생성
            └── gsa/              # 서비스 계정 생성
```

## 🔄 파이프라인 흐름

```
GCS 버킷 (데이터)
    ↓
전처리 컨테이너 (preprocess)
- CSV 데이터 읽기
- 단어/태그 전처리
- X, y 생성 후 GCS 저장
    ↓
학습 컨테이너 (train)
- Bidirectional LSTM 모델 학습
- 모델 저장 (GCS)
    ↓
배포 컨테이너 (deploy)
- 모델 서빙
```

## ☁️ GCP 리소스 구성 (Terraform)

| 리소스 | 용도 |
|--------|------|
| GCS 버킷 | 데이터/모델 파일 저장 |
| Artifact Registry | Docker 이미지 저장 |
| Service Account | GCP 접근 권한 관리 |

## 🚀 실행 방법

### 1. 환경 세팅
```bash
# Docker Desktop 실행 후
minikube start --driver=docker

# Kubeflow 설치
cd ch07/manifests
while ($true) { kustomize build example | kubectl apply --server-side --force-conflicts -f -; if ($?) { break }; echo "Retrying"; sleep 20 }
```

### 2. GCP 인프라 생성
```bash
# GCS 버킷 생성
cd terraform/morise-kubeflow/gcs
terraform init && terraform apply

# GAR 생성
cd ../gar
terraform init && terraform apply

# 서비스 계정 생성
cd ../gsa
terraform init && terraform apply
```

### 3. 도커 이미지 빌드 & 푸시
```bash
# GCP 인증
gcloud auth configure-docker asia-northeast3-docker.pkg.dev

# 빌드 & 푸시
cd named_entity_recognition/components
bash build_components.sh
bash copy_specification.sh
```

### 4. Kubeflow 대시보드 접속
```bash
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```
브라우저에서 `http://localhost:8080` 접속
- 이메일: user@example.com
- 비밀번호: 12341234

## ⚠️ 주의사항

- `build_image.sh`, `main.tf`, `backend.tf`의 프로젝트 ID와 버킷 이름을 본인 것으로 수정 필요
- `.sh` 파일은 Git Bash에서 실행 (PowerShell 불가)
- GCP 사용 후 VM 인스턴스 및 Workbench 반드시 중지
- `terraform destroy`로 불필요한 리소스 삭제

## 📝 참고

- [Kubeflow 공식 문서](https://www.kubeflow.org/docs/)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
