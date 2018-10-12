import numpy as np
import pandas
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

def box_smooth(y, box_pts):
    """
    A thin wrapper around numpy to do box smoothing
    :param y:
    :param box_pts:
    :return:
    """
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')  # TODO: check mode

    return y_smooth

def load_csv(data_path):
    """
    load a csv file
    :param str data_path:
    :return: Pandas Dataframe object
    """
    data_path = "data/studentCourse_Vm.csv"
    dataframe = pandas.read_csv(data_path)

    return dataframe

def main():
    peak_window_width = 501
    baseline_window_widthj = 25001
    refractory_period = 1000
    poly_order = 1
    threshold = 15

    plot = True

    for column_name in dataframe.keys():
        if column_name.startswith('Vm'):

            raw = dataframe[column_name].values

            smoothed = savgol_filter(raw, polyorder=poly_order, window_length=peak_window_width)

            baseline = savgol_filter(raw, polyorder=poly_order, window_length=baseline_window_widthj)

            # subtract baseline
            normalized = smoothed - baseline

            # find peaks
            peak_idxs, peak_dict = find_peaks(normalized, distance=refractory_period, height=threshold)
            peak_vals = peak_dict['peak_heights']

            if plot:
                plt.plot(normalized, label="normalized and smoothed")
                plt.plot(peak_idxs, peak_vals, 'o', color="red", label="spike")
    if plot:
        # plt.legend()
        plt.show()


if __name__ == '__main__':
    main()
