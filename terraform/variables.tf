variable "name" {
  default = "dev-gke-cluster"
}

variable "project" {
  type = string
  description = "The GCP project you want to run a GKE cluster in."
  default = "YOURPROJECT"
}

variable "location" {
  default = "us-west2"
}

variable "node_count" {
  default = 2
}

variable "machine_type" {
  default = "g1-small"
}
