from .connection import Connection
from .s3_connection import S3Connection
from pyspark.sql import SparkSession
from loguru import logger
import json


class SparkS3Connection(Connection):
    NAME = "spark_s3"

    def __init__(self) -> None:
        self.s3_connection: S3Connection = S3Connection()
        self.spark_session: SparkSession = SparkS3Connection.connect(self)

    def __create_spark_session__(self) -> SparkSession:
        spark = SparkSession.builder.appName("BudgetGuard").getOrCreate()
        aws_credentials = json.loads(
            self.s3_connection.get_aws_secret("budget_guard_aws_credentials")
        )
        spark._jsc.hadoopConfiguration().set(
            "fs.s3a.access.key", aws_credentials["aws_access_key_id"]
        )
        spark._jsc.hadoopConfiguration().set(
            "fs.s3a.secret.key", aws_credentials["aws_secret_access_key"]
        )
        spark._jsc.hadoopConfiguration().set(
            "fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )
        spark._jsc.hadoopConfiguration().set(
            "com.amazonaws.services.s3.enableV4", "true"
        )
        spark._jsc.hadoopConfiguration().set(
            "fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider",
        )
        spark._jsc.hadoopConfiguration().set(
            "fs.s3a.endpoint", "us-east-1.amazonaws.com"
        )
        return spark

    def connect(self) -> SparkSession:
        logger.info("Connecting to Spark session...")
        return self.__create_spark_session__()
