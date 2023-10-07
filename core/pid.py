import numpy as np


class ControlPID:
    def __init__(self, system, kp, ki, kd, range, noise=0):
        self.system = system
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.range = range
        self.noise = noise

        self._last = system.current(0)
        self._intr = 0

    def iterate(self, target, time_step):
        current = self.system.current(time_step)
        current += np.random.normal(loc=0.0, scale=self.noise)

        dist = current - target

        # Integral using trapezoidal rule.
        # Assumes the target didnt changed since the last iteration.
        self._intr += 0.5 * (current - self._last) * time_step

        diff = (current - self._last) / time_step

        self._last = current

        pwm_prop = self.kp(dist, self._intr, diff) * dist
        pwm_intr = self.ki(dist, self._intr, diff) * self._intr
        pwm_diff = self.kd(dist, self._intr, diff) * diff

        pwm = pwm_prop + pwm_intr + pwm_diff
        pwm = self.range[0] if pwm < self.range[0] else pwm
        pwm = self.range[1] if pwm > self.range[1] else pwm

        return pwm, (pwm_prop, pwm_intr, pwm_diff)
