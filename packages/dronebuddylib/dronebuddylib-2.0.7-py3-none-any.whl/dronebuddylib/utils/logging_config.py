import datetime
import logging
import sys

from dronebuddylib.models.enums import LoggerColors


class Logger:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    def log_error(self, error_message):
        sys.stdout.write(LoggerColors.RED.value)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write('\n' + current_time + " : ERROR : " + error_message + '\n\n')

    def log_info(self, info_message):
        sys.stdout.write(LoggerColors.YELLOW.value)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write('\n' + current_time + " : INFO :" + info_message + '\n\n')

    def log_debug(self, debug_message):
        sys.stdout.write(LoggerColors.BLUE.value)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write('\n' + current_time + " : DEBUG :" + debug_message + '\n\n')

    def log_warning(self, warning_message):
        sys.stdout.write(LoggerColors.CYAN.value)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write('\n' + current_time + " : WARNING :" + warning_message + '\n\n')

    def log_success(self, success_message):
        sys.stdout.write(LoggerColors.GREEN.value)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write('\n' + current_time + " : SUCCESS :" + success_message + '\n\n')
