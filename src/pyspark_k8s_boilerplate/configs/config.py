import logging
import os
from os.path import join
import pathlib
import yaml
#import appdirs

logger = logging.getLogger(__name__)


abs_config_path = os.getenv("PYSPARK_CONFIG_DIR")

if abs_config_path:
	parent = pathlib.Path(abs_config_path).parent.resolve()
else:
	parent = pathlib.Path(__file__).parent.resolve()

with open(join(parent, "conf.yaml"), 'r') as stream:
	try:
		print(yaml.safe_load(stream))
	except yaml.YAMLError as exc:
		print(exc)