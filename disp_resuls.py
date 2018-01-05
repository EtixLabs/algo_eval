#!/usr/bin/env python3

import os
import json
import csv
import matplotlib.pyplot as plt
import numpy as np


def on_click(event):
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    print("mouse click (x, y): (" + str(xmouse) + "," + str(ymouse) + ")")
    #~ artist.set_offset_position('data')
    fpr = artist.get_offsets()[event.ind][0][0]
    hr = artist.get_offsets()[event.ind][0][1]
    print("hr:  " + str(hr))
    print("fpr: " + str(fpr))
    print()
    
    for index, item in list(enumerate(HR)):
        if ((abs(item - hr) < 0.000001) and (abs(FPR[index] - fpr) < 0.000001)):
            break
    
    print("index: " + str(index))
    print("HR[index]: " + str(HR[index]))
    print("FPR[index]: " + str(FPR[index]))
    print("algo: " + algo[index])
    print("rsz: " + str(rsz[index]))
    print("alpha: " + str(alpha[index]))
    print("dist: " + str(dist[index]))
    print("pre_filt: " + str(pre_filt[index]))
    print("pre_sz: " + str(post_sz[index]))
    print("post_filt: " + str(post_filt[index]))
    print("post_sz: " + str(post_sz[index]))
    print("merge: " + str(merge[index]))
    print("merge_mrg: " + str(merge_mrg[index]))
    print("thresh: " + str(thresh[index]))
    
    
#  User Input
# ***********
RESULTS_PATH = "/home/tanman/work/dev/test_samples/eval/"
#~ RESULTS_PATH = "/home/tanman/work/dev/test_samples/eval/CASA/"
#~ RESULTS_PATH = "/home/tanman/work/dev/test_samples/eval/CASA/CASA_int/"
#~ RESULTS_PATH = "/home/tanman/work/dev/test_samples/eval/CASA/CASA_ext/"
#~ RESULTS_PATH = "/home/tanman/work/dev/test_samples/eval/STH/"
#~ RESULTS_PATH = "/home/tanman/work/dev/test_samples/eval_valid"
#~ RESULTS_PATH = "/home/tanman/work/dev/test_samples/eval_testing"

#  Select here the parameter to be used for clustering in color/marker
#  can be one of {algorithm, resize_factor, max_detectable_distance, alpha, pre_filter, pre_filt_sz, post_filter, post_filt_sz, merge_algo, merge_margin, thresh}:
COLOR_CLUSTER = "max_detectable_distance"
MARKER_CLUSTER = "thresh"
#  Color and marker palette
COLORS = ["r", "g", "b", "k", "c", "m", "y"]
MARKERS = ["o", "s", "*", "x", "+", "^", "h", "d"]

# Flag to control the plotting of FPS histograms
PLOT_FPS = False

#  Variables Declaration
# **********************
folders = []
Frames = []
TP = []
TN = []
FP = []
FN = []
HR = []
FPR = []
Acc = []
Pre = []
F1 = []
Runtime = []
algo = []
rsz = []
alpha = []
dist = []
pre_filt = []
pre_sz = []
post_filt = []
post_sz = []
merge = []
merge_mrg = []
thresh = []
legends = []
cluster = {}
cluster["algorithm"] = algo
cluster["resize_factor"] = rsz
cluster["max_detectable_distance"] = dist
cluster["alpha"] = alpha
cluster["pre_filter"] = pre_filt
cluster["pre_filt_sz"] = pre_sz
cluster["post_filter"] = post_filt
cluster["post_filt_sz"] = post_sz
cluster["merge_algo"] = merge
cluster["merge_margin"] = merge_mrg
cluster["thresh"] = thresh

