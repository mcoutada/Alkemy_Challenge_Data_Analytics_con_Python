import pkg.extract as extract
import pkg.logger as logger

log = logger.setup_applevel_logger(
    logger_name="MyAwesomeApp", is_debug=True, file_name="app_debug.log"
)


log.debug("Calling module function.")
extract.main()
log.debug("Finished.")
