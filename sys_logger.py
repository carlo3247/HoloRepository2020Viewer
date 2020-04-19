import logging

def configureLogger(logger_name: str, log_switch: bool):
    # create logger
    logger = logging.getLogger(logger_name)
    if log_switch == True:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    return logger