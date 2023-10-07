import numpy as np
cimport numpy as np

cdef class System:
    cdef double temp_extern
    cdef double temp_fluid
    cdef double temp_heater
    cdef object heater
    cdef object room
    cdef object fluid
    cdef double noise
    cdef double _flux_heater

    def __init__(self, double temp_extern, object heater, object room, object fluid, double noise=0.0):
        self.temp_extern = temp_extern
        self.temp_fluid = self.temp_extern
        self.temp_heater = self.temp_extern
        self.heater = heater
        self.room = room
        self.fluid = fluid
        self.noise = noise
        self._flux_heater = 0.0

    cpdef double get_temp_fluid(self):
        return self.temp_fluid

    cpdef double get_temp_heater(self):
        return self.temp_heater

    cpdef set_heater_power(self, power):
        self.heater.power = power

    cpdef void reset(self):
        self.temp_fluid = self.temp_extern
        self.temp_heater = self.temp_extern
        self._flux_heater = 0.0
        self.heater.power = 0.0

    cpdef double current(self, double time_step):
        self.simulate(time_step)
        return self.temp_fluid

    cpdef double heat_loss(self):
        cdef double convection_sides = 2.5
        cdef double heat_loss_sides = (4 * (self.temp_fluid - self.temp_extern) * (self.room.lenght * self.room.height) /
                                       ((self.room.thickness / self.room.conductivity) + (1 / convection_sides)))

        cdef double convection_upper = 2.0
        cdef double heat_loss_upper = ((self.temp_fluid - self.temp_extern) * (self.room.lenght ** 2) /
                                       ((self.room.thickness / self.room.conductivity) + (1 / convection_upper)))

        cdef double heat_loss_bottom = ((self.temp_fluid - self.temp_extern) * (self.room.lenght ** 2) /
                                        (self.room.thickness / self.room.conductivity))

        cdef double heat_loss = heat_loss_sides + heat_loss_upper + heat_loss_bottom

        return heat_loss

    cpdef void simulate(self, double time_step_pid, double time_step_sim=5e-3, int iters=1):
        cdef double[::1] time = np.append(np.arange(0, time_step_pid, time_step_sim), time_step_pid)
        cdef int i
        cdef double internal_convection
        cdef double temp_heater_aux
        cdef double heat_loss

        for i in range(1, len(time)):
            internal_convection = self.get_convection_coeff()
            temp_heater_aux = self.temp_heater

            for _ in range(iters):
                temp_heater_aux = self.temp_heater + ((self.heater.power - self._flux_heater) * (time[i] - time[i - 1]) /
                                                       (self.heater.mass * self.heater.specific_heat))
                self._flux_heater = self.heater.area * internal_convection * (temp_heater_aux - self.temp_fluid)

            self.temp_heater = temp_heater_aux
            heat_loss = self.heat_loss()
            self.temp_fluid += ((self._flux_heater - heat_loss) * (time[i] - time[i - 1]) /
                                (self.room.volume * self.fluid.density * self.fluid.cp))

            self.temp_fluid += np.random.normal(loc=0.0, scale=self.noise)

    cpdef double get_convection_coeff(self, double gravity=9.81):
        cdef double rayleigh_aux = self.fluid.prandtl * gravity * (self.heater.diameter ** 3)
        cdef double rayleigh = rayleigh_aux * (self.temp_heater - self.temp_fluid) * self.fluid.beta / (self.fluid.viscosity * self.fluid.diffusivity)
        rayleigh = max(0.0, rayleigh)

        cdef double nussel_aux = np.power(1 + np.power(0.559 / self.fluid.prandtl, 9 / 16), 8 / 27)
        cdef double nussel = np.power(0.60 + 0.387 * np.power(rayleigh, 1 / 6) / nussel_aux, 2)
        cdef double convection = self.heater.conductivity * nussel / self.heater.diameter

        return convection
