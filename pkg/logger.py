"""
Logging template credits:
https://towardsdatascience.com/the-reusable-python-logging-template-for-all-your-data-science-apps-551697c8540
https://github.com/yashprakash13/Python-Cool-Concepts/blob/main/logging_template/logger/logger.py


+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
| Level    | Numeric value | Description                                                                                                                 |
+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
| CRITICAL | 50            | A serious error, indicating that the program itself may be unable to continue running.                                      |
+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
| ERROR    | 40            | Due to a more serious problem, the software has not been able to perform some function.                                     |
+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
| WARNING  | 30            | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). |
|          |               | The software is still working as expected.                                                                                  |
+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
| INFO     | 20            | Confirmation that things are working as expected.                                                                           |
+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
| DEBUG    | 10            | Detailed information, typically of interest only when diagnosing problems.                                                  |
+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
| NOTSET   | 0             | This is the initial default setting of a log when it is created.                                                            |
|          |               | It is not really relevant and most developers will not even take notice of this category.                                   |
|          |               | In many circles, it has already become nonessential. The root log is usually created with level WARNING.                    |
+----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+


"""
import logging
import sys
from datetime import datetime
import os

LOG_DIR = os.path.join(os.path.normpath(os.getcwd()), 'logs')

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

APP_LOGGER_NAME = 'Alkemy_challenge'
# APP_LOG_FILE_NAME = os.path.join(LOG_DIR, f'{APP_LOGGER_NAME}_{datetime.now():%Y%m%d_%H%M%S-%f}.log')
APP_LOG_FILE_NAME = os.path.join(LOG_DIR, f'{APP_LOGGER_NAME}.log')

def setup_applevel_logger(logger_name=APP_LOGGER_NAME,
                          is_debug=True,
                          file_name=APP_LOG_FILE_NAME):
    
    # Set up the logger (to avoid using the root logger)
    logger = logging.getLogger(logger_name)
    
    # Set up the logging level (to know which messages to log)
    # Sets the threshold for this logger to level.
    # Logging messages which are less severe than level will be ignored.
    # logging messages which have severity level or higher will be emitted by whichever handler or handlers service this logger, unless a handler’s level has been set to a higher severity level than level.
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    # Set up a logging format
    formatter = logging.Formatter(
        # "%(asctime)s - %(name)s - %(levelname)s - %(message)s" # Default
        # fmt="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        fmt='%(asctime)s.%(msecs)03d %(name)-30s [%(filename)s:%(lineno)d] %(levelname)-8s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Set up a console handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    
    # Add the console handler to the logger for the messages to be shown on the console
    logger.addHandler(sh)

    # Set up a file handler if a file name is provided for the messages to be logged to a log file
    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        # Add the file handler to the logger
        logger.addHandler(fh)

    return logger


def get_child_logger(module_name, logger_name=APP_LOGGER_NAME):
    """
    Returns a logger which is a descendant to this logger, as determined by the suffix.
    Thus, logging.getLogger('abc').getChild('def.ghi') would return the same logger as would be returned by logging.getLogger('abc.def.ghi').
    This is a convenience method, useful when the parent logger is named using e.g. __name__ rather than a literal string.
    
    Args:
        module_name (str): module's __name__ from where we are calling the logger
        logger_name (str): Parent/ancestor logger name.

    Returns:
        logging.Logger: Child logger
    """    

    logger = logging.getLogger(logger_name).getChild(module_name)

    return logger




# def debug(func, log):
#     def wrapper():
#         log.debug("Calling module function.")
#         func()
#         log.debug("Finished.")
#     return wrapper



