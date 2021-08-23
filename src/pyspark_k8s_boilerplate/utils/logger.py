import logging

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
