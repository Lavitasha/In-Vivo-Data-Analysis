import numpy as np


def subthreshold_analysis(trace, spike_times_idx, baseline_end_time, ccw_t, cw_t):
    """

    :param np.array trace: Ephys recording
    :param np.array spike_times_idx: array of INDICES where spikes are detected
    :param int baseline_end_time: end time of baseline period
    :param np.array ccw_t: array of INDICES where mouse is rotated CCW
    :param np.array cw_t: array of INDICES where mouse is rotated CW
    :return:
    """
    avg_baseline_vm = avg_baseline(trace, spike_times_idx, baseline_end_time)
    normalised_trace = trace.copy() - avg_baseline_vm

    avg_vm_ccw = normalised_trace[ccw_t].mean()
    avg_vm_cw = normalised_trace[cw_t].mean()
    DSI_subthreshold = avg_vm_ccw/avg_vm_cw

    return avg_vm_ccw, avg_vm_cw, DSI_subthreshold


def avg_baseline(trace, spike_times_idx, baseline_end_time, spike_half_width=3, dt=0.12):
    """

    :param np.array trace: Ephys recording
    :param np.array spike_times_idx: array of indices where spikes are detected
    :param int baseline_end_time: end time of baseline period
    :param int spike_half_width:
    :param int dt:
    :return:
    """
    clipped_trace = clip_spikes(trace, spike_times_idx, spike_half_width)

    baseline_end_pt = baseline_end_time/dt
    avg_baseline_vm = clipped_trace[:baseline_end_pt].mean()

    return avg_baseline_vm


def clip_spikes(input_trace, spike_times_idx, spike_half_width=3, avg_window_width=5,dt=0.12):
    """

    :param np.array input_trace:
    :param np.array spike_times_idx:
    :param int spike_half_width:
    :param int avg_window_width:
    :param int dt:
    :return:
    """
    trace = input_trace.copy()
    spike_half_width /=dt
    avg_window_width /=dt
    for spike_t in spike_times_idx:
        start_clip = spike_t - spike_half_width
        end_clip = spike_t + spike_half_width

        value_before_clip = trace[start_clip - avg_window_width:start_clip].mean()
        value_after_clip = trace[end_clip + 1:end_clip + avg_window_width].mean()

        spike_replacement_line = np.linspace(value_before_clip, value_after_clip, (end_clip - start_clip))
        trace[start_clip:end_clip] = spike_replacement_line
    return trace


def test():
    n_points = 100
    baseline_end_time = 75
    test_trace = np.full(n_points, -60)
    test_trace[50:53] = 40
    test_trace[baseline_end_time:] = -50
    test_trace = test_trace + np.random.normal(0, 1, n_points)

    spike_times = [51]

    clipped_trace = clip_spikes(test_trace, spike_times)

    assert clipped_trace.max() < -40, "Expected a maximum value below -40 , test failed"

    test_avg = avg_baseline(test_trace, spike_times, baseline_end_time)

    assert test_avg < -50, "Expected average value below -50, test failed"

    # plt.plot(test_trace)
    # plt.plot(clipped_trace)
    # plt.axvline(spike_times[0], color='r')
    # plt.show()


if __name__ == '__main__':
    test()
