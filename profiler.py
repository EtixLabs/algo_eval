#!/usr/bin/env python3

import os
import json
from threading import Thread
import time
import datetime


def run_eval(t_id, algorithm, resize_factor, alpha, max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio,
             pre_filter, pre_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, bg_thresh):

    run_counter = 0
    total_runs = (len(algorithm) * len(resize_factor) * len(alpha) * len(mvt_tolerance) * len(pre_filter) * len(pre_filt_size) *
                  len(max_detectable_distance) * len(min_obj_height) * len(obj_ratio) * len(post_filter) * len(post_filt_size) *
                  len(merge_algo) * len(merge_margin) * len(bg_thresh))

    for algo in algorithm:
        data["plugins"]["motion_detection"]["algorithm"] = algo
        for rsz in resize_factor:
            data["plugins"]["motion_detection"]["configuration"]["resize_factor"] = rsz
            for a in alpha:
                data["plugins"]["motion_detection"]["configuration"]["alpha"] = a
                for max_dist in max_detectable_distance:
                    data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"] = max_dist
                    for pr_filt in pre_filter:
                        data["plugins"]["motion_detection"]["configuration"]["pre_filter"] = pr_filt
                        for pr_sz in pre_filt_size:
                            data["plugins"]["motion_detection"]["configuration"]["pre_filt_size"] = pr_sz
                            for ps_filt in post_filter:
                                data["plugins"]["motion_detection"]["configuration"]["post_filter"] = ps_filt
                                for ps_sz in post_filt_size:
                                    data["plugins"]["motion_detection"]["configuration"]["post_filt_size"] = ps_sz
                                    for merge in merge_algo:
                                        data["plugins"]["motion_detection"]["configuration"]["merge_algo"] = merge
                                        for merge_mrg in merge_margin:
                                            data["plugins"]["motion_detection"]["configuration"]["merge_margin"] = merge_mrg
                                            for thresh in bg_thresh:
                                                data["plugins"]["motion_detection"]["configuration"]["bg_thresh"] = thresh

                                                with open(CONF_PATH + "ECV.json", "w") as edited_file:
                                                    json.dump(data, edited_file, indent=4, sort_keys=True)
                                                run_counter += 1
                                                print("[" + str(datetime.datetime.now()) + "] Running thread " + str(t_id) + ", test " + str(run_counter) + "/" + str(total_runs) + "...", flush=True)
                                                print("algorithm:%s, resize_factor:%d, alpha:%f, max_detectable_distance:%d, pre_filter:%d, pre_filt_sz:%d, post_filter:%d, post_filt_sz:%d, merge_algo:%d, merge_margin:%d, bg_thresh:%d" % (algo, rsz, a, max_dist, pr_filt, pr_sz, ps_filt, ps_sz, merge, merge_mrg, thresh), flush=True)
                                                print("valgrind --tool=callgrind --callgrind-out-file=callgrind.out.rel." + str(run_counter) + " " + EVAL_PATH + " " + CONF_PATH + "ECV_tools.json", flush=True)
                                                os.system("valgrind --tool=callgrind --callgrind-out-file=callgrind.out.rel." + str(run_counter) + " " + EVAL_PATH + " " + CONF_PATH + "ECV_tools.json")
                                                print("[" + str(datetime.datetime.now()) + "] Thread " + str(t_id) + ", test " + str(run_counter) + " finished", flush=True)


EVAL_PATH = "/home/tanman/work/dev/dcim/cctv/computer_vision_tools/algo_eval/build-release/algo_eval"
CONF_PATH = "/home/tanman/work/dev/dcim/cctv/cctv-server/deployment/conf/"

data = []
with open(CONF_PATH + "ECV.json", "r") as data_file:
    text = data_file.read()
    data = json.loads(text)

algorithm = ["adaptive_average"]
resize_factor = [2, 3]
alpha = [0.05]
max_detectable_distance = [50]
mvt_tolerance = [0]
min_obj_height = [1.6]
obj_ratio = [0.41]
pre_filter = [1, 2]
pre_filt_size = [5, 7, 11, 15]
post_filter = [1, 2]
post_filt_size = [5, 7, 11, 15]
merge_algo = [1]
merge_margin = [0.1]
bg_thresh = [15]
t_id = 0

for a in alpha:
    for th in bg_thresh:
        t_id += 1
        t = Thread(target=run_eval, args=(t_id, algorithm, resize_factor, [a], max_detectable_distance, mvt_tolerance, min_obj_height, obj_ratio,
                   pre_filter, pre_filt_size, post_filter, post_filt_size, merge_algo, merge_margin, [th],))
        t.start()
        time.sleep(60)  # wait to make sure the correct ECV.json file will have been read (TODO: use of mutex http://effbot.org/zone/thread-synchronization.htm)

print("Saving results in profile_total_instr.txt")
os.system("cat callgrind.out.rel.* | grep totals: > profile_total_instr.txt")
