from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os, json
from crawler import MovieDB
from schema import MOVIE_SCHEMA

load_dotenv()

scala_version = '2.12'
spark_version = '3.2.3'

MASTER = os.environ["MASTER"]
KAFKA_BROKER1 = os.environ["KAFKA_BROKER1"]
MOVIE_TOPIC = os.environ["MOVIE_TOPIC"]
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages io.delta:delta-core_2.12:2.2.0 --driver-memory 4g pyspark-shell'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.0',
    'org.apache.hadoop:hadoop-client:3.2.0',
    'org.elasticsearch:elasticsearch-spark-30_2.12:7.17.16',
]

spark = SparkSession.builder \
   .master(MASTER) \
   .appName("Movie Producer") \
   .config("spark.jars.packages", ",".join(packages)) \
   .config("spark.cores.max", "1") \
   .config("spark.executor.memory", "1g") \
   .getOrCreate()

spark.sparkContext.setLogLevel("error")

movie = MovieDB()
mv_data = []

# produce
for i in range(1, 10):
    print(i)
    print('________________')
    mv_data = movie.get_movies(page=i)
    df = spark.createDataFrame(mv_data, MOVIE_SCHEMA)
    df.show()
    query = df.selectExpr("CAST(id AS STRING)", "to_json(struct(*)) AS value") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER1) \
        .option("topic", MOVIE_TOPIC) \
        .save()
