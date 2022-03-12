# py ita_ocr.py -v vid1.mp4 -d ./Frames

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

# from statistics import mean, median

def main():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True,
                    help="video to treat with OCR")
    ap.add_argument("-d", "--destination", required=True,
                    help="where to save frames")
    args = vars(ap.parse_args())

    produce_frames(args["video"], args["destination"])
    values = recognize_value(args["destination"])

    print(f'\nTreated: {len(values)}')
    print(f'Min: {min(values)}\tMax: {max(values)}')
    # print(f'Mean: {mean(values)}\Median: {median(values)}')


def produce_frames(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        print("Chosen directory is not empty. Do you want to clear it? y/n")
        u_input = input()
        if (u_input == 'y'):
            for f in os.listdir(dest):
                os.remove(os.path.join(dest, f))
        else:
            exit()

    capture = cv2.VideoCapture(src)

    frameNr = 0
    total = 0

    while (True):
        success, frame = capture.read()

        if success:
            total += 1
            if total % 20 == 0:  # between 6 and 12 fps depending if 30/60 hz
                frame = frame[200:300, 100:250]
                cv2.imwrite(dest + f'/{frameNr:06d}.png', frame)
                frameNr += 1
        else:
            break

    print(f'Generated {frameNr} / {total}\n')
    capture.release()


def recognize_value(path):
    frames = os.listdir(path)
    values = []

    for frame in frames:
        image = cv2.imread(path + '/' + frame)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        res_scan = pytesseract.image_to_string(rgb, config="outputbase digits")

        if(len(re.findall("\d+\.\d+", res_scan)) != 0):
            val = float(re.findall("\d+\.\d+", res_scan)[0])

            if val > 0 and val < 20:
                frameNr = re.findall(r'\d+', frame)[0]
                values.append("{:.2f}".format(val))
                print(f'{frameNr} : {"{:.2f}".format(val)}')

    return values


if __name__ == "__main__":
    main()
