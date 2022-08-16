import pkg.extract as extract
import pkg.logger as logger
import sys

def main():

    log = logger.setup_applevel_logger(
        # Check if the user has passed in a command line argument
        is_debug=True if sys.argv[1:2] == ['DEBUG'] else False
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
