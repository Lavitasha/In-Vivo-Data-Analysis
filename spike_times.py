import numpy as np
import pandas
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter
from scipy.signal import find_peaks as scipy_find_peaks


def load_csv(data_path):
    """
    load a csv file
    :param: data_path
    :return: pandas Dataframe
    """
    dataframe = pandas.read_csv(data_path)

    return dataframe


def box_smooth(y, box_pts):
    """
    A thin wrapper around numpy to box smooth 1D signal
    :param y:
    :param box_pts:
    :return:
    """
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')  # TODO: check mode

    return y_smooth


def subtract_baseline(signal, window_width):
    """
    subtract the DC offset of a signal using a box filter

    :return:
    """
    baseline = box_smooth(signal, window_width)

    # subtract baseline
    return signal - baseline


def find_spike_times(signal, poly_order=1, window_width=501, refractory_period=1000, threshold=15):
    """
    find peaks of a sav-gol smoothed and offest 1D voltage trace


    :param signal:
    :param poly_order:
    :param int window_width:
    :param refractory_period:
    :param float threshold:
    :return: indices and values of spikes for the original signal
    """

    smoothed = savgol_filter(signal, polyorder=poly_order, window_length=window_width)
    processed_offset = subtract_baseline(smoothed, int(len(smoothed)/5))
    peak_idxs, peak_dict = scipy_find_peaks(processed_offset, distance=refractory_period, height=threshold)

    return peak_idxs


def main():
    data_path = "data/studentCourse_Vm.csv"
    poly_order = 1
    peak_window_width = 501
    refractory_period = 1000
    threshold = 15

    dataframe = load_csv(data_path)

    for column_name in dataframe.keys():
        if column_name.startswith('Vm'):
            signal = dataframe[column_name].values
            spike_idxs = find_spike_times(signal, poly_order, peak_window_width, refractory_period, threshold)

            if __debug__ == True:
                plt.plot(signal, label="normalized and smoothed")
                plt.plot(spike_idxs, 30*np.ones(len(spike_idxs)), 'o', color="red", label="spike")
    if __debug__ == True:
        plt.show()

if __name__ == '__main__':
    main()
