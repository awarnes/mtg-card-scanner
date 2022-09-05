import math

import cv2
import fuzzywuzzy as fw
import numpy as np
import pytesseract

from constants import (
    BINARY_THRESHOLD,
    FRAME_ROTATION_DEGREES,
    MIN_CARD_SIZE,
    SEARCH_HEIGHT_PERCENT,
    SEARCH_WIDTH_PERCENT
)
from ui_helpers import display_image
from utils import logger

def angle3pt(a, b, c):
    """Counterclockwise angle in degrees by turning from a to c around b
        Returns a float between 0.0 and 360.0"""
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def find_string(img):
    return pytesseract.image_to_string(img, config=r'--psm 7')

def ocr_image(src):
    # Convert from RGB to grayscale (cvCvtColor)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # Smooth
    src_gray2 = cv2.blur(src_gray, (5,5))

    # Threshold
    _, thresh = cv2.threshold(src_gray2, 127, 255, cv2.THRESH_OTSU)

    # Find edges
    canny_output = cv2.Canny(thresh, 50, 100)

    # Find contours
    contours, _ = cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort out contours and get the biggest one
    try:
        max_cnt = sorted(contours, key=cv2.contourArea)[-1]
    except IndexError:
        return ('', '')

    # This size contour is to find the full card
    if cv2.contourArea(max_cnt) > MIN_CARD_SIZE:
        boundRect = cv2.boundingRect(max_cnt)

        # Crop the original image to the top 10% of found size
        cropped_source = src_gray[int(boundRect[1]):int(boundRect[1] + boundRect[3] * SEARCH_HEIGHT_PERCENT), \
            int(boundRect[0]):int(boundRect[0] + boundRect[2] * SEARCH_WIDTH_PERCENT)]

        cropped_thresh = remove_noise_and_smooth(cropped_source)

        # OCR the image with pytesseract
        found_string = find_string(cropped_thresh)

        display_image(cropped_thresh)

        # Process results to remove anything unnecessary preventing processing on nothing later on
        return (fw.utils.full_process(found_string), boundRect)
    return ('', '')

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(img):
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

    # ###### CHECKS FOR SQUARES (NOT WORKING WELL YET - NEED BETTER INPUT?) #######
    # squares = []
    # for cnt in contours_poly:
    #     if len(cnt) == 4 and cv2.isContourConvex(cnt) and cv2.contourArea(cnt) > 20: # need size?
    #         maxCosine = 0
    #         for k in range(2, 5):
    #             cosine = math.cos(angle3pt(cnt[k % 4][0], cnt[k - 2][0], cnt[k - 1][0]))
    #             maxCosine = max(maxCosine, cosine)
    #         if maxCosine < 0.3:
    #             squares.append(cnt)

    # for i in range(len(squares)):
    #     color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
    #     # cv2.rectangle(src, (int(squares[i][0][0][0]), int(squares[i][1][0][1])), \
    #     #     (int(squares[i][0][0][0] + squares[i][2][0][1]), int(squares[i][1][0][0] + squares[i][3][0][1])), color, 2)

    #     # print(squares[i])
    #     # print(len(squares[i]))
    #     for pt in list(squares[i]):
    #         # print(f"Point: {pt}")
    #         drawPoint(src, tuple(pt[0]))
    # ################################################################################

def get_search_section(frame):
    (height, width) = frame.shape[:2]
    # calculate the center of the image
    center = (width / 2, height / 2)

    M = cv2.getRotationMatrix2D(center, FRAME_ROTATION_DEGREES, 1)
    search_section = cv2.warpAffine(frame, M, (width, height))

    display_image(search_section)

    return search_section

def get_ocr_data(search_section):
    result, bound_rect = ocr_image(search_section)

    logger(f'OCR RESULT: {result}')

    return result, bound_rect