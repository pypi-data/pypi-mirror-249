# from macronpy.macro import *
#%%导入包
import pandas as pd
from pandas.core.base import PandasObject #用于为pandas增加函数

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option('plotting.backend', 'plotly')
from pandas.tseries.offsets import MonthEnd
from pandas.tseries.offsets import QuarterEnd
import numpy as np
from numpy import nan as NA
import re
import datetime

import warnings
warnings.filterwarnings("ignore")

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#数据库
# import cx_Oracle

#数据框交互
# import qgrid
# PandasObject.show_grid = qgrid.show_grid

from sklearn.decomposition import PCA

import statsmodels.api as sm
from statsmodels.formula.api import ols #加载ols模型
from statsmodels.api import tsa #时间序列分析

# 插值模块
import scipy.interpolate as sci
from scipy.interpolate import interp1d#!!!
#信号处理
import scipy.signal as signal
#统计运算
from scipy.stats.mstats import gmean
#规划
import scipy.optimize as sco
#线性代数
from scipy import linalg

#机器学习的回归
from sklearn.linear_model import LinearRegression

#引入凸规划的包
from cvxopt import matrix, solvers

#风险收益业绩评价
import empyrical

# 迭代器
import itertools

#循环加进度条
from tqdm import tqdm

# # 万得
# from WindPy import *
# # w.stop();
# w.start()


# 随机数
import random
# stata
# import ipystata
#小波分析库
import pywt

#functools，主要是用reduce
from functools import reduce

#优势分析相关的包
# from dominance_analysis import Dominance
#%%默认日期
# global start
# start_date='2005-01-01'
# global end
# end_date=str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
cd=os.getcwd()

#HP滤波
from statsmodels.tsa.filters.hp_filter import hpfilter
from statsmodels.tsa.filters.bk_filter import bkfilter

import statsmodels.formula.api as smf
#最卷pandas可视化工具！！！！！！！！！！！！！！！！没有之一
# import dtale

# import talib
import calendar

# import modin
import sqlite3

from lunardate import LunarDate

# import backtrader as bt

#美联储数据库
from fredapi import Fred
