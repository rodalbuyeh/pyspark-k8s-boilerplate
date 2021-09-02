import time

from pyspark_k8s_boilerplate.utils.pyspark import get_spark_session
from pyspark_k8s_boilerplate.utils.log import logger
from pyspark_k8s_boilerplate.config.handlers import data_cfg


def execute(seconds: int = data_cfg.titanic_root) -> None:
	"""Spark on k8s doesn't have great support for interactive sessions. Run this job to keep the cluster up
	and SSH in to the driver node to run spark-shell/pyspark/etc"""
	spark = get_spark_session("interactive")

	logger.info(f"Begin dummy job to persist cluster. State will last for {seconds} seconds")

	time.sleep(seconds)

	logger.info("Interactive session out of time.")

	spark.stop()


if __name__ == "__main__":
	execute()
