# PySpark On Cloud Kubernetes Boilerplate

A fully customized and extendable template for PySpark on cloud Kubernetes.

### Introduction and Motivation
After deploying a few production applications in Spark using both the Scala and
Python APIs, running on both Amazon's EMR and GCP's Dataproc, we've decided to 
bite the bullet and build a prod-ready framework for Kubernetes that is fully
customized, and relatively easy to toggle versions and extend. This project is 
inspired by a few 'PySpark Boilerplate' versions that are out there, including
[Eran Kampf's](https://github.com/ekampf/PySpark-Boilerplate),
[Alex Ioannides's](https://github.com/AlexIoannides/pyspark-example-project), 
and [Mehdi Ouazza's](https://github.com/mehd-io/pyspark-boilerplate-mehdio)
respective implementations. 

We migrated to Spark on Kubernetes because:

1. we were frustrated with being tied 
to our cloud providers' release cycles for fully managed clusters. Sometimes
spark would release new features and we did not want to wait for them to be
propagated to a stable cluster release. 
2. we like the benefits of containerization which allow for higher speed 
iteration, environment-agnostic running, and dependency isolation. 
3. we would like to avoid vendor lock-in to the extent it is possible. 


### Prerequisites and Assumptions

- You should be confortable working in a Linux environment 
- [Working familiaity with docker](https://www.docker.com/get-started).
- [A local installation of Minikube](https://minikube.sigs.k8s.io/docs/start/) 
for development and testing.
- [Working familiarity with kubectl's API](https://kubernetes.io/docs/tasks/tools/)
- [A local installation of helm](https://helm.sh/docs/intro/quickstart/)
- We assume you know how to deal with authentication and permissions on your
 cloud platform, or are working with someone who does. For the purposes of
 this template we prioritize developer friendliness over security, but for 
 production applications please follow industry best practices (more on this
 later). 
- Comfort working in any cloud environment is helpful. The implementation listed
here is built for GCP's GKE, but it wouldn't take much refactoring to toggle to 
Amazon's EKS, Azure's AKS, etc. We opted for GKE because we believe it's the 
best kubernetes service available. 
- Ideally, working knowledge of terraform 
[and a local installation of it](https://learn.hashicorp.com/tutorials/terraform/install-cli),
or any IaC implementation.


### The Spark Base Image
The Dockerfile in the root repository is fully customized to allow for easy
(but at your own risk) toggling of Spark/Scala/Python/Hadoop/JDK versions. 
Note that there may be interactions and downstream effects of changing these, 
so test thoroughly when making changes here. There are defined sections for 
software installations as well as a block for cloud provider configuration, in
this case GCP. Feel free to modify, remove, or replace with your provider of 
choice.

This base image is also designed to allow for local development as if you are
on a cloud virtual machine. This means you can run interactive analysis in
Spark on a docker container running locally. The benefit of this is that 
prototyping is very cheap and easy to scale. You can also run distributed 
sessions locally via Minikube, or scale on a cloud cluster by changing the 
kubectl pointer. The same image can be used to run unit tests, etc. 

Note that the resulting image from this dockerfile can be relatively heavy large,
so you might want to run the build process remotely on a cloud build server and 
push to your remote container registry, rather than building locally and 
pushing layers over the internet.



### On Infrastructure as Code 

Note that there is a terraform directory with simple samples for what's 
necessary to spin up a remote cluster to run this application on. Note that 
typically you will not have your infrastructure code live in the same repository
as your application code, this is just for educational/informational purposes. 
How things are partitioned and maintained really depends on the organization
structure. 


### Application and Utility Structure

The basic project structure is as follows:

```bash
manifests/
 |   pyspark-interactive.yaml
 |   pyspark-k8s-boilerplate-cloud-etl.yaml
 |   pyspark-k8s-boilerplate-pi.yaml
 |   spark-namespace.yaml
 |   spark-rbac.yaml
secrets/
 |   key-file
 |   key-file-k8s-secret.yaml
src/pyspark_k8s_boilerplate/
 |-- config/
 |   |-- conf.yaml
 |   |-- handlers.py
 |-- jobs/
 |   |-- cloud_etl.py
 |   |-- interactive.py
 |   |-- pi.py
 |-- utils/
 |   |-- log.py
 |   |-- pyspark.py
 |   main.py
terraform/
 |   main.tf
 |   outputs.tf
 |   variables.tf
 |   versions.tf
tests/
 |   test_stub.py
Dockerfile
Makefile
MANIFEST.in
pyproject.toml
setup.cfg
spark-defaults.conf

```

The main python application is in `src/pyspark_k8s_boilerplate`. Configurations
can be set in the config directory, with conf.yaml and the handlers classes 
defining default configurations, which can be overridden by the CLI entrypoint 
in `src/pyspark_k8s_boilerplate/main.py`. Note that there are specific config
handlers defined for different domains, see the classes in handlers.py for more
information. 

There are three sample jobs that can be used for testing. The lowest bar is 
the pi.py job, which uses spark to approximate π. The higher bar is the 
cloud_etl job, which reads titanic.csv in object storage (you should stage 
this in GS, S3, etc). 
[Here's a direct link to the file](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv).

There is also an interactive.py module which we use to bootstrap an interactive
pyspark session. This was more challenging than expected as kubernetes support 
for distributed pyspark interactive shell sessions is lacking. More on this later. 

Note that all of the job modules must have an `execute()` function in order
for the optional (and recommended) command line entrypoint to work. You can also
run the job.py files directly without the entrypoint, but this includes a loss 
of flexibility to interactively override configurations.

Logging is set up in log.py, the pyspark session is initialized in pyspark.py
and is imported by the respective jobs and unit tests. 

A few comments about the other project artifacts: MANIFEST.in points to the 
yaml file which will be included in the python wheel/tarball distribution. 
pyproject.toml specifies the build requirements. We use setup.cfg in lieu of 
a setup.py file but in effect it serves the same function. 

The spark-defaults.conf file is critical for two things: enabling distributed
read from object storage, and pointing to the key file which gets mounted as a 
volume to the pod. 



- add environment variables: KUBEUSER, PROJECT (optional and TODO make this conditional in docker)... see: https://www.dev-diaries.com/social-posts/conditional-logic-in-dockerfile/
THASSIT 


- NOTE you can add an environment varibale for PYSPARK_CONFIG_DIR and it'll override the baked-in config 
- should prob put a burb in the readme on config management 








Note that the entrypoint only works if you have an 'execute' method but you can still run modules directly. Main purpose of the cli is to add args to a job that override config.yaml. 

Put a blurb on how they'll need their own container registry/ container repository .


Make sure kubnernetes cluster (minikube, perhaps GKE as well) is configured to read from container registry. 

note if they are having problems with image pull, run docker pull to get image locally.

I think you HAVE to reference the infrastructure and auth setup, and also indicate that you HAVE to patch the registry on the cluster. 


you'll need envsubst (native on most linux + mac dists) and the following environment vars:
- PROJECT 


Add a description of how the job yamls are structured, with an eye towards how the CLI works.

Walk through the initialization steps of kubernetes cluster (including terraform yaml..)

Blurb on the key file authentication and how there are better authentication methods... have a link to GCP and also make a note on how you'll see similar patterns for other cloud providers. 

Have a blurb on what docker interactive workflow would look like, how you can do local development on a container and then deploy it. 

Add some lines on the makefile, what each line does (even document it), and then a breakdown of each step. 

The interactive shell thing could be a 'clever solution to a stupid problem.' This is especially important given that MANY DS folks use spark instead of SQL for interactive analyses. Put a note that you can either run an interactive session in a container, and then explain that the current implementation of spark operator doesn't have a good solution for distributed interactive sessions so I made a workaround that is somewhat janky but seems to work. Remember.. you have to launch the job then kill one of the executors then you can ssh in.. 

Okay another prereq is that you mount the key file locally for docker interactive sessions, and then apply the key-file yaml with base64 encoding
