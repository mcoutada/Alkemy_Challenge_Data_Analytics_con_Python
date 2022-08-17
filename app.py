import pkg.extract as extract
import pkg.logger as logger
import sys

def main():

    # Check if the user has passed in a command line DEBUG argument
    logger.debug_flg = True if sys.argv[1:2] == ['DEBUG'] else False
    
    # Set the logger for this file
    log = logger.set_logger(
        logger_name=logger.get_rel_path(__file__),
        is_debug= logger.debug_flg
    )
    log.info("Start Main")

    # Log basic debug information like function calls and returns (log level must be set to DEBUG).
    basic_debug = logger.Debug2Log()
    basic_debug.set_trace()

    b = {'a': 1, 'b': 2}
    extract.test(b)

    log.info("End Main")

if __name__ == '__main__':
    main()
