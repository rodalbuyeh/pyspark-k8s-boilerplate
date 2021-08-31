from pyspark_k8s_boilerplate.utils.pyspark import get_spark_session
from pyspark_k8s_boilerplate.utils.log import logger
from pyspark.sql import DataFrame
from pyspark_k8s_boilerplate.config.handlers import data_cfg


def execute(bucket_root: str = data_cfg.titanic_root) -> None:

	spark = get_spark_session("cloud_etl")

	logger.info("Read titanic.csv to spark dataframe")
	df: DataFrame = spark.read.csv(f"{bucket_root}titanic.csv", header=True)

	logger.info("Summarize and write to object storage as parquet")
	df.describe().write.mode("overwrite").parquet(f"{bucket_root}titanic_summary.parquet")

	logger.info("Cloud ETL job done.")
	spark.stop()


if __name__ == "__main__":
	execute()