#  Parse the results.csv
# *****************************
with open(os.path.join(RESULTS_PATH, "results.csv"), "r") as res_file:
    for line in res_file:
        line = line.strip()
        values = line.split(",")
        if (values[0] == "Frames"): # Ignore (first) header line
            continue
        Frames.append(int(values[0]))
        TP.append(int(values[1]))
        TN.append(int(values[2]))
        FP.append(int(values[3]))
        FN.append(int(values[4]))
        HR.append(float(values[5]))
        FPR.append(float(values[6]))
        Acc.append(float(values[7]))
        Pre.append(float(values[8]))
        F1.append(float(values[9]))
        Runtime.append(int(values[10]))
        algo.append(values[11])
        rsz.append(int(values[12]))
        alpha.append(float(values[13]))
        dist.append(int(values[14]))
        pre_filt.append(int(values[15]))
        pre_sz.append(int(values[16]))
        post_filt.append(int(values[17]))
        post_sz.append(int(values[18]))
        merge.append(int(values[19]))
        merge_mrg.append(float(values[20]))
        thresh.append(int(values[21]))
        
#  Process and plot the results
# *****************************
x = np.array(FPR)
y = np.array(HR)
rt_array = np.array(Runtime)
fr_array = np.array(Frames)
fps = np.round(fr_array / rt_array)

color_mask = np.array(cluster[COLOR_CLUSTER])
marker_mask = np.array(cluster[MARKER_CLUSTER])
size_mask = fps

fig, ax = plt.subplots()
for i, col_val in enumerate(sorted(set(color_mask))):
    xc = x[color_mask == col_val]
    yc = y[color_mask == col_val]
    color_marker_mask = marker_mask[color_mask == col_val]
    size = size_mask[color_mask == col_val]
    c = COLORS[i%len(COLORS)]
    for j, mark_val in enumerate(sorted(set(marker_mask))):
        xcm = xc[color_marker_mask == mark_val]
        ycm = yc[color_marker_mask == mark_val]
        s = size[color_marker_mask == mark_val]
        m = MARKERS[j%len(MARKERS)]
        sc = ax.scatter(xcm, ycm, s=5*(s-min(fps))+20, marker=m, c=c, alpha=0.5, label=COLOR_CLUSTER+"="+str(col_val)+", "+MARKER_CLUSTER+"="+str(mark_val), picker=10)
plt.legend(loc="lower right")
plt.title("ROC curve (" + str(len(HR)) + " tests)")
plt.xlabel("FPR (%)")
plt.ylabel("HR (%)")
plt.grid(True)
plt.axis([0, plt.xlim()[1], 0, 110])
#~ plt.axis([0, 10, 40, 100])
fig.canvas.callbacks.connect('pick_event', on_click)

#~ print(str(len(ax.collections)))
#~ d = ax.collections[0]
#~ print(d.properties())

#~ d = ax.collections[1]
#~ d.set_offset_position('data')
#~ print(d.properties())

