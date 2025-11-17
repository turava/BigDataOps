FROM jupyter/base-notebook:x86_64-python-3.11.6

USER root

# Dependencias básicas
RUN dpkg --configure -a && apt-get update && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends curl gcc openjdk-11-jdk

ENV SPARK_HOME="/opt/spark"
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/"

# Crear carpeta spark
RUN mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

# ============================
# Spark local predescargado
# ============================
# Copiamos el archivo .tgz descargado desde spark/
COPY spark-3.4.2-bin-hadoop3.tgz /tmp/spark.tgz

RUN tar -xzf /tmp/spark.tgz --directory /opt/spark --strip-components=1 \
 && rm -f /tmp/spark.tgz
# =============================

ENV SPARK_HOME="/opt/spark"

WORKDIR /home/jovyan

# Versión de pyspark igual a Spark
ARG spark_version=3.4.2
ENV PYSPARK_VERSION="pyspark==${spark_version}"

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install ${PYSPARK_VERSION}

ENTRYPOINT ["start-notebook.sh", "--NotebookApp.token=''"]
