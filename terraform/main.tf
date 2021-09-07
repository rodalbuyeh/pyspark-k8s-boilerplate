provider "google" {
  project = var.project
  region  = "us-west2"
  zone    = "us-west2-b"
}


resource "google_service_account" "kubernetes-default" {
  account_id   = "k8s-service-account"
  display_name = "Kubernetes Service Account"
}

resource "google_container_cluster" "primary" {
  name     = var.name
  location = var.location
  description = "development kubernetes cluster"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "${var.name}-node-pool"
  project    = var.project
  location   = var.location
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    preemptible  = true
    machine_type = "n1-highmem-2"

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.kubernetes-default.email
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/trace.append"
    ]
  }
}
