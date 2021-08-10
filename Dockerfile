FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install curl -y
RUN apt-get install vim -y


# install python and pip
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install -y python3.8 python3-pip


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

# download and install hadoop
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
        tar -zx hadoop-${HADOOP_VERSION}/lib/native && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    echo Hadoop ${HADOOP_VERSION} native libraries installed in /opt/hadoop/lib/native

ADD spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ADD secrets/key-file /key-file

# install gcloud client (remove or replace with your provider of choice)

RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN curl https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-2.2.2.jar \
 > ${SPARK_HOME}/jars/gcs-connector-hadoop3-2.2.2.jar
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# activate gcloud service account
RUN gcloud auth activate-service-account --key-file=/key-file

# set service account authentication as application default credentials if you want to use it in context of other libs
ENV GOOGLE_APPLICATION_CREDENTIALS /key-file

# set default project
RUN gcloud config set project albell-dev
