import logging
import os
import json
from pythonjsonlogger import jsonlogger

path = os.path.dirname(os.path.abspath(__file__))

# create a folder for logs
if not os.path.exists(path + '/logs'):
    os.makedirs(path + '/logs')

logs_path = path + '/logs'


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.INFO)

    def log_info(self, message):
        self.info(message)

    def log_error(self, message):
        self.error(message)

    def log_debug(self, message):
        self.debug(message)

    def log_warning(self, message):
        self.warning(message)

    def log_critical(self, message):
        self.critical(message)

    def log_exception(self, message):
        self.exception(message)


class Admin_Logger(Logger):
    def __init__(self):
        super().__init__(__name__)
        adminhandler = logging.FileHandler(logs_path + '/admin_log.log')
        adminhandler.setLevel(logging.INFO)

        adminformatter = jsonlogger.JsonFormatter('[%(asctime)s %(created)f] [%(levelname)s] %(message)s [%(filename)s %(module)s %(funcName)s %(lineno)d]')
        adminhandler.setFormatter(adminformatter)

        self.addHandler(adminhandler)

    def read_adminlog(self):
        array = []
        with open(logs_path + '/admin_log.log', 'r') as f:
            for line in f:
                array.append(line)

        dictionary = {}
        for i in range(len(array)):
            dictionary[i] = array[i]

        return dictionary


class User_Logger(Logger):
    def __init__(self):
        super().__init__(__name__)
        userhandler = logging.FileHandler(logs_path + '/user_log.log')
        userhandler.setLevel(logging.INFO)

        userformatter = jsonlogger.JsonFormatter('[%(asctime)s %(created)f] [%(levelname)s] %(message)s [%(filename)s %(module)s %(funcName)s %(lineno)d]')
        userhandler.setFormatter(userformatter)
        self.addHandler(userhandler)

    def read_userlog(self):
        array = []
        with open(logs_path + '/user_log.log', 'r') as f:
            for line in f:
                array.append(line)

        dictionary = {}
        for i in range(len(array)):
            dictionary[i] = array[i]

        return dictionary


# if __name__ == "__main__":
#     a = Admin_Logger()
#     a.log_info("today very tired")

#     b = User_Logger()
#     b.log_info("sdfsdfgs")  

import logging
import google.cloud.logging

service_key_path = "/Users/YP/Documents/NYP_Applications_Security_Project/Assignments/Tommy-Destiny/google.json"
client = google.cloud.logging.Client.from_service_account_json(service_key_path)

client.setup_logging()
logging.warning("This is a warning!")