# Plot histograms with information about the algorithm's speed
if PLOT_FPS:

    bin_sz = 1
    bins = int(max(fps)/bin_sz)

    # FPS histogram split based on MD algo variant
    speed_algo = plt.figure()
    plt.title("FPS histogram (algo split)")
    plt.xlabel("FPS")
    algo_array = np.array(algo)
    fps_algo = [fps[algo_array == "adaptive_average"], fps[algo_array == "adaptive_average_channel_fusion"]]
    plt.hist(fps_algo, bins, histtype="barstacked", label=["gray", "color_fusion"])
    plt.legend(loc="upper right")

    # FPS histogram split based on resize factor
    speed_rsz = plt.figure()
    plt.title("FPS histogram (resize split)")
    plt.xlabel("FPS")
    rsz_array = np.array(rsz)
    fps_rsz = [fps[rsz_array == 1], fps[rsz_array == 2], fps[rsz_array == 3]]
    plt.hist(fps_rsz, bins, histtype="barstacked", label=["rsz=1", "rsz=2", "rsz=3"])
    plt.legend(loc="upper right")

    # FPS histogram split based on type of pre filter
    speed_pre_filt = plt.figure()
    plt.title("FPS histogram (resize pre filtering)")
    plt.xlabel("FPS")
    pre_filt_array = np.array(pre_filt)
    fps_pre_filt = [fps[pre_filt_array == 0], fps[pre_filt_array == 1], fps[pre_filt_array == 2]]
    plt.hist(fps_pre_filt, bins, histtype="barstacked", label=["none", "gauss", "median"])
    plt.legend(loc="upper right")

    # FPS histogram split based on pre filter size
    speed_pre_sz = plt.figure()
    plt.title("FPS histogram (pre filter size)")
    plt.xlabel("FPS")
    pre_sz_array = np.array(pre_sz)
    fps_pre_sz = [fps[pre_sz_array == 7], fps[pre_sz_array == 15]]
    plt.hist(fps_pre_sz, bins, histtype="barstacked", label=["pre_sz=7", "pre_sz=15"])
    plt.legend(loc="upper right")

    # FPS histogram split based on type of post filter
    speed_post_filt = plt.figure()
    plt.title("FPS histogram (resize post filtering)")
    plt.xlabel("FPS")
    post_filt_array = np.array(post_filt)
    fps_post_filt = [fps[post_filt_array == 0], fps[post_filt_array == 1], fps[post_filt_array == 2]]
    plt.hist(fps_post_filt, bins, histtype="barstacked", label=["none", "closing", "median"])
    plt.legend(loc="upper right")

    # FPS histogram split based on post filter size
    speed_post_sz = plt.figure()
    plt.title("FPS histogram (post filter size)")
    plt.xlabel("FPS")
    post_sz_array = np.array(post_sz)
    fps_post_sz = [fps[post_sz_array == 7], fps[post_sz_array == 15]]
    plt.hist(fps_post_sz, bins, histtype="barstacked", label=["post_sz=7", "post_sz=15"])
    plt.legend(loc="upper right")

    # FPS histogram split based on maximum detectable distance
    speed_dist = plt.figure()
    plt.title("FPS histogram (max detectable distance)")
    plt.xlabel("FPS")
    dist_array = np.array(dist)
    fps_dist = [fps[dist_array == 25], fps[dist_array == 50], fps[dist_array == 75], fps[dist_array == 100]]
    plt.hist(fps_dist, bins, histtype="barstacked", label=["dist=25", "dist=50", "dist=75", "dist=100"])
    plt.legend(loc="upper right")

    # FPS histogram split based on alpha parameter (adaptation)
    speed_alpha = plt.figure()
    plt.title("FPS histogram (alpha)")
    plt.xlabel("FPS")
    alpha_array = np.array(alpha)
    fps_alpha = [fps[alpha_array == 0.025], fps[alpha_array == 0.05], fps[alpha_array == 0.1]]
    plt.hist(fps_alpha, bins, histtype="barstacked", label=["alpha=0.025", "alpha=0.05", "alpha=0.1"])
    plt.legend(loc="upper right")

    # FPS histogram split based on motion threshold
    speed_thresh = plt.figure()
    plt.title("FPS histogram (thresh)")
    plt.xlabel("FPS")
    thresh_array = np.array(thresh)
    fps_thresh = [fps[thresh_array == 10], fps[thresh_array == 15], fps[thresh_array == 20], fps[thresh_array == 25], fps[thresh_array == 30], fps[thresh_array == 35], fps[thresh_array == 40]]
    plt.hist(fps_thresh, bins, histtype="barstacked", label=["thresh=10", "thresh=15", "thresh=20", "thresh=25", "thresh=30", "thresh=35", "thresh=40"])
    plt.legend(loc="upper right")

    # FPS histogram
    speed = plt.figure()
    plt.title("FPS histogram")
    plt.xlabel("FPS")
    plt.hist(fps, bins)
    plt.legend(loc="upper right")

plt.show()
