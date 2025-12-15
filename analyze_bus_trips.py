from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Create Spark session
spark = SparkSession.builder \
    .appName("BusTripsAnalysis") \
    .getOrCreate()

# Read CSV from HDFS
df = spark.read.option("header", "true") \
    .csv("hdfs://namenode:9000/datos-uax/bus_trips.csv")

# Inspect data
df.printSchema()
df.show(5)

# Select relevant columns and cast type
df_selected = df.select(
    "destination",
    F.col("trip_duration_hours").cast("float").alias("trip_duration_hours")
)

# Group by destination and count trips
df_grouped = df_selected.groupBy("destination") \
    .agg(F.count("*").alias("trip_count"))

df_grouped.orderBy(F.desc("trip_count")).show()

# Register temp view for Spark SQL
df_selected.createOrReplaceTempView("bus_trips")

# SQL: trip count per destination
trip_count_sql = spark.sql("""
    SELECT destination, COUNT(*) AS trip_count
    FROM bus_trips
    GROUP BY destination
    ORDER BY trip_count DESC
""")

trip_count_sql.show()

# SQL: average duration > 60
avg_duration_sql = spark.sql("""
    SELECT destination, AVG(trip_duration_hours) AS avg_duration
    FROM bus_trips
    GROUP BY destination
    HAVING avg_duration > 60
    ORDER BY avg_duration DESC
""")

avg_duration_sql.show()

# Save results in Parquet
trip_count_sql.write.mode("overwrite") \
    .parquet("hdfs://namenode:9000/datos-uax/trip_analysis.parquet")

avg_duration_sql.write.mode("overwrite") \
    .parquet("hdfs://namenode:9000/datos-uax/avg_duration.parquet")

# Stop Spark
spark.stop()
