import os
#from statistics import mean, median

import PySimpleGUI as sg
from pytesseract import pytesseract


from ita_ocr import produce_frames, recognize_value

pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

sg.theme('DarkBrown')

layout = [[sg.Text('Settings:')],
          [sg.Text('Path to video'), sg.InputText(), sg.FileBrowse(
              initial_folder='./', file_types=(("MP4", "*.mp4"), ("MOV", "*.mov"), ("FLV", "*.flv"), ("WMV", "*.wmv"), ("AVI", "*.avi")))],
          [sg.Text('Save frames under'), sg.InputText(), sg.FolderBrowse(
              initial_folder='./')],
          [sg.Text('Speed'), sg.Slider(range=(1, 60),
                                       default_value=5,
                                       size=(30, 15),
                                       orientation='horizontal'), sg.Text('frames per second')],
          [sg.Checkbox('Centered crop', default=True,
                       tooltip='Adds more precision sometimes', key="-CROP-")],
          [sg.Output(size=(60, 30), key='-OUTPUT-')],
          [sg.Button('Run'), sg.Button('Exit')]]

window = sg.Window('ITA OCR', layout)


def run_ocr(values):
    print(f'Extracting frames to {values[1]}')
    frameNr, total = produce_frames(
        values[0], values[1], values[2], values["-CROP-"])
    print(f'Generated {frameNr} / {total}')
    print('Recognition started\n\nResults:')
    results, frame_numbers = recognize_value(values[1])
    print('\nDone!')
    print(f'Successfully recognized: {len(results)} / {frameNr}')
    print(f'Success Rate: {"{:.2f}".format((len(results) / frameNr) * 100)}%')
    print(f'Min: {min(results)}\tMax: {max(results)}')
    # print(f'Mean: {mean(results)}\Median: {median(results)}')


def main():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            break

        if event == 'Run':
            if values[1] == '':
                values[1] = './Frames'

            if values[0] == '':
                sg.popup('You have to specify a valid source path',
                         title='Invalid Path')
            else:
                if not os.path.exists(values[1]):
                    os.makedirs(values[1])
                    run_ocr(values)
                else:
                    answer = sg.popup_yes_no(
                        'Chosen directory is not empty (Potentially with old frames). Do you want to clear it?', title='Folder is not empty', keep_on_top=True)

                    if answer == 'Yes':
                        window['-OUTPUT-'].update('')
                        print('Clearing the folder')
                        for f in os.listdir(values[1]):
                            os.remove(os.path.join(values[1], f))
                        run_ocr(values)
                    if answer == 'No':
                        print('Aborted!')

    window.close()


if __name__ == "__main__":
    main()
