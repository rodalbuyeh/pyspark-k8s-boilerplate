import argparse
from argparse import Namespace
import importlib
import os
import time
from typing import Dict, Tuple

from pyspark_k8s_boilerplate.config import cfg
from pyspark_k8s_boilerplate.utils.log import logger


def get_args() -> Namespace:
    """Get arguments passed to pyspark entrypoint."""

    parser = argparse.ArgumentParser(description=f"Run a {cfg.app_name} job")
    parser.add_argument('--job', type=str, required=True, dest='job_name',
                        help="The Name of the job module you want to run")
    parser.add_argument('--job-args', nargs='*', dest='job_args',
                        help="extra args to send to the job, for instance:"
                             " jobs=prep, jobs=train")

    arguments = parser.parse_args()

    logger.info("Called with arguments %s" % arguments)

    return arguments


def get_job_args(arguments: Namespace) -> Tuple[Dict[str, str],
                                                Dict[str, str]]:
    """Get any additional job arguments associated with a given spark job."""

    environment = {
        'JOB-ARGS': ' '.join(arguments.job_args) if arguments.job_args else ''
    }

    if arguments.job_args:
        job_args_tuples = [arg_str.split('=') for arg_str in
                           arguments.job_args]
        logger.info('job_args_tuples: %s' % job_args_tuples)
        job_args = {a[0]: a[1] for a in job_args_tuples}
    else:
        job_args = {}

    logger.info('\nRunning job %s...\nenvironment is %s\n'
                % (arguments.job_name, environment))

    return job_args, environment


def run_job(args: Namespace, job_args: Dict[str, str]) -> None:
    """
    Run the desired pyspark job with any indicated module and job arguments.
    """

    job_module = importlib.import_module(args.job_name)

    start = time.time()
    job_module.execute(**job_args)  # type: ignore
    end = time.time()

    total = end - start

    logger.info("\nExecution of job %s took %s minutes."
                % (args.job_name, str(round((total / 60), 2))))


if __name__ == "__main__":
    args = get_args()

    job_args, env = get_job_args(args)

    os.environ.update(env)

    run_job(args, job_args)

# TODO document, add infra code
# TODO maybe jupyter on master
# TODO spark history server
