#!/user/bin/python3
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: logger.py
# @Author: Qing-Yuan Jiang
# @Mail: qyjiang24 AT gmail.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++

import logging
import os

from logging import handlers

from utils.args import args


class Logger(object):
    def __init__(self, filename,
                 when='D',
                 back_count=0,
                 fmt='[%(asctime)s][%(levelname)s]: %(message)s'):
        self.logger = logging.getLogger()
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        self.logger.addHandler(sh)
        if args.en_local_log:
            th = handlers.TimedRotatingFileHandler(filename=filename,
                                                   when=when,
                                                   backupCount=back_count,
                                                   encoding='utf-8')
            th.setFormatter(format_str)
            self.logger.addHandler(th)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def exception(self, message):
        self.logger.exception(message)


logfile = os.path.join(args.logdir, '-'.join([args.approach, args.timestamp, 'log.log']))

logger = Logger(logfile)
logger.info(logfile)

