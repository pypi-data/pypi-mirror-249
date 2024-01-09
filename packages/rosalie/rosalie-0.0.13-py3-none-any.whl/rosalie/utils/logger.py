import logging

# Check if the root logger has any handlers and remove them if so.
# This unsures that root handler settings in modules we import don't
# affect logging output
root_logger = logging.getLogger()
if root_logger.hasHandlers():
    # Clear all existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)


def module_logger(name):
    log_format = "%(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
