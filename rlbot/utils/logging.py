import logging
import sys

DEFAULT_LOGGER_NAME = "rlbot"
DEFAULT_LOGGER = None
LOGGING_LEVEL = logging.INFO

logging.getLogger().setLevel(logging.NOTSET)


class CustomFormatter(logging.Formatter):
    GREY = "\x1b[38;20m"
    LIGHT_BLUE = "\x1b[94;20m"
    YELLOW = "\x1b[33;20m"
    GREEN = "\x1b[32;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    SECTIONS = [
        "%(asctime)s " + RESET,
        "%(levelname)8s:" + RESET + GREEN + "%(name)12s" + RESET,
        "[%(filename)20s:%(lineno)3s - %(funcName)25s() ]" + RESET + " ",
        "%(message)s" + RESET,
    ]

    FORMATS = {
        logging.DEBUG: [GREY, GREY, GREY, GREY],
        logging.INFO: [GREY, LIGHT_BLUE, GREY, LIGHT_BLUE],
        logging.WARNING: [YELLOW, YELLOW, YELLOW, YELLOW],
        logging.ERROR: [RED, RED, RED, RED],
        logging.CRITICAL: [RED, BOLD_RED, RED, BOLD_RED],
    }

    def format(self, record: logging.LogRecord) -> str:
        colors = self.FORMATS[record.levelno]

        log_fmt = ""
        for color, section in zip(colors, self.SECTIONS):
            log_fmt += color + section

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(logger_name: str, log_creation: bool = True) -> logging.Logger:
    if logger_name == DEFAULT_LOGGER_NAME and DEFAULT_LOGGER is not None:
        return DEFAULT_LOGGER

    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        ch.setLevel(LOGGING_LEVEL)
        logger.addHandler(ch)
    logging.getLogger().handlers = []

    if log_creation:
        logger.debug("creating logger for %s", sys._getframe().f_back)
    return logger


DEFAULT_LOGGER = get_logger(DEFAULT_LOGGER_NAME, log_creation=False)
