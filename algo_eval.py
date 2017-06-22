#!/usr/bin/env python

import sys
import os
import json
from pprint import pprint
from threading import Thread
import subprocess
import time
import datetime

def run_eval(t_id, algorithm, resize_factor, alpha, max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio, \
        smooth_filter, smooth_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_er_thresh, bg_dl_thresh):

    run_counter = 0
    total_runs = len(algorithm) * len(resize_factor) * len(alpha) * len(mvt_tolerance) * len(smooth_filter) * len(smooth_filt_size) * \
    len(max_detectable_distance) * len(min_obj_height) * len(obj_ratio) * len(post_filter) * len(post_filt_size) * len(merge_algo) * \
    len(merge_margin) * len(bg_er_thresh) * len(bg_dl_thresh)

    for algo in algorithm:
        data["plugins"]["motion_detection"]["algorithm"] = algo
        for rsz in resize_factor:
            data["plugins"]["motion_detection"]["configuration"]["resize_factor"] = rsz
            for a in alpha:
                data["plugins"]["motion_detection"]["configuration"]["alpha"] = a
                for max_dist in max_detectable_distance:
                    data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"] = max_dist
                    for sm_filt in smooth_filter:
                        data["plugins"]["motion_detection"]["configuration"]["smooth_filter"] = sm_filt
                        for sm_sz in smooth_filt_size:
                            data["plugins"]["motion_detection"]["configuration"]["smooth_filt_size"] = sm_sz
                            for ps_filt in post_filter:
                                data["plugins"]["motion_detection"]["configuration"]["post_filter"] = ps_filt
                                for ps_sz in post_filt_size:
                                    data["plugins"]["motion_detection"]["configuration"]["post_filt_size"] = ps_sz
                                    for merge in merge_algo:
                                        data["plugins"]["motion_detection"]["configuration"]["merge_algo"] = merge
                                        for merge_mrg in merge_margin:
                                            data["plugins"]["motion_detection"]["configuration"]["merge_margin"] = merge_mrg
                                            for thresh in bg_er_thresh:
                                                data["plugins"]["motion_detection"]["configuration"][algo]["bg_er_thresh"] = thresh

                                                with open(conf_path + "ECV.json", "w") as edited_file:
                                                    json.dump(data, edited_file, indent=4, sort_keys=True)
                                                run_counter += 1
                                                print("[" + str(datetime.datetime.now()) + "] Running thread " + str(t_id) + ", test " + str(run_counter) + "/" + str(total_runs) + "...")
                                                print("algorithm:%s, resize_factor:%d, alpha:%f, max_detectable_distance:%d, smooth_filter:%d, smooth_filt_sz:%d, post_filter:%d, post_filt_sz:%d,
                                                merge_algo:%d, merge_margin:%d, bg_er_thresh:%d" % (algo, rsz, a, max_dist, sm_filt, sm_sz, ps_filt, ps_sz, merge, merge_mrg, thresh))
                                                os.system(eval_path + "ecv_algo_eval " + conf_path + "ECV_tools.json")
                                                # os.system(eval_path + "ecv_algo_eval " + conf_path + "ECV_tools.json >/dev/null 2>&1")
                                                # subprocess.run(["xterm", "-e", eval_path + "ecv_algo_eval " + conf_path + "ECV_tools.json"], stdout=subprocess.PIPE)
                                                print("[" + str(datetime.datetime.now()) + "] Thread " + str(t_id) + ", test " + str(run_counter) + " finished")



if len(sys.argv) < 3:
    print("Not enought input arguments. \nPlease provide the full path to ecv_algo_eval binary as first argument and the full path to the configuration file as a second argument.")
    print("Example: python3 algo_eval.py /cctv/tests/ /conf/")
    sys.exit()
else:
    eval_path = sys.argv[1]
    conf_path = sys.argv[2]

data = []
with open(conf_path + "ECV.json", "r") as data_file:
    text = data_file.read()
    data = json.loads(text)

algorithm = ["adaptive_average", "adaptive_average_channel_fusion"]
resize_factor = [1, 2, 3]
alpha = [0.025, 0.2]
max_detectable_distance = [25, 100]
mvt_tolerance = [0]
min_obj_height = [1.6]
obj_ratio = [0.41]
smooth_filter = [0, 1, 2]
smooth_filt_size =[7, 15]
post_filter = [0, 1, 2]
post_filt_size = [7, 15]
merge_algo = [1]
merge_margin = [0.1]
bg_er_thresh = [10, 40]
bg_dl_thresh = [30]
t_id = 0

run_eval(t_id, algorithm, resize_factor, alpha, max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio, \
        smooth_filter, smooth_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_er_thresh, bg_dl_thresh)

#~ for a in alpha:
    #~ for th in bg_er_thresh:
        #~ t = Thread(target=run_eval, args=(t_id, algorithm, resize_factor, alpha, max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio, \
        #~ smooth_filter, smooth_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_er_thresh, bg_dl_thresh,))
        #~ t.start()
        #~ t_id += 1
        #~ time.sleep(30) #  wait 30s to make sure the correct ECV.json file will have been read (TODO: use of mutex http://effbot.org/zone/thread-synchronization.htm)
