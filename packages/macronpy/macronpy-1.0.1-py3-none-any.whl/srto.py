# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/27 13:21
@Author  : Jicong Hu
@FileName: sector_rotation_test_operations.py
@Software: PyCharm

@Description:
With assumption that pre-processed alpha data is valid, and other data could be fetched.
alpha data should be one of followed:
    1.  named as alpha_frame, typed as pivot pd.DataFrame with stock symbol as columns and date as index
    2.  named as alpha_sheet, typed as stack pd.DataFrame with attribute(at least three, e.g. stock_code, signal_date, alpha_value) as columns.
close data should be one of followed:
    1.  named as close_frame, typed as pivot pd.DataFrame with stock symbol as columns and date as index
signal date data should be list-like(list, pd.Series)
"""
from macronpy.sapo import sheet_to_frame
# from strateval.sector_alpha_preprocess_operations import sheet_to_frame
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

_function_list = {
    'alpha_description':                '构建因子描述文件序列',
    'close_to_return':                  '日频收盘价序列转化为所需收益率数据',
    'get_ic_series_from_frame':         '单因子ic序列(alpha_frame版)',
    'get_ic_series_from_sheet':         '单因子ic序列(alpha_sheet版)',
    'ic_series_stats':                  '输出单因子ic序列统计特征',
    'ic_decay_series':                  '计算ic衰减序列',
    'add_group_tag':                    '按因子值大小进行分组',
    'folio_position_from_frame':        '基于因子数据（frame）构建持仓初始数据',
    'folio_net_value':                  '基于已有持仓数据计算净值',
    'alpha_portfolio_group_test':       '组合分组测试净值',
    'relative_nav_test':                '多头组合、空头组合、多空组合&相对等权基准超额净值 与 多头换手序列',
    'nav_performance':                  '计算净值统计数据',
    'performance_by_year':              '净值数据分年度统计'
}


# 显示该文件所涉及的所有函数方法
def show_functions():
    for func in _function_list:
        print(func)


# 构建因子描述文件序列
def alpha_description(alpha_sheet):
    description = alpha_sheet.groupby('signal_date').alpha_value.describe()
    return description


# 日频收盘价序列转化为所需收益率数据
def close_to_return(close_frame, signal_date_list=None):
    if signal_date_list is None:
        return close_frame / close_frame.shift(1) - 1
    else:
        specific_close = close_frame.loc[signal_date_list]
        return specific_close / specific_close.shift(1) - 1


# 单因子ic序列(alpha_frame版)
def get_ic_series_from_frame(alpha_frame, return_frame, is_rank_ic=False):
    shifted_alpha = alpha_frame.loc[return_frame.index.intersection(alpha_frame.index)].shift(1)
    if is_rank_ic:
        ic_series = return_frame.corrwith(shifted_alpha, axis=1, method='spearman')
    else:
        ic_series = return_frame.corrwith(shifted_alpha, axis=1)
    return ic_series

#自定义的ic计算函数！
def factor_ic_cal(factor_long_data, match_price_wide_data, factor_date_name, factor_asset_name, factor_name,
                  is_rank_ic=True):
    '''
    计算因子的ic
    返回值：index为因子频率的日期、columns为 'rank_ic','rank_ic_cum' 或者 'ic','ic_cum'的数据框
    factor_long_data：因子的sql结构数据
    match_price_wide_data：依照因子里的资产提取的资产价格数据框，二维宽表
    factor_date_name,factor_asset_name,factor_name：因子sql结构数据的三要素列名
    '''
    factor_dataset = factor_long_data.copy()
    price_dataset = match_price_wide_data.copy()
    # if len(list(set(factor_dataset[factor_date_name]))[0]) == 8:
    if len(str(list(set(factor_dataset[factor_date_name])))[0]) == 8:
        factor_dataset.long2dt(factor_date_name, inplace=True)

    factor_wide_data = factor_dataset.pivot_table(factor_name, factor_date_name, factor_asset_name, 'sum')
    col_intersection = price_dataset.columns.intersection(factor_wide_data.columns)
    price_dataset = price_dataset[col_intersection]
    factor_wide_data = factor_wide_data[col_intersection]
    factor_wide_data=factor_wide_data.date_index()

    ic = get_ic_series_from_frame(factor_wide_data, price_dataset.pct(), True).to_frame()
    # display(ic.iloc[-5:,-5:])
    ic_sum = ic.cumsum()
    ic_data = ic.mg(ic_sum)

    if is_rank_ic:
        ic_data.columns = ['rank_ic', 'rank_ic_cum']
    else:
        ic_data.columns = ['ic', 'ic_cum']

    return ic_data
def factor_ic_decay(factor_long_data, match_price_wide_data, factor_date_name, factor_asset_name, factor_name,
                  is_rank_ic=True):
    '''
    计算因子的ic衰减序列
    返回值：
    factor_long_data：因子的sql结构数据
    match_price_wide_data：依照因子里的资产提取的资产价格数据框，二维宽表
    factor_date_name,factor_asset_name,factor_name：因子sql结构数据的三要素列名
    '''
    factor_dataset = factor_long_data.copy()
    price_dataset = match_price_wide_data.copy()
    # if len(list(set(factor_dataset[factor_date_name]))[0]) == 8:
    if len(str(list(set(factor_dataset[factor_date_name])))[0]) == 8:
        factor_dataset.long2dt(factor_date_name, inplace=True)

    factor_wide_data = factor_dataset.pivot_table(factor_name, factor_date_name, factor_asset_name, 'sum')
    col_intersection = price_dataset.columns.intersection(factor_wide_data.columns)
    price_dataset = price_dataset[col_intersection]
    factor_wide_data = factor_wide_data[col_intersection]
    factor_wide_data=factor_wide_data.date_index()

    ic_decay= ic_decay_series_from_frame(factor_wide_data, price_dataset.pct(), True).to_frame()

    return ic_decay

# 单因子ic序列(alpha_sheet版）
def get_ic_series_from_sheet(alpha_sheet, return_frame, is_rank_ic=False):
    alpha_frame = sheet_to_frame(alpha_sheet)
    return get_ic_series_from_frame(alpha_frame, return_frame, is_rank_ic)


# 输出单因子ic序列统计特征
def ic_series_stats(ic_series):
    ic_count = ic_series.count()
    ic_mean = ic_series.mean()
    ic_std = ic_series.std()
    icir = abs(ic_mean / ic_std)
    ic_positive_rate = 0.5 * (np.sign(ic_series).mean() + 1)
    ic_stats = pd.Series([ic_count, ic_mean, ic_std, icir, ic_positive_rate],
                         index=['sample_num', 'ic_mean', 'ic_std', 'icir', 'positive_rate'])
    return ic_stats

# 自定义的单因子ic序列统计特征！
def ic_df_stats(ic_df):
    '''
    ic_df是数据框，是factor_ic_cal的返回结果
    '''
    try:
        ic_series=ic_df[['ic']]
        tag='ic'
    except:
        ic_series=ic_df[['rank_ic']]
        tag='rank_ic'
    ic_count = ic_series.count()
    ic_mean = ic_series.mean()
    ic_std = ic_series.std()
    icir = abs(ic_mean / ic_std)
    ic_positive_rate = 0.5 * (np.sign(ic_series).mean() + 1)
    ic_stats = pd.Series([ic_count.values[0], ic_mean.values[0], ic_std.values[0], icir.values[0], ic_positive_rate.values[0]],
                         index=['sample_num', 'ic_mean', 'ic_std', 'icir', 'positive_rate'])
    return ic_stats.to_frame().col(tag+'_stats').round(3)


# 计算ic衰减序列
def ic_decay_series(alpha_sheet, return_frame, decay_period=12, is_rank_ic=False):
    alpha_frame = sheet_to_frame(alpha_sheet).loc[return_frame.index.intersection(sheet_to_frame(alpha_sheet).index)]
    if is_rank_ic:
        ic_series_list = [return_frame.corrwith(alpha_frame.shift(x), axis=1, method='spearman') for x in range(1, decay_period+1)]
    else:
        ic_series_list = [return_frame.corrwith(alpha_frame.shift(x), axis=1, method='pearson') for x in range(1, decay_period + 1)]
    ic_frame = pd.DataFrame(ic_series_list, index=range(1, decay_period + 1)).T
    return ic_frame
def ic_decay_series_from_frame(alpha_frame, return_frame, decay_period=12, is_rank_ic=False):
    alphaframe = alpha_frame.loc[return_frame.index.intersection(sheet_to_frame(alpha_sheet).index)]
    # alpha_frame = sheet_to_frame(alpha_sheet).loc[return_frame.index.intersection(sheet_to_frame(alpha_sheet).index)]
    if is_rank_ic:
        ic_series_list = [return_frame.corrwith(alphaframe.shift(x), axis=1, method='spearman') for x in range(1, decay_period+1)]
    else:
        ic_series_list = [return_frame.corrwith(alphaframe.shift(x), axis=1, method='pearson') for x in range(1, decay_period + 1)]
    ic_frame = pd.DataFrame(ic_series_list, index=range(1, decay_period + 1)).T
    return ic_frame

# 计算与其它因子的截面相关性
def cross_section_corr(alpha_sheet, *other_factors_sheet):
    dropped_labels = alpha_sheet.columns.drop(['stock_code', 'signal_date'])

    def one_period_cross_section_corr(groupin_data):
        groupin_frame = groupin_data.set_index('stock_code')
        groupin_alpha = groupin_frame.alpha_value
        groupin_factors = groupin_frame.drop(dropped_labels, axis=1)
        one_period_corr = groupin_factors.apply(lambda x: x.corr(groupin_alpha))
        return one_period_corr

    multi_factors = alpha_sheet.copy()
    for other_factor in other_factors_sheet:
        multi_factors = multi_factors.merge(other_factor, on=['signal_date', 'stock_code'], how='left')
    return multi_factors.groupby('signal_date').apply(one_period_cross_section_corr).mean()


# 计算与其它因子的IC相关性
def ic_corr(ic_series, return_frame, *other_factors_sheet):
    def get_factor_ic(other_factor):
        factor_name = other_factor.columns.drop(['stock_code', 'signal_date'])[-1]
        factor_copy = other_factor.rename(columns={factor_name: 'alpha_value'})
        factor_ic = get_ic_series_from_sheet(factor_copy, return_frame, False)
        factor_ic.name = factor_name
        return factor_ic
    ic_list = [get_factor_ic(x) for x in other_factors_sheet]
    ic_list = [x * np.sign(x.mean()) for x in ic_list]
    ic_frame = pd.concat(ic_list, axis=1)
    corr_series = ic_frame.apply(lambda x: x.corr(ic_series))
    return corr_series


# 按因子值大小进行分组
def add_group_tag(alpha_sheet, total_group_num):
    grouped_alpha_sheet = alpha_sheet.copy()
    grouped_alpha_sheet['rank'] = grouped_alpha_sheet.groupby(['signal_date']).alpha_value.rank(pct=True)
    grouped_alpha_sheet['group'] = np.searchsorted(
        [1. / total_group_num * x + 1e-4 for x in range(1, total_group_num)], grouped_alpha_sheet['rank'])
    return grouped_alpha_sheet


# 按因子值大小挑选排名靠前的进行打标签
def add_rank_tag(alpha_sheet, total_pick_num):
    grouped_alpha_sheet = alpha_sheet.copy()
    grouped_alpha_sheet['rank'] = grouped_alpha_sheet.groupby(['signal_date']).alpha_value.rank(ascending=False)
    return grouped_alpha_sheet[grouped_alpha_sheet['rank'] <= total_pick_num]


# 基于因子数据（frame）构建持仓初始数据
def folio_position_from_frame(alpha_frame):
    holding_status = alpha_frame / alpha_frame
    holding_status = (holding_status.T / holding_status.sum(axis=1)).T
    return holding_status


# 基于已有持仓数据计算净值
def folio_net_value(position_frame, daily_return_frame, cost):
    first_holding = position_frame.dropna(how='all').index[0]
    net_value_frame = position_frame.loc[first_holding:].fillna(0)
    trade_made = net_value_frame.sum(axis=1).to_list()
    previous_index = None
    net_value_list = []
    turnover_list = []
    for index_num in range(len(net_value_frame)):
        current_index = net_value_frame.index[index_num]
        if trade_made[index_num] > 0:
            if previous_index is None:
                net_value_list.append(net_value_frame.loc[current_index] * (1 - cost))
                current_turnover = 1
            else:
                previous_net_value = net_value_list[-1]
                current_net_value = net_value_frame.loc[current_index]
                current_cost = np.abs(
                    previous_net_value - previous_net_value.sum() * current_net_value) * cost
                net_value_list.append((previous_net_value.sum() - current_cost.sum()) * current_net_value *
                                      (1 + daily_return_frame.loc[current_index]))
                current_turnover = np.abs(previous_net_value / previous_net_value.sum() - current_net_value).sum()
            turnover_list.append([current_index, current_turnover])
        else:
            net_value_list.append(np.multiply(net_value_list[-1], (1 + daily_return_frame.loc[current_index])))
        previous_index = current_index
    net_value_frame = pd.DataFrame(net_value_list, index=net_value_frame.index)
    portfolio_net_value = net_value_frame.sum(axis=1)
    return portfolio_net_value, \
           pd.DataFrame(turnover_list, columns=['trade_made', 'turnover']).set_index('trade_made').turnover


# 组合分组测试净值
def alpha_portfolio_group_test(grouped_alpha_sheet, close_frame):
    daily_return_frame = close_to_return(close_frame)

    def process_grouped_frame(groupin_sheet):
        groupin_frame = sheet_to_frame(groupin_sheet)
        groupin_position = folio_position_from_frame(groupin_frame)
        index_end = min(groupin_position.index.max(), daily_return_frame.index.max())
        daily_holding = pd.DataFrame(index=daily_return_frame.loc[:index_end].index, columns=daily_return_frame.columns)
        daily_holding.update(groupin_position)
        daily_holding = daily_holding.shift(1)
        net_value, turnover = folio_net_value(daily_holding, daily_return_frame, 0.0)
        return net_value

    group_folio = grouped_alpha_sheet.groupby(['group']).apply(process_grouped_frame)
    return group_folio.T


# 多头组合、空头组合、多空组合&相对等权基准超额净值 与 多头换手序列
def relative_nav_test(grouped_alpha_sheet, close_frame, signal_direction=1):
    daily_return_frame = close_to_return(close_frame)
    max_group = grouped_alpha_sheet.group.max()

    def process_grouped_frame(groupin_sheet):
        groupin_frame = sheet_to_frame(groupin_sheet)
        groupin_position = folio_position_from_frame(groupin_frame)
        daily_holding = pd.DataFrame(index=daily_return_frame.index, columns=daily_return_frame.columns)
        daily_holding.update(groupin_position)
        daily_holding = daily_holding.shift(1)
        net_value, turnover = folio_net_value(daily_holding, daily_return_frame, 0.0005)
        return net_value, turnover

    if signal_direction == 1:
        nav_long, turnover_long = process_grouped_frame(grouped_alpha_sheet[grouped_alpha_sheet.group == max_group])
        nav_short, turnover_short = process_grouped_frame(grouped_alpha_sheet[grouped_alpha_sheet.group == 0])
    else:
        nav_long, turnover_long = process_grouped_frame(grouped_alpha_sheet[grouped_alpha_sheet.group == 0])
        nav_short, turnover_short = process_grouped_frame(grouped_alpha_sheet[grouped_alpha_sheet.group == max_group])
    nav_long_short = nav_long / nav_short
    nav_benchmark, nav_turnover = process_grouped_frame(grouped_alpha_sheet)
    nav_over_bench = nav_long / nav_benchmark
    nav_frame = pd.concat([nav_long, nav_short, nav_benchmark, nav_long_short, nav_over_bench], axis=1)
    nav_frame.columns = ['多头组合', '空头组合', '等权基准', '多空组合', '超额基准']
    return nav_frame, turnover_long


# 计算净值统计数据
def nav_performance(nav_series, period=1, compact=True):
    return_series = (nav_series - nav_series.shift(1)) / (nav_series.shift(1))
    return_series = return_series.dropna()
    # 年化收益率
    annual_ratio = (nav_series.iloc[len(nav_series)-1] / nav_series.iloc[0]) ** (240./period/len(nav_series)) - 1
    # 年化波动率
    annual_volatility = np.sqrt(return_series.var()*240/period)
    # 夏普比率
    sharp_ratio = (return_series.mean()/np.sqrt(return_series.var())) * np.sqrt(240/period)
    # 最大回撤
    ever_max = nav_series.expanding().max()
    max_drawdown = ((1 - nav_series/ever_max).max())
    # 月度胜率
    monthly_nav = nav_series.resample('M').last()
    monthly_return = monthly_nav / monthly_nav.shift(1) - 1
    monthly_win_rate = 0.5 * (np.sign(monthly_return).mean() + 1)
    if compact:
        indicator = pd.Series([annual_ratio, annual_volatility, sharp_ratio, max_drawdown, monthly_win_rate],
                              index=['annual_ratio', 'annual_volatility', 'sharpe_ratio', 'max_drawdown',
                                     'monthly_win_rate'])
        return indicator
    else:
        return annual_ratio, annual_volatility, sharp_ratio, max_drawdown, monthly_win_rate


# 净值数据分年度统计
def performance_by_year(nav_series):
    nav_return = nav_series / nav_series.shift(1) - 1
    monthly_nav = nav_series.resample('M').last()
    monthly_return = monthly_nav / monthly_nav.shift(1) - 1
    year_index_ret = nav_return.to_period('A-DEC')
    year_monthly_ret = monthly_return.to_period('A-DEC')

    def get_annual_stats(one_year_daily_return, one_year_monthly_return):
        ret = one_year_daily_return.mean() * 240
        vol = one_year_daily_return.std() * np.sqrt(240)
        sharpe = ret / vol
        one_year_nav = (one_year_daily_return + 1).cumprod()
        one_year_max = one_year_nav.expanding().max()
        one_year_max = one_year_max.transform(lambda x: max(x, 1))
        mdd = (1 - one_year_nav / one_year_max).max()
        win_rate = 0.5 * (np.sign(one_year_monthly_return).mean() + 1)
        return [ret, vol, sharpe, mdd, win_rate]

    years = year_index_ret.index.unique()
    stats_list = [get_annual_stats(year_index_ret.loc[x], year_monthly_ret.loc[x]) for x in years]
    stats_mat = pd.DataFrame(stats_list, index=years,
                             columns=['return', 'volatility', 'sharpe_ratio', 'mdd', 'win_rate'])
    return stats_mat

