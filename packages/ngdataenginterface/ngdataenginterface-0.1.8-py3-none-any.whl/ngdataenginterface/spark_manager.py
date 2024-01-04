from pyspark import SQLContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf


class SparkManager:
    def set_spark_config(
        self, name, aws_access_key_id=None, aws_secret_access_key=None
    ):
        # Create a SparkConf object and set the application name
        config = SparkConf().setAppName(name)

        # Set the Parquet datetimeRebaseModeInRead, datetimeRebaseModeInWrite, and int96RebaseModeInWrite to "LEGACY"
        config.set("spark.sql.parquet.datetimeRebaseModeInRead", "LEGACY")
        config.set("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
        config.set("spark.sql.parquet.int96RebaseModeInWrite", "LEGACY")
        # Set the packages to be used by Spark for Hadoop AWS integration
        config.set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.1")
        # config.set("spark.jars.packages", "com.amazonaws:aws-java-sdk:1.11.469")
        # config.set('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')

        # Add AWS credentials to Spark config if provided
        # This is needed when running GitLab CI or running locally
        # If the credentials are not provided, the Spark application will use the IAM role assigned to the EMR cluster
        if aws_access_key_id and aws_secret_access_key:
            config.set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
            config.set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)

        return config

    def __init__(self, app_name, aws_access_key_id=None, aws_secret_access_key=None):
        # Set the Spark configuration based on the provided AWS credentials and application name
        conf = self.set_spark_config(
            name=app_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.conf = conf
        # Create the SparkSession using the specified configuration
        self.spark = SparkSession.builder.config(conf=conf).getOrCreate()
        sc = self.spark.sparkContext
        sc.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")
        sc._jsc.hadoopConfiguration().set(
            "fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )