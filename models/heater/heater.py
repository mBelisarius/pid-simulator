import numpy as np


class Heater:
    def __init__(self, max_power, diameter, lenght, density, conductivity, specific_heat):
        """
        :param max_power: Maximum power (W)
        :param diameter: Diameter (m)
        :param lenght: Lenght (m)
        :param density: Density (kg m-3)
        :param conductivity: Thermal conductivity (W m-1 K-1)
        :param specific_heat: Specific heat capacity (J kg-1 K-1)

        """
        self.max_power = max_power
        self.diameter = diameter
        self.lenght = lenght
        self.density = density
        self.conductivity = conductivity
        self.specific_heat = specific_heat

        self.power = 0
        self.area = np.pi * self.lenght * self.diameter
        self.volume = (np.pi / 4) * self.lenght * self.diameter ** 2
        self.mass = self.volume * self.density
