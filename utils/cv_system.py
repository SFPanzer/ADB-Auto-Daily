import cv2
import numpy as np
import matplotlib.pyplot as plt


def match_template(screenshot: np.ndarray, element: np.ndarray) -> np.ndarray:
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    gray_element = cv2.cvtColor(element, cv2.COLOR_BGR2GRAY)
    laplacian_screenshot = cv2.Laplacian(gray_screenshot, cv2.CV_8U)
    laplacian_element = cv2.Laplacian(gray_element, cv2.CV_8U)
    return cv2.matchTemplate(laplacian_screenshot, laplacian_element, cv2.TM_CCOEFF_NORMED)


def single_element_location(screenshot: np.ndarray, element: np.ndarray) -> (int, int):
    matches = match_template(screenshot, element)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matches)
    return max_loc[0] + int(element.shape[1] / 2), max_loc[1] + int(element.shape[0] / 2)


def multiple_elements_location(screenshot: np.ndarray, element: np.ndarray) -> list[(int, int)]:
    matches = match_template(screenshot, element)
    threshold = 0.9
    result = []
    locations = np.where(matches >= threshold)
    for location_index in range(len(locations[0])):
        x = locations[1][location_index] + int(element.shape[1] / 2)
        y = locations[0][location_index] + int(element.shape[0] / 2)
        result.append((x, y))
    return result


def image_element_visual_mark(image: np.ndarray, element_shape: tuple[int, int], location: tuple[int, int]):
    top_left = (location[0] - int(element_shape[1] / 2), location[1] - int(element_shape[0] / 2))
    bottom_right = (location[0] + int(element_shape[1] / 2), location[1] + int(element_shape[0] / 2))
    cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
    cv2.rectangle(image, location, location, (255, 0, 255), 10)
