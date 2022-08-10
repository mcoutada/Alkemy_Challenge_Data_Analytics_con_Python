import pkg.extract as extract
import pkg.logger as logger


def main():

    log = logger.setup_applevel_logger(
    )

    # Uncomment the following lines to log basic debug information (DEBUG
    # level = 10)
    log.setLevel(level=10)
    extract.test = logger.Debug2Log(extract.test, log)

    b = {'a': 1, 'b': 2}
    extract.test(b)


if __name__ == '__main__':
    main()
