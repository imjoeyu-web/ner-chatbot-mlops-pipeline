provider "google" {
  project = "project-47ee8279-d093-40d1-8f6"
  region  = "asia-northeast3"
}
resource "google_service_account" "my_service_account" {
  account_id   = "gsa-kubeflow"
  display_name = "gsa-kubeflow"
}
resource "google_storage_bucket_iam_binding" "my_bucket_iam_binding" {
  bucket = "joey-kubeflow-datasets"
  role   = "roles/storage.admin"
  members = [
    "serviceAccount:gsa-kubeflow@project-47ee8279-d093-40d1-8f6.iam.gserviceaccount.com",
  ]
}