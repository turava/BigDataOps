from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCount").getOrCreate()

df = spark.read.text("hdfs://namenode:9000/datos-uax/simple_text.txt")

words = df.selectExpr("explode(split(value, ' ')) as word")

word_counts = words.groupBy("word").count()

word_counts.show()

word_counts.write.csv("hdfs://namenode:9000/datos-uax/output_wordcount", mode="overwrite")

spark.stop()
