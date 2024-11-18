# This file will attempt to quantify object permanence across a yolo'd dataset 
#  to see if it ends up being a good metric.


# TODO: 
# make function to determine if two objects are the same -> some pixel delta in
#  both dims
# See average num of new objects per image per section. 
# If low, and upon visual inspection, most differences are actually differences,
#  this is justification to make the pruning algorithm as I want because 
#  deleting low diff imgs will likely actually delete the unimportant ones
# Simulate application of algorithm until we see if we have the most important 
#  ones
# See if there are "glitches" in continuity - redo metrics except objs over 2
#  imgs are counted as the same now, 1 img bug is skipped, window widens.

# DOING:
# Try to measure what "counts as the same object"
# -> make a threshold that satisfies tv
# -> make a histogram for each of the dims
# DONE
# Make a fn that sees how many objs change
# make a fn that prints out traces -> top 10% or whatever

import pickle
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def calculate_frequency(arr):
    frequency = {}  # Initialize an empty dictionary to store frequencies
    for item in arr:
        if item in frequency:
            frequency[item] += 1  # Increment the count for the item
        else:
            frequency[item] = 1  # Add the item to the dictionary with count 1
    return frequency

# # Function to plot a histogram
# def plot_histogram(data, title, ax):
#     """
#     Plots a histogram on the provided axis.
    
#     Parameters:
#     - data: The data to be plotted (numpy array or list)
#     - title: The title of the histogram
#     - ax: The axis object to plot the histogram on
#     """

#     bins = np.arange(0, 1.01, 0.005)

#     ax.hist(data, bins=bins, edgecolor='black', alpha=0.6)
#     ax.set_title(title)
#     ax.set_xlabel('Number')
#     ax.set_ylabel('Frequency')
def plot_histogram(data, title, ax):
    """
    Plots a histogram on the provided axis with automatically selected bins.
    
    Parameters:
    - data: The data to be plotted (numpy array or list)
    - title: The title of the histogram
    - ax: The axis object to plot the histogram on
    """
    data = np.array(data)    
    num_bins = 100
    data_min = np.min(data)
    data_max = np.max(data)
    bins = np.linspace(data_min, data_max, num_bins + 1)  # +1 because we need num_bins edges
    ax.hist(data, bins=bins, edgecolor='black', alpha=0.6)
    ax.set_title(title)
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')


def remove_identical_elements(list1, list2, are_identical):
    # Iterate over a copy of list1 to avoid modifying it while iterating
    for item1 in list1[:]:
        for item2 in list2[:]:
            if are_identical(item1, item2):  # Check if the two items are identical
                list1.remove(item1)  # Remove the item from list1
                list2.remove(item2)  # Remove the item from list2
                break  # Once removed, no need to check the rest of list2 for this item

    return list1, list2


def get_count_arr(tsteps, this_slice, obj_name):
    count_arr = []
    for tstep in tsteps[this_slice]:
        curr_count = 0
        for obj in tstep[1]:
            if obj[0] == obj_name:
                curr_count += 1
        # print(f"{tstep[0]} has {curr_count} {obj_name}s")
        count_arr.append(curr_count)
    return count_arr


def get_instance_arr(tsteps, this_slice, obj_name):
    instance_arr = []
    for tstep in tsteps[this_slice]:
        for obj in tstep[1]:
            if obj[0] == obj_name:
                instance_arr.append(obj)
    return instance_arr

def decompose_locs(arr):
    coords = ([],[],[],[])
    for elem in arr:
        for i in range(4):
            coords[i].append(elem[i+1])
    return coords


def check_obj_same(obj1, obj2):
    # Distance threshold is .06 in any direction
    if obj1[0] != obj2[0]:
        return False
    return abs(obj1[1]-obj2[1]) < 0.06 and \
        abs(obj1[2]-obj2[2]) < 0.06 and \
        abs(obj1[3]-obj2[3]) < 0.06 and \
        abs(obj1[4]-obj2[4]) < 0.06

