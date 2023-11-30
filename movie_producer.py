from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os
from crawler import MovieDB
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from schema import MOVIE_SCHEMA

load_dotenv()

scala_version = '2.12'
spark_version = '3.5.0'
# MASTER = 'local'
MASTER = 'local'
KAFKA_BROKER1 = os.environ["KAFKA_BROKER1"]
MOVIE_TOPIC = os.environ["MOVIE_TOPIC"]

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.0',
    'org.apache.hadoop:hadoop-client:3.0.0',
]

spark = SparkSession.builder \
   .master(MASTER) \
   .appName("Movie Producer") \
   .config("spark.jars.packages", ",".join(packages)) \
   .getOrCreate()


movie = MovieDB()
movie_schema = MOVIE_SCHEMA


# produce
for i in range(1, 5):
    print(i)
    print('________________')
    mv_data = movie.get_movies(page=i)
    df = spark.createDataFrame(mv_data, movie_schema)
    df.selectExpr("CAST(id AS STRING)", "to_json(struct(*)) AS value") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER1) \
        .option("topic", MOVIE_TOPIC) \
        .save()

