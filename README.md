# BigDataOps – Entorno Local Big Data (Hadoop, Spark, Jupyter)

Proyecto Docker para levantar un entorno Big Data completo con HDFS, YARN, Spark, Jupyter y servicios auxiliares.

## Arranque del entorno

docker compose up -d
docker ps

## Interfaces del ecosistema

NameNode (HDFS): http://localhost:9870
YARN ResourceManager: http://localhost:8088
Spark Master UI: http://localhost:8080
Spark History Server: http://localhost:18080
JupyterLab: http://localhost:8889

##Comandos básicos de HDFS

Entrar al contenedor del NameNode:

docker exec -it namenode bash

Crear carpeta en HDFS y subir archivos:

hdfs dfs -mkdir -p /datos-uax
hdfs dfs -put /hadoop/applications/bus_trips.csv /datos-uax/
hdfs dfs -ls /datos-uax

Subir un archivo desde la máquina local:

Host → contenedor
docker cp simple_text.txt namenode:/tmp/simple_text.txt

Dentro del contenedor
docker exec -it namenode bash
hdfs dfs -put /tmp/simple_text.txt /datos-uax/

## Ejecución de trabajos Spark

docker cp script.py spark-master:/tmp/script.py
docker exec -it spark-master bash
cd /tmp
spark-submit script.py

Comprobar resultados en HDFS:

hdfs dfs -ls /datos-uax/output_wordcount
hdfs dfs -cat /datos-uax/output_wordcount/part-00000*.csv

# Uso de Spark desde Jupyter
http://localhost:8889

## Ejemplo básico en un notebook:

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df = spark.read.csv(
    "hdfs://namenode:9000/datos-uax/bus_trips.csv",
    header=True,
    inferSchema=True
)

df.show(5)
spark.stop()

## Preparación para Spark History Server

Si es necesario crear la ruta de logs:
docker exec -it namenode bash
hdfs dfs -mkdir -p /shared/spark-logs
hdfs dfs -chmod -R 777 /shared

## Parar el entorno
docker compose down

## Para eliminar volúmenes:

docker compose down -v
