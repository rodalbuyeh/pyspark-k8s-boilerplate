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
- Permissions to a container registry, either via Dockerhub or a private
registry (the latter is recommended). 
- We assume you know how to deal with authentication and permissions on your
 cloud platform, or are working with someone who does. For the purposes of
 this template we prioritize developer friendliness over security, but for 
 production applications please follow industry best practices (more on this
 later). Additionally your kubernetes cluster should be configured to have 
 permissions to read from the container registry. We will include some sample 
 code for patching your cluster, more on this later.
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
for distributed pyspark interactive shell sessions is lacking. More on this later. Note that all of the job modules must have an `execute()` function in order
for the optional (and recommended) command line entrypoint to work. You can also
run the job.py files directly without the entrypoint, but this includes a loss 
of flexibility to interactively override configurations.

Logging is set up in log.py, the pyspark session is initialized in pyspark.py
and is imported by the respective jobs and unit tests. A few comments about the other project artifacts: MANIFEST.in points to the 
yaml file which will be included in the python wheel/tarball distribution. 
pyproject.toml specifies the build requirements. We use setup.cfg in lieu of 
a setup.py file but in effect it serves the same function. The spark-defaults.conf file is critical for two things: enabling distributed
read from object storage, and pointing to the key file which gets mounted as a 
volume to the pod. 

### Required environment variables for development 

We have tried to keep the required environment variables to a minimum for the 
purposes of this template. All you should need is the following:

```bash
export PROJECT=$(gcloud info --format='value(config.project)')
export KUBEUSER='name'
export KUBEDOMAIN='domain.com'
```
You can modify and source the env.example file if it is more convenient. 

