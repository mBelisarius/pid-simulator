class Fluid:
    def __init__(self, density, cp, viscosity, conductivity, beta, prandtl):
        """
        :param density: Density (kg m-3)
        :param cp: (J kg-1 K-1)
        :param viscosity: Cinematic viscosity (m2 s-1)
        :param conductivity: Thermal conductivity (W m-1 K-1)
        :param beta: Thermal expansion coefficient for ideal gas (K-1)
        :param prandtl: Prandtl number (adimensional)

        """
        self.density = density
        self.cp = cp
        self.viscosity = viscosity
        self.conductivity = conductivity
        self.beta = beta
        self.prandtl = prandtl

        self.diffusivity = self.conductivity / (self.density * self.cp)  # Thermal diffusivity (m2 s-1)
