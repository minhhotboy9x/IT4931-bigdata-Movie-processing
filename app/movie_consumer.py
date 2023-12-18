from pyspark.sql import SparkSession
from schema import MOVIE_SCHEMA, GENRE_SCHEMA
from pyspark.sql.functions import to_timestamp, from_json, expr, to_date, current_timestamp
from pyspark.sql.types import StringType, ArrayType
import os, json
from dotenv import load_dotenv
import requests
load_dotenv()
scala_version = '2.12'
spark_version = '3.5.0'
MASTER = 'local'
# MASTER = 'spark://192.168.137.1:7077'
# MASTER = 'spark://172.28.240.1:7077'
KAFKA_BROKER1 = os.environ["KAFKA_BROKER1"]
MOVIE_TOPIC = os.environ["MOVIE_TOPIC"]
ES_NODES = os.environ['ES_NODES']
ES_RESOURCE = "movie"
genre_path = 'genres.json'
# ------------------------------------------------------------

def map_genre_ids_to_names(genre_ids):
    return [genre_names.get(gid, None) for gid in genre_ids]

def write_to_elasticsearch(df, epoch_id):
    df.show()
    df.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", ES_NODES) \
        .option("es.resource", ES_RESOURCE) \
        .option("es.index.auto.create", "true") \
        .option("es.nodes.wan.only", "true") \
        .mode("overwrite") \
        .save(ES_RESOURCE)

# ----------------------------------------------------------
    
with open(genre_path, 'r') as f:
    genre_names = json.loads(f.read())

genre_names = {item['id']: item['name'] for item in genre_names}

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.0',
    'org.apache.hadoop:hadoop-client:3.0.0',
    'org.elasticsearch:elasticsearch-spark-30_2.12:7.17.16'
]

spark = SparkSession.builder \
    .master(MASTER) \
    .appName("Movie Consumer") \
    .config("spark.jars.packages", ",".join(packages)) \
    .config("spark.cores.max", "2") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("Error")


# Định nghĩa hàm UDF từ hàm Python
spark.udf.register("map_genre_ids_to_names", map_genre_ids_to_names, ArrayType(StringType()))

# Read streaming data with watermark
df_msg = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER1) \
    .option("subscribe", MOVIE_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# df_msg.printSchema()
df_msg = df_msg.selectExpr("CAST(value AS STRING)", "timestamp") \
                .select(from_json("value", MOVIE_SCHEMA).alias('movie'))

# Extract movie information
df_movie = df_msg.select('movie.*')

# Convert vote_average and popularity to float
df_movie = df_movie.withColumn("popularity", expr("cast(popularity as double)"))
df_movie = df_movie.withColumn("vote_average", expr("cast(vote_average as double)"))

df_movie = df_movie.withColumn("genres", expr("map_genre_ids_to_names(genre_ids)"))

df_movie = df_movie.withColumn("release_date", to_date("release_date", "yyyy-MM-dd"))

df_movie = df_movie.drop('genre_ids')

query = df_movie.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_elasticsearch) \
    .start()

query.awaitTermination()
