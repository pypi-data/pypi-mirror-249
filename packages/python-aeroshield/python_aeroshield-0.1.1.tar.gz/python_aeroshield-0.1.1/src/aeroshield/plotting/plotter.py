import numpy as np

from matplotlib import pyplot as plt


class Plotter:
    def __init__(self) -> None:
        self._create_empty_figure()

    def _create_empty_figure(self):
        self.fig, self.ax = plt.subplots(ncols=1, nrows=3, sharex=True)

        self.ref_line = self.ax[0].plot(0, 0, label="reference", linestyle="--", color="k")[0]
        self.angle_line = self.ax[0].plot(0, 0, label="angle")[0]
        self.ax[0].legend()
        self.ax[0].set_title("Reference tracking")
        self.ax[0].set_ylabel(r"Angle [$\degree$]")
        self.ax[0].grid(True)

        self.motor_line = self.ax[1].plot(0, 0, label="motor input")[0]
        self.ax[1].set_title("Motor Input")
        self.ax[1].set_ylabel("8-bit input value [-]")
        self.ax[1].grid(True)

        self.dt_line = self.ax[2].plot(0, 0, label="dt")[0]
        self.ax[2].set_title("Time steps")
        self.ax[2].set_xlabel("Time [s]")
        self.ax[2].set_ylabel("dt [ms]")
        self.ax[2].grid(True)

    def plot_hist(self, hist):
        self.ref_line.set_data(hist[:, 0], hist[:, 1])
        self.angle_line.set_data(hist[:, 0], hist[:, 2])
        self.ax[0].relim()
        self.ax[0].autoscale_view()

        self.motor_line.set_data(hist[:, 0], hist[:, 3])
        self.ax[1].relim()
        self.ax[1].autoscale_view()

        self.dt_line.set_data(hist[:, 0], 1000*np.gradient(hist[:, 0]))
        self.ax[2].relim()
        self.ax[2].autoscale_view()

        return self.fig, self.ax
