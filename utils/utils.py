import json
import logging
from logging.config import dictConfig


def setup_logging():
    with open('config.json') as config_file:
        config = json.load(config_file)
    dictConfig(config['logging_config'])
    return logging.getLogger('ADB-Auto-Daily')
