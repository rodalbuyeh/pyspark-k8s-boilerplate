from random import random
from operator import add

from pyspark_k8s_boilerplate.utils.pyspark import get_spark_session
from pyspark_k8s_boilerplate.utils.log import logger


def spark_pi(partitions: int = 2) -> None:

    spark = get_spark_session("PythonPi")

    n = 100000 * partitions

    def f(_: int) -> int:
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1),
                                           partitions).map(f).reduce(add)

    logger.info("Pi is roughly %f" % (4.0 * count / n))

    spark.stop()


if __name__ == "__main__":
    spark_pi()
