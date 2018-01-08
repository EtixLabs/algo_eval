#!/usr/bin/env python3

import os
import json
import csv
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint


#  User Input
# ***********
RESULTS_PATH = "/samples/eval/validation"
#~ RESULTS_PATH = "/samples/eval/validation/CASA"
#~ RESULTS_PATH = "/samples/eval/validation/CASA/CASA_int"
#~ RESULTS_PATH = "/samples/eval/validation/CASA/CASA_ext"
#~ RESULTS_PATH = "/samples/eval/validation/STH"
#~ RESULTS_PATH = "/samples/eval/testing"

#  Variables Declaration
# **********************
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
results = {'Frames', 'TP', 'TN', 'FP', 'FN', 'Runtime'}

algo = []
algo_idx = []
algo_set = set()
rsz = []
rsz_idx = []
rsz_set = set()
alpha = []
alpha_idx = []
alpha_set = set()
dist = []
dist_idx = []
dist_set = set()
pre_filt = []
pre_filt_idx = []
pre_filt_set = set()
pre_sz = []
pre_sz_idx = []
pre_sz_set = set()
post_filt = []
post_filt_idx = []
post_filt_set = set()
post_sz = []
post_sz_idx = []
post_sz_set = set()
merge = []
merge_idx = []
merge_set = set()
merge_mrg = []
merge_mrg_idx = []
merge_mrg_set = set()
thresh = []                   
thresh_idx = []                   
thresh_set = set()


#  Parse results directories
# **************************

