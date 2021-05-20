# -*- coding: utf-8

"""
@File       :   plot_time-by-time_accs.py
@Author     :   Zitong Lu
@Contact    :   zitonglu1996@gmail.com
@License    :   MIT License
"""

from neurora.rsa_plot import plot_tbyt_decoding_acc
import numpy as np

accs = np.loadtxt("results3.txt")

plot_tbyt_decoding_acc(accs, start_time=-0.5, end_time=1.5, time_interval=0.02, chance=0.0625, p=0.05, cbpt=False,
                           stats_time=[0.2, 1.5], color='r', xlim=[-0.5, 1.5], ylim=[0.05, 0.15], figsize=[6.4, 3.6], x0=0,
                           fontsize=16, avgshow=False)