import tkinter
import cv2 # pip install opencv-python
import PIL.Image, PIL.ImageTk # pip install pillow
from functools import partial
import threading
import time
import imutils


stream = cv2.VideoCapture("Steve Smith crazy catch against New Zealand - Mast.Video.mp4")

flag = True


def play(speed):
    global flag

    print("Play is called")
    # play video in reverse/forward direction
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)


    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(140, 25, fill="white", font="Times 20 italic bold", text="Decision Pending")
    flag = not flag


def pending(decision):
    # display decision pending image
    frame = cv2.cvtColor(cv2.imread("decision pending(1).png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    # wait for a second
    time.sleep(1.5)

    # display sponcer image
    frame = cv2.cvtColor(cv2.imread("sponcer.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    # wait for a second
    time.sleep(1.5)

    # display real decision(Out/Not-Out image)
    if decision == 'out':
        decisionImg = "out (1).png"
    else:
        decisionImg = "Not Out.png"

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)


def out():
    thread = threading.Thread(target=pending, args=('out',))
    thread.daemon = 1
    thread.start()
    print("player is out")


def not_out():
    thread = threading.Thread(target=pending, args=('not_out',))
    thread.daemon = 1
    thread.start()
    print("player is not out")


# height and width of the frame(main screen)
SET_WIDTH = 1280
SET_HEIGHT = 580

# create window (tkinter gui starts here)
window = tkinter.Tk()
window.title("This is Python Decision Review System")
cv_img = cv2.cvtColor(cv2.imread("decision pending(1).png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()


# buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)", width=30, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=30, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>", width=30, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>", width=30, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Give Out!", width=30, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not-Out!", width=30, command=not_out)
btn.pack()

window.mainloop()