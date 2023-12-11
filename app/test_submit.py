from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages io.delta:delta-core_2.12:2.2.0 --driver-memory 4g pyspark-shell'
# MASTER = 'spark://172.28.240.1:7077'
MASTER = 'spark://192.168.137.1:7077'
# MASTER = 'local'
# Create a SparkSession
spark = SparkSession.builder \
   .appName("My App") \
   .master(MASTER) \
   .config("spark.executorEnv.PYSPARK_PYTHON", "/usr/local/bin/python") \
   .getOrCreate()
spark.sparkContext.setLogLevel("Error")
rdd = spark.sparkContext.parallelize(range(1, 100))

print("THE SUM IS HERE: ", rdd.sum())
# Stop the SparkSession
spark.stop()