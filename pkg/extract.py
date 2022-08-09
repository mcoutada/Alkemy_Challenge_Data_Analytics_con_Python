import pkg.logger as logger
log = logger.get_child_logger(module_name=__name__)

def main():
    log.info("Executing module function.")
    a = 1/0
    return None

if __name__ == '__main__':
    main()
