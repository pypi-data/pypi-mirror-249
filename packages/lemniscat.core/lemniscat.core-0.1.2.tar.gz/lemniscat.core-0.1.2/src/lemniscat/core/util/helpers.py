import logging
import os
import sys
from logging import Logger, StreamHandler, DEBUG
from typing import Union, Optional

import yaml


class FileSystem:

    @staticmethod
    def __get_base_dir():
        """At most all application packages are just one level deep"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, '../..')

    @staticmethod
    def __get_config_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'settings')

    @staticmethod
    def get_plugins_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'plugins')

    @staticmethod
    def load_configuration(name: str = 'configuration.yaml', config_directory: Optional[str] = None) -> dict:
        if config_directory is None:
            config_directory = FileSystem.__get_config_directory()
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data
    
    @staticmethod
    def load_configuration_path(path: str = None) -> dict:
        with open(path) as file:
            input_data = yaml.safe_load(file)
        return input_data

class CustomFormatter(logging.Formatter):
    purple = "\x1b[35;20m"
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    grey = "\x1b[38;20m"
    orange = "\x1b[33;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _FORMATTER = "%(asctime)s [%(name)s][%(levelname)s] %(message)s"
    _FORMATTER_PLUGIN = "%(asctime)s    [%(name)s][%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: blue + _FORMATTER + reset,
        logging.INFO: grey + _FORMATTER + reset,
        logging.WARNING: orange + _FORMATTER + reset,
        logging.ERROR: red + _FORMATTER + reset,
        logging.CRITICAL: bold_red + _FORMATTER + reset,
        70: green + _FORMATTER + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        if("plugin." in record.name and (record.levelno == logging.INFO or record.levelno == logging.DEBUG)):
            log_fmt = self.purple + self._FORMATTER_PLUGIN + self.reset
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LogUtil(Logger):
    
    def __init__(
            self,
            name: str,
            level: Union[int, str] = DEBUG,
            *args,
            **kwargs
    ) -> None:
        super().__init__(name, level)
        logging.SUCCESS = 70
        logging.addLevelName(logging.SUCCESS, 'SUCCESS')
        self.addHandler(self.__get_stream_handler())

    def __get_stream_handler(self) -> StreamHandler:
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter())
        return handler    
    
    @staticmethod
    def create(log_level: str = 'DEBUG') -> Logger:
        # create logger with 'spam_application'
        logging.setLoggerClass(LogUtil)
        logger = logging.getLogger("lemniscat")
        logger.setLevel(log_level)
        return logger