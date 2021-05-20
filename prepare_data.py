# -*- coding: utf-8

"""
@File       :   prepare_data.py
@Author     :   Zitong Lu
@Contact    :   zitonglu1996@gmail.com
@License    :   MIT License
"""

import os
from six.moves import urllib
from pyctrsa.util.download_data import schedule
from pyctrsa.util.unzip_data import unzipfile
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 数据下载地址（一个压缩包，包含5个被试的数据+标签文件）
url = 'https://attachment.zhaokuangshi.cn/BaeLuck_2018jn_data_ERP_5subs.zip'
# 压缩包文件名
filename = 'BaeLuck_2018jn_data_ERP_5subs.zip'
# 压缩包保存地址
data_dir = 'data/'
# 完整压缩包地址
filepath = data_dir + filename

# 下载压缩包
exist = os.path.exists(filepath)
if exist == False:
    os.makedirs(data_dir)
    urllib.request.urlretrieve(url, filepath, schedule)
    print('Download completes!')
elif exist == True:
    print('Data already exists!')

# 解压压缩包
unzipfile(filepath, data_dir)