from pyspark.sql.types import StructField, StructType, StringType, LongType, \
                                FloatType, IntegerType, DoubleType, DecimalType, \
                                ArrayType, BooleanType, DateType

MOVIE_SCHEMA = StructType([
    StructField("id", StringType(), nullable=True),
    StructField("adult", BooleanType(), nullable=True),
    StructField("genres", ArrayType(
        StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True)
        ])
    ), nullable=True),
    StructField("original_language", StringType(), nullable=True),
    StructField("overview", StringType(), nullable=True),
    StructField("popularity", StringType(), nullable=True),
    StructField("release_date", StringType(), nullable=True),
    StructField("title", StringType(), nullable=True),
    StructField("production_companies", ArrayType(
        StructType([
            StructField("id", IntegerType(), True),
            StructField("logo_path", StringType(), True),
            StructField("name", StringType(), True),
            StructField("origin_country", StringType(), True),
        ])
    ), nullable=True),
    StructField("production_countries", ArrayType(
        StructType([
            StructField("iso_3166_1", StringType(), True),
            StructField("name", StringType(), True),
        ])
    ),nullable=True),
    StructField("runtime", StringType(), nullable=True),
    StructField("budget", StringType(), nullable=True),
    StructField("revenue", StringType(), nullable=True),
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