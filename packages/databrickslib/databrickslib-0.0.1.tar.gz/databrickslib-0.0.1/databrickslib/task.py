from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Dict, Any
import yaml
import pathlib
from pyspark.sql import SparkSession, DataFrame
import sys

def get_dbutils(
    spark: SparkSession,
):  # please note that this function is used in mocking by its name
    try:
        from pyspark.dbutils import DBUtils  # noqa

        if "dbutils" not in locals():
            utils = DBUtils(spark)
            return utils
        else:
            return locals().get("dbutils")
    except ImportError:
        return None
        
class Task(ABC):
    """
    This is an abstract class that provides handy interfaces to implement workloads (e.g. jobs or job tasks).
    Create a child from this class and implement the abstract launch method.
    Class provides access to the following useful objects:
    * self.spark is a SparkSession
    * self.dbutils provides access to the DBUtils
    * self.logger provides access to the Spark-compatible logger
    * self.conf provides access to the parsed configuration of the job
    """

    def __init__(self, spark=None, init_conf=None):
        self.spark = self._prepare_spark(spark)
        self.logger = self._prepare_logger()
        self.dbutils = self.get_dbutils()
        if init_conf:
            self.conf = init_conf
        else:
            self.conf = self._provide_config()
        
        
        input = dict(**self.conf['input']) if 'input' in self.conf else {}
        output = dict(**self.conf['output']) if 'output' in self.conf else {}        
        self.all_conf = {**input,  **output} 
        self._log_conf()
        self.post_init()
        print(self.all_conf)

    @staticmethod
    def _prepare_spark(spark) -> SparkSession:
        if not spark:
            return SparkSession.builder.getOrCreate()
        else:
            return spark

    def get_dbutils(self):
        utils = get_dbutils(self.spark)

        if not utils:
            self.logger.warn("No DBUtils defined in the runtime")
        else:
            self.logger.info("DBUtils class initialized")

        return utils

    def _provide_config(self):
        self.logger.info("Reading configuration from --conf-file job option")
        conf_file = self._get_conf_file()
        if not conf_file:
            self.logger.info(
                "No conf file was provided, setting configuration to empty dict."
                "Please override configuration in subclass init method"
            )
            return {}
        else:
            self.logger.info(f"Conf file was provided, reading configuration from {conf_file}")
            return self._read_config(conf_file)

    @staticmethod
    def _get_conf_file():
        p = ArgumentParser()
        p.add_argument("--conf-file", required=False, type=str)
        namespace = p.parse_known_args(sys.argv[1:])[0]
        return namespace.conf_file

    @staticmethod
    def _read_config(conf_file) -> Dict[str, Any]:
        config = yaml.safe_load(pathlib.Path(conf_file).read_text())
        return config

    def _prepare_logger(self):
        log4j_logger = self.spark._jvm.org.apache.log4j  # noqa
        return log4j_logger.LogManager.getLogger(self.__class__.__name__)

    def _log_conf(self):
        # log parameters
        self.logger.info("Launching job with configuration parameters:")
        for key, item in self.conf.items():
            self.logger.info("\t Parameter: %-30s with value => %-30s" % (key, item))
            
            
    @staticmethod
    def write_stream(
        dataframe: DataFrame,
        table_name: str,
        checkpoint_location: str,
        format: str = "delta",
        output_mode: str = "append",
        merge_schema: str = "true",
        trigger_time: str = "15 seconds",
    ) -> None:
        """
        Write stream dataframe to a table.

        :param dataframe: DataFrame
        :param table_name: table name e.g. raw.merchant
        :param checkpoint_location: checkpoint location e.g. /mnt/raw/checkpoint/issuer
        :param format: write format e.g. delta, parquet, orc
        :param output_mode: output mode e.g. append, update, complete
        :param merge_schema: schema evolution e.g. true, false to raise error when schema changes
        :param trigger_time: trigger processing time
        :return: None
        """
        dataframe.writeStream.format(format).outputMode(output_mode).option(
            "mergeSchema", merge_schema
        ).option("checkpointLocation", checkpoint_location).trigger(
            processingTime=trigger_time
        ).toTable(
            table_name
        )            

    @abstractmethod
    def launch(self):
        """
        Main method of the job.
        :return:
        """
        pass


    @abstractmethod
    def post_init(self):
        """
        Post Init
        :return:
        """
        pass