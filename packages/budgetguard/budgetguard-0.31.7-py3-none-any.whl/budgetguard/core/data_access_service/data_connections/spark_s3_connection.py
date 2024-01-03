from .connection import Connection
from .s3_connection import S3Connection
from pyspark.sql import SparkSession
from loguru import logger

# import json


class SparkS3Connection(Connection):
    NAME = "spark_s3"

    def __init__(self) -> None:
        self.s3_connection: S3Connection = S3Connection()
        self.spark_session: SparkSession = SparkS3Connection.connect(self)

    def __create_spark_session__(self) -> SparkSession:
        spark = SparkSession.builder.appName("BudgetGuard").getOrCreate()
        return spark

    def connect(self) -> SparkSession:
        logger.info("Connecting to Spark session...")
        return self.__create_spark_session__()
