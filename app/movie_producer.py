from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os, json
from crawler import MovieDB
from schema import MOVIE_SCHEMA

load_dotenv()

scala_version = '2.12'
spark_version = '3.5.0'
# MASTER = 'spark://172.28.240.1:7077'
# MASTER = 'spark://192.168.137.1:7077'
MASTER = 'local'
KAFKA_BROKER1 = os.environ["KAFKA_BROKER1"]
MOVIE_TOPIC = os.environ["MOVIE_TOPIC"]

# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages io.delta:delta-core_2.12:2.2.0 --driver-memory 4g pyspark-shell'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.0',
    'org.apache.hadoop:hadoop-client:3.0.0',
    'io.delta:delta-core_2.12:2.2.0'
]

spark = SparkSession.builder \
   .master(MASTER) \
   .appName("Movie Producer") \
   .config("spark.jars.packages", ",".join(packages)) \
   .config("spark.cores.max", "2") \
   .config("spark.executor.memory", "2g") \
   .getOrCreate()

spark.sparkContext.setLogLevel("Error")

movie = MovieDB()
mv_data = []

# produce
for i in range(20, 40):
    print(i)
    print('________________')
    mv_data = movie.get_movies(page=i)
    df = spark.createDataFrame(mv_data, MOVIE_SCHEMA)
    query = df.selectExpr("CAST(id AS STRING)", "to_json(struct(*)) AS value") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "127.0.0.1:9093") \
        .option("topic", MOVIE_TOPIC) \
        .save()
