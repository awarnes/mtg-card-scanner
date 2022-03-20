import numpy as np
import pytesseract, cv2
import json, math, os, random, re, time
from collections import defaultdict
from fuzzywuzzy import process, utils

random.seed(102421)
MIN_CARD_SIZE = 200000
MATCH_PERCENTAGE = 95
SEARCH_HEIGHT_PERCENT = 13 / 100
SEARCH_WIDTH_PERCENT = 80 / 100
FRAME_ROTATION_DEGREES = 0
BINARY_THREHOLD = 180

OCR_STYLE = 'tesseract'

def angle3pt(a, b, c):
    """Counterclockwise angle in degrees by turning from a to c around b
        Returns a float between 0.0 and 360.0"""
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def find_string(img):
    if OCR_STYLE == 'tesseract':
        return pytesseract.image_to_string(img, config=r'--psm 7')
    # elif OCR_STYLE == 'keras':
    #     # keras-ocr will automatically download pretrained
    #     # weights for the detector and recognizer.
    #     pipeline = keras_ocr.pipeline.Pipeline()

    #     # Get a set of three example images

    #     # Each list of predictions in prediction_groups is a list of
    #     # (word, box) tuples.
    #     prediction_groups = pipeline.recognize([img])
        
    #     print(prediction_groups)
        # Plot the predictions
        # fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
        # for ax, image, predictions in zip(axs, images, prediction_groups):
        #     keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
    # elif OCR_STYLE == 'easy':
    #     reader = easyocr.Reader(['en'], gpu=False) # need to run only once to load model into memory
    #     result = reader.readtext(img)
    #     print(f'RESULT: {result}')
    #     return result
    else:
        return ''
    

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
        # print(found_string)
        cv2.imshow(TITLE_WINDOW, cropped_thresh)
        cv2.waitKey(0)

        # Process results to remove anything unnecessary preventing processing on nothing later on
        return (utils.full_process(found_string), boundRect)
    return ('', '')

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
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

TITLE_WINDOW = 'frame'
    
def ocr_video(file, path):
    choice_data = []

    with open('/Users/alexanderwarnes/code/mtg-card-manager/card-scanner-api/src/test/AtomicCards.json') as f:
        data = json.load(f)
        choice_data += data['data'].keys()

    match_choices = defaultdict(list)
    for choice in choice_data:
        if re.match(r'[1_\+"a]', choice[0].lower()):
            match_choices['a'].append(choice)
        else:
            match_choices[choice[0].lower()].append(choice)

    capture = cv2.VideoCapture(path)

    found_cards = set()
    current_match = ''
    frame_index = 0
    cv2.namedWindow(TITLE_WINDOW)

    while capture.isOpened():
        ret, frame = capture.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Don't process every frame, randomly choose which to process
        frame_index += 1
        # random.randint(3,10)
        if not frame_index % 3 == 0:
            continue

        (height, width) = frame.shape[:2]
        # calculate the center of the image
        center = (width / 2, height / 2)

        M = cv2.getRotationMatrix2D(center, FRAME_ROTATION_DEGREES, 1)
        frame = cv2.warpAffine(frame, M, (width, height))

        # Get OCR from image
        result, bound_rect = ocr_image(frame)

        print(f'OCR RESULT: {result}')

        if bound_rect:
            # View the found area
            cv2.rectangle(frame, (int(bound_rect[0]), int(bound_rect[1])), (int(bound_rect[0] + bound_rect[2]), \
                int(bound_rect[1] + bound_rect[3])), (255,0,0), 5)

            cv2.rectangle(frame, (int(bound_rect[0]), int(bound_rect[1])), \
                (int(bound_rect[0] + bound_rect[2]), int(bound_rect[1] + bound_rect[3] * SEARCH_HEIGHT_PERCENT)), (0,255,0), 5)

            drawPoint(frame, (bound_rect[0], bound_rect[1]))
            drawPoint(frame, (int(bound_rect[0] + bound_rect[2]), int(bound_rect[1] + bound_rect[3])))

        if utils.validate_string(result):
            top_matches = process.extract(result, match_choices[result[0].lower()], limit=3)
            if any([match for match in top_matches if match[1] >= MATCH_PERCENTAGE]):

                found_cards.add(top_matches[0][0])
                current_match = top_matches[0][0]

        cv2.putText(frame, current_match, (int(frame.shape[0] / 2), int(frame.shape[1] / 2)), cv2.FONT_HERSHEY_SIMPLEX, 4,(0,0,255),2,cv2.LINE_AA)

        cv2.imshow(TITLE_WINDOW, frame)
        key_pressed = cv2.waitKey(33)
        if key_pressed == ord('q'):    # q key to stop
            print('Pressed Q to Quit...')
            break
        elif key_pressed == 32:  # space to continue
            print('Pressed space to continue...')
            continue

    capture.release()
    cv2.destroyAllWindows()
    return found_cards

movie = 'all_cards'
overall_start = time.time()

found_cards = ocr_video(movie, 0)

# found_cards = ocr_video(movie, os.path.join(path,f"{movie}.mov"))

print(len(found_cards))
print(sorted(found_cards))