
# This file is used to help pick a threshold for MSE pixel difference

# For each of the 4 "zones" of my trace, it shows how many images would be 
#  included/removed for a given threshold. Some sample thresh results are
#  printed below.

# This is also currently tailored towards my specific dataset, but since idt 
#  others will make their own, I am ok with that...

nums = []

with open("./uncommitted/mse_diffs.txt", "r") as f:
# with open("./uncommitted/abs_diffs.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        num = line.strip().split(' ')[1]
        nums.append(float(num))



# Convert nums into a numpy array for easier slicing
# nums = np.array(nums)

# Define index ranges for the different periods
nothing_indices = slice(55, 264)  # Indices 56-263 inclusive
init_indices = slice(12, 56)      # Indices 13-55 inclusive
eating_indices = slice(263, 579)  # Indices 264-578 inclusive
desk_work_indices = slice(702, 2496)  # Indices 703-2495 inclusive



def calc_thresh_count(nums, idxs, thold):
    vals = nums[idxs]
    acc = 0
    for val in vals:
        if val <= thold:
            acc += 1
    return len(vals) - acc, acc

def print_thresh_count(name, accepted, removed):
    print(f"{name}- accepted:{accepted}, removed:{removed}")


threshold = 27

(nothing_acc, nothing_rem) = calc_thresh_count(nums, nothing_indices, threshold)
print_thresh_count("nothing", nothing_acc, nothing_rem)
(init_acc, init_rem) = calc_thresh_count(nums, init_indices, threshold)
print_thresh_count("init", init_acc, init_rem)
(eating_acc, eating_rem) = calc_thresh_count(nums, eating_indices, threshold)
print_thresh_count("eating", eating_acc, eating_rem)
(desk_work_acc, desk_work_rem) = calc_thresh_count(nums, desk_work_indices, threshold)
print_thresh_count("desk_work", desk_work_acc, desk_work_rem)

# idk pick something from this interval...

# 25
# nothing- accepted:182, removed:27
# init- accepted:41, removed:3
# eating- accepted:316, removed:0
# desk_work- accepted:1736, removed:58

# 27
# nothing- accepted:4, removed:205
# init- accepted:32, removed:12
# eating- accepted:294, removed:22
# desk_work- accepted:1550, removed:244

# 30:
# nothing- accepted:2, removed:207
# init- accepted:31, removed:13
# eating- accepted:267, removed:49
# desk_work- accepted:1008, removed:786

# 40
# nothing- accepted:0, removed:209
# init- accepted:27, removed:17
# eating- accepted:57, removed:259
# desk_work- accepted:357, removed:1437





