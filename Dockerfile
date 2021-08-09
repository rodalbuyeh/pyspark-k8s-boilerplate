FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install curl -y
RUN apt-get install vim -y


# install python and pip
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install -y python3.8 python3-pip

# install gcloud client (remove or replace with your provider of choice)

RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# install java 8
RUN apt-get install openjdk-8-jdk -y

# install scala 2.12
RUN apt-get install wget -y
RUN wget www.scala-lang.org/files/archive/scala-2.12.0.deb
RUN dpkg -i scala-2.12.0.deb

# install spark
RUN wget https://mirrors.sonic.net/apache/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
RUN tar xvf spark-3.1.2-bin-hadoop3.2.tgz
RUN mv spark-3.1.2-bin-hadoop3.2 /opt/spark

ENV SPARK_HOME /opt/spark
ENV PATH $PATH:/opt/spark/bin
ENV PYSPARK_PYTHON /usr/bin/python3.8



ENV HADOOP_VERSION 3.2.2
ENV SPARK_VERSION 3.1.2
