import cv2
import fuzzywuzzy as fw
import json, re, time
from src.data_helpers import get_card_data
from src.ocr_helpers import get_ocr_data, get_search_section
from src.ui_helpers import show_found_area
from src.constants import (
    TITLE_WINDOW,
    MATCH_PERCENTAGE
)
from src.utils import logger

def ocr_video(path):
    match_options = get_card_data()

    capture = cv2.VideoCapture(path) # TODO: CONFIGURATION

    found_cards = set() # TODO: handle multiple cards without accidental duplicates
    current_match = ''
    frame_index = 0
    cv2.namedWindow(TITLE_WINDOW)

    while capture.isOpened():
        ret, frame = capture.read()
        # if frame is read correctly ret is True
        if not ret:
            logger("Can't receive frame (stream end?). Exiting ...")
            break

        # Don't process every frame, process every third frame
        frame_index += 1 # TODO: CONFIGURATION

        if not frame_index % 3 == 0:
            continue
        
        search_section = get_search_section(frame)

        result, bound_rect = get_ocr_data(search_section)

        if bound_rect:
            show_found_area(frame, bound_rect)

        if fw.utils.validate_string(result):
            top_matches = fw.process.extract(result, match_options[result[0].lower()], limit=3)
            if any([match for match in top_matches if match[1] >= MATCH_PERCENTAGE]):

                found_cards.add(top_matches[0][0])
                current_match = top_matches[0][0]

        cv2.putText(frame, current_match, (int(frame.shape[0] / 2), int(frame.shape[1] / 2)), cv2.FONT_HERSHEY_SIMPLEX, 4,(0,0,255),2,cv2.LINE_AA)

        cv2.imshow(TITLE_WINDOW, frame)
        key_pressed = cv2.waitKey(33)

        if key_pressed == ord('q'):    # q key to stop
            logger('Pressed Q to Quit...')
            break
        elif key_pressed == 32:  # space to continue
            logger('Pressed space to continue...')
            continue

    capture.release()
    cv2.destroyAllWindows()
    return found_cards


found_cards = ocr_video(0)

# found_cards = ocr_video(os.path.join(path,f"{movie}.mov"))

logger(len(found_cards))
logger(sorted(found_cards))