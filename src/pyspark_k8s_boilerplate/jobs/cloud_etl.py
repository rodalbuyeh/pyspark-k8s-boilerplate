from pyspark_k8s_boilerplate.utils.pyspark import get_spark_session
from pyspark_k8s_boilerplate.utils.log import logger


def run_cloud_etl(bucket_root: str):

	spark = get_spark_session()

	logger.info("Read titanic.csv to spark dataframe")
	df = spark.read.csv(f"{bucket_root}titanic.csv", header=True)

	logger.info("Summarize and write to object storage as parquet")
	df.describe().write.parquet(f"{bucket_root}titanic_summary.parquet")

	spark.stop()

