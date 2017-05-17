#!/usr/bin/env python

import os
import tkinter as tk
from PIL import Image, ImageTk


cam_id = 14
root_dir = "/home/tanman/work/dev/test_samples/eval/2017-05-12T20:54:23_cam14CASA_det20/samples/CASA/videos/"
err_type = "FP" #  "FP" or "FN"

cam_dir = root_dir + str(cam_id)
output_filename = "/samples/CASA/gt/gt_cam" + str(cam_id).zfill(2) + ".txt"
check_icon = Image.open("resources/transparent-green-checkmark-md.png")
new_gt = []


def load_gt(gt_path):
    gt_file = open(gt_path, 'r')
    gt_fnames = []
    for line in gt_file:
        line = line.strip()
        gt_fnames.append(line)
    print("loaded " + str(len(gt_fnames)) + " gt frames")
    return gt_fnames


def get_video_name(filename):
    path = os.path.split(filename)[0]
    vid_name = path.split("/")[-2]
    return vid_name


def get_frame_name(filename):
    fr_name = os.path.split(filename)[1]
    return fr_name


def get_frame_id(filename):
    fr_id = int(os.path.split(filename)[1][6:-4])
    return fr_id


gt_fnames = load_gt(output_filename)
print(cam_dir)
for root, dirs, files in os.walk(cam_dir):
    for filename in files:
        if os.path.split(root)[1] == err_type and filename.endswith((".png")):
            path = root.split(os.sep)[-6:]  # keep path as 'cam_id/year/month/day/video_filename/FP/frame_XXXXX.png'
            new_gt.append(os.path.join(*path, filename))
if len(new_gt) == 0:
    print("No " + err_type + " images were found")
    exit()
new_gt.sort()

window = tk.Tk()
idx = tk.IntVar()
img = ImageTk.PhotoImage(Image.open(root_dir + new_gt[idx.get()]))
window.title(new_gt[idx.get()])
print(get_video_name(new_gt[0]) + "/" + get_frame_name(new_gt[0]) + "\t" + str(1) + "/" + str(len(new_gt)))

# make the window the size of the image
window.geometry("%dx%d+%d+%d" % (img.width(), img.height(), 0, 0))

# window has no image argument, so use a label as a panel
panel = tk.Label(window, image=img)
panel.pack(side='top', fill='both', expand='yes')

# save the panel's image from 'garbage collection'
panel.image = img


def escapeKey(event):
    window.destroy()


def fastPrevKey(event):
    idx.set(idx.get() - 1000)
    show_image(idx.get())


def prevKey(event):
    idx.set(idx.get() - 1)
    show_image(idx.get())


def nextKey(event):
    idx.set(idx.get() + 1)
    show_image(idx.get())


def fastNextKey(event):
    idx.set(idx.get() + 1000)
    show_image(idx.get())


def show_image(id):
    img_id = id % len(new_gt)
    image_fname = new_gt[img_id]
    print(get_video_name(image_fname) + "/" + get_frame_name(image_fname) + "\t" + str(img_id+1) + "/" + str(len(new_gt)))
    window.title(image_fname)
    img = Image.open(root_dir + image_fname)
    if image_fname in gt_fnames:
        (w, h) = img.size
        (w2, h2) = check_icon.size
        img.paste(check_icon, (w-w2,0), check_icon)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img


def saveKey(event):
    fname = new_gt[idx.get() % len(new_gt)]
    fr_id = get_frame_id(fname)
    if fname not in gt_fnames:
        gt_fnames.append(fname)
        print("saved " + get_frame_name(fname))
    else:
        print(get_frame_name(fname) + " has been already added")
    nextKey(event)


def saveAllKey(event):
    for fname in new_gt:
        if fname not in gt_fnames:
            gt_fnames.append(fname)
    print("added all candidates in ground truth")


def deleteKey(event):
    fname = new_gt[idx.get() % len(new_gt)]
    fr_id = get_frame_id(fname)
    if fname in gt_fnames:
        gt_fnames.remove(fname)
        print("removed " + get_frame_name(fname))
    else:
        print(get_frame_name(fname) + " is not in the ground truth list")
    nextKey(event)


window.bind_all('<Escape>', escapeKey)
window.bind_all('<Control-Left>', fastPrevKey)
window.bind_all('<Left>', prevKey)
window.bind_all('<Right>', nextKey)
window.bind_all('<Control-Right>', fastNextKey)
window.bind_all('<s>', saveKey)
window.bind_all('<S>', saveKey)
window.bind_all('<Control-s>', saveAllKey)
window.bind_all('<d>', deleteKey)
window.bind_all('<D>', deleteKey)

# start the event loop
window.mainloop()

#~ print(gt_fnames)

file_cam_gt = open(output_filename, "w+")
for fname in gt_fnames:
    file_cam_gt.write(fname + "\n")
file_cam_gt.close()
