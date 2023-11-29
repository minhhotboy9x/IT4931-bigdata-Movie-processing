# IT4931-bigdata-Movie-processing
Course project.

The crawled movie data is streamed and processed by Kafka and PySpark.

### Install (window)
#### Download
Install python 3.10, jdk 1.8.0_202

Pip install the package including all requirements in a Python>=3.10 environment.

Download [Spark 3.5.0](https://spark.apache.org/downloads.html) and extract to `C:\Spark`

Download [winutils 3.0.0](https://github.com/steveloughran/winutils) and extract to `C:\Hadoop`

Download [Kafka 3.5.0 Scala 2.12](https://kafka.apache.org/downloads) and extract to `C:\Kafka`

#### Setup environment variables
Add `SPARK_HOME`: `C:\Spark\spark-3.5.0-bin-hadoop3`

Add `HADOOP_HOME`: `C:\Spark\spark-3.5.0-bin-hadoop3`

Add `JAVA_HOME`: `C:\Program Files\Java\jdk1.8.0_202`

Add `PYSPARK_PYTHON`: `C:\Program Files\Python310\python.exe`

- #### Add `PATH`
  Add `%SPARK_HOME%\bin`, `%HADOOP_HOME%\bin`, `%JAVA_HOME%\bin`


### Usage
Start the master:
```
cd %SPARK_HOME%
bin\spark-class2.cmd org.apache.spark.deploy.master.Master
```
Start the wokers: (run this cmd multiple times for multiple workers)
```
cd %SPARK_HOME%
bin\spark-class2.cmd org.apache.spark.deploy.worker.Worker <master url>
```
