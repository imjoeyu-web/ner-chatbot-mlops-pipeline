terraform {
  backend "gcs" {
    bucket  = "morise-kubeflow-cr"
    prefix  = "infra/gar"
  }
}

