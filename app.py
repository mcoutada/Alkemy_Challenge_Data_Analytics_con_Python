import sys
import pkg.extract as e
import pkg.load as l
import pkg.logger as logger
import pkg.transform as t


def main():

    ###### Logger setup - Start ######
    # Check if the user has passed in a command line DEBUG argument
    logger.debug_flg = True if sys.argv[1:2] == ["DEBUG"] else False

    # Set the logger for this file
    log = logger.set_logger(logger_name=logger.get_rel_path(__file__))
    log.info("Start Main")

    # Log basic debug information like function calls and returns (log level
    # must be set to DEBUG).
    basic_debug = logger.Debug2Log()
    basic_debug.set_trace()

    ###### Logger setup - End ######

    csvs_dic = e.download_csvs()
    dfs_dic = t.transform(csvs_dic)
    l.load(dfs_dic)

    log.info("End Main")


if __name__ == "__main__":
    main()
