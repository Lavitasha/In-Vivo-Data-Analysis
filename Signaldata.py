import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Params
sampling_interval = 0.0001
file_path = '/Users/Hester/Desktop/In-Vivo-Data-Analysis/data/studentCourse_command.csv'

def main():
    # IMPORT and read data
    data_file_path = file_path
    data = pd.read_csv(data_file_path)
    data = data['command'].values

    movement_first_pnt_idx, movement_last_pnt_idx = get_movmenent_range(data)

    plot_raw_data(data, movement_first_pnt_idx, movement_last_pnt_idx, sampling_interval=sampling_interval)

    differential, direction = get_direction(data)

    plot_differential_plot_direction(differential, direction, sampling_interval)


def plot_differential_plot_direction(differential, direction, sampling_interval):
    x_axis = np.linspace(0, sampling_interval * len(differential), len(differential))
    plt.plot(x_axis, differential)
    plt.show()
    plt.plot(x_axis, direction)
    plt.show()


def get_direction(data):
    differential = np.diff(data)
    direction = np.zeros(differential.shape, dtype=np.int64)
    direction[differential > 0] = 1
    direction[differential < 0] = -1
    return differential, direction

def plot_raw_data(data, movement_first_pnt_idx, movement_last_pnt_idx, sampling_interval=0.0001):
    x_axis = np.linspace(0, sampling_interval * len(data), len(data))
    plt.plot(x_axis, data)
    plt.axvline(movement_first_pnt_idx * sampling_interval, color='r')
    plt.axvline(movement_last_pnt_idx * sampling_interval, color='g')
    plt.show()

def get_movmenent_range(data):
    """

    :param np.array data:
    :return:
    """
    movement_first_pnt_idx = (np.where(data != 0)[0][0])
    movement_last_pnt_idx = (np.where(data != 0)[0][-1])
    return movement_first_pnt_idx, movement_last_pnt_idx


if __name__ == '__main__':
    main()


# direction is an array of 0 and 1's defining turing direction at a certain time point
# ti is the index at which the turns start (for the time: ti*0.0001)
# tf is the index at which the turn ends (for the time: tf*0.0001)