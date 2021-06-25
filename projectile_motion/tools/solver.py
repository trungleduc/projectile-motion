import numpy
import math


class PointMassSolution:
    """Trajectory of a projectile with air resistance.
    Parameters
    ----------
    mass: float
        Mass of projectile (kg)
    k: float
        Friction coefficient
    speed: float
        Launch speed (m/s)
    angle: float
        Launch angle (deg.)
    x0: ndarray
        Initial position (m)
    Outputs
    -------
        Trajectory, speed and acceleration over time
    """

    def __init__(self, mass: float, k: float, speed: float, angle: float, x0=numpy.zeros(3)):
        g = numpy.r_[0, 0, -9.81]
        angle = math.radians(angle)
        if mass <= 0:
            raise ValueError("Mass must be strictly positive")
        x0 = numpy.asarray(x0)
        v0 = numpy.asarray([speed*math.cos(angle), 0., speed*math.sin(angle)])
        g = numpy.asarray(g)
        self.x0 = x0
        if k > 0:
            omega = k / mass
            tau = 1 / omega
            A = g * tau
        else:
            omega, tau = 0, numpy.inf
            A = numpy.full_like(g, numpy.inf)
        B = v0 - A

        def x_impl(t):
            wt = omega * t
            if wt < 1e-7:  # asymptotic expansion, to avoid exp overflow
                x = x0 + v0 * t + (0.5 * t) * (g * t - wt * v0) * (1 - wt / 3 * (1 - 0.25 * wt))
            else:
                x = x0 + A * t + B * tau * (1 - numpy.exp(-wt))
            return x

        def v_impl(t):
            wt = omega * t
            if wt < 1e-7:  # asymptotic expansion, to avoid exp overflow
                v = v0 + (g * t - v0 * wt) * (1 - wt * (0.5 - wt / 6))
            else:
                v = A + B * numpy.exp(-wt)
            return v
        self.__x = x_impl
        self.__v = v_impl
        self.__a = lambda t: g - self.__v(t) * omega
        self.__omega = omega

    @property
    def omega(self):
        return self.__omega

    def a(self, t):
        return self.__a(t)

    def v(self, t):
        return self.__v(t)

    def x(self, t):
        return self.__x(t)

    def position(self):
        time_step = 0.01
        t = 0.
        position = [[], []]
        speed = [[], []]
        acceleration = [[], []]
        height = self.x0[2]
        time_step_list = []
        while True:
            current_pos = self.x(t)
            spd = self.v(t)
            acc = self.a(t)
            height = current_pos[2]
            if height < 0:
                break
            else:
                position[0].append(current_pos[0])
                position[1].append(current_pos[2])
                speed[0].append(spd[0])
                speed[1].append(spd[2])
                acceleration[0].append(acc[0])
                acceleration[1].append(acc[2])
                time_step_list.append(t)
                t += time_step

        return numpy.array(position), numpy.array(speed), numpy.array(acceleration), numpy.array(time_step_list), t
