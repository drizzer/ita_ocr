# py ita_ocr.py -s vid1.mp4

'''
https://github.com/UB-Mannheim/tesseract/wiki

1. Download and add to PATH
2. pip install pytesseract tesseract
3. add this line to code:
    pytesseract.pytesseract.tesseract_cmd = 'C:/OCR/Tesseract-OCR/tesseract.exe'

1 minute video
    at 30 fps: 60 * 30 = 1800 frame
    at 60 fps: 60 * 60 = 3600 frame

'''

import os
import re
import argparse

import pytesseract
import cv2


def main():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", required=True,
                    help="video to treat with OCR")
    args = vars(ap.parse_args())

    produce_frames(args["source"], "./Frames")
    recognize_value("./Frames")


def produce_frames(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    capture = cv2.VideoCapture(src)

    frameNr = 0
    total = 0

    while (True):
        success, frame = capture.read()

        if success:
            total += 1
            if total % 5 == 0:
                cv2.imwrite(dest + f'/{frameNr:06d}.png', frame)
                frameNr += 1
        else:
            break

    capture.release()


def recognize_value(path):
    frames = os.listdir(path)

    for frame in frames:
        image = cv2.imread(path + '/' + frame)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        res_scan = pytesseract.image_to_string(rgb, config="outputbase digits")

        if(len(re.findall("\d+\.\d+", res_scan)) != 0):
            val = float(re.findall("\d+\.\d+", res_scan)[0])

            if val > 0 and val < 20:
                frameNr = re.findall(r'\d+', frame)[0]
                print("{:.2f}".format(val))


if __name__ == "__main__":
    main()
