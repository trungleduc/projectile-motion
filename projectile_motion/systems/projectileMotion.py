from cosapp.systems import System
import numpy
from projectile_motion.tools import PointMassSolution


class ProjectileMotion(System):

    def setup(self):
        self.add_inward("mass", value=1.5, unit="kg", dtype=float, desc="Mass of projectile", limits=[0, 10])
        self.add_inward("k", value=0.0, dtype=float, desc="Friction coefficient", limits=[0, 1])
        self.add_inward("angle", value=50., dtype=float, desc="Launch angle", limits=[0, 90])
        self.add_inward("speed", value=12.5, unit="m/s", dtype=float, desc="Launch speed", limits=[0, 20])

        self.add_outward("coordinate", numpy.zeros(0),  desc="Coordinate of projectile")
        self.add_outward("spd",  numpy.zeros(0), desc="Speed of projectile")
        self.add_outward("acc",  numpy.zeros(0), desc="Acceleration of projectile")
        self.add_outward("time_step",  numpy.zeros(0), desc="Time step")
        self.add_outward("total_time", 0, desc="Total time")

    def compute(self):
        solution = PointMassSolution(mass=self.mass, k=self.k, speed=self.speed, angle=self.angle, x0=[0., 0., 0.])
        self.coordinate, self.spd, self.acc, self.time_step, self.total_time = solution.position()
