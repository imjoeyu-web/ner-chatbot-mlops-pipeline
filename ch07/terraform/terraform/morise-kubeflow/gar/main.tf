provider "google" {
  project = "project-47ee8279-d093-40d1-8f6"
  region  = "asia-northeast3"
}

resource "google_artifact_registry_repository" "my_repository" {
  location      = "asia-northeast3"
  repository_id = "morise-kubeflow-cr"
  description   = "Kubeflow container registry"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository_iam_binding" "public_access" {
  location    = google_artifact_registry_repository.my_repository.location
  project     = google_artifact_registry_repository.my_repository.project
  repository  = google_artifact_registry_repository.my_repository.repository_id
  role        = "roles/artifactregistry.reader"
  members     = ["allUsers"]
}
