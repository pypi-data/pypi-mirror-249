import numpy as np
import time

from typing import Optional, Iterable

from .aeroshield import AeroShield
from .plotting import LivePlotter


class AeroController:
    def __init__(self, aero_shield:AeroShield) -> None:
        self.aero_shield = aero_shield

    def controller(self, t: float, dt: float, ref: float, pot: float, angle: float) -> tuple[float]:
        """Implement the controller here. You can subclass AeroController and overwrite the controller.

        :param t: Time since start of run in seconds.
        :type t: float
        :param dt: Length of current time step in seconds.
        :type dt: float
        :param ref: reference value for the current step.
        :type ref: float
        :param pot: potentiometer value in percent.
        :type pot: float
        :param angle: calibrated angle in degrees.
        :type angle: float
        :return: input value for motor. the motor value will be saturated (int between 0 and 255 incl.) afterwards
        :rtype: float
        """

        return 0  # motor value

    def run(self, freq: int, duration: float|int, ref: Optional[Iterable[float|int]]=None, live_plot: bool=False):
        """Run the controller on the AeroShield.

        :param freq: Desired frequency of the loop.
        :type freq: int
        :param duration: Duration of the run in seconds.
        :type duration: float | int
        :param ref: The reference to follow should have a lenght equal to freq * time.
        :type ref: np.ndarray[float|int]
        """
        cntr = 0
        maxcntr = int(duration*freq)
        period = 1/freq

        # t1 - tstart, ref, angle, motor
        hist = np.zeros((maxcntr, 4))

        if ref is None:
            ref = np.zeros(maxcntr)

        if live_plot:
            plotter = LivePlotter(maxcntr, duration)
            plot_process = plotter.get_process()
            plot_process.start()

        with self.aero_shield as shield:

            shield.write(shield.RUN, 0)

            tstart = time.perf_counter()
            t0 = t1 = tstart

            done = False
            while not done:
                try:
                    print(f"\r{cntr}", end="")

                    while (t1 - t0) < period:
                        t1 = time.perf_counter()

                    dt = t1 - t0
                    t0 = t1

                    pot, angle = shield.read()
                    u = self.controller(t1 - tstart, dt, ref[cntr], pot, angle)
                    motor = shield.write(shield.RUN, u)

                    hist[cntr] = t1 - tstart, ref[cntr], angle, motor
                    if live_plot:
                        plotter.add_data_to_queue(t1 - tstart, ref[cntr], angle, motor)

                    cntr += 1
                    if cntr == maxcntr:
                        done = True

                except KeyboardInterrupt:
                    done = True

            print()

        # signals to terminate live plot
        if live_plot:
            plotter.add_data_to_queue(-1, -1, -1, -1)
            plot_process.join()

        return hist
