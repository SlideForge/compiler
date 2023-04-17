"""
Copyright (c) 2023 SlideForge.

This file is part of SlideForge compiler.

SlideForge compiler is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SlideForge compiler.  If not, see <http://www.gnu.org/licenses/>.
"""

from logging import FileHandler, Formatter, Logger, StreamHandler, getLogger

from compiler.config import Config


FORMAT = "%(levelname)s %(asctime)s | %(name)s | %(message)s"


def get_logger(name: str) -> Logger:
    """
    Function to create a basic logger
    :param name: the loggers name
    :return: the logger
    """
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
