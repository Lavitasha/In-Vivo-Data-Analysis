import os

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt


def plot_command(cmd, sampling_interval=0.0001):
    x_axis = np.linspace(0, sampling_interval * len(cmd), len(cmd))
    plt.plot(x_axis, cmd)
    plt.show()


def get_command(data_folder, command_file_name):
    command_file_path = os.path.join(data_folder, command_file_name)
    cmd_df = pd.read_csv(command_file_path)
    cmd = cmd_df['command'].values
    return cmd


def main():
    data_folder = '/Users/lavitasha/Documents/in_vivo_data_analysis_repo/data/'
    command_file_name = 'studentCourse_Command.csv'
    cmd = get_command(data_folder, command_file_name)

    plt.xlabel('time(s)')
    plt.ylabel('Position')
    plot_command(cmd, sampling_interval=0.0001)
    plt.savefig('InVivo Position vs time')



    vm_file_name = 'studentCourse_Vm.csv'
    vm_file_path = os.path.join(data_folder, vm_file_name)

    vm_df = pd.read_csv(vm_file_path)

    print(vm_df.keys())
    for column_name in vm_df.keys():
        vm = vm_df[column_name].values
        x_axis = np.linspace(0, 0.0001 * len(vm), len(vm))
        plt.plot(x_axis, vm_df[column_name], label=column_name)
        plt.xlabel('time(s)')
        plt.ylabel('mV')
        plt.savefig('InVivo mV vs time')
    plt.legend()
    plt.show()


    #for column_name in vm_df.keys():
     #   vm = vm_df[column_name].values
     #   x_axis = np.linspace(0, 0.0001 * len(vm), len(vm))
      #  plt.plot(x_axis, vm_df['Vm_1'])
   # plt.show()


if __name__ == '__main__':
    main()
