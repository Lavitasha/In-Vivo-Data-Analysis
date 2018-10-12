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

    movement_first_pnt_idx, movement_last_pnt_idx = get_movement_range(data)
    differential, direction = get_direction(data)
    get_direction_index(direction)

    plot_raw_data(data, movement_first_pnt_idx, movement_last_pnt_idx, sampling_interval=sampling_interval)
    plot_differential_plot_direction(differential, direction, sampling_interval)


def get_direction(data):
    """
    :param data: Movement command waveform
    :return: Gives
     direction: an array of 0 and 1's defining turing direction at a certain time point
     differential: first derivative of the movement command waveform
    """
    differential = np.diff(data)
    direction = np.zeros(differential.shape, dtype=np.int64)
    direction[differential > 0] = 1
    direction[differential < 0] = -1
    return differential, direction


def get_direction_index(direction):
    movement_clockwise_idx = [np.where(direction == 1)[0][0:]]
    movement_anticlockwise_idx = [np.where(direction == -1)[0][0:]]
    print(movement_clockwise_idx)
    print(movement_anticlockwise_idx)
    return movement_clockwise_idx, movement_anticlockwise_idx


def get_movement_range(data):
    """
    :param np.array data: Data is the movement command waveform
    :return:
    """
    is_moving = np.where(data != 0)[0]
    movement_first_pnt_idx = (is_moving[0])
    movement_last_pnt_idx = (is_moving[-1])
    return movement_first_pnt_idx, movement_last_pnt_idx


def plot_raw_data(data, movement_first_pnt_idx, movement_last_pnt_idx, sampling_interval=0.0001):
    """
    :param data: Movement command waveform
    :param movement_first_pnt_idx: first non zero movement command waveform index
    :param movement_last_pnt_idx: last non zero movement command waveform index
    :param sampling_interval: clock speed of the motor driver
    :return: Plot showing first and last non zero movement command waveform index
    """
    x_axis = np.linspace(0, sampling_interval * len(data), len(data))
    plt.plot(x_axis, data)
    plt.axvline(movement_first_pnt_idx * sampling_interval, color='r')
    plt.axvline(movement_last_pnt_idx * sampling_interval, color='g')
    plt.show()


def plot_differential_plot_direction(differential, direction, sampling_interval):
    """
    :param differential: first derivative of movement command waveform
    :param direction: an array of 0 and 1's defining turing direction at a certain time point
    :param sampling_interval: clock speed of the motor driver
    :return: Plots showing first derivative of movement command waveform and direction logic of movement command waveform
    """
    x_axis = np.linspace(0, sampling_interval * len(differential), len(differential))
    plt.plot(x_axis, differential)
    plt.show()
    plt.plot(x_axis, direction)
    plt.show()


if __name__ == '__main__':
    main()
