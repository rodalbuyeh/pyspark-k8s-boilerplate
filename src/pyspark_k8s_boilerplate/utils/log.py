import logging

from pyspark_k8s_boilerplate.config import cfg

logger = logging.getLogger(cfg.app_name)

logger.setLevel(logging.INFO)


def apply_logger_handlers() -> None:
    """Apply generic configuration of logger."""
    # create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(f'/tmp/{cfg.app_name}.log')

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')

    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)


apply_logger_handlers()
