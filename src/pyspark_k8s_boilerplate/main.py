import argparse
import importlib
import os
import time

from pyspark_k8s_boilerplate.config.handlers import cfg
from pyspark_k8s_boilerplate.utils.log import logger


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=f"Run a {cfg.app_name} job")
    parser.add_argument('--job', type=str, required=True, dest='job_name',
                        help="The Name of the job module you want to run")
    parser.add_argument('--job-args', nargs='*', dest='job_args',
                        help="extra args to send to the job, for instance:"
                             " jobs=prep, jobs=train")

    args = parser.parse_args()
    logger.info("Called with arguments %s" % args)

    environment = {
        'JOB-ARGS': ' '.join(args.job_args) if args.job_args else ''
    }

    if args.job_args:
        job_args_tuples = [arg_str.split('=') for arg_str in args.job_args]
        logger.info('job_args_tuples: %s' % job_args_tuples)
        job_args = {a[0]: a[1] for a in job_args_tuples}
    else:
        job_args = {}

    logger.info('\nRunning job %s...\nenvironment is %s\n'
                % (args.job_name, environment))

    os.environ.update(environment)
    job_module = importlib.import_module(args.job_name)

    start = time.time()
    job_module.execute(**job_args)
    end = time.time()

    total = end - start

    logger.info("\nExecution of job %s took %s minutes."
                % (args.job_name, str(round((total / 60), 2))))
