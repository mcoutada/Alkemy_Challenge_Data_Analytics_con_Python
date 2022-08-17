"""
Logging template credits:
https://towardsdatascience.com/the-reusable-python-logging-template-for-all-your-data-science-apps-551697c8540
https://github.com/yashprakash13/Python-Cool-Concepts/blob/main/logging_template/logger/logger.py

"""
import logging
import os
import sys
import time

LOG_DIR = os.path.join(os.getcwd(), "logs")
global debug_flg
debug_flg = False

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# Set a logger's name, in case it's not provided, to the base project's
# folder name is used by default
# (Alkemy_Challenge_Data_Analytics_con_Python)
APP_LOGGER_NAME = os.path.basename(os.getcwd())

# Use this line to generate one log file per file run
# from datetime import datetime
# APP_LOG_FILE_NAME = os.path.join(LOG_DIR,
# f'{APP_LOGGER_NAME}_{datetime.now():%Y%m%d_%H%M%S_%f}.log') # TODO:
# erase or uncomment (leave one)
APP_LOG_FILE_NAME = os.path.join(LOG_DIR, f"{APP_LOGGER_NAME}.log")


def set_logger(
        logger_name=APP_LOGGER_NAME,
        is_debug=debug_flg,
        file_name=APP_LOG_FILE_NAME):
    """
    Sets up the logger at app level

    Args:
        logger_name (str, optional): main logger's name. Defaults to APP_LOGGER_NAME.
        is_debug (bool, optional): Sets log's level to DEBUG. Defaults to True.
        file_name (str, optional): If set, the log's output will be stored into a file in the /logs folder. Defaults to APP_LOG_FILE_NAME.

    Returns:
        logging.Logger: Main logger
    """

    # Set up the logger (to avoid using the default/root logger)
    logger = logging.getLogger(logger_name)

    # Set up the logging level (to know which messages to log)
    # Logging messages whith less severe level will be ignored, higher ones will be emitted.
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | Level    | Numeric value | Description                                                                                                                 |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | CRITICAL | 50            | A serious error, indicating that the program itself may be unable to continue running.                                      |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | ERROR    | 40            | Due to a more serious problem, the software has not been able to perform some function.                                     |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | WARNING  | 30            | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). |
    # |          |               | The software is still working as expected.                                                                                  |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | INFO     | 20            | Confirmation that things are working as expected.                                                                           |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | DEBUG    | 10            | Detailed information, typically of interest only when diagnosing problems.                                                  |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | NOTSET   | 0             | This is the initial default setting of a log when it is created.                                                            |
    # |          |               | It is not really relevant and most developers will not even take notice of this category.                                   |
    # |          |               | In many circles, it has already become nonessential. The root log is usually created with level WARNING.                    |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+

    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    # Set up a logging format
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d [%(name)-20s:%(lineno)-4d] %(levelname)8s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set up a console handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()

    # Add the console handler to the logger for the messages to be shown on
    # the console
    logger.addHandler(sh)

    # sys.excepthook(*exc_info) prints out a given traceback and exception to
    # sys.stderr
    new_excepthook = lambda *exc_info: log_unhandled_exception(
        logger, *exc_info)
    sys.excepthook = new_excepthook

    # Set up a file handler if a file name is provided for the messages to be
    # logged to a log file
    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        # Add the file handler to the logger
        logger.addHandler(fh)

    return logger


def log_unhandled_exception(in_logger, *in_exc_info):
    exc_type, exc_value, exc_traceback = in_exc_info
    """
    Logging uncaught exceptions in Python
    https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python/16993115#16993115

    When an exception is raised and uncaught, the interpreter calls sys.excepthook with three arguments:
    the exception class, exception instance, and a traceback object.
    In an interactive session this happens just before control is returned to the prompt;
    in a Python program this happens just before the program exits.
    The handling of such top-level exceptions can be customized by assigning another three-argument function to sys.excepthook.
    sys.excepthook = log_unhandled_exception

    Args:
        *exc_info is unpacked to:
        exc_type (type): Gets the type of the exception being handled (a subclass of BaseException). Example: <class 'ZeroDivisionError'>
        exc_value (error): Gets the exception instance (an instance of the exception type). Example: division by zero
        exc_traceback (traceback): Gets a traceback object which encapsulates the call stack at the point where the exception originally occurred. Example: <traceback object at 0x7f8b8b8b8b8>
    """

    # Ignore KeyboardInterrupt so a console python program can exit with Ctrl
    # + C.
    if issubclass(exc_type, KeyboardInterrupt):
        # calls default excepthook
        # sys.__excepthook__ contains the original values of excepthook
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Rely entirely on python's logging module for formatting the exception.
    in_logger.critical(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


class Debug2Log:
    """
    Class used to log debug messages.
    """

    def __init__(self):
        # As the messages are triggered in this script, the logger's name is
        # set to this file's name.
        self.logger = set_logger(
            logger_name=get_rel_path(__file__),
            is_debug=debug_flg)
        self.timer = {}

    def tracefunc(self, frame, event, arg):
        """tracefunc is a trace function for the sys.setprofile function.
        sys.setprofile(profilefunc):
        Profile functions should have three arguments: frame, event, and arg.
        'call': A function is called (or some other code block entered). The profile function is called; arg is None.
        'return': A function (or other code block) is about to return. The profile function is called; arg is the value that will be returned, or None if the event is caused by an exception being raised.
        'c_call': A C function is about to be called. This may be an extension function or a built-in. arg is the C function object.
        'c_return':A C function has returned. arg is the C function object.
        'c_exception':A C function has raised an exception. arg is the C function object.
        Args:
            frame (frame): is the current stack frame. A stack frame represents a single function call. You can visualize functions that call one another as virtual frames stacking on top of one another. The stack data structure is actually used for this
            event (str): is a string: 'call', 'return', 'c_call', 'c_return', or 'c_exception'.
            arg (?): depends on the event type.

        Returns:
            function: set tracefunc
        """

        # Log only the functions from this project, imported modules are
        # ignored.
        if frame.f_code.co_filename.startswith(os.getcwd()):
            # Get the relative path of the file. E.g. \pkg\extract.py
            rel_path_fname = os.sep + os.path.relpath(
                frame.f_code.co_filename, start=os.getcwd()
            )
            if event == "call":
                self.timer[rel_path_fname] = time.time()
                self.logger.debug(
                    f"Call {rel_path_fname} {frame.f_code.co_name} locals: {'' if frame.f_locals is None else frame.f_locals}"
                )
            elif event == "return" and rel_path_fname in self.timer:
                duration = time.time() - self.timer[rel_path_fname]
                self.logger.debug(
                    f"End {rel_path_fname} {frame.f_code.co_name} returning: {arg} elapsed: {duration:.4f}"
                )
            return self.tracefunc

    def set_trace(self):
        return sys.setprofile(self.tracefunc)


def get_rel_path(in_file_name):
    """
    Returns the relative path of the file. E.g. \\pkg\\extract.py
    Args:
        in_file_name (str): __file__ (Absolute path + file name)
    Returns:
        str: relative path of the file
    """

    return os.sep + os.path.relpath(in_file_name, start=os.getcwd())
