import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Use TkAgg backend for matplotlib (you can change this depending on your environment)
matplotlib.use('TkAgg')  # Or 'Qt5Agg', 'WebAgg', etc.

# Function to plot a histogram
def plot_histogram(data, bins, title, ax):
    """
    Plots a histogram on the provided axis.
    
    Parameters:
    - data: The data to be plotted (numpy array or list)
    - bins: The bin edges (list or numpy array)
    - title: The title of the histogram
    - ax: The axis object to plot the histogram on
    """
    ax.hist(data, bins=bins, edgecolor='black', alpha=0.6)
    ax.set_title(title)
    ax.set_xlabel('Number')
    ax.set_ylabel('Frequency')

# List to hold the numerical data from the file
nums = []

# Swap this to plot different traces
with open("./uncommitted/mse_diffs.txt", "r") as f:
# with open("./uncommitted/abs_diffs.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        num = line.strip().split(' ')[1]
        nums.append(float(num))

# Convert nums into a numpy array for easier slicing
nums = np.array(nums)

# Define index ranges for the different periods
nothing_indices = np.arange(55, 264)  # Indices 56-263 inclusive
init_indices = np.arange(12, 56)      # Indices 13-55 inclusive
eating_indices = np.arange(263, 579)  # Indices 264-578 inclusive
desk_work_indices = np.arange(702, 2496)  # Indices 703-2495 inclusive

# Create a figure with 4 subplots (2 rows, 2 columns)
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Define bin edges for histograms
bins = np.arange(min(nums), max(nums) + 2) - 0.5

# Plot the histograms using the reusable function
plot_histogram(nums[nothing_indices], bins, 'Empty', axs[0, 0])
plot_histogram(nums[init_indices], bins, 'Active', axs[0, 1])
plot_histogram(nums[eating_indices], bins, 'Eating', axs[1, 0])
plot_histogram(nums[desk_work_indices], bins, 'Desk Work', axs[1, 1])

# Adjust layout to prevent overlapping labels
plt.tight_layout()

# Show the plot
plt.show()
