from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
import os
scala_version = '2.12'
spark_version = '3.5.0'
# TODO: Ensure match above values match the correct versions
# os.environ['PYSPARK_SUBMIT_ARGS'] ="--master local[*] pyspark-shell"
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.0',
    'org.apache.hadoop:hadoop-client:3.0.0',
]
# Tạo một phiên Spark
spark = SparkSession.builder \
   .master("spark://172.18.32.1:7077") \
   .appName("movie consumer") \
   .config("spark.jars.packages", ",".join(packages)) \
   .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
# Địa chỉ của Kafka broker
# kafka_brokers = "localhost:9092"
kafka_brokers = "localhost:9095"
