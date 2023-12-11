from pyspark.sql.types import StructField, StructType, StringType, LongType, \
                                FloatType, IntegerType, DoubleType, DecimalType, \
                                ArrayType, BooleanType, DateType

MOVIE_SCHEMA = StructType([
    StructField("id", StringType(), nullable=True),
    StructField("adult", BooleanType(), nullable=True),
    StructField("genre_ids", ArrayType(IntegerType()), nullable=True),
    StructField("original_language", StringType(), nullable=True),
    StructField("overview", StringType(), nullable=True),
    StructField("popularity", StringType(), nullable=True),
    StructField("release_date", StringType(), nullable=True),
    StructField("title", StringType(), nullable=True),
    StructField("vote_average", StringType(), nullable=True),
    StructField("vote_count", IntegerType(), nullable=True),
])

GENRE_SCHEMA = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
])

ACTOR_SCHEMA =  StructType([
    StructField("id", StringType(), nullable=True),
    StructField("name", StringType(), nullable=True),
    StructField("adult", BooleanType(), True),
    StructField("gender", IntegerType(), True),
    StructField("known_for_department", StringType(), True),
    StructField("popularity", StringType(), True),
])