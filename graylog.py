import logging
import graypy
import os
from loguru import logger


PYTHON_ENVIRONMENT_NAME = "PYTHON_ENVIRONMENT"


class AddtitionalFieldsFilter(logging.Filter):
    def __init__(self):
        # In an actual use case would dynamically get this
        # (e.g. from memcache)
        self.environment = os.environ[PYTHON_ENVIRONMENT_NAME]

    def filter(self, record):
        record.environment = os.environ[PYTHON_ENVIRONMENT_NAME]
        return PYTHON_ENVIRONMENT_NAME in os.environ


graylog_logger = logging.getLogger("language_detector_logger")
handler = graypy.GELFHTTPHandler("graylog-input.corp.tiburon-research.ru", 12201)
graylog_logger.addHandler(handler)
graylog_logger.addFilter(AddtitionalFieldsFilter())


def make_extra(payload: str):
    return {"solution": "FastunaAI", "source": "Language.Detection", "payload": payload}


def netlog_error(message: str, need_trace: bool):
    try:
        if need_trace:
            logger.exception(message)
        else:
            logger.error(message)
        graylog_logger.critical(message)
    except Exception as e:
        print(e)


def netlog_info(message: str, payload: str):
    try:
        logger.info(message)
        graylog_logger.debug(message, extra=make_extra(payload))
    except Exception as e:
        print(e)
