from pyspark.sql import SparkSession
from schema import MOVIE_SCHEMA, GENRE_SCHEMA
from pyspark.sql.functions import explode, col, from_json, current_timestamp, expr, udf
from pyspark.sql.types import StringType, ArrayType
import os, json
from dotenv import load_dotenv

load_dotenv()
scala_version = '2.12'
spark_version = '3.5.0'
# MASTER = 'local'
MASTER = 'spark://192.168.137.1:7077'
KAFKA_BROKER1 = os.environ["KAFKA_BROKER1"]
MOVIE_TOPIC = os.environ["MOVIE_TOPIC"]
genre_path = 'genres.json'

with open('genres.json', 'r') as f:
    genre_names = json.loads(f.read())

genre_names = {item['id']: item['name'] for item in genre_names}

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.0',
    'org.apache.hadoop:hadoop-client:3.0.0',
]

spark = SparkSession.builder \
    .master(MASTER) \
    .appName("Movie Consumer") \
    .config("spark.jars.packages", ",".join(packages)) \
    .config("spark.driver.maxResultSize", "4g") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


# Broadcast bảng genre để sử dụng như một biến
genre_mapping = spark.sparkContext.broadcast(genre_names)

def map_genre_ids_to_names(genre_ids):
    return [genre_mapping.value.get(gid, None) for gid in genre_ids]

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

# Convert vote_average to float
df_movie = df_movie.withColumn("genres", expr("map_genre_ids_to_names(genre_ids)"))

df_movie = df_movie.drop('genre_ids')

query = df_movie.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
