import logging
import graypy
from loguru import logger

handler = graypy.GELFHTTPHandler(
    "graylog-input.corp.tiburon-research.ru", 12201)

graylog_logger = logging.getLogger('python_logger')
graylog_logger.setLevel(logging.DEBUG)
graylog_logger.addHandler(handler)


def make_extra(payload: str):
    return {
            "solution": "FastunaAI",
            "source": "Language.Detection",
            "payload": payload
        };


def netlog_error(message: str, payload: str):
    try:
        logger.exception(message)
        graylog_logger.critical(message, extra=make_extra(payload))
    except Exception as e:
        print(e)


def netlog_info(message: str, payload: str):
    try:
        logger.info(message)
        graylog_logger.debug(message, extra=make_extra(payload))
    except Exception as e:
        print(e)
