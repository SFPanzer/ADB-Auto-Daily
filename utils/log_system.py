import json
import logging
import os
from datetime import time
from logging.config import dictConfig

import cv2
import numpy as np

import utils.cv_system

config: dict


def setup_logging():
    with open('config.json') as config_file:
        global config
        config = json.load(config_file)
    dictConfig(config['logging_config'])
    return logging.getLogger('ADB-Auto-Daily')


def image_logging(image: np.ndarray):
    logs_path = "./logs"
    file_name = f"{time.strftime('%Y%m%d-%H%M%s')}"
    file_full_name = logs_path + "/" + file_name + ".png"
    cv2.imwrite(file_full_name, image)
    # Check and remove extra image logs.
    files = [f for f in os.listdir(logs_path) if f.endswith('.png')]
    if len(files) > config["backup_count"]:
        files.sort(key=lambda f: os.path.getctime(os.path.join(logs_path, f)))
        old_files = files[:len(files) - config["backup_count"]]
        for f in old_files:
            os.remove(os.path.join(logs_path, f))


def image_element_logging(image: np.ndarray, element_shape: tuple[int, int],
                          location: list[(int, int)] | tuple[int, int]):
    result = image.copy()
    if location is tuple[int, int]:
        location = [location]
    for loc in location:
        utils.cv_system.image_element_visual_mark(result, element_shape, loc)

    image_logging(result)
