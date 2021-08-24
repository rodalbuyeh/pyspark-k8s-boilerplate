from pyspark_k8s_boilerplate.utils.pyspark import get_spark_session
from pyspark_k8s_boilerplate.utils.log import logger
from pyspark.sql import DataFrame
from pyspark_k8s_boilerplate.config.handlers import data_cfg


def run_cloud_etl(bucket_root: str = data_cfg.object_bucket) -> None:

	spark = get_spark_session("cloud_etl")

	logger.info("Read titanic.csv to spark dataframe")
	df: DataFrame = spark.read.csv(f"{bucket_root}titanic.csv", header=True)

	logger.info("Summarize and write to object storage as parquet")
	df.describe().write.parquet(f"{bucket_root}titanic_summary.parquet")

	spark.stop()


if __name__ == "__main__":
	run_cloud_etl()
