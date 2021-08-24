import logging

from pyspark_k8s_boilerplate.config.handlers import cfg


logger = logging.getLogger(cfg.app_name)

# create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(f'/tmp/{cfg.app_name}.log')

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