### Cloud Authentication
There are many ways to handle authentication. For instance, GCP offers
[a number of methods](https://cloud.google.com/container-registry/docs/advanced-authentication). 
Here we have tried to strike a balance between clarity and reasonable security. 
We opted for using a service account key to allow for longer lived
(and accordingly less overhead but higher risk authentication). Rather than 
baking the key into the container, we mount it as a volume from a local path, 
pushed to Kubernetes as a Kubernetes secret. 

If you are working with PII data, please consult your system administrators and
comply with your organization's best practices on authentication. 


### Order of Operations for Running K8s Spark Jobs 

**Step 0: Have a Kubernetes cluster running locally and remotely, with the 
spark operator and application dependencies installed and mounted.**

For your local:

```bash
minikube start --driver=hyperkit --memory 8192 --cpus 4
```

Toggle resources as you see fit. 

For GKE as used in this example, run this from the terraform directory:

```bash
terraform apply
```

Create a spark namespace: 

```bash 
kubectl apply -f manifests/spark-namespace.yaml
```

Install the spark operator: 

```bash
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install my-release spark-operator/spark-operator --namespace spark-operator --set image.tag=v1beta2-1.2.3-3.1.1
```

Create a cluster role binding: 
```bash
kubectl create clusterrolebinding ${KUBEUSER}-cluster-admin-binding --clusterrole=cluster-admin \
--user=${KUBEUSER}@${KUBEDOMAIN}
```

Set the spark operator namespace as default if it is not already:

```bash
kubectl config set-context --current --namespace=spark-operator
```

Initialize spark RBAC: 

```bash
kubectl apply -f manifests/spark-rbac.yaml
```

Push your base64 encoded key-file to kubernetes as a [secret](https://kubernetes.io/docs/concepts/configuration/secret/): 

```bash
kubectl apply -f secrets/key-file-k8s-secret.yaml
```
	
Verify that DNS is working properly:

```bash
kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
sleep 20
kubectl exec -i -t dnsutils -- nslookup kubernetes.default
kubectl delete -f https://k8s.io/examples/admin/dns/dnsutils.yaml
```

If things are working correctly, the result should look something like this:

```bash
Server:    10.0.0.10
Address 1: 10.0.0.10

Name:      kubernetes.default
Address 1: 10.0.0.1
```

If not, see [these instructions](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/#check-the-local-dns-configuration-first) to debug. 

If you are using a private repository, patch your cluster to use service account credentials:

```bash
kubectl --namespace=spark-operator create secret docker-registry gcr-json-key \
          --docker-server=https://gcr.io \
          --docker-username=_json_key \
          --docker-password="$$(cat secrets/key-file)" \
          --docker-email=${KUBEUSER}@${KUBEDOMAIN}

kubectl --namespace=spark-operator patch serviceaccount my-release-spark \
          -p '{"imagePullSecrets": [{"name": "gcr-json-key"}]}'
```

**Step 1: Build and push your image.**

```bash
docker build -t pyspark-k8s-boilerplate:latest . --build-arg gcp_project=${PROJECT}
docker tag pyspark-k8s-boilerplate gcr.io/${PROJECT}/pyspark-k8s-boilerplate
docker push gcr.io/${PROJECT}/pyspark-k8s-boilerplate
```

Note that you might have another root for the container registry. 

**Step 2: Run desired job via Kubernetes manifest.**

For example:

```bash
kubectl apply -f manifests/pyspark-k8s-boilerplate-cloud-etl.yaml
```

Note the structure of the cloud etl yaml file: 

```yaml
apiVersion: "sparkoperator.k8s.io/v1beta2"
kind: SparkApplication
metadata:
  name: pyspark-k8s-boilerplate-cloud-etl
  namespace: spark-operator
spec:
  type: Python
  pythonVersion: "3"
  mode: cluster
  image: "gcr.io/${PROJECT}/pyspark-k8s-boilerplate:latest"
  imagePullPolicy: Always
  mainApplicationFile: local:///opt/spark/work-dir/src/pyspark_k8s_boilerplate/main.py
  arguments:
    - --job
    - pyspark_k8s_boilerplate.jobs.cloud_etl
  sparkVersion: "3.1.2"
  restartPolicy:
    type: Never
  volumes:
    - name: "shared-volume"
      hostPath:
        path: "/shared"
        type: Directory
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "512m"
    labels:
      version: 3.1.2
    serviceAccount: my-release-spark
    volumeMounts:
      - name: "shared-volume"
        mountPath: "/shared"
    secrets:
      - name: key-file
        path: /secrets
        secretType: generic
  executor:
    cores: 1
    instances: 1
    memory: "1024m"
    labels:
      version: 3.1.2
    volumeMounts:
      - name: "shared-volume"
        mountPath: "/shared"
    secrets:
      - name: key-file
        path: /secrets
        secretType: generic
```

See the [spark operator user guide](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/user-guide.md)
for more details on this. We will note a few critical details here. The
`image` key should correspond to your application's docker image, as follows:
```yaml
image: "gcr.io/${PROJECT}/pyspark-k8s-boilerplate:latest"
```

```mainApplicationFile``` corresponds to the absolute path in the docker container
to the pyspark application entry point, as follows:
```yaml
mainApplicationFile: local:///opt/spark/work-dir/src/pyspark_k8s_boilerplate/main.py
```

`arguments` corresponds to the arguments passed to the cli entrypoint, 
the current implementation accepts the job parameter which corresponds to the actual
module in the application, and the execute function accepts additional parameters 
via the `--job-args` argument. Seee the following from the pyspark-k8s-boilerplate-pi.yaml:

```yaml
  arguments:
    - --job
    - pyspark_k8s_boilerplate.jobs.pi
    - --job-args
    - partitions=10
    - message=yummy
```

To view the spark UI for a running job, you can run the following to port
forward and access the UI at localhost:4041

```bash
kubectl port-forward -n spark-operator $(spark-driver) 4041:4040
```


### Python Development Workflow

You can run tests (pytest with code coverage) in the docker container as follows:

```bash
docker run pyspark-k8s-boilerplate make test
```

You can also run interactive sessions by running a docker container with the
secrets directory which contains your keyfile mounted to the container, as 
follows:

```bash
docker run --mount type=bind,source=/abs/path/to/secrets,target=/secrets -it pyspark-k8s-boilerplate bash
```

Then you can run make commands to build and install the python tarball and wheel.
More on this in the Makefile section. 

You can also run `make analyze` in the running container to get code analysis. 


### On the Makefile 

For this project we rely heavily on Make, rather than a variety of shell scripts
and functions. Here are the current available make commands which can be run for a variety 
of steps already discussed, including building the container, pushing, initializing
spark, running pyspark tests, etc. You can also view help by running `make help` 
from the project root: 

```bash
----------------------------------------------------------------------
The purpose of this Makefile is to abstract common commands for
building and running the pyspark-k8s-boilerplate application.
----------------------------------------------------------------------
help:                       show this help
build-image:                build docker image
it-shell: build-image       run interactive shell in docker container
push-image:                 push image to GCR
get-gke-cred:               get GKE credentials (if applicable)
start-k8s-local:            start local k8s via minikube
verify-k8s-dns:             verify that k8s dns is working properly
init-spark-k8s:             inititalize spark on kubernetes environment in your current kubectl context
spark-port-forward:         port forward spark UI to localhost:4041
patch-container-registry:   patch cluster to point to private repository - usually necessary for Minikube
create-activate-venv:       make and activate python virtual environment
build:                      build python tarball and wheel
install:                    install python wheel
clean-install: clean build  clean artifacts and install install python wheel
clean:                      clean artifacts
check_types:                run mypy type checker
lint:                       run flake8 linter
analyze: check_types lint   run full code analysis
test:                       run tests locally
docker-test: build-image    run tests in docker
get_pyspark_shell_conf:     move and modify injected spark operator configs for pyspark shell
run_k8s_pyspark_shell:      run pyspark shell on the kubernetes cluster
```

### BONUS: Bootstrapping Interactive Distributed Pyspark Sessions 

The interactive shell thing could be a 'clever solution to a stupid problem.' This is especially important given that MANY DS folks use spark instead of SQL for interactive analyses. Put a note that you can either run an interactive session in a container, and then explain that the current implementation of spark operator doesn't have a good solution for distributed interactive sessions so I made a workaround that is somewhat janky but seems to work. Remember.. you have to launch the job then kill one of the executors then you can ssh in.. 

Okay another prereq is that you mount the key file locally for docker interactive sessions, and then apply the key-file yaml with base64 encoding


## Other things that came to mind...

Put a note on how I build a wheel on local/build server and pushed directly into container, but you can (and should) also push to pypi-like repo to share utilities. 

Note that the structure of this app is data science focused, specifically for batch + lambda layers.. where configs are the input and the output is data, model artifacts, etc. 