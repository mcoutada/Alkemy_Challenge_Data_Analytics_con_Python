import pkg.extract as extract
import pkg.logger as logger


def main():

    log = logger.setup_applevel_logger(
        is_debug=True
    )
    log.info("Start Main")

    # Uncomment the following lines to log basic debug information (DEBUG
    # level = 10)
    # log.setLevel(level=10)
    # extract.test = logger.Debug2Log(extract.test, log)
    basicdebug = logger.Debug2Log2()
    basicdebug.basic_debug2log()

    b = {'a': 1, 'b': 2}
    extract.test(b)

    log.info("End Main")

if __name__ == '__main__':
    main()
