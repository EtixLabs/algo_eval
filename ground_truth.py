#!/usr/bin/env python

import os.path
from collections import defaultdict

#  input parameters
tolerance = 100  # merge events being apart less or equal than this number of frames
print_flag = 0  # if flag == 0 avoid printing
filelist = "/home/tanman/work/test_samples/CASA/playlists/gt_cam03.txt"  # list of videos & event frames

file_cam01 = open(filelist, "r")
prefix = "frame_"
suffix = ".png"
prefix_len = len(prefix)
suffix_len = len(suffix)
videos = defaultdict(list)

for line in file_cam01:
    line = line.strip()
    parts = line.split("/")
    sz = len(parts)
    video_fname = parts[sz-3]  # video filenmame
    fr_name = parts[sz-1]  # frame_xxx.png
    fr_id = int(fr_name[prefix_len:len(fr_name)-suffix_len])  # extract frame number xxx
    videos[video_fname].append(fr_id)
    #~ path = 
    #~ paths[video_fname] = path

for key in videos.keys():
    frame_seq = videos[key]
    frame_seq.sort()
    if print_flag != 0:
        print("*******************************************")
        print("* " + key + " (sorted) *")
        print("*******************************************")
        print(frame_seq)
        print()
    
    idx = 0
    prev_val = -1
    next_val = frame_seq[len(frame_seq)-1]
    #~ frame_seq = [81, 83, 86, 92, 93, 94, 95, 96, 97, 98, 99]
    #~ print("*******************************************")
    #~ print("*******************************************")
    #~ print("*******************************************")
    #~ print(frame_seq)
    seqfill = list(frame_seq)
    for val in frame_seq:
        missing = val - prev_val - 1        
        if idx < len(frame_seq)-1:  # ensure no out-of-range error
            next_val = frame_seq[idx+1]
            next_dif = next_val - val - 1
        if missing > 0:  # we have a frame jump
            if prev_val >= 0:
                if print_flag != 0:
                    print("prev_val->val: " + str(prev_val) + "->" + str(val) + " missing frames: " + str(missing))
            if (missing > tolerance) and (next_dif > tolerance):
                seqfill.remove(val)
                if print_flag != 0:
                    print("removed " + str(val) + " because missing frames before=" + str(missing) + ", missing frames after=" + str(next_dif) + " and tolerance=" + str(tolerance))
                    print(seqfill)
            elif (missing <= tolerance):
                for i in range(1, missing+1):
                    seqfill.append(prev_val+i)
                    seqfill.sort()
                    if print_flag != 0:
                        print("added " + str(prev_val+i) + " because missing frames=" + str(missing) + " and tolerance=" + str(tolerance))
                if print_flag != 0:
                    print(seqfill)
        prev_val = val
        idx = idx + 1
    if print_flag != 0:
        print()
        print(seqfill)
    
    path = "/"
    for i in range(4, len(parts)-3):
        path = path + parts[i] + "/"
    gt_fname = key[:-3] + "txt"
    gt_file = open(path + gt_fname, "w")
    prev_val = seqfill[0]
    start = seqfill[0]
    for val in seqfill:
        jump = val - prev_val
        if jump > 1:
            end = prev_val
            gt_file.write(str(start) + " " + str(end) + " " + str(end-start+1) + "\n")
            start = val
        prev_val = val
    end = val
    gt_file.write(str(start) + " " + str(end) + " " + str(end-start+1) + "\n")
    
