from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os, json
from crawler import MovieDB
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from schema import MOVIE_SCHEMA

load_dotenv()

scala_version = '2.12'
spark_version = '3.5.0'
MASTER = 'spark://192.168.137.1:7077'
# MASTER = 'local'
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
   .config("spark.driver.maxResultSize", "4g") \
   .getOrCreate()

movie = MovieDB()
mv_data = []

# produce
for i in range(1, 10):
    print(i)
    print('________________')
    mv_data.extend(movie.get_movies(page=i))

df = spark.createDataFrame(mv_data, MOVIE_SCHEMA)
df.write.parquet("temp/movie_temp.parquet", mode="overwrite")
streaming_df = spark.readStream.schema(df.schema).parquet("temp/movie_temp.parquet")

    # query = df.selectExpr("CAST(id AS STRING)", "to_json(struct(*)) AS value") \
    #     .write \
    #     .format("kafka") \
    #     .option("kafka.bootstrap.servers", KAFKA_BROKER1) \
    #     .option("topic", MOVIE_TOPIC) \
    #     .save()

query = streaming_df \
    .selectExpr("CAST(id AS STRING)", "to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER1) \
    .option("topic", MOVIE_TOPIC) \
    .option("checkpointLocation", 'stream_ckpt') \
    .start()

query.awaitTermination()