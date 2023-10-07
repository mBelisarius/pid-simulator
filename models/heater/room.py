class Room:
    def __init__(self, lenght, height, thickness, conductivity):
        """
        :param lenght: (m)
        :param height: (m)
        :param thickness: (m)
        :param conductivity: Thermal conductivity (W m-1 K-1)

        """
        self.lenght = lenght
        self.height = height
        self.thickness = thickness
        self.conductivity = conductivity

        self.volume = self.lenght * self.lenght * self.height  # (m3)
