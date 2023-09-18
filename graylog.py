import logging
import graypy
import os
from loguru import logger


PYTHON_ENVIRONMENT_NAME = "PYTHON_ENVIRONMENT"


class AddtitionalFieldsFilter(logging.Filter):
    def __init__(self):
        # In an actual use case would dynamically get this
        # (e.g. from memcache)
        if PYTHON_ENVIRONMENT_NAME in os.environ:
            self.environment = os.environ[PYTHON_ENVIRONMENT_NAME]

        self.solution = "FastunaAI"
        self.source = "Language.Detection"

    def filter(self, record):
        if PYTHON_ENVIRONMENT_NAME in os.environ:
            record.environment = os.environ[PYTHON_ENVIRONMENT_NAME]

        record.solution = "FastunaAI"
        record.source = "Language.Detection"

        return True


graylog_logger = logging.getLogger("language_detector_logger")
handler = graypy.GELFHTTPHandler("graylog-input.corp.tiburon-research.ru", 12201)
graylog_logger.addHandler(handler)
graylog_logger.addFilter(AddtitionalFieldsFilter())


def make_extra(payload: str):
    return {"payload": payload}


def netlog_error(message: str, need_trace: bool):
    try:
        graylog_logger.critical(message)
        if need_trace:
            logger.exception(message)
        else:
            logger.error(message)
    except Exception as e:
        logger.exception("Error sending logs")


def netlog_info(message: str, payload: str):
    try:
        graylog_logger.info(message, extra=make_extra(payload))
        logger.info(message)
    except Exception as e:
        logger.exception("Error sending logs")
