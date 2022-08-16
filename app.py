import pkg.extract as extract
import pkg.logger as logger
import sys

def main():

    debug_flg = False

    # Checking if the user has passed in a command line argument
    # If the argument is DEBUG, set the debug flag to True.
    if len(sys.argv) == 2:
        debug_flg == True if sys.argv[1] == 'DEBUG' else False

    log = logger.setup_applevel_logger(
        is_debug=debug_flg
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
