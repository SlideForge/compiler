from logging import getLogger, StreamHandler, Formatter, Logger, FileHandler
from compiler.config import Config

FORMAT = "%(levelname)s %(asctime)s | %(name)s | %(message)s"


def get_logger(name: str) -> Logger:
	logger = getLogger(name)
	logger.setLevel(Config.LOG_LEVEL)

	if hasattr(Config, "LOG_FILE"):
		fh = FileHandler(filename=Config.LOG_FILE, encoding="utf-8")
		logger.addHandler(fh)

	formatter = Formatter(FORMAT)

	ch = StreamHandler()
	ch.setLevel(Config.LOG_LEVEL)
	ch.setFormatter(formatter)

	logger.addHandler(ch)

	return logger
