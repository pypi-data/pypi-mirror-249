import numpy as np

from matplotlib import pyplot as plt
from multiprocessing import Pipe, Process

from .plotter import Plotter


class LivePlotter(Plotter):
    def __init__(self, data_points, max_time) -> None:
        super().__init__()

        self.fig.canvas.mpl_connect("close_event", self.close)

        self.ax[0].set_xlim(-.05, 1.01*max_time)
        self.ax[0].set_ylim(-5, 180)
        self.ax[1].set_xlim(-.05, 1.01*max_time)
        self.ax[1].set_ylim(-5, 260)
        self.ax[2].set_xlim(-.05, 1.01*max_time)
        self.ax[2].set_ylim(4.95, 10)

        self.receiving_conn, self.sending_conn = Pipe(duplex=False)
        self.data_length = data_points
        self.cntr = 0

        self.t_data = np.zeros(self.data_length)
        self.ref_data = np.zeros(self.data_length)
        self.angle_data = np.zeros(self.data_length)
        self.motor_data = np.zeros(self.data_length)

        self.terminate = False

    def add_data_to_queue(self, t, ref, angle, motor):
        self.sending_conn.send((t, ref, angle, motor))

    def get_data_from_queue(self):
        done = False
        while not done:
            if self.receiving_conn.poll():
                data = self.receiving_conn.recv()
                if data[0] == -1:
                    self.terminate = True

                else:
                    self.t_data[self.cntr], self.ref_data[self.cntr], self.angle_data[self.cntr], self.motor_data[self.cntr] = data

                self.cntr += 1

            else:
                done = True

    def get_process(self):
        return Process(target=self.run, daemon=True)

    def run(self):
        self.terminate = False

        while not self.terminate:
            self.get_data_from_queue()

            if self.cntr > 0:
                self.ref_line.set_data(self.t_data[:self.cntr], self.ref_data[:self.cntr])
                self.angle_line.set_data(self.t_data[:self.cntr], self.angle_data[:self.cntr])
                self.motor_line.set_data(self.t_data[:self.cntr], self.motor_data[:self.cntr])
                self.dt_line.set_data(self.t_data[:self.cntr], 1000*np.gradient(self.t_data[:self.cntr]))

            self.fig.canvas.draw()

            plt.pause(1/60)

        plt.close(self.fig)

    def close(self, event):
        self.terminate = True
        plt.close(self.fig)
