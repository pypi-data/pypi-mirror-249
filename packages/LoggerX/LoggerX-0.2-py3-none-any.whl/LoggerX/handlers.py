#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/3
# @Author  : alan
# @File    : handlers.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler


class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


class CustomLogger:
    def __init__(self, logger_name: str, log_dir: str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(process)d - %(thread)d - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s")

        for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
            # handler = logging.FileHandler(f'{logging.getLevelName(level).lower()}.log')
            handler = TimedRotatingFileHandler(
                os.path.join(log_dir, '{}.log'.format(logging.getLevelName(level).lower())),
                when='d',
                interval=1, backupCount=7,
                encoding="utf8", delay=False)
            handler.setLevel(level)
            handler.setFormatter(formatter)
            filter_ = LevelFilter(level)
            handler.addFilter(filter_)
            self.logger.addHandler(handler)

    def get_logger(self, level):
        return self.logger


class iLog(object):
    def __init__(self, app: str = "app", log_dir: str = "./"):
        self.app = app
        self.logger_instance = CustomLogger(self.app, log_dir)

    # def set_app(self, app_name):
    #     self.app = app_name
    #     self.logger_instance = CustomLogger(self.app)

    def info(self, message):
        self.logger_instance.get_logger(logging.INFO).info(message)

    def warning(self, message):
        self.logger_instance.get_logger(logging.WARNING).warning(message)

    def error(self, message):
        self.logger_instance.get_logger(logging.ERROR).error(message)

    def critical(self, message):
        self.logger_instance.get_logger(logging.CRITICAL).critical(message)
