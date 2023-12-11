from pyspark.sql import SparkSession
from schema import ACTOR_SCHEMA, GENRE_SCHEMA
from pyspark.sql.functions import explode, col, from_json, current_timestamp, expr, udf
from pyspark.sql.types import StringType, ArrayType
import os, json
from dotenv import load_dotenv

load_dotenv()
scala_version = '2.12'
spark_version = '3.5.0'
MASTER = 'local'
# MASTER = 'spark://spark-master:7077'
# MASTER = 'spark://172.28.240.1:7077'
KAFKA_BROKER1 = os.environ["KAFKA_BROKER1"]
ACTOR_TOPIC= os.environ["ACTOR_TOPIC"]
gender_path = 'genders.json'

with open(gender_path, 'r') as f:
    gender_names = json.loads(f.read())

gender_names = {item['id']: item['name'] for item in gender_names}

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.0',
    'org.apache.hadoop:hadoop-client:3.0.0',
]

spark = SparkSession.builder \
    .master(MASTER) \
    .appName("Movie Consumer") \
    .config("spark.jars.packages", ",".join(packages)) \
    .config("spark.cores.max", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("Error")

def map_gender_id_to_name(gender_id):
    return gender_names.get(gender_id, None) 

# Định nghĩa hàm UDF từ hàm Python
spark.udf.register("map_gender_id_to_name", map_gender_id_to_name, StringType())

# Read streaming data with watermark
df_msg = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER1) \
    .option("subscribe", ACTOR_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# df_msg.printSchema()
df_msg = df_msg.selectExpr("CAST(value AS STRING)", "timestamp") \
                .select(from_json("value", ACTOR_SCHEMA).alias('actor'))

df_actor = df_msg.select('actor.*')

df_actor = df_actor.withColumn("popularity", expr("cast(popularity as double)"))
df_actor = df_actor.withColumn('gender', expr("map_gender_id_to_name(gender)"))

query = df_actor.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
