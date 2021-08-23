import logging
import os
from os.path import join
import pathlib
import yaml
from typing import List, Any, Dict


logger = logging.getLogger(__name__)


def read_config() -> Dict[str, Any]:

	abs_config_path = os.getenv("PYSPARK_CONFIG_PATH")

	if abs_config_path:
		path: str = abs_config_path
	else:
		path: str  = join(pathlib.Path(__file__).parent.resolve(), "conf.yaml")

	with open(path, 'r') as stream:
		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			logger.exception(exc)


class Config(object):

	def __init__(self):
		self._config: Dict[str, Any] = read_config()


class GeneralConfig(Config):
	@property
	def app_name(self) -> str:
		return self._config["general"]["app_name"]

	@property
	def test_configs(self) -> List[str]:
		return self._config["general"]["sample_configs"]


class DataConfig(Config):
	@property
	def object_bucket(self) -> str:
		return self._config["data"]["object_bucket"]

	@property
	def database(self) -> str:
		return self._config["data"]["database"]


class ModelConfig(Config):
	@property
	def cv_strategy(self) -> str:
		return self._config["model"]["cv_strategy"]

	@property
	def imputation(self) -> List[str]:
		return self._config["model"]["imputation"]

	@property
	def selection(self) -> str:
		return self._config["model"]["selection"]

	@property
	def exclude_features(self) -> List[str]:
		return self._config["model"]["exclude_features"]

