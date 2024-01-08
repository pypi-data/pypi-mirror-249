import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import pandas as pd
from jgtpy.JGTADS import plot_from_cds_df

from jgtpy.JGTChartConfig import JGTChartConfig


class Chart:
    def __init__(
        self,
        data,
        instrument,
        timeframe,
        show=True,
        plot_ao_peaks=True,
        cc=None,
    ):
        if cc is None:
            cc = JGTChartConfig()
        if nb_bar_on_chart == -1:
            nb_bar_on_chart = cc.nb_bar_on_chart

        self.fig, self.axes.self.cdf = plot_from_cds_df(
            data, instrument, timeframe, show=show, plot_ao_peaks=plot_ao_peaks, cc=cc
        )

    def get_jaw_plot(self):
        return self.fig.axes[0].lines[0]

    def get_teeth_plot(self):
        return self.fig.axes[0].lines[1]

    def get_lips_plot(self):
        return self.fig.axes[0].lines[2]

    def get_fractal_up_plot(self):
        return self.fig.axes[0].scatter(
            [], [], marker="^", c=cc.fractal_up_color, s=cc.fractal_marker_size
        )[0]

    def get_fractal_down_plot(self):
        return self.fig.axes[0].scatter(
            [], [], marker="v", c=cc.fractal_dn_color, s=cc.fractal_marker_size
        )[0]

    def get_fractal_up_plot_higher(self):
        return self.fig.axes[0].scatter(
            [],
            [],
            marker="^",
            c=cc.fractal_up_color_higher,
            s=cc.fractal_degreehigher_marker_size,
        )[0]

    def get_fractal_down_plot_higher(self):
        return self.fig.axes[0].scatter(
            [],
            [],
            marker="v",
            c=cc.fractal_dn_color_higher,
            s=cc.fractal_degreehigher_marker_size,
        )[0]

    def get_fdbb_up_plot(self):
        return self.fig.axes[0].scatter(
            [],
            [],
            marker=cc.fdb_signal_marker,
            c=cc.fdb_signal_buy_color,
            s=cc.fdb_marker_size,
        )[0]

    def get_fdbs_down_plot(self):
        return self.fig.axes[0].scatter(
            [],
            [],
            marker=cc.fdb_signal_marker,
            c=cc.fdb_signal_sell_color,
            s=cc.fdb_marker_size,
        )[0]

    def get_sb_plot(self):
        return self.fig.axes[1].scatter(
            [],
            [],
            marker=cc.saucer_marker,
            c=cc.saucer_buy_color,
            s=cc.saucer_marker_size,
        )[0]

    def get_ss_plot(self):
        return self.fig.axes[1].scatter(
            [],
            [],
            marker=cc.saucer_marker,
            c=cc.saucer_sell_color,
            s=cc.saucer_marker_size,
        )[0]

    def get_ao_plot(self):
        return self.fig.axes[1].lines[0]

    def get_ac_plot(self):
        return self.fig.axes[2].lines[0]

    def get_acs_plot(self):
        return self.fig.axes[2].scatter(
            [],
            [],
            marker=cc.ac_signal_marker,
            c=cc.ac_signal_sell_color,
            s=cc.ac_signals_marker_size,
        )[0]

    def get_acb_plot(self):
        return self.fig.axes[2].scatter(
            [],
            [],
            marker=cc.ac_signal_marker,
            c=cc.ac_signal_buy_color,
            s=cc.ac_signals_marker_size,
        )[0]
