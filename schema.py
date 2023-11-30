from pyspark.sql.types import StructField, StructType, StringType, LongType, \
                                FloatType, IntegerType, DoubleType, DecimalType, \
                                ArrayType, BooleanType, DateType

MOVIE_SCHEMA = StructType([
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

GENRE_SCHEMA = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True)
])