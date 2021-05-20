# -*- coding: utf-8

"""
@File       :   time-by-time_decoding.py
@Author     :   Zitong Lu
@Contact    :   zitonglu1996@gmail.com
@License    :   MIT License
"""

import scipy.io as sio
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


# 被试id
subs = ["201", "202", "203", "204", "205"]

accs = np.zeros([5, 5, 100, 100, 3])

sub_index = 0
for sub in subs:

    # 加载单个被试的ERP数据
    subdata = sio.loadmat("data/data/ERP" + sub + ".mat")["filtData"]

    # shape of subdata: 640*27*750
    # 640 - 试次数； 27 - 导联； 750 - 时间点  250Hz， 1 - 0.004s  3s [-1.5s至1.5s]

    # -0.5s至1.5s
    subdata = subdata[:, :, 250:]

    avgt_subdata = np.zeros([640, 27, 100])

    for t in range(100):
        avgt_subdata[:, :, t] = np.average(subdata[:, :, t*5:t*5+5], axis=2)

    # avgt_subdata - 降采样后的数据

    avgt_subdata_16 = np.zeros([16, 40, 27, 100])

    sublabel = np.loadtxt("data/labels/ori_" + sub +".txt")[:, 1]

    index = np.zeros([16], dtype=int)
    for i in range(640):
        labeli = int(sublabel[i])
        avgt_subdata_16[labeli, index[labeli]] = avgt_subdata[i]
        index[labeli] = index[labeli] + 1

    # 迭代5次
    for k in range(5):

        final_subdata = np.zeros([16, 3, 27, 100])
        index_trials = np.array(range(40))
        shuffle = np.random.permutation(index_trials)
        avgt_subdata_16 = avgt_subdata_16[:, shuffle]

        # avgt_subdata_16 : 对同朝向试次打乱之后的数据

        for i in range(3):
            final_subdata[:, i] = np.average(avgt_subdata_16[:, i * 13:i * 13 + 13], axis=1)

        # final_subdata : 同朝向每13个试次进行平均

        final_subdata = np.reshape(final_subdata, [48, 27, 100])
        final_label = np.zeros([16, 3])
        for i in range(16):
            final_label[i] = i
        final_label = np.reshape(final_label, [48])

        # 逐时间点计算
        for t in range(100):
            datat = final_subdata[:, :, t]
            # shape: 48 * 27

            state = np.random.randint(0, 100)
            kf = StratifiedKFold(n_splits=3, shuffle=True, random_state=state)

            fold_index = 0
            # 3-fold
            for train_index, test_index in kf.split(datat, final_label):
                x_train, x_test, y_train, y_test = datat[train_index], datat[test_index], \
                                                   final_label[train_index], final_label[test_index]
                scaler = StandardScaler()
                x_train = scaler.fit_transform(x_train)
                x_test = scaler.transform(x_test)
                # 分类
                svm = SVC(kernel="linear")
                svm.fit(x_train, y_train)
                acc = svm.score(x_test, y_test)
                accs[sub_index, k, t, t, fold_index] = acc

                for tt in range(100):
                    if tt != t:
                        datatt = final_subdata[:, :, tt]
                        acc = svm.score(scaler.transform(datatt[test_index]), y_test)
                        accs[sub_index, k, t, tt, fold_index] = acc

                fold_index = fold_index + 1

                print(sub_index, k, t, t, fold_index, acc)

    sub_index = sub_index + 1

accs = np.average(accs, axis=(1, 4))
# accs shape: 5 * 100 * 100
accs = np.reshape(accs, [5, 10000])
np.savetxt("results2.txt", accs)

