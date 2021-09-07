from pyspark.sql import SparkSession  # type: ignore
from pyspark_k8s_boilerplate.config import cfg
from pyspark_k8s_boilerplate.utils.log import logger


def get_spark_session(app_name: str) -> SparkSession:
    """
    Create or get a spark session
    :param app_name: The name of the spark job you want to run within a spark
    session.
    :return: A spark session
    """
    logger.info("Getting the Spark Session.")

    return SparkSession.builder.config("spark.eventLog.enabled", "true") \
        .config("spark.eventLog.dir", cfg.log_bucket) \
        .appName(app_name) \
        .getOrCreate()
