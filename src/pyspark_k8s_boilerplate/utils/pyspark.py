
from pyspark_k8s_boilerplate.utils.log import logger
from pyspark.sql import SparkSession


def get_spark_session(app_name: str) -> SparkSession:
    """
    Create or get a spark session
    :param app_name:
    :return: A spark session
    """
    logger.info("Getting the Spark Session.")
    return SparkSession.builder.appName(app_name).getOrCreate()
