# -*- coding: utf-8

"""
@File       :   plot_cross-temporal_accs.py
@Author     :   Zitong Lu
@Contact    :   zitonglu1996@gmail.com
@License    :   MIT License
"""

from neurora.rsa_plot import plot_ct_decoding_acc
import numpy as np

accs = np.loadtxt("results2.txt")
accs = np.reshape(accs, [5, 100, 100])

plot_ct_decoding_acc(accs, start_timex=-0.5, end_timex=1.5, start_timey=-0.5, end_timey=1.5, time_intervalx=0.02,
                         time_intervaly=0.02, chance=0.0625, p=0.05, cbpt=False, stats_timex=[0.2, 1.5], stats_timey=[0.2, 1.5],
                         xlim=[-0.5, 1.5], ylim=[-0.5, 1.5], clim=[0.06, 0.08], figsize=[6.4, 4.8], cmap="viridis", fontsize=16)