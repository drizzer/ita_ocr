import os
import re

from pytesseract import pytesseract
import cv2 as cv
import numpy as np


def produce_frames(src, dest, speed, crop):
    capture = cv.VideoCapture(src)

    frameNr = 0
    total = 0

    while (True):
        success, frame = capture.read()

        if success:
            total += 1
            if total % speed == 0:
                if crop == True:
                    frame = frame[200:400, 100:300]
                cv.imwrite(dest + f'/{frameNr:06d}.png', frame)
                frameNr += 1
        else:
            break

    capture.release()
    return frameNr, total


def recognize_value(path):
    frames = os.listdir(path)
    values = []
    frame_numbers = []

    for frame in frames:
        image = cv.imread(path + '/' + frame)
        gray = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        gray = zoom(gray, 3)

        # sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpen = cv.filter2D(gray, -1, sharpen_kernel)

        # !
        # roi = cv.selectROI(sharpen)
        # roi_cropped = sharpen[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

        res_scan = pytesseract.image_to_string(
            sharpen, config="outputbase digits")
        # outputbase digits
        # --psm 10 --oem 3 -c tessedit_char_whitelist=0123456789
        # print(res_scan)

        if(len(re.findall("\d+\.\d+", res_scan)) != 0):
            val = float(re.findall("\d+\.\d+", res_scan)[0])

            if val > 0 and val < 5:
                values.append("{:.2f}".format(val))
                frameNr = re.findall(r'\d+', frame)[0]
                frame_numbers.append(frameNr)
                print(f'Frame N°{frameNr} : {values[-1]} m/s')

    return values, frame_numbers


def zoom(img, zoom_factor=2):
    return cv.resize(img, None, fx=zoom_factor, fy=zoom_factor)
