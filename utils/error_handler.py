import logging

def handle_error(e, message):
    logger = logging.getLogger(__name__)
    logger.error(message, e)
    raise RuntimeError(message) from e