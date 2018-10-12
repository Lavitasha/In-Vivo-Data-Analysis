import os, sys

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

import analyse_command
from spike_times import find_spike_times


src_folder = sys.argv[1]
# command_file_name = 'studentCourse_command.csv'
command_file_name = 'cell1_contra_eye.csv'
cmd_file_path = os.path.join(src_folder, command_file_name)
data_file_name = 'cell1_contra_eye.csv'
data_file_path = os.path.join(src_folder, data_file_name)

cmd = pd.read_csv(cmd_file_path)['command'].values
data_df = pd.read_csv(data_file_path)

_, direction = analyse_command.get_direction(cmd)
movement_clockwise_idx, movement_anticlockwise_idx = analyse_command.get_direction_index(direction)

all_clockwise_counts = []
all_counter_clockwise_counts = []

for column_name in data_df.keys():
    if not column_name.startswith('Vm'):
        continue
    trial = data_df[column_name].values
    plt.plot(trial)
    plt.show()
    spike_times = find_spike_times(trial, threshold=-7.5)
    print("Number of spikes: {}".format(spike_times))

    clockwise_spike_count = np.intersect1d(spike_times, movement_clockwise_idx).size
    print(clockwise_spike_count)
    counter_clockwise_spike_count = np.intersect1d(spike_times, movement_anticlockwise_idx).size
    print(counter_clockwise_spike_count)
    try:
        dsi = max(clockwise_spike_count, counter_clockwise_spike_count) / (clockwise_spike_count + counter_clockwise_spike_count)
    except ZeroDivisionError:
        dsi = 0

    print(dsi)

    all_clockwise_counts.append(clockwise_spike_count)
    all_counter_clockwise_counts.append(counter_clockwise_spike_count)

sum(all_counter_clockwise_counts)
sum(all_clockwise_counts)