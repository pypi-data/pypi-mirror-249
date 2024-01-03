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
        self.spark_s3_connection = connect(self.NAME)

    def __build_file_path__(
        self, datalake_config: Dict[str, str], partition_config: Dict[str, str]
    ):
        """
        Method for building the file path.
        """
        return "s3a://{0}/{1}".format(
            datalake_config["datalake_key"],
            self.build_partition_path(partition_config),
        )

    def read(
        self, datalake_config: Dict[str, str], partition_config: Dict[str, str]
    ):
        """
        Method for reading data from the datalake.
        """
        logger.info("Reading data from datalake.")
        file_path = self.__build_file_path__(datalake_config, partition_config)
        options = datalake_config.get("options", {})
        schema = datalake_config.get("spark_schema", None)
        if schema:
            return (
                self.spark_s3_connection.spark_session.read.format(
                    datalake_config["file_extension"]
                )
                .options(**options)
                .schema(schema)
                .load(file_path)
            )
        else:
            return (
                self.spark_s3_connection.spark_session.read.format(
                    datalake_config["file_extension"]
                )
                .options(**options)
                .load(file_path)
            )

    def write(
        self,
        dataframe,
        datalake_config: Dict[str, str],
        partition_config: Dict[str, str],
    ):
        """
        Method for writing data to the datalake.
        """
        logger.info("Writing data to datalake.")
        file_path = self.__build_file_path__(datalake_config, partition_config)
        (
            dataframe.write.format(datalake_config["file_extension"])
            .options(**datalake_config["options"])
            .mode("overwrite")
            .save(file_path)
        )
