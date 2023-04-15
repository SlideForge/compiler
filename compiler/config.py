from typing import Any
from pathlib import Path
from yaml import safe_load
import logging


class Config:
	REPO_LINK: str
	LOG_LEVEL: int
	LOG_FILE: str


def load_log_level(log_level: str | int) -> int:
	if isinstance(log_level, int):
		return log_level

	num_log_level = getattr(logging, log_level.upper())

	if not isinstance(num_log_level, int):
		raise ValueError(f"Invalid log level: {log_level}")

	return num_log_level


def load_config(path: Path) -> None:
	"""
	Load the configuration from a yaml config file
	:param path: the path to the config file
	"""

	with path.open() as config_file:
		config = safe_load(config_file)

	Config.REPO_LINK = config["repo"]
	Config.LOG_LEVEL = load_log_level(config["log"]["level"])
	Config.LOG_FILE = config["log"]["file"]
