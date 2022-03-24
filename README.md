How-To-Use:
https://github.com/UB-Mannheim/tesseract/wiki

1. Download and add to PATH
2. install dependencies:
    pip install pytesseract tesseract PySimpleGUI
3. adjust this line of code:
    pytesseract.tesseract_cmd = 'C:/path/to/tesseract.exe'
4. run:
    py gui.py
