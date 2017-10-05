#!/usr/bin/env python3

import sys
import os
import json
from threading import Thread
import subprocess
import time
import datetime


def run_eval(t_id, algorithm, resize_factor, alpha, max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio,
             pre_filter, pre_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_thresh):

    run_counter = 0
    total_runs = (len(algorithm) * len(resize_factor) * len(alpha) * len(mvt_tolerance) * len(pre_filter) * len(pre_filt_size) *
                  len(max_detectable_distance) * len(min_obj_height) * len(obj_ratio) * len(post_filter) * len(post_filt_size) *
                  len(merge_algo) * len(merge_margin) * len(bg_thresh))

    for algo in algorithm:
        for rsz in resize_factor:
            for a in alpha:
                for pr_filt in pre_filter:
                    for pr_sz in pre_filt_size:
                        for ps_filt in post_filter:
                            for ps_sz in post_filt_size:
                                for max_dist in max_detectable_distance:
                                    for merge in merge_algo:
                                        for merge_mrg in merge_margin:
                                            for thresh in bg_thresh:
                                                data["plugins"]["motion_detection"]["algorithm"] = algo
                                                data["plugins"]["motion_detection"]["configuration"]["resize_factor"] = rsz
                                                data["plugins"]["motion_detection"]["configuration"]["alpha"] = a
                                                data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"] = max_dist
                                                data["plugins"]["motion_detection"]["configuration"]["pre_filter"] = pr_filt
                                                data["plugins"]["motion_detection"]["configuration"]["pre_filt_size"] = pr_sz
                                                data["plugins"]["motion_detection"]["configuration"]["post_filter"] = ps_filt
                                                data["plugins"]["motion_detection"]["configuration"]["post_filt_size"] = ps_sz
                                                data["plugins"]["motion_detection"]["configuration"]["merge_algo"] = merge
                                                data["plugins"]["motion_detection"]["configuration"]["merge_margin"] = merge_mrg
                                                data["plugins"]["motion_detection"]["configuration"]["bg_thresh"] = thresh

                                                with open(CONF_PATH + "ECV.json", "w") as edited_file:
                                                    json.dump(data, edited_file, indent=4, sort_keys=True)
                                                run_counter += 1
                                                print("[" + str(datetime.datetime.now()) + "] Running thread " + str(t_id) + ", test " + str(run_counter) + "/" + str(total_runs) + "...", flush=True)
                                                print("algorithm:%s, resize_factor:%d, alpha:%f, max_detectable_distance:%d, pre_filter:%d, pre_filt_sz:%d, post_filter:%d, post_filt_sz:%d, merge_algo:%d, merge_margin:%d, bg_thresh:%d" % (algo, rsz, a, max_dist, pr_filt, pr_sz, ps_filt, ps_sz, merge, merge_mrg, thresh), flush=True)
                                                # os.system(EVAL_PATH + " " + CONF_PATH + "ECV_tools.json >/dev/null 2>&1")
                                                # os.system(EVAL_PATH + " " + CONF_PATH + "ECV_tools.json")
                                                os.system(EVAL_PATH + " " + CONF_PATH + "ECV_tools.json > log" + str(t_id) + "_" + str(run_counter) + ".txt")
                                                # subprocess.run(["xterm", "-e", EVAL_PATH + " " + CONF_PATH + "ECV_tools.json"], stdout=subprocess.PIPE)
                                                print("[" + str(datetime.datetime.now()) + "] Thread " + str(t_id) + ", test " + str(run_counter) + " finished", flush=True)


if len(sys.argv) < 3:
    print("Not enough input arguments. \nPlease provide the full path to ecv_algo_eval binary as first argument and the full path to the configuration folder as a second argument.")
    print("Example: python3 algo_eval.py /cctv/tests/ecv_algo_eval /conf/")
    sys.exit()
else:
    EVAL_PATH = sys.argv[1]
    CONF_PATH = sys.argv[2]

data = []
with open(CONF_PATH + "ECV.json", "r") as data_file:
    text = data_file.read()
    data = json.loads(text)

algorithm = ["adaptive_average"]
resize_factor = [3, 2]
alpha = [0.025, 0.05, 0.1]
max_detectable_distance = [25, 50, 75, 100]
mvt_tolerance = [0]
min_obj_height = [1.6]
obj_ratio = [0.41]
pre_filter = [1]
pre_filt_size = [7, 15]
post_filter = [1]
post_filt_size = [7, 15]
merge_algo = [1]
merge_margin = [0.1]
bg_thresh = [10, 15, 20, 25, 30, 35, 40]
t_id = 0

for a in alpha:
    for th in bg_thresh:
        t_id += 1
        t = Thread(target=run_eval, args=(t_id, algorithm, resize_factor, [a], max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio,
                   pre_filter, pre_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, [th]))
        t.start()
        time.sleep(1)  # wait to make sure the correct ECV.json file will have been read (TODO: use of mutex http://effbot.org/zone/thread-synchronization.htm)
