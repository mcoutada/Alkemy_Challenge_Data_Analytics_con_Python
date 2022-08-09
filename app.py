import pkg.extract as extract
import pkg.logger as logger

log = logger.setup_applevel_logger(
    is_debug=True
)

extract.main()
