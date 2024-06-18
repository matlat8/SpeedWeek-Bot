import logging
import os

def setup_logger(name):
    log_level = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(numeric_level)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('bot.log')
    fh.setLevel(numeric_level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger