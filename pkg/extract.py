import pkg.logger as logger

# Set the logger for this file
log = logger.set_logger(logger_name=logger.get_rel_path(__file__))


def test(b):
    log.info("Executing module function.")
    a = 1 / 2
    return b


if __name__ == "__main__":
    test()
