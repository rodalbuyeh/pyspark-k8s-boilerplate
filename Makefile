## ----------------------------------------------------------------------
## The purpose of this Makefile is to abstract common commands for
## building and running the pyspark-k8s-boilerplate application.
## ----------------------------------------------------------------------


help:                       ## show this help
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)


# docker commands -- TODO make the GCP stuff conditional on the build arg!

build_image:                ## build docker image
	docker build -t pyspark-k8s-boilerplate:latest . --build-arg gcp_project=${PROJECT}

it_shell:                   ## run interactive shell in docker container
	docker run -it pyspark-k8s-boilerplate bash


# k8s commands

start_k8s_local:            ## start local k8s via minikube
	minikube start --driver=hyperkit --memory 8192 --cpus 4

stop_k8s_local:             ## stop local k8s
	minikube stop

delete_k8s_local:           ## delete local k8s
	minikube delete

verify_k8s_dns:             ## verify that k8s dns is working properly
	kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
	sleep 10
	kubectl get pods dnsutils
	kubectl exec -i -t dnsutils -- nslookup kubernetes.default
	kubectl delete -f https://k8s.io/examples/admin/dns/dnsutils.yaml


# python

create_venv:                ## make and activate python virtual environment
	python3 -m venv env
	source env/bin/activate

delete_venv:                ## delete python virtual environment
	rm -r env

build:                      ## build python tarball and wheel
	python3 -m build

install: clean build        ## install python wheel
	pip3 install dist/pyspark_k8s_boilerplate-*.whl --no-cache-dir --force-reinstall

clean:                      ## clean artifacts
	rm -r -f dist
	rm -r -f src/*.egg-info

clear_mypy_cache:           ## clear mypy cache
	rm -r -f .mypy_cache


analyze_code:               ## run code analysis
	mypy src/pyspark_k8s_boilerplate
	flake8 src/pyspark_k8s_boilerplate
