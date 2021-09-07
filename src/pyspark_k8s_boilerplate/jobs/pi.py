from operator import add
from random import random
from typing import Optional

from pyspark_k8s_boilerplate.config.handlers import data_cfg
from pyspark_k8s_boilerplate.utils.log import logger
from pyspark_k8s_boilerplate.utils.pyspark import get_spark_session


def execute(partitions: int = int(data_cfg.pi_partitions),  # type: ignore
            message: str = "delicious",
            output: bool = True) -> Optional[float]:
    """
    Execute job for generating pi with Pyspark.
    :param partitions: Desired number of partitions
    :param message: Message for 'Pi is... ___'
    :param output: Optional parameter for whether you want this function to
    return a value or just write to storage.
    :return: Either no return value (write to object storage) or return a float
     close to pi.
    """

    spark = get_spark_session("PythonPi")

    # note: the argument parser in main.py converts all dynamic job arguments
    # to strings, we'll handle here
    if isinstance(partitions, str) and partitions.isnumeric():
        partitions = int(partitions)
    elif isinstance(partitions, str) and not partitions.isnumeric():
        logger.exception(
            "Please supply a valid integer-like format in the CLI")

    n = 100000 * partitions

    def f(_: int) -> int:
        x: float = random() * 2 - 1
        y: float = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1),
                                           partitions).map(f).reduce(add)

    result = (4.0 * count / n)

    logger.info("Pi is roughly %f" % result)

    logger.info(f"And pi is {message}")

    spark.stop()

    if output:
        return result


if __name__ == "__main__":
    execute()
