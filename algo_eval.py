#!/usr/bin/env python3

import sys
import os
import json
from threading import Thread
import time
import datetime
from shutil import copyfile


def run_eval(t_id, algorithm, resize_factor, alpha, max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio,
             pre_filter, pre_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_thresh):

    run_counter = 0
    total_runs = (len(algorithm) * len(resize_factor) * len(alpha) * len(mvt_tolerance) * len(pre_filter) * len(pre_filt_size) *
                  len(max_detectable_distance) * len(min_obj_height) * len(obj_ratio) * len(post_filter) * len(post_filt_size) *
                  len(merge_algo) * len(merge_margin) * len(bg_thresh))

    ECV_THREAD_SAFE_FILENAME = "ECV_" + str(t_id) + ".json"
    copyfile(CONF_PATH + "ECV.json", CONF_PATH + ECV_THREAD_SAFE_FILENAME)
    ECV_TOOLS_THREAD_SAFE_FILENAME = CONF_BASENAME_NO_EXT  + "_" + str(t_id) + ".json"
    copyfile(CONF_FILE, CONF_PATH + ECV_TOOLS_THREAD_SAFE_FILENAME)
    tools_data = []
    with open(CONF_PATH + ECV_TOOLS_THREAD_SAFE_FILENAME, "r") as tools_data_file:
        tools_text = tools_data_file.read()
        tools_data = json.loads(tools_text)
        tools_data["ECV_conf"] = ECV_THREAD_SAFE_FILENAME
        OUTPUT_PATH = tools_data["ECV_algo_eval"]["output_path"]
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        LOGS_PATH = OUTPUT_PATH + "/logs/"
        if not os.path.exists(LOGS_PATH):
            os.makedirs(LOGS_PATH)
    with open(CONF_PATH + ECV_TOOLS_THREAD_SAFE_FILENAME, "w") as tools_data_file:
        json.dump(tools_data, tools_data_file, indent=4, sort_keys=True)

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

                                                with open(CONF_PATH + ECV_THREAD_SAFE_FILENAME, "w") as edited_file:
                                                    json.dump(data, edited_file, indent=4, sort_keys=True)

                                                run_counter += 1
                                                print("[" + str(datetime.datetime.now()) + "] Running thread " + str(t_id) + ", test " + str(run_counter) + "/" + str(total_runs) + "...", flush=True)
                                                print("algorithm:%s, resize_factor:%d, alpha:%f, max_detectable_distance:%d, pre_filter:%d, pre_filt_sz:%d, post_filter:%d, post_filt_sz:%d, merge_algo:%d, merge_margin:%d, bg_thresh:%d" % (algo, rsz, a, max_dist, pr_filt, pr_sz, ps_filt, ps_sz, merge, merge_mrg, thresh), flush=True)
                                                # os.system(ALGO_EVAL + " " + CONF_FILE + ECV_TOOLS_THREAD_SAFE_FILENAME + " >/dev/null 2>&1")
                                                os.system(ALGO_EVAL + " " + CONF_PATH + ECV_TOOLS_THREAD_SAFE_FILENAME + " > " + LOGS_PATH + "log" + str(t_id) + "_" + str(run_counter) + ".txt")
                                                print("[" + str(datetime.datetime.now()) + "] Thread " + str(t_id) + ", test " + str(run_counter) + " finished", flush=True)

    os.remove(CONF_PATH + ECV_TOOLS_THREAD_SAFE_FILENAME)
    os.remove(CONF_PATH + ECV_THREAD_SAFE_FILENAME)

#~ **********************
#~ Start of the program *
#~ **********************
if len(sys.argv) < 3:
    print("Not enough input arguments. \nPlease provide the full path to ecv_algo_eval binary as first argument and the full path to the configuration folder as a second argument.")
    print("Example: python3 algo_eval.py ~/cctv/bin/algo_eval ~/cctv/conf/ECV_tools.json")
    sys.exit()
else:
    ALGO_EVAL = sys.argv[1]
    CONF_FILE = sys.argv[2]
    CONF_PATH = os.path.dirname(CONF_FILE) + "/"
    CONF_BASENAME = os.path.basename(CONF_FILE)
    conf_spl = CONF_BASENAME.split(".")
    conf_base = ""
    for i in range(0, len(conf_spl)-1):
        conf_base += conf_spl[i] + "."
    CONF_BASENAME_NO_EXT = conf_base[:-1]

data = []
with open(CONF_PATH + "ECV.json", "r") as data_file:
    text = data_file.read()
    data = json.loads(text)

algorithm = ["adaptive_average"]
resize_factor = [3]
alpha = [0.025, 0.05, 0.1, 0.15, 0.2]
max_detectable_distance = [10, 25, 50, 100]
mvt_tolerance = [0]
min_obj_height = [1.6]
obj_ratio = [0.41]
pre_filter = [1]
pre_filt_size = [15]
post_filter = [1]
post_filt_size = [7]
merge_algo = [1]
merge_margin = [0.1]
bg_thresh = [10, 20, 30]
t_id = 0

for a in alpha:
    for dist in max_detectable_distance:
        t_id += 1
        t = Thread(target=run_eval, args=(t_id, algorithm, resize_factor, [a], [dist], mvt_tolerance, min_obj_height, obj_ratio,
                   pre_filter, pre_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_thresh))
        t.start()
        time.sleep(10)  # wait to make a copy ECV.json file before the next thread access it.
