# py test.py -v ./Samples/vid1.mp4
# py test.py -v ./Samples/vid1.mp4 -d path/where/to/save/frames -s 100

'''
https://github.com/UB-Mannheim/tesseract/wiki

1. Download and add to PATH
2. pip install pytesseract tesseract
3. add this line to code:
    pytesseract.tesseract_cmd = 'C:/path/to/tesseract.exe'
'''

import argparse

from pytesseract import pytesseract

from ita_ocr import produce_frames, recognize_value

pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
                help="video to treat with OCR")
ap.add_argument("-d", "--destination", required=False,
                help="where to save frames", default='./Frames')
ap.add_argument("-s", "--speed", required=False,
                help="extracted frames per second", default=10)

args = vars(ap.parse_args())

produce_frames(args["video"], args["destination"], int(args["speed"]), True)
recognize_value(args["destination"])
