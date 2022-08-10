import pkg.logger as logger

log = logger.get_child_logger(module_name=__name__)


def test(b):
    log.info("Executing module function.")
    a = 1 / 2
    return b


if __name__ == "__main__":
    test()
