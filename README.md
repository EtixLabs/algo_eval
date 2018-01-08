# algo_eval
Python scripts that help to annotate video files with motion activity events, run motion detection algorithm on a validation set and plot the evaluation results

Functions inside the MD_gt (Motion Detection ground truth) help in the creation of the ground truth for scenes involved in the Motion Detection algorithm. select_gt.py allows browsing a folder and selecting which frames are indeed involved in motion (TP), while create_gt.py reads the intermediate saved result from select_gt and saves it in a proper format, by aggregating (temporal) neighboring frames, according to a tolerance.

algo_eval.py is responsible to call the algorithm evaluation (cpp code) multiple times, with different input algorithm parameters each time. Results and logs are saved in a pre-defined folder.

read_results.py parses the output of algo_eval.py, aggregates the results for multiple cameras and parameter settings and saves them in a results.csv file

disp_results.py parses the results.csv file, plots the ROC curve and illustrates the impact of each parameter to the algorithm's performance (HR, FPR, fps, etc...)

profiler.py is similar to algo_eval, only that the cpp code is called within valgrind, in order to get details on the time spent in the algorithm's parts (profiling)
