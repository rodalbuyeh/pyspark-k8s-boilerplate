from pyspark.sql import DataFrame  # type: ignore
from pyspark_k8s_boilerplate.config.handlers import data_cfg
from pyspark_k8s_boilerplate.utils.log import logger
from pyspark_k8s_boilerplate.utils.pyspark import get_spark_session


def execute(bucket_root: str = data_cfg.titanic_root) -> None:
    """
    This job is critical to indicate whether you have sufficient permissions to
     read/write from/to object storage.
    :param bucket_root: path to titanic.csv - you should stage this in advance
    :return: No python return value, writes to object storage
    """

    spark = get_spark_session("cloud_etl")

    logger.info("Read titanic.csv to spark dataframe")
    df: DataFrame = spark.read.csv(f"{bucket_root}titanic.csv", header=True)

    logger.info("Summarize and write to object storage as parquet")
    df.describe().write.mode("overwrite").parquet(
        f"{bucket_root}titanic_summary.parquet")

    logger.info("Cloud ETL job done.")
    spark.stop()


if __name__ == "__main__":
    execute()
