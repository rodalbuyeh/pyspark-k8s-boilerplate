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