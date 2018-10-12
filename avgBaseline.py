import numpy as np

from matplotlib import pyplot as plt


def avg_baseline(trace, spike_times, baseline_end_time, spike_half_width=3, dt):
    """

    :param np.array trace:
    :param np.array spike_times:
    :param int baseline_end_time:
    :param int spike_half_width:
    :param int dt:
    :return:
    """
    clipped_trace = clip_spikes(trace, spike_times, spike_half_width,dt)

    baseline_end_pt = baseline_end_time/dt
    avg_baseline_vm = clipped_trace[:baseline_end_pt].mean()

    return avg_baseline_vm


def clip_spikes(input_trace, spike_times_idx, spike_half_width=3, avg_window_width=5,dt):
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
