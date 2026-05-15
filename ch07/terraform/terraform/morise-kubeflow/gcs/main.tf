provider "google" {
  project = "project-47ee8279-d093-40d1-8f6"
  region  = "asia-northeast3"
}

resource "google_storage_bucket" "my_bucket" {
  name = "joey-kubeflow-datasets"
  location = "asia-northeast3"
  uniform_bucket_level_access = true
  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
}