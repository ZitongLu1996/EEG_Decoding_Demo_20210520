# -*- coding: utf-8

"""
@File       :   cross-temporal_decoding1.py
@Author     :   Zitong Lu
@Contact    :   zitonglu1996@gmail.com
@License    :   MIT License
"""

import scipy.io as sio
import numpy as np

# 被试id
subs = ["201", "202", "203", "204", "205"]

data = np.zeros([5, 640, 27, 500])
label = np.zeros([5, 640])

sub_index = 0
for sub in subs:

    # 加载单个被试的ERP数据
    subdata = sio.loadmat("data/data/ERP" + sub + ".mat")["filtData"]

    # shape of subdata: 640*27*750
    # 640 - 试次数； 27 - 导联； 750 - 时间点  250Hz， 1 - 0.004s  3s [-1.5s至1.5s]

    # -0.5s至1.5s
    subdata = subdata[:, :, 250:]

    sublabel = np.loadtxt("data/labels/ori_" + sub + ".txt")[:, 1]

    data[sub_index] = subdata
    label[sub_index] = sublabel

    sub_index = sub_index + 1

from neurora.decoding import ct_decoding_kfold

accs = ct_decoding_kfold(data, label, n=16, navg=13, time_win=5, time_step=5, nfolds=3, nrepeats=10, smooth=True)

# shape 5* 100 * 100
accs = np.reshape(accs, [5, 10000])
np.savetxt("results4.txt", accs)