for root, dirs, files in os.walk(RESULTS_PATH): #  explore configuration files and find all possible parameters' configurations
    dirs.sort()    
    for filename in files:
        if filename == "ECV.json":  #  parse configuration file and save all possible parameters' values
            with open(os.path.join(root, filename), "r") as ecv_file:
                text = ecv_file.read()
                data = json.loads(text)
                algo_ = data["plugins"]["motion_detection"]["algorithm"]
                algo_set.add(algo_)
                rsz_set.add(data["plugins"]["motion_detection"]["configuration"]["resize_factor"])
                alpha_set.add(data["plugins"]["motion_detection"]["configuration"]["alpha"])
                dist_set.add(data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"])
                pre_filt_set.add(data["plugins"]["motion_detection"]["configuration"]["smooth_filter"])
                pre_sz_set.add(data["plugins"]["motion_detection"]["configuration"]["smooth_filt_size"])
                post_filt_set.add(data["plugins"]["motion_detection"]["configuration"]["post_filter"])
                post_sz_set.add(data["plugins"]["motion_detection"]["configuration"]["post_filt_size"])
                merge_set.add(data["plugins"]["motion_detection"]["configuration"]["merge_algo"])
                merge_mrg_set.add(data["plugins"]["motion_detection"]["configuration"]["merge_margin"])
                thresh_set.add(data["plugins"]["motion_detection"]["configuration"][algo_]["bg_er_thresh"])

algo = list(algo_set)
algo.sort()
rsz = list(rsz_set)
rsz.sort()
alpha = list(alpha_set)
alpha.sort()
dist = list(dist_set)
dist.sort()
pre_filt = list(pre_filt_set)
pre_filt.sort()
pre_sz = list(pre_sz_set)
pre_sz.sort()
post_filt = list(post_filt_set)
post_filt.sort()
post_sz = list(post_sz_set)
post_sz.sort()
merge = list(merge_set)
merge.sort()
merge_mrg = list(merge_mrg_set)
merge_mrg.sort()
thresh = list(thresh_set)
thresh.sort()

hist = np.zeros((len(results),len(algo),len(rsz),len(alpha),len(dist),len(pre_filt),len(pre_sz),len(post_filt),len(post_sz),len(merge),len(merge_mrg),len(thresh)), np.int32)
pprint(np.shape(hist))
print("Created empty histogram")

iter = 0
for root, dirs, files in os.walk(RESULTS_PATH):
    dirs.sort()
    iter += 1
    #~ pprint("dir iter:" + str(iter))
    #~ pprint("root: " + root)
    files.sort()
    #~ pprint("files: " + str(files))
    for filename in files:
        if filename == "ECV.json":  #  parse configuration file and save all possible parameters' values
            with open(os.path.join(root, filename), "r") as ecv_file:
                text = ecv_file.read()
                data = json.loads(text)
                algo_ = data["plugins"]["motion_detection"]["algorithm"]
                algo_idx = algo.index(algo_)
                rsz_idx = rsz.index(data["plugins"]["motion_detection"]["configuration"]["resize_factor"])
                alpha_idx = alpha.index(data["plugins"]["motion_detection"]["configuration"]["alpha"])
                dist_idx = dist.index(data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"])
                pre_filt_idx = pre_filt.index(data["plugins"]["motion_detection"]["configuration"]["smooth_filter"])
                pre_sz_idx = pre_sz.index(data["plugins"]["motion_detection"]["configuration"]["smooth_filt_size"])
                post_filt_idx = post_filt.index(data["plugins"]["motion_detection"]["configuration"]["post_filter"])
                post_sz_idx = post_sz.index(data["plugins"]["motion_detection"]["configuration"]["post_filt_size"])
                merge_idx = merge.index(data["plugins"]["motion_detection"]["configuration"]["merge_algo"])
                merge_mrg_idx =merge_mrg.index(data["plugins"]["motion_detection"]["configuration"]["merge_margin"])
                thresh_idx = thresh.index(data["plugins"]["motion_detection"]["configuration"][algo_]["bg_er_thresh"])
        
        elif filename.startswith("eval_"): #  parse results' files
            with open(os.path.join(root, filename), "r") as res_file:
                for line in res_file:
                    line = line.strip()
                    metrics = line.split(": ")
                    if len(metrics) < 2:  # line without metrics or wrong format (should be "metric_name: metric_value")
                        break
                    key = metrics[0]
                    val = metrics[1]
                    if key == "Frames":
                        hist[0][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx] += int(val)
                    elif key == "TP":
                        hist[1][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx] += int(val)
                    elif key == "TN":
                        hist[2][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx] += int(val)
                    elif key == "FP":
                        hist[3][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx] += int(val)
                    elif key == "FN":
                        hist[4][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx] += int(val)
                    elif key == "Runtime":
                        hist[5][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx] += int(val)
                    #~ else:
                        #~ print("Could not understand metric, skipping line: \'" + line + "\' in folder \'" + root + "\'")

print("Populated histogram")
with open(os.path.join(RESULTS_PATH, "results.csv"), "w") as results_file:
    writer = csv.writer(results_file)
    row = ["Frames", "TP", "TN", "FP", "FN", "HR", "FPR", "Acc", "Pre", "F1", "Runtime", "algorithm", "resize_factor", "alpha", "max_detectable_distance", \
    "pre_filter", "pre_filt_sz", "post_filter", "post_filt_sz", "merge", "merge_margin", "thresh"]
    writer.writerow(row)
    for algo_idx in range(0, len(algo)):
        for rsz_idx in range(0, len(rsz)):
            for alpha_idx in range(0, len(alpha)):
                for dist_idx in range(0, len(dist)):
                    for pre_filt_idx in range(0, len(pre_filt)):
                        for pre_sz_idx in range(0, len(pre_sz)):
                            for post_filt_idx in range(0, len(post_filt)):
                                for post_sz_idx in range(0, len(post_sz)):
                                    for merge_idx in range(0, len(merge)):
                                        for merge_mrg_idx in range(0, len(merge_mrg)):
                                            for thresh_idx in range(0, len(thresh)):
                                                Frames = hist[0][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx]
                                                if (Frames == 0):
                                                    continue
                                                TP = hist[1][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx]
                                                TN = hist[2][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx]
                                                FP = hist[3][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx]
                                                FN = hist[4][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx]
                                                if (TP+FN != 0):
                                                    HR = 100.0 * TP / (TP+FN)
                                                else:
                                                    HR = 100.0
                                                FPR = 100.0 * FP / Frames
                                                Acc = 100.0 * (TP+TN)/(TP+TN+FP+FN)
                                                if (TP+FP != 0):
                                                    Pre = 100.0 * TP / (TP+FP)
                                                else:
                                                    Pre = 100.0
                                                if (Pre+HR != 0):
                                                    F1 = 2*Pre*HR/(Pre+HR)
                                                else:
                                                    F1 = 0.0
                                                Runtime = hist[5][algo_idx][rsz_idx][alpha_idx][dist_idx][pre_filt_idx][pre_sz_idx][post_filt_idx][post_sz_idx][merge_idx][merge_mrg_idx][thresh_idx]

                                                row = [Frames , TP, TN, FP, FN, HR, FPR, Acc, Pre, F1, Runtime, \
                                                algo[algo_idx], rsz[rsz_idx], alpha[alpha_idx], dist[dist_idx], \
                                                pre_filt[pre_filt_idx], pre_sz[pre_sz_idx], post_filt[post_filt_idx], post_sz[post_sz_idx], \
                                                merge[merge_idx], merge_mrg[merge_mrg_idx], thresh[thresh_idx]]
                                                #~ pprint(row)
                                                writer.writerow(row)
