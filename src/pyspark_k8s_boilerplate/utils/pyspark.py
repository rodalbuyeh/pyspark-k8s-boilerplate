
from pyspark_k8s_boilerplate.utils.log import logger
from pyspark_k8s_boilerplate.config.handlers import cfg
from pyspark.sql import SparkSession
from pyspark import SparkConf


def get_spark_session(app_name: str) -> SparkSession:
    """
    Create or get a spark session
    :param app_name:
    :return: A spark session
    """
    logger.info("Getting the Spark Session.")

    return SparkSession.builder.config("spark.eventLog.enabled", "true")\
        .config("spark.eventLog.dir", cfg.log_bucket)\
        .appName(app_name)\
        .getOrCreate()
