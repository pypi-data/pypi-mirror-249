# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/27 20:27
@Author  : Jicong Hu
@FileName: sector_alpha_preprocess_operations.py
@Software: PyCharm

@Description:
Preprocessing Operations needed to be done to raw alpha
alpha data should be one of followed:
    1.  named as alpha_frame, typed as pivot pd.DataFrame with stock symbol as columns and date as index
    2.  named as alpha_sheet, typed as stack pd.DataFrame with attribute(at least three, e.g. stock_code, signal_date,
    alpha_value) as columns.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import warnings

warnings.filterwarnings('ignore')

_function_list = {
    'frame_to_sheet':           '将因子数据由alpha_frame转为alpha_sheet',
    'sheet_to_frame':           '将因子数据由alpha_sheet转为alpha_frame',
    'outlier_mad':              '极值处理（3倍MAD法）',
    'outlier_winsor':           '极值处理（分位数剪枝）',
    'alpha_zscorelized':        '正态标准化',
    'alpha_standardization':    '因子数据标准化（可选择是否行业中性，暂不做风格中性）',
    'alpha_neutral':            '因子数据风格中性化（截面回归取残差，默认风格因子已标准化）'
}


# 显示该文件所涉及的所有函数方法
def show_functions():
    for func in _function_list:
        print(func)


# 将因子数据由alpha_frame转为alpha_sheet
def frame_to_sheet(alpha_frame):
    stacked_alpha = alpha_frame.stack().reset_index()
    stacked_alpha.columns = ['signal_date', 'stock_code', 'alpha_value']
    return stacked_alpha.rename(columns={0: 'alpha_value'})


# 将因子数据由alpha_sheet转为alpha_frame
def sheet_to_frame(alpha_sheet):
    sheet_to_process = alpha_sheet[['stock_code', 'signal_date', 'alpha_value']].drop_duplicates(
        subset=['stock_code', 'signal_date'])
    return sheet_to_process.pivot(index='signal_date', columns='stock_code', values='alpha_value')


# 极值处理（3倍MAD法）
def outlier_mad(grouped_in_series):
    """
    outlier process, it should be used after the groupby method, on a groupby alpha_value
    :param grouped_in_series:
    :return:
    """
    median = grouped_in_series.median()
    mad = (grouped_in_series - median).abs().median()
    upper_bound = median + 3 * 1.4826 * mad
    lower_bound = median - 3 * 1.4826 * mad
    grouped_in_series[grouped_in_series > upper_bound] = upper_bound
    grouped_in_series[grouped_in_series < lower_bound] = lower_bound
    return grouped_in_series


# 极值处理（分位数剪枝）
def outlier_winsor(grouped_in_series):
    upper_bound = np.nanpercentile(grouped_in_series, 95)
    lower_bound = np.nanpercentile(grouped_in_series, 5)
    grouped_in_series[grouped_in_series > upper_bound] = upper_bound
    grouped_in_series[grouped_in_series < lower_bound] = lower_bound
    return grouped_in_series


# 正态标准化
def alpha_zscorelized(grouped_in_series):
    return (grouped_in_series - grouped_in_series.mean()) / grouped_in_series.std()


# 因子数据标准化（暂不做风格中性）
def alpha_standardization(alpha_sheet):
    sheet_standardized = alpha_sheet[['stock_code', 'signal_date', 'alpha_value']]
    groupby_set = ['signal_date']
    sheet_standardized['alpha_value'] = sheet_standardized.groupby(groupby_set).alpha_value.apply(outlier_mad)
    sheet_standardized['alpha_value'] = sheet_standardized.groupby(groupby_set).alpha_value.apply(alpha_zscorelized)
    sheet_standardized['alpha_value'] = sheet_standardized.alpha_value.fillna(0)
    return sheet_standardized


# 因子数据风格中性化（截面回归取残差，默认风格因子已标准化）
def alpha_neutral(standardized_alpha_sheet, *style_factors_sheet):
    regre_data = standardized_alpha_sheet.copy()
    for correlated_factor in style_factors_sheet:
        merged_on = ['stock_code', 'signal_date']
        correlated_factor_copy = correlated_factor.drop_duplicates().dropna()
        regre_data = pd.merge(regre_data, correlated_factor_copy, how='left', on=merged_on)
        regre_data = regre_data.fillna(0)

    def neutralize(alphas_sheet):
        y = alphas_sheet['alpha_value'].values
        x = alphas_sheet.drop(['stock_code', 'alpha_value'], axis=1).values
        alphas_sheet['alpha_value'] = sm.OLS(y, x).fit().resid
        return alphas_sheet

    regre_data = pd.concat([regre_data['signal_date'], regre_data.groupby('signal_date').apply(neutralize)], axis=1)
    factor_neutralized = regre_data[['stock_code', 'signal_date', 'alpha_value']]
    return factor_neutralized
