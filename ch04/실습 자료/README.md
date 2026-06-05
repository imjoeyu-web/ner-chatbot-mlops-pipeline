# 패스트캠퍼스 강의 예제
- [10개 프로젝트로 한 번에 끝내는 MLOps 파이프라인 구현](https://fastcampus.co.kr/data_online_mlopspj)
  - ```Part4-CH03. 금융 이상탐지 수행을 위한 MLOps 파이프라인 구축```
  - ```Part4-CH04. 금융 이상탐지 파이프라인의 효과적인 모니터링과 성능개선을 위한 환경 구성```

## Download sample datasets
1. 다운로드: [Fraudulent Transactions Data](https://www.kaggle.com/datasets/chitwanmanchanda/fraudulent-transactions-data) (Kaggle)
2. 받은 압축파일을 프로젝트 디렉토리로 이동
3. 압축파일명을 ```sample_data.zip```으로 변경

## Setting Hosts File
### Part4-CH03
```
127.0.0.1	gitlab.mlops.io
127.0.0.1	docker-registry.mlops.io
127.0.0.1	airflow.mlops.io
127.0.0.1	airflow-worker.mlops.io
```

### Part4-CH04
```
127.0.0.1	mlflow.mlops.io
127.0.0.1	grafana.mlops.io
127.0.0.1	prometheus.mlops.io
127.0.0.1	minio.mlops.io
127.0.0.1	mlservice.mlops.io
```
