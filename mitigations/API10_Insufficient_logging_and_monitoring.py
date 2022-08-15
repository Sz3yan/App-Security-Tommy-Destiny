import os
import logging
import google.cloud.logging
import pathlib

from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging_v2.handlers import setup_logging


class GoogleCloudLogging:
    def __init__(self):
        path = pathlib.Path(__file__).parent.parent.absolute()
        path = os.path.join(path, 'google.json')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
        self.__client = google.cloud.logging.Client()

        # explicitly set up a CloudLoggingHandler to send logs over the network
        self.__handler = CloudLoggingHandler(self.__client)
        setup_logging(self.__handler)

    def write_entry_debug(self, message):
        return logging.debug(message)

    def write_entry_info(self, message):
        return logging.info(message)

    def write_entry_warning(self, message):
        return logging.warning(message)

    def write_entry_error(self, message):
        return logging.error(message)

    def write_entry_critical(self, message):
        return logging.critical(message)

    def write_entry_exception(self, message):
        return logging.exception(message)
