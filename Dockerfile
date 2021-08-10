FROM ubuntu:18.04

# change shell to one that supports parameter expansion
SHELL ["/bin/bash", "-c"]

# toggle these versions judiciously, there are downstream effects and interactions between them
ENV HADOOP_VERSION 3.2.2
ENV SPARK_VERSION 3.1.2
ENV SCALA_VERSION 2.12.0
ENV PYTHON_VERSION 3.8
ENV JDK_VERSION 8

RUN apt-get update
RUN apt-get install curl -y
RUN apt-get install vim -y

# install python and pip
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION:0:1}-pip

# install jdk
RUN apt-get install openjdk-${JDK_VERSION}-jdk -y

# install scala
RUN apt-get install wget -y
RUN wget www.scala-lang.org/files/archive/scala-${SCALA_VERSION}.deb
RUN dpkg -i scala-${SCALA_VERSION}.deb

# install spark
RUN wget https://mirrors.sonic.net/apache/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION:0:3}.tgz
RUN tar xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION:0:3}.tgz
RUN mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION:0:3} /opt/spark

ENV SPARK_HOME /opt/spark
ENV PATH $PATH:/opt/spark/bin
ENV PYSPARK_PYTHON /usr/bin/python${PYTHON_VERSION}

# download and install hadoop
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
        tar -zx hadoop-${HADOOP_VERSION}/lib/native && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    echo Hadoop ${HADOOP_VERSION} native libraries installed in /opt/hadoop/lib/native

ADD spark-defaults.conf /opt/spark/conf/spark-defaults.conf

####################################################################################################
# Cloud provider specific configuration -- modify, remove, or replace with your provider of choice #
####################################################################################################

# set GCP project
ARG gcp_project

# install gcloud client and hadoop storage connector
ENV GCS_LIB_VERS 2.2.2
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN curl https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop${HADOOP_VERSION:0:1}-${GCS_LIB_VERS}.jar \
 > ${SPARK_HOME}/jars/gcs-connector-hadoop${HADOOP_VERSION:0:1}-${GCS_LIB_VERS}.jar
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# activate gcloud service account
ADD secrets/key-file /key-file
RUN gcloud auth activate-service-account --key-file=/key-file

# set service account authentication as application default credentials if you want to use it in context of other libs
ENV GOOGLE_APPLICATION_CREDENTIALS /key-file

# set default project
RUN gcloud config set project ${gcp_project}
