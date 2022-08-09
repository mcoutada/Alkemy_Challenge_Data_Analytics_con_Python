import pkg.extract as extract
import pkg.logger as logger

log = logger.setup_applevel_logger(
    is_debug=True
)
def main():
    extract.main()


if __name__ == '__main__':
    main()
