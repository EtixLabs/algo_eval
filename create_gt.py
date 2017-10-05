#!/usr/bin/env python3

import collections
import os.path

# input parameters
CAM_ID = 1
TOLERANCE = 100  # merge events being apart less or equal than this number of frames
PRINT_FLAG = False  # if False, avoid printing
DATASET_PATH = "/samples/CASA/videos/"  # dataset's root directory
FILELIST = "/samples/CASA/gt/gt_cam" + str(CAM_ID).zfill(2) + ".txt"  # list of videos & event frames
PREFIX = "frame_"
SUFFIX = ".png"

# Open file with list of frames with event(s)
prefix_len = len(PREFIX)
suffix_len = len(SUFFIX)
videos = collections.defaultdict(list)
paths = {}
with open(FILELIST, "r") as file_cam:
    # Read file line by line
    for line in file_cam:
        #  Extract video filename and frame number
        line = line.strip()
        parts = line.split(os.sep)
        sz = len(parts)
        video_fname = parts[sz-3]  # video_filenmame.mp4
        fr_name = parts[sz-1]  # frame_xxx.png
        fr_id = int(fr_name[prefix_len:len(fr_name)-suffix_len])  # extract frame number xxx
        #  Store event frames for each video file
        videos[video_fname].append(fr_id)
        paths[video_fname] = parts

# Loop over all videos
for key in videos.keys():
    #  list with event frames for specific video
    frame_seq = videos[key]
    #  numerically sort, in case alphabetically sorting had frame 50 after 101...
    frame_seq.sort()
    if PRINT_FLAG:
        print("*******************************************")
        print("* " + key + " (sorted) *")
        print("*******************************************")
        print(frame_seq)
        print()

    # Loop over event frames and remove isolated frames and fill gap between blocks of frames with distance < TOLERANCE
    idx = 0
    prev_val = -1
    next_val = frame_seq[len(frame_seq)-1]
    seqfill = list(frame_seq)
    for val in frame_seq:
        missing = val - prev_val - 1
        if idx < len(frame_seq)-1:  # ensure no out-of-range error
            next_val = frame_seq[idx+1]
            next_dif = next_val - val - 1
        if missing > 0:  # we have a frame jump
            if prev_val >= 0:
                if PRINT_FLAG:
                    print("prev_val->val: " + str(prev_val) + "->" + str(val) + " missing frames: " + str(missing))
            if (missing > TOLERANCE) and (next_dif > TOLERANCE):
                seqfill.remove(val)
                if PRINT_FLAG:
                    print("removed " + str(val) + " because missing frames before=" + str(missing) + ", missing frames after=" + str(next_dif) + " and tolerance=" + str(TOLERANCE))
                    print(seqfill)
            elif (missing <= TOLERANCE):
                for i in range(1, missing+1):
                    seqfill.append(prev_val+i)
                    seqfill.sort()
                    if PRINT_FLAG:
                        print("added " + str(prev_val+i) + " because missing frames=" + str(missing) + " and tolerance=" + str(TOLERANCE))
                if PRINT_FLAG:
                    print(seqfill)
        prev_val = val
        idx = idx + 1
    if PRINT_FLAG:
        print("final filtered 'event' frames:")
        print(seqfill)
        print()

    # Write ground truth file
    path = DATASET_PATH
    path_parts = paths[key]
    for i in range(0, len(path_parts)-3):
        path = path + path_parts[i] + os.sep
    gt_fname = key[:-3] + "txt"
    # Create file at the same directory as the video file
    # Format of ground truth is: START_FRAME END_FRAME DURATION
    with open(path + gt_fname, "w") as gt_file:
        prev_val = seqfill[0]
        start = seqfill[0]
        for val in seqfill:
            jump = val - prev_val
            if jump > 1:  # a new block of frames (a new event) starts here. Write line with the previous event start, end and duration data.
                end = prev_val
                gt_file.write(str(start) + " " + str(end) + " " + str(end-start+1) + "\n")
                start = val
            prev_val = val
        end = val
        gt_file.write(str(start) + " " + str(end) + " " + str(end-start+1) + "\n")
