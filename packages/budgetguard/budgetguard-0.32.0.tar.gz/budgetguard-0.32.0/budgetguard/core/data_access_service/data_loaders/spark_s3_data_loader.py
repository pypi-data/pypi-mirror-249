from .data_loader import DataLoader
from ..data_connections import connect
from loguru import logger
from typing import Dict


class SparkS3DataLoader(DataLoader):
    NAME = "spark_s3"

    def __init__(self):
        """
        Constructor for SparkS3DataLoader class.
        """
        super().__init__()
        self.spark_s3_connection = connect(self.NAME)

    def __build_file_path__(
        self, datalake_config: Dict[str, str], partition_config: Dict[str, str]
    ):
        """
        Method for building the file path.
        """
        bucket_prefix = self.__get_bucket_prefix__()
        return "{0}{1}/{2}/{3}".format(
            bucket_prefix,
            datalake_config["datalake_bucket"],
            datalake_config["datalake_key"],
            self.build_partition_path(partition_config),
        )

    def __get_bucket_prefix__(self) -> str:
        """
        Method for getting the bucket prefix.
        """
        if (
            self.spark_s3_connection.platform
            == self.spark_s3_connection.__Platform__.LOCAL
        ):
            return "s3a://"
        elif (
            self.spark_s3_connection.platform
            == self.spark_s3_connection.__Platform__.EMR
        ):
            return "s3://"
        else:
            raise Exception("Unknown platform!")

    def read(
        self, datalake_config: Dict[str, str], partition_config: Dict[str, str]
    ):
        """
        Method for reading data from the datalake.
        """
        file_path = self.__build_file_path__(datalake_config, partition_config)
        logger.info("Reading data from path: {0}".format(file_path))
        options = datalake_config.get("options", {})
        schema = datalake_config.get("spark_schema", None)
        if schema:
            df = (
                self.spark_s3_connection.spark_session.read.format(
                    datalake_config["file_extension"]
                )
                .options(**options)
                .schema(schema)
                .load(file_path)
            )
        else:
            df = (
                self.spark_s3_connection.spark_session.read.format(
                    datalake_config["file_extension"]
                )
                .options(**options)
                .load(file_path)
            )
        logger.info("Finished reading data from path: {0}".format(file_path))
        return df

    def write(
        self,
        dataframe,
        datalake_config: Dict[str, str],
        partition_config: Dict[str, str],
    ):
        """
        Method for writing data to the datalake.
        """
        file_path = self.__build_file_path__(datalake_config, partition_config)
        logger.info("Writing data to path: {0}".format(file_path))
        options = datalake_config.get("options", {})
        (
            dataframe.write.format(datalake_config["file_extension"])
            .options(**options)
            .mode("overwrite")
            .save(file_path)
        )
