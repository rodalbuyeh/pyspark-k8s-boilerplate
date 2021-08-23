## ----------------------------------------------------------------------
## The purpose of this Makefile is to abstract common commands for
## building and running the pyspark-k8s-boilerplate application.
## ----------------------------------------------------------------------


help:                       ## show this help
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)


# docker commands -- TODO make the GCP stuff conditional on the build arg!

build-image:                ## build docker image
	docker build -t pyspark-k8s-boilerplate:latest . --build-arg gcp_project=${PROJECT}

it-shell:                   ## run interactive shell in docker container
	docker run -it pyspark-k8s-boilerplate bash


# k8s commands

show-k8s-contexts:          ## show available kubernetes contexts
	kubectl config get-contexts


use-k8s-context:
ifdef name
	kubectl config use-context $(name)
else
	@echo 'No name defined. Run *kubectl config get-contexts pods* then indicate selection as follows:'
	@echo 'make name=clustername use_k8s_context'
endif

start-k8s-local:            ## start local k8s via minikube
	minikube start --driver=hyperkit --memory 8192 --cpus 4

stop-k8s-local:             ## stop local k8s
	minikube stop

delete-k8s-local:           ## delete local k8s
	minikube delete

verify-k8s-dns:             ## verify that k8s dns is working properly
	sleep 10
	kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
	sleep 20
	kubectl get pods dnsutils
	kubectl exec -i -t dnsutils -- nslookup kubernetes.default
	kubectl delete -f https://k8s.io/examples/admin/dns/dnsutils.yaml

init-spark-k8s:             ## inititalize spark on kubernetes environment in your current kubectl context
	kubectl apply -f manifests/spark-namespace.yaml
	helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
	helm install my-release spark-operator/spark-operator --namespace spark-operator --set image.tag=v1beta2-1.2.3-3.1.1
	kubectl create clusterrolebinding ${KUBEUSER}-cluster-admin-binding --clusterrole=cluster-admin \
	--user=${KUBEUSER}@${KUBEDOMAIN}
	helm status --namespace spark-operator my-release
	kubectl config set-context --current --namespace=spark-operator
	echo 'switched k8s context to spark operator namespace'
	kubectl get namespace
	sleep 5
	kubectl get pods
	kubectl apply -f manifests/spark-rbac.yaml

spark-port-forward:
ifdef spark-driver
	kubectl port-forward -n spark-operator $(spark-driver) 4041:4040
else
	@echo 'No driver defined. Run *kubectl get pods* then indicate as follows: *make spark-driver=podname port_forward*'
endif

set-default-namespace:
ifdef namespace
	kubectl config set-context --current --namespace=$(namespace)
else
	@echo 'No namespace defined. Indicate as follows: *make namespace=name set_default_namespace*'
endif


# python

create-activate-venv:       ## make and activate python virtual environment
	python3 -m venv env
	source env/bin/activate
	pip install build

delete-venv:                ## delete python virtual environment
	rm -r env

build:                      ## build python tarball and wheel
	python3 -m build

install:                    ## install python wheel
	pip3 install dist/pyspark_k8s_boilerplate-*.whl --no-cache-dir --force-reinstall

clean-install: clean build  ## clean artifacts and install install python wheel
	pip3 install dist/pyspark_k8s_boilerplate-*.whl --no-cache-dir --force-reinstall

clean:                      ## clean artifacts
	rm -r -f dist
	rm -r -f src/*.egg-info
	rm -r -f .mypy_cache

analyze:                    ## run code analysis
	mypy src/pyspark_k8s_boilerplate
	flake8 src/pyspark_k8s_boilerplate
