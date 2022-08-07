import pkg.extract as extract
import pkg.logger as logger

log = logger.setup_applevel_logger(file_name = 'app_debug.log')


log.debug('Calling module function.')
extract.main()
log.debug('Finished.')