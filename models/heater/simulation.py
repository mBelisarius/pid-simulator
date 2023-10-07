from core import utils

import numpy as np
import matplotlib.pyplot as plt


def simulate(time, temp_extern, target, heater, system, control):
    system.reset()

    temperature = np.full_like(time, temp_extern)
    temperature_heater = np.full_like(time, temp_extern)

    pid_res = np.zeros_like(time)
    pid_data = np.zeros((time.shape[0], 3))

    for i in range(1, time.shape[0]):
        temperature[i] = system.get_temp_fluid()
        temperature_heater[i] = system.get_temp_heater()

        pid_res[i], pid_data[i] = control.iterate(target, time[i] - time[i - 1])

        system.set_heater_power(heater.max_power * pid_res[i] / (control.range[1] - control.range[0]))

    return temperature, temperature_heater, pid_res, pid_data


def plot_results(time, temperature, temperature_heater, pid_res, pid_data, target, pid_range, dpi=600):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=dpi)

    ax1.plot(time, np.array(time.shape[0] * [utils.to_celsius(target)]), label="Target T")
    ax1.plot(time, utils.to_celsius(temperature_heater), label="Heater T")
    ax1.plot(time, utils.to_celsius(temperature), label="Current T")

    ax2.plot(time, pid_data[:, 2], label="PWM-D")
    ax2.plot(time, pid_data[:, 1], label="PWM-I")
    ax2.plot(time, pid_data[:, 0], label="PWM-P")
    ax2.plot(time, pid_res, label="PWM")
    ax2.set_ylim(pid_range)

    ax1.grid()
    ax1.legend()
    ax2.grid()
    ax2.legend()
    fig.tight_layout()

    plt.show()

    return fig
