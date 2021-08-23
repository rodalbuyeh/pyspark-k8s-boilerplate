import argparse
import importlib
import logging
import os
import time

if __name__ == "__main__":

    logger = logging.getLogger('freelunch')
    logger.setLevel(logging.DEBUG)
    # create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('/tmp/freelunch.log')
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)
    # create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s -' +
                                  ' %(levelname)s - %(message)s')
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.info(("Pipeline configs set"))
    logger.info("Model Name: " + str("model_name"))

    parser = argparse.ArgumentParser(description="Run a freelunch job")
    parser.add_argument('--job', type=str, required=True, dest='job_name',
                        help="The Name of the job module you want to run")
    parser.add_argument('--class', type=str, required=True, dest='class_name',
                        help="The name of the class you want to run")
    parser.add_argument('--job-args', nargs='*', dest='job_args',
                        help="extra args to send to the job, " +
                             "for instance: jobs=prep, jobs=train")

    args = parser.parse_args()
    logger.info("Called with arguments %s" % args)

    environment = {
        'FREE-LUNCH-JOB-ARGS': ' '.join(args.job_args) if args.job_args else ''
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
    getattr(job_module, args.class_name)().main(**job_args)
    end = time.time()

    total = end - start

    logger.info("\nExecution of job %s took %s minutes."
                % (args.job_name, str(round((total / 60), 2))))
