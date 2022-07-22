import logging


class Admin_Logger(logging.Logger):
    def __init__(self):
        super().__init__(__name__)
        self.setLevel(logging.INFO)

        # create a file handler
        handler = logging.FileHandler('logs/admin_log.log')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('[%(asctime)s %(created)f] [%(levelname)s] %(message)s [%(filename)s %(module)s %(funcName)s %(lineno)d]')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        self.addHandler(handler)

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


class User_Logger(logging.Logger):
    def __init__(self):
        super().__init__(__name__)
        self.setLevel(logging.INFO)

        # create a file handler
        handler = logging.FileHandler('logs/user_log.log')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('[%(asctime)s %(created)f] [%(levelname)s] %(message)s [%(filename)s %(module)s %(funcName)s %(lineno)d]')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        self.addHandler(handler)

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
        

# if __name__ == "__main__":
#     admin_logging_class = Admin_Logger()
#     admin_logging_class.log_info("test")
#     admin_logging_class.log_error("test")
#     admin_logging_class.log_debug("test")
#     admin_logging_class.log_warning("test")
#     admin_logging_class.log_critical("test")

#     user_logging_class = User_Logger()
#     user_logging_class.log_info("test")
#     user_logging_class.log_error("test")
#     user_logging_class.log_debug("test")
#     user_logging_class.log_warning("test")
#     user_logging_class.log_critical("test")
