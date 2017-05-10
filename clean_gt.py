#!/usr/bin/env python

import os
import tkinter as tk
from PIL import Image
from PIL import ImageTk

root_dir = "/home/tanman/work/dev/test_samples/eval/2017-05-06T20:33:53_valCASA_det100/samples/CASA/videos/3/2017/January/03/3_test2-12-19-22--12-19-52.mp4" #~ "/home/tanman/work/dev/test_samples/eval/2017-05-06T20:33:53_valCASA_det100/samples/"
file_count = 0
fp = 0
FPs = []

for root, dirs, files in os.walk(root_dir):
    for filename in files:
        if os.path.split(root)[1] == "FP" and filename.endswith((".png")):
            file_count += 1
            FPs.append(os.path.join(root, filename))
            
FPs.sort()
#~ print(file_count)
#~ print(len(FPs))

window = tk.Tk()
idx = tk.IntVar()

img = ImageTk.PhotoImage(Image.open(FPs[idx.get()]))
window.title(FPs[idx.get()])

# make the window the size of the image
window.geometry("%dx%d+%d+%d" % (img.width(), img.height(), 0, 0))

# window has no image argument, so use a label as a panel
panel = tk.Label(window, image=img)
panel.pack(side='top', fill='both', expand='yes')

# save the panel's image from 'garbage collection'
panel.image = img


def qKey(event):
    exit()
    
def prevKey(event):
    print("Left arrow key pressed")
    idx.set(idx.get() - 1)
    show_image(idx.get())

def nextKey(event):
    print("Right arrow key pressed")
    idx.set(idx.get() + 1)
    show_image(idx.get())
    
def show_image(id):
    print("id = " + str(id % len(FPs)))
    image_fname = FPs[id % len(FPs)]
    window.title(image_fname)
    img = ImageTk.PhotoImage(Image.open(image_fname))
    panel.configure(image = img)
    panel.image = img

def sKey(event):
    print("saved")

window.bind_all('<Escape>', qKey)
window.bind_all('<Left>', prevKey)
window.bind_all('<Right>', nextKey)
window.bind_all('<s>', sKey)
window.bind_all('<S>', sKey)

# start the event loop
window.mainloop()

#~ for img_fname in FPs:
    #~ img = ImageTk.PhotoImage(Image.open(FPs[idx]))

