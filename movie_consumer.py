from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, LongType, \
                                FloatType, IntegerType, DoubleType, DecimalType, \
                                ArrayType, BooleanType, DateType
from pyspark.sql.functions import explode, col, udf
from pyspark.sql.functions import split, expr
from crawler import MovieDataset, MovieDB
import os
import json

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
   .master("local") \
   .appName("Movie Consumer") \
   .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

@udf(ArrayType(StringType()))
def map_genre_names(genre_ids):
    genre_names = [row['name'] for row in df_genre.collect() if row['genre_id'] in genre_ids]
    return genre_names

# Define the schema
movie_schema = StructType([
    StructField("id", StringType(), nullable=False),
    StructField("adult", BooleanType(), nullable=False),
    StructField("genre_ids", ArrayType(IntegerType()), nullable=True),
    StructField("original_language", StringType(), nullable=True),
    StructField("overview", StringType(), nullable=True),
    StructField("popularity", DoubleType(), nullable=True),
    StructField("release_date", StringType(), nullable=True),
    StructField("title", StringType(), nullable=True),
    StructField("vote_average", StringType(), nullable=True),
    StructField("vote_count", IntegerType(), nullable=True),
])

genre_schema = StructType([
    StructField("id", IntegerType(), nullable=True),
    StructField("name", StringType(), nullable=True)
])


# Get movie data
movies = MovieDB()
mv_json = movies.get_movies(page=1)

# Create DataFrame
df_movie = spark.createDataFrame(mv_json, schema=movie_schema)

df_genre = spark.createDataFrame(movies.genres, schema=genre_schema)

df_genre.createOrReplaceTempView("df_genre")

df_movie = df_movie.withColumn("vote_average", col("vote_average").cast("float"))

# Explode the genre_ids array
df_exploded = df_movie.select(col("id").alias("id_mv"), "genre_ids").withColumn("genre_id", explode("genre_ids"))

# Join with df_genre to get genre_names
df_result = df_exploded.join(df_genre, df_exploded["genre_id"] == df_genre["id"]) \
        .withColumnRenamed('genre_id', '_genre_id')  \
        .groupBy("id_mv").agg({"name": "collect_list"})

# Rename the column
df_result = df_result.withColumnRenamed("collect_list(name)", "genres")

# Join the result back to the original dataframe
df_movie = df_movie.join(df_result, df_movie['id'] == df_result['id_mv'] , "left")

df_movie = df_movie.drop("genre_ids").drop("id_mv")

df_movie.show()