def find_score_single(inf_pre, inf_curr):
    # get tally of how many objects exist in new that don't exist in old, 
    # -> naive implementation means that moved objects will get 2x tally, and 
    #  new/removed objects will only get 1x
    # Use category to check -> if there is a different number of the new object
    # then 2x weight
    
    # some long-term memory might be useful but many of the sequences seem to be
    #  longer than it would be practical to have memory for.
    
    obj_name_set = set()
    # Create object frequency dictionary for the current and previous inferences
    pre_dic = {}
    for obj in inf_pre[1]:
        obj_name = obj[0]
        obj_name_set.add(obj_name)
        if not obj_name in pre_dic:
            pre_dic[obj_name] = []
        pre_dic[obj_name].append(obj)
    
    curr_dic = {}
    for obj in inf_curr[1]:
        obj_name = obj[0]
        obj_name_set.add(obj_name)
        if not obj_name in curr_dic:
            curr_dic[obj_name] = []
        curr_dic[obj_name].append(obj)

    # Next stage, create lists of different objects
    # Remove all identical from both
    for key1 in curr_dic:
        if key1 in pre_dic:
            (curr_dic[key1], pre_dic[key1]) = \
                remove_identical_elements(curr_dic[key1], pre_dic[key1], check_obj_same)

    # Add 1 for each element of each list
    # Add 1 for each difference
    total_score = 0
    for obj_name in obj_name_set:
        if obj_name in curr_dic:
            
            if obj_name in pre_dic:
                # print(obj_name, max(len(curr_dic[obj_name]), len(pre_dic[obj_name])))
                total_score += 2 * max(len(curr_dic[obj_name]), len(pre_dic[obj_name]))
            else:
                # print(obj_name, len(curr_dic[obj_name]))
                total_score += 2 * len(curr_dic[obj_name])
        elif obj_name in pre_dic:
            # print(obj_name, len(pre_dic[obj_name]))
            total_score += 2 * len(pre_dic[obj_name])

    return total_score

def get_scores(tsteps, this_slice):
    tsteps = tsteps[this_slice]
    scores = []
    for i in range(len(tsteps)-1):
        ssingle = find_score_single(tsteps[i], tsteps[i+1])
        scores.append(ssingle)
    return scores


with open("uncommitted/inferences.pkl", "rb") as f:
    inferences = pickle.load(f)

    # for inf in inferences:
    #     print(inf)
# ('img_path', 
#   [
#       ('obj name', tensor(num), tensor(num), tensor(num), tensor(num)), 
#       ('obj name', tensor(num), tensor(num), tensor(num), tensor(num)) 
#   ]
# )

# Note: it does not even waver for nothing. However, even tv's wavers for my 
#  monitors.

    # Try to find the variation score of 'person'and both TVs

    nothing_indices = slice(55, 264)  # Indices 56-263 inclusive
    init_indices = slice(12, 56)      # Indices 13-55 inclusive
    eating_indices = slice(263, 579)  # Indices 264-578 inclusive
    desk_work_indices = slice(702, 2496)  # Indices 703-2495 inclusive
    all_indices = slice(None)



    # ============================================================ 
    # Print number of TVs at each timestep - 
    # Rudimentary way to see if objects persist 
    # ============================================================ 

    # nothing_tv_exists = get_count_arr(inferences, nothing_indices, 'tv')
    # print(nothing_tv_exists)
    # tv_exists = get_count_arr(inferences, all_indices, 'tv')
    # print(tv_exists)



    # ============================================================ 
    # Try to get thresholds by printing out tv location histograms
    # ============================================================ 
    # # let's say if within .0600 distance then same object

    # locs = decompose_locs(get_instance_arr(inferences, all_indices, 'tv'))

    # # Create a figure with 4 subplots (2 rows, 2 columns)
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # plot_histogram(locs[0], "one", axs[0,0])
    # plot_histogram(locs[1], "two", axs[0,1])
    # plot_histogram(locs[2], "three", axs[1,0])
    # plot_histogram(locs[3], "four", axs[1,1])






    # # Adjust layout to prevent overlapping labels
    # plt.tight_layout()

    # plt.show()


    # ============================================================ 
    # Verify that can reliably check that objects are the same, seems to work
    # in empty case
    # ============================================================ 

    # # # 
    # # #  in empty case
    # # # 56,57
    # inf1 = inferences[60]
    # inf2 = inferences[61]
    # print(inf1)
    # print(inf2)
    # # for obj1 in inf1[1]:
    # #     for obj2 in inf2[1]:
    # #         res = check_obj_same(obj1, obj2)
    # #         print(res, obj1, obj2)

    # print(find_score_single(inf1, inf2))


    # ============================================================ 
    # Try to see overall patterns
    # ============================================================ 
    nothing_scores = get_scores(inferences, nothing_indices)
    init_scores = get_scores(inferences, init_indices)
    eating_scores = get_scores(inferences, eating_indices)
    desk_work_scores = get_scores(inferences, desk_work_indices)


    plot_histogram(nothing_scores, 'Empty', axs[0, 0])
    plot_histogram(init_scores, 'Active', axs[0, 1])
    plot_histogram(eating_scores, 'Eating', axs[1, 0])
    plot_histogram(desk_work_scores, 'Desk Work', axs[1, 1])

    plt.tight_layout()

    plt.show()
