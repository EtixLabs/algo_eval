#!/usr/bin/env python

import os
from pprint import pprint
import matplotlib.pyplot as plt
import json
import csv
import numpy as np


#  User Input
# ***********
results_path = "/samples/eval"
#~ results_path = "/home/tanman/work/dev/test_samples/eval_valid"
#~ results_path = "/home/tanman/work/dev/test_samples/eval_testing"
#  Select here the parameter to be used for clustering in color/marker
#  can be one of {algorithm, resize_factor, max_detectable_distance, alpha, smooth_filter, smooth_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_er_thresh}:
color_cluster = "max_detectable_distance"
marker_cluster = "resize_factor"
#  Color and marker palette
colors = ["r", "g", "b", "k", "c", "m", "y"]
markers = ["o", "s", "*", "x", "+", "^", "h", "d"]


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
sm_filt = []
sm_sz = []
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
cluster["smooth_filter"] = sm_filt
cluster["smooth_filt_size"] = sm_sz
cluster["post_filter"] = post_filt
cluster["post_filt_size"] = post_sz
cluster["merge_algo"] = merge
cluster["merge_margin"] = merge_mrg
cluster["bg_er_thresh"] = thresh


#  Parse results
# **************
for root, dirs, files in os.walk(results_path):
    dirs.sort()
    if len(files) >= 3:  #  we expect to have at least 3 files: ECV.json, ECV_tools.json and eval_motion_detection.txt
        folders.append(os.path.split(root)[-1])
        for filename in files:
            if filename == "eval_motion_detection.txt": #  parse results file
                with open(os.path.join(root, filename), "r") as res_file:
                    for line in res_file:
                        line = line.strip()
                        metrics = line.split(": ")
                        if len(metrics) < 2:  # line without metrics or wrong format (should be "metric_name: metric_value")
                            break
                        key = metrics[0]
                        val = metrics[1]
                        if key == "Frames":
                            Frames.append(int(val))
                        elif key == "TP":
                            TP.append(int(val))
                        elif key == "TN":
                            TN.append(int(val))
                        elif key == "FP":
                            FP.append(int(val))
                        elif key == "FN":
                            FN.append(int(val))
                        elif key == "HR":
                            float_val = float(val[:-1])
                            HR.append(float_val)
                        elif key == "FPR":
                            float_val = float(val[:-1])
                            FPR.append(float_val)
                        elif key == "Acc":
                            float_val = float(val[:-1])
                            Acc.append(float_val)
                        elif key == "Pre":
                            float_val = float(val[:-1])
                            Pre.append(float_val)
                        elif key == "F1":
                            float_val = float(val[:-1])
                            F1.append(float_val)
                        elif key == "Runtime":
                            Runtime.append(int(val))
                        else:
                            print("Could not understand metric, skipping line: \'" + line + "\' in folder \'" + folders[-1] + "\'")
            
            elif filename == "ECV.json":  #  parse configuration file and save parameter values
                with open(os.path.join(root, filename), "r") as ecv_file:
                    text = ecv_file.read()
                    data = json.loads(text)
                    algo_ = data["plugins"]["motion_detection"]["algorithm"]
                    algo.append(algo_)
                    rsz.append(data["plugins"]["motion_detection"]["configuration"]["resize_factor"])
                    alpha.append(data["plugins"]["motion_detection"]["configuration"]["alpha"])
                    dist.append(data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"])
                    sm_filt.append(data["plugins"]["motion_detection"]["configuration"]["smooth_filter"])
                    sm_sz.append(data["plugins"]["motion_detection"]["configuration"]["smooth_filt_size"])
                    post_filt.append(data["plugins"]["motion_detection"]["configuration"]["post_filter"])
                    post_sz.append(data["plugins"]["motion_detection"]["configuration"]["post_filt_size"])
                    merge.append(data["plugins"]["motion_detection"]["configuration"]["merge_algo"])
                    merge_mrg.append(data["plugins"]["motion_detection"]["configuration"]["merge_margin"])
                    thresh.append(data["plugins"]["motion_detection"]["configuration"][algo_]["bg_er_thresh"])
            
            #  Make sure FPR and HR have same dimension
            if len(HR) > len(FPR):
                del HR[-1]
            if len(FPR) > len(HR):
                del FPR[-1]


#  Export results
# *****************************
rows = zip(["Frames"]+Frames, ["TP"]+TP, ["TN"]+TN, ["FP"]+FP, ["FN"]+FN, ["HR"]+HR, ["FPR"]+FPR, ["Acc"]+Acc, ["Pre"]+Pre,["F1"]+F1, \
["Runtime"]+Runtime, ["algorithm"]+algo, ["resize_factor"]+rsz, ["alpha"]+alpha, ["max_detectable_distance"]+dist, \
["smooth_filter"]+sm_filt, ["smooth_filt_size"]+sm_sz, ["post_filter"]+post_filt, ["post_filt_size"]+post_sz, \
["merge"]+merge, ["merge_margin"]+merge_mrg, ["bg_er_thresh"]+thresh, ["folder"]+folders[0:])
with open(os.path.join(results_path, "results.csv"), "w") as results_file:
    writer = csv.writer(results_file)
    for row in rows:
        writer.writerow(row)


#  Process and plot the results
# *****************************
x = np.array(FPR)
y = np.array(HR)
rt_array = np.array(Runtime)
fr_array = np.array(Frames)
fps = np.round(fr_array / rt_array)

color_mask = np.array(cluster[color_cluster])
marker_mask = np.array(cluster[marker_cluster])
size_mask = fps

roc = plt.figure(1)
for i, col_val in enumerate(sorted(set(color_mask))):
    xc = x[color_mask == col_val]
    yc = y[color_mask == col_val]
    color_marker_mask = marker_mask[color_mask == col_val]
    size = size_mask[color_mask == col_val]
    c = colors[i%len(colors)]
    for j, mark_val in enumerate(sorted(set(marker_mask))):
        xcm = xc[color_marker_mask == mark_val]
        ycm = yc[color_marker_mask == mark_val]
        s = size[color_marker_mask == mark_val]
        m = markers[j%len(markers)]
        plt.scatter(xcm, ycm, s=5*(s-min(fps))+20, marker=m, c=c, alpha=0.5, label=color_cluster+"="+str(col_val)+", "+marker_cluster+"="+str(mark_val))
plt.legend(loc="lower right")
plt.title("ROC curve (" + str(len(HR)) + " tests)")
plt.xlabel("FPR (%)")
plt.ylabel("HR (%)")
plt.grid(True)
plt.axis([0, plt.xlim()[1], 0, 100])
#~ for x_, y_, fps_ in np.broadcast(x, y, fps):
    #~ plt.annotate(fps_, (x_,y_))

bin_sz = 20
bins = int(max(fps)/bin_sz)

speed_algo = plt.figure(2)
plt.title("FPS histogram (algo split)")
plt.xlabel("FPS")
algo_array = np.array(algo)
fps_algo = [fps[algo_array == "adaptive_average"], fps[algo_array == "adaptive_average_channel_fusion"]]
plt.hist(fps_algo, bins, histtype="barstacked", label=["gray", "color_fusion"])
plt.legend(loc="upper right")

speed_rsz = plt.figure(3)
plt.title("FPS histogram (resize split)")
plt.xlabel("FPS")
rsz_array = np.array(rsz)
fps_rsz = [fps[rsz_array == 1], fps[rsz_array == 2], fps[rsz_array == 3]]
plt.hist(fps_rsz, bins, histtype="barstacked", label=["rsz=1", "rsz=2", "rsz=3"])
plt.legend(loc="upper right")

speed_sm_filt = plt.figure(4)
plt.title("FPS histogram (resize pre filtering)")
plt.xlabel("FPS")
sm_filt_array = np.array(sm_filt)
fps_sm_filt = [fps[sm_filt_array == 0], fps[sm_filt_array == 1], fps[sm_filt_array == 2]]
plt.hist(fps_sm_filt, bins, histtype="barstacked", label=["none", "gauss", "median"])
plt.legend(loc="upper right")

speed_ps_filt = plt.figure(5)
plt.title("FPS histogram (resize post filtering)")
plt.xlabel("FPS")
ps_filt_array = np.array(post_filt)
fps_ps_filt = [fps[ps_filt_array == 0], fps[ps_filt_array == 1], fps[ps_filt_array == 2]]
plt.hist(fps_ps_filt, bins, histtype="barstacked", label=["none", "closing", "median"])
plt.legend(loc="upper right")

speed = plt.figure(6)
plt.title("FPS histogram")
plt.xlabel("FPS")
plt.hist(fps, bins)
plt.legend(loc="upper right")

plt.show()
