#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os
from logging import handlers



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Loger(object):
    def __init__(self):
        log_path = os.path.join(BASE_DIR, 'logs')
        self.log_info = os.path.join(log_path,'info.log')
        self.log_error = os.path.join(log_path,'error.log')

    def logger_info(self,LOG_INFO,LOG_LEVEL,log_type):
        logger = logging.getLogger(log_type)
        logger.setLevel(LOG_LEVEL)
        ch = logging.StreamHandler()
        fh = handlers.RotatingFileHandler(self.log_info, maxBytes=4, backupCount=2)
        fh.setLevel(LOG_LEVEL)
        ch.setLevel(LOG_LEVEL)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
        logger.info(LOG_INFO)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        return logger


    def logger_warning(self,LOG_INFO,LOG_LEVEL,log_type):
        logger = logging.getLogger(log_type)
        logger.setLevel(LOG_LEVEL)
        ch = logging.StreamHandler()
        fh = handlers.RotatingFileHandler(self.log_info, maxBytes=4, backupCount=2)
        fh.setLevel(LOG_LEVEL)
        ch.setLevel(LOG_LEVEL)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
        logger.warning(LOG_INFO)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        return logger

    def logger_error(self,LOG_INFO,LOG_LEVEL,log_type):
        logger = logging.getLogger(log_type)
        logger.setLevel(LOG_LEVEL)
        ch = logging.StreamHandler()
        fh = handlers.RotatingFileHandler(self.log_error, maxBytes=4, backupCount=2)
        fh.setLevel(LOG_LEVEL)
        ch.setLevel(LOG_LEVEL)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
        logger.error(LOG_INFO)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        return logger


logger = Loger()