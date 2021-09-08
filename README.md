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
- working knowledge of terraform (or other IAC), iam, etc.. 
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

I think I'll move all of the terraform stuff into a directory here. Call it terraform. Put a note that typically you won't have your infra in the same repo depending on the organization.   

you'll need envsubst (native on most linux + mac dists) and the following environment vars:
- PROJECT 


Add a description of how the job yamls are structured, with an eye towards how the CLI works.

Walk through the initialization steps of kubernetes cluster (including terraform yaml..)

Blurb on the key file authentication and how there are better authentication methods... have a link to GCP and also make a note on how you'll see similar patterns for other cloud providers. 

A note on the config file, including the yaml itself and the handlers and how it gets called elsewhere. Note that there are other ways of doing the config but I like this one. 

A note on the jobs module, specifically the cloud etl and pi jobs. note that you have to conform to the execute API for the CLI to work.   

A note on the logging module.

A note on the pyspark session module. rename that to sparksession... 

Have a blurb on what docker interactive workflow would look like, how you can do local development on a container and then deploy it. 

Have a quick blurb on benefits of kubernetes over fully managed spark. 

Add some lines on the makefile, what each line does (even document it), and then a breakdown of each step. 

Might want to re-name main.py to cli.py because that's really what it is. 

The interactive shell thing could be a 'clever solution to a stupid problem.' This is especially important given that MANY DS folks use spark instead of SQL for interactive analyses. Put a note that you can either run an interactive session in a container, and then explain that the current implementation of spark operator doesn't have a good solution for distributed interactive sessions so I made a workaround that is somewhat janky but seems to work. Remember.. you have to launch the job then kill one of the executors then you can ssh in.. 

Okay another prereq is that you mount the key file locally for docker interactive sessions, and then apply the key-file yaml with base64 encoding
