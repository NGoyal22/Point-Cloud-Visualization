import PySimpleGUI as sg
import os.path
from VTKDraft import vtkDraft;

# First the window layout in 2 columns

titleFont = ("Arial", 15)

def blank_frame():
    return sg.Frame("", [[sg.Image(key='-IMAGE-')]], pad=(5, 3), expand_x=True, expand_y=True, border_width=0)

file_Title_Frame= [
    [
        sg.Text("Exploring Annotated Object", size=(20, 1), key='-text-', font=titleFont, expand_x=True, expand_y=True),
        sg.Push(),
        sg.Button("Information", size=(23, 1)),
        sg.Button("Setting_Icon", size=(23, 1)),
    ]
]

Swap_Buttons_Frame= [
    [
        sg.Button("Previous Object", size=(23, 1)),
        sg.Button("Next Object", size=(23, 1)),
    ]
]


layout_frame1 = [
    [sg.Frame(layout=file_Title_Frame, title='', size=(1300, 30), element_justification='c')],
    # Frame for figures display
    [sg.Frame("Object Central Median", [[blank_frame()]], pad=(5, 3), size=(75, 50), expand_x=True), 
     sg.Frame("Object Central Average", [[blank_frame()]], pad=(5, 3), size=(80, 50), expand_x=True)],
    # Frame for views display
    [sg.Frame("360 View", [[blank_frame()]], pad=(5, 3), expand_x=True, expand_y=True), 
     sg.Frame("Side View", [[blank_frame()]], pad=(5, 3), expand_x=True, expand_y=True)],
    [sg.Frame("Top View", [[blank_frame()]], pad=(5, 3), size=(95, 30), expand_x=True, expand_y=True), 
     sg.Frame("Annotated Objects", [[blank_frame()]], pad=(5, 3), expand_x=True, expand_y=True),],
    # Frame for Swapping item buttons
    [sg.Frame("Object Central Median", layout=Swap_Buttons_Frame, pad=(5, 3), size=(75, 50), expand_x=True, element_justification='c')],
]






# ----- Full layout -----
layout = [
    [
        sg.Frame("Frame 1", layout_frame1, size=(1200, 700), title_location=sg.TITLE_LOCATION_TOP),
    ]
]

window = sg.Window("Point Cloud Data Viewer", layout, size=(1280, 720), element_justification='c')

while True:
    event, values = window.read()
    window['-IMAGE-'](data=vtkDraft())
    #Defining info button event
    if event == "Information":
        ch = sg.popup_ok_cancel("Rotate Object:\n\n" + "Please use CTRL + Mouse to rotate the object \n", "Zoom in/out Object:", "Please use CTRL + Mouse Roller to Zoom in/ out \n", title="Information", font=titleFont)
        if ch=="OK":
            print ("You pressed OK")
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()

