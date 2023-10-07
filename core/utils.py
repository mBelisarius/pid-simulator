import numpy as np


def to_kelvin(temp):
    return temp + 273.15


def to_celsius(temp):
    return temp - 273.15


def cost_function(data, target, norm=2):
    return np.power(np.power(np.abs(data - target), norm).sum() / data.shape[0], 1.0 / norm)
