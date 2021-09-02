# pyspark-k8s-boilerplate
Template for PySpark on Kubernetes

Assuming:
- you know how to deal with authentication, note that there are a number of ways but for the purposes of this demo I'm using the easiest (and most insecure)

Have a thing about prerequisites
- unix or linux like OS, and accordingly know some bash scripting
- make installed on machine
- docker installed on machine 
- minikube (installations differ by machine )
- kubectl 
- helm 
- add environment variables: KUBEUSER, PROJECT (optional and TODO make this conditional in docker)
THASSIT 

You might also indicate that GCP is an almost-prerequisite if you want to run this for cloud ops 

- NOTE you can add an environment varibale for PYSPARK_CONFIG_DIR and it'll override the baked-in config 
- should prob put a burb in the readme on config management 

References:
- https://github.com/mehd-io/pyspark-boilerplate-mehdio
- https://github.com/AlexIoannides/pyspark-example-project
- https://github.com/ekampf/PySpark-Boilerplate


This looks interesting too, stash for later:

https://github.com/AlexIoannides/kubernetes-mlops

- also note that you have specific config handlers, and specific loggers 

TODO add an interactive cluster mode 
TODO drop root user installations 

Note that the entrypoint only works if you have an 'execute' method but you can still run modules directly. Main purpose of the cli is to add args to a job that override config.yaml. 

Put a blurb on how they'll need their own container registry/ container repository .

This can be a heavy weight image so you might want to run this on a build server in the cloud and push to whatever container registry.. rather than locally and pushing layers over network.

Make sure kubnernetes cluster (minikube, perhaps GKE as well) is configured to read from container registry. 

note if they are having problems with image pull, run docker pull to get image locally.

I think you HAVE to reference the infrastructure and auth setup, and also indicate that you HAVE to patch the registry on the cluster. 

I think I'll move all of the terraform stuff into a directory here. Call it terraform.    