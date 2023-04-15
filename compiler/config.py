from os import getenv
from pathlib import Path
from yaml import safe_load


class Config:
	REPO_LINK: str
	LOG_LEVEL: str


def load_config(path: Path) -> None:
	"""
	Load the configuration from a yaml config file
	:param path: the path to the config file
	"""

	with path.open() as config_file:
		config = safe_load(config_file)

	Config.REPO_LINK = config.repo
	Config.LOG_LEVEL = config.log_level
