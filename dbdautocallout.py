import random
from PIL import Image, ImageGrab, ImageTk, ImageEnhance

import tkinter
import keyboard

import ctypes
import pytesseract

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

window = tkinter.Tk()
window.title("DBDAutoCallout")
window_x = screen_width - 275
window.geometry("275x275+"+str(window_x)+"+0")
window.attributes('-topmost', True) 
window.overrideredirect(True)

canvas = tkinter.Canvas(window, width=575, height=575)
canvas.pack()

image = Image.open("Callouts\\Empty.png")
image = image.resize((275, 275))
photo = ImageTk.PhotoImage(image)
photo_id = canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

def check_screen():
    screenshot_name = "screenshot.png"

    print("Reading")
    screenshot = ImageGrab.grab(bbox=(0.0445*screen_width, 0.815*screen_height, screen_width / 2, 0.854*screen_height))
    screenshot = screenshot.resize((round(screenshot.size[0]*2), round(screenshot.size[1]*2)))
    screenshot = ImageEnhance.Color(screenshot).enhance(0)
    screenshot.save("screenshot.png")
    screenshot.close()

    white = Image.open("screenshot.png").convert('HSV')

    _, _, V = white.split()

    export = V.point(lambda p: p > 220 and 255)
    export.save("screenshot.png")

    pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'

    map_name = pytesseract.image_to_string(Image.open("screenshot.png"), lang='eng', config='--psm 7')

    print(map_name)

    map_name = map_name.replace('\n', '').replace(' ', '').replace('|', 'I').replace("'", '')

    map_load = "Callouts\\"+str(map_name)+".png"

    print(map_load)

    try:
        new_image = Image.open(map_load)
        new_image = new_image.resize((275, 275))
        new_photo = ImageTk.PhotoImage(new_image)
        canvas.itemconfig(photo_id, image = new_photo)
        canvas.imgref = new_photo
    except:
        print("Exception")
    window.after(500, check_screen)

def on_key(event):
    if event.name == "]":
        print("quitting")
        window.destroy()

keyboard.on_press(on_key)

window.after(500, check_screen)
window.mainloop()