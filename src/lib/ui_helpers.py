import cv2
import random
from constants import SEARCH_HEIGHT_PERCENT
from src.constants import (
    TITLE_WINDOW
)

def drawPoint(img, center):
    thickness = 25
    line_type = 8
    color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))

    cv2.circle(img,
               center,
               5,
               color,
               thickness,
               line_type)

def show_found_area(frame, bound_rect):
    # View the found area
    cv2.rectangle(frame, (int(bound_rect[0]), int(bound_rect[1])), (int(bound_rect[0] + bound_rect[2]), \
        int(bound_rect[1] + bound_rect[3])), (255, 0, 0), 5)

    cv2.rectangle(frame, (int(bound_rect[0]), int(bound_rect[1])), \
        (int(bound_rect[0] + bound_rect[2]), int(bound_rect[1] + bound_rect[3] * SEARCH_HEIGHT_PERCENT)), (0, 255, 0), 5)

    drawPoint(frame, (bound_rect[0], bound_rect[1]))
    drawPoint(frame, (int(bound_rect[0] + bound_rect[2]), int(bound_rect[1] + bound_rect[3])))

def display_image(image, window=TITLE_WINDOW):
    # Display an image in a given window, default to base window
    cv2.imshow(window, image)
    cv2.waitKey(0)