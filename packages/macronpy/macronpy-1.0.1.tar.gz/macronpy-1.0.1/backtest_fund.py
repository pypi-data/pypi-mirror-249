from macronpy.asset_analysis import *
from macronpy.database_connect import *
from macronpy.eco_analysis import *
from macronpy.macro import *
from macronpy.plotly_plot import *
from macronpy.port_model import *
from macronpy.dbmake import *

import datetime
import math
from numba import jit #函数加速器
from functools import lru_cache

#【注意】fund_pool_data现在还是全局变量，要改一下
class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value




#功能：返回一个起止日期时间段内所有的日期
#参数：beginDate：开始日期;endDate:结束日期
# @jit
# def dateRange(beginDate, endDate):
#     dates = []
#     dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
#     date = beginDate[:]
#     while date <= endDate:
#         dates.append(date)
#         dt = dt + datetime.timedelta(1)
#         date = dt.strftime("%Y-%m-%d")
#     return dates
# 样本基金池的数据
# @jit
# @lru_cache(maxsize=128)
def get_fund_pool_navdata(fund_code_list, startdate, enddate, fq=True, db=wds):
    '''
    startdate ,enddate：yyyy-mm-dd
    【返回值】index为时间，column为基金代码的数据框，存的是基金净值
    db可以选wds\wdb
    '''
    fund_code_list_set = deduplicate_list(fund_code_list)
    START = startdate.replace("-", "")
    END = enddate.replace("-", "")

    # 复权映射字典
    fa_dict = {True: 'F_NAV_ADJUSTED', False: 'F_NAV_UNIT'}
    indicator = fa_dict[fq]

    fund_code_list_new = [x[:-3] for x in fund_code_list]

    #     # 构造模糊匹配的基金代码列表
    #     fund_code_list = [f"'{code[:-3]}%'" for code in fund_code_list]
    #     # 将基金代码列表转换为逗号分隔的字符串
    #     fund_code_string = ','.join(fund_code_list)

    # 构建基金代码的模糊匹配条件
    fund_code_num = [fund[:-3] for fund in fund_code_list_set]

    #     fund_code_num_formatch=[f"F_INFO_WINDCODE LIKE '{fund[:-3]}%' " for fund in fund_code_list_set]
    #     like_conditions = ' OR '.join(fund_code_num_formatch)
    if len(fund_code_list)==1:
        select_code="('"+fund_code_list[0][:-3]+"')"
    else:
        select_code=tuple(fund_code_num)
    query = f'''
        SELECT F_INFO_WINDCODE,
        SUBSTRING(F_INFO_WINDCODE, 1, LENGTH(F_INFO_WINDCODE) - 3) AS truncated_string,
        PRICE_DATE, {indicator}
        FROM ChinaMutualFundNAV
        WHERE PRICE_DATE >= '{START}' AND PRICE_DATE <= '{END}'
        AND truncated_string in {select_code}
        AND F_INFO_WINDCODE NOT LIKE '%!%'
    '''

    print("正在提取基金净值数据")
    wds_dataframe_ts = pd.read_sql(query, db).pivot_table(indicator, 'PRICE_DATE', 'F_INFO_WINDCODE','sum').date_index()
    #     print("wds_dataframe_ts的列名",wds_dataframe_ts.columns.tolist())
    #     print("wds_dataframe_ts的列长度",len(wds_dataframe_ts.columns.tolist()))
    result_fund_code_num = [fund[:-3] for fund in wds_dataframe_ts.columns.tolist()]
    wds_dataframe_ts.columns = result_fund_code_num
    wds_dataframe_ts = wds_dataframe_ts[fund_code_num]
    # wds_dataframe_ts = wds_dataframe_ts[fund_code_list_set]
    wds_dataframe_ts.columns = fund_code_list_set

    trade_datelist = trade_date_wind(startdate, enddate)
    wds_dataframe_ts.fillna(method='ffill', inplace=True)
    wds_dataframe_ts_new = trade_datelist.mg(wds_dataframe_ts, how='left')

    print("提取完毕")
    if (type(fund_code_list_set) != list):
        return np.nan
    else:
        return wds_dataframe_ts_new


#功能：获取开放式基金列表里所有基金的净值
#参数：fund_code_list:基金代码列表；tradedate：交易日
# @jit
# @lru_cache(maxsize=128)
# def select_Fundlist_NetValue(fund_code_list, startdate ,enddate,fund_pool_data):
#     '''
#     利用预定义的基金池数据，筛选目标数据集
#     '''
#     data=fund_pool_data.loc[startdate:enddate,deduplicate_list(fund_code_list)]
#     return data
#计算基金列表的净值序列
# @jit
# @lru_cache(maxsize=128)
def Cal_Fundlist_NetValue(fund_code_list,fund_pool_data,*date):
    if(type(fund_code_list)!=list):
        return np.nan
    if(len(date)==1):
        # v = list(select_Fundlist_NetValue(fund_code_list,date,today(),fund_pool_data).iloc[:,0])
        v = list(fund_pool_data.loc[date:today(), deduplicate_list(fund_code_list)].iloc[:, 0])
        if len(v)==0:
            return np.nan
    if(len(date)==2):
        # return select_Fundlist_NetValue(fund_code_list,date[0],date[1],fund_pool_data)
        return fund_pool_data.loc[date[0]:date[1],deduplicate_list(fund_code_list)]
# 功能：获取某只开放式基金的净值
# 参数：fund_code:基金代码；tradedate：交易日
# @jit
# @lru_cache(maxsize=128)
def Cal_NetValue(fund_code, tradedate ,fund_pool_data):
    try:
        data = fund_pool_data.loc[tradedate, fund_code]
    except:
        data = np.nan
    return data
# 功能：定义账户类
# @jit
# @lru_cache(maxsize=128)
class Account(object):
    # @lazyproperty
    # @lru_cache(maxsize=128)
    def __init__(self, init_base):
        # 属性：init_base:初始账户;fund_list:基金持仓
        self.init_base = init_base
        self.fund_list = {}
        pass

    # 功能：获取持仓基金列表
    # @lazyproperty
    # @lru_cache(maxsize=128)
    def getbase(self):
        return self.account.init_base

    # 功能：获取账户
    # @lazyproperty
    # @lru_cache(maxsize=128)
    def get_initbase(self):
        return self.init_base
# 功能：定义回测类，继承了账户类
# @jit
# class fund_backTest():
#     # @lazyproperty
#     # @lru_cache(maxsize=128)
#     def __init__(self, begin_date, end_date, init_base ,fund_pool_data):
#         self.begin_date = begin_date
#         self.end_date = end_date
#         self.account = Account(init_base) #继承了账户类
#         self.fund_pool_data=fund_pool_data
#         self.flag = 0
#         self.data = pd.DataFrame(index=pd.date_range(self.begin_date,
#                                                      self.end_date,
#                                                      freq='d').astype('str').tolist(),
#                                  columns=['init_base', 'fund_list', 'flag'])
#         self.data['fund_list'] = self.data['fund_list'].astype('object')
#
#     # 功能：申购或买入函数，用于买入指定数量的基金
#     # 参数：fundcode：基金代码;num：申购数量;date：交易日期
#     # @lazyproperty
#     # @lru_cache(maxsize=128)
#     def buy(self, fundcode, num, date):
#         # 计算交易日净值
#         netvalue = Cal_NetValue(fundcode, date ,self.fund_pool_data)
#         # 如果申购额度大于账户余额则交易无效
#         if netvalue * num > self.account.init_base:
#             pass
#         else:
#             self.account.init_base -= netvalue * num
#         ##获取fundlist中fundcode的持仓，如果有则相加，如果没有持仓则更新
#         if fundcode not in self.account.fund_list.keys():
#             self.account.fund_list.update({fundcode: num})
#         else:
#             remain_num = self.account.fund_list[fundcode] + num
#             self.account.fund_list.update({fundcode: remain_num})
#         #         print('buy函数调用')
#         # 更新从购买日之后起的data
#         self.update_data(date, self.end_date, self.account.init_base, self.account.fund_list.copy())
#
#     # @lazyproperty
#     # @lru_cache(maxsize=128)
#     def buy_list(self, fundcode_list, date):
#         # 传入的基金列表类型必须为列表
#         if (type(fundcode_list) != list):
#             pass
#         # 计算购买清单长度
#         l = len(fundcode_list)
#         # 每一只基金总共有n_quota元用于申购
#         n_quota = math.floor(self.account.init_base / l)
#         # try:
#         #
#         #     for code in fundcode_list:
#         #         netvalue = Cal_NetValue(code, date ,self.fund_pool_data)
#         #         # 计算某种基金申购额度，采用金额/净值并向下取整
#         #         num = math.floor(n_quota / netvalue)
#         #         self.buy(code, num, date)
#         # except Exception as e:
#         #     print(e)
#         #     print('出问题的是日期', date)
#         #     print('出问题的是代码', code)
#         #     print('netvalue是', netvalue)
#         for code in fundcode_list:
#             netvalue = Cal_NetValue(code, date ,self.fund_pool_data)
#             # 计算某种基金申购额度，采用金额/净值并向下取整
#             try:
#                 num = math.floor(n_quota / netvalue)
#             except:
#                 print("netvalue是",netvalue)
#                 print("出问题的code是",code)
#                 print("出问题的date是", date)
#             self.buy(code, num, date)
#     # 赎回或卖出函数，用于卖出指定数量的基金
#     # @lazyproperty
#     # @lru_cache(maxsize=128)
#     def sell(self, fundcode, num, date):
#         netvalue = Cal_NetValue(fundcode, date ,self.fund_pool_data)
#         # 如果持仓列表里没有这个基金，则跳过不执行
#         if fundcode not in self.account.fund_list.keys():
#             pass
#         # 如果持仓列表里有这个基金，则可以卖出
#         else:
#             remain_num = self.account.fund_list[fundcode] - num
#             # 如果小于等于零，则相当于全部卖出
#             if (remain_num <= 0):
#
#                 self.account.init_base += self.account.fund_list[fundcode] * netvalue
#                 self.account.fund_list.pop(fundcode)
#             else:
#                 self.account.fund_list.update({fundcode: remain_num})
#                 self.account.init_base += num * netvalue
#             #         print('sell函数调用')
#         # 更新从购买日之后起的data
#         self.update_data(date, self.end_date, self.account.init_base, self.account.fund_list.copy())
#
#         # 清仓或卖出所有函数，用于将持仓的基金全部卖出
#
#     # @lazyproperty
#     # @lru_cache(maxsize=128)
#     def sell_all(self, date):
#         # print(date)
#         # display(self.data.loc[date])
#         for k, v in self.data.loc[date]['fund_list'].items():
#             self.sell(k, v, date)
#
#     # 更新持仓函数，用于每次有买入或卖出时更新账户并更新data
#     # @lazyproperty
#     # @lru_cache(maxsize=128)
#     def update_data(self, begin_date, end_date, *args):
#
#         self.flag = self.flag + 1
#         self.data.loc[begin_date:end_date, 'flag'] = self.flag
#         self.data.loc[begin_date:end_date, 'init_base'] = args[0]
#         date_list=pd.date_range(begin_date, end_date, freq='d').astype('str').tolist()
#         for date in date_list:
#             self.data.at[date, 'fund_list'] = args[1]
#         # 用这句话简化了for循环，但是不能这样用，否则会在for k, v in self.data.loc[date]['fund_list'].items():这里报错
#         # self.data.loc[date_list, 'fund_list'] = args[1]
#         # display("self.data.loc[date_list, 'fund_list']")
#         # display(self.data.loc[date_list, 'fund_list'])
#         # date=date_list[-1]
#
#
#
#         #    new_init_base=args[0]
#         #    new_fund_list=args[1]
#         # self.data.update({date:{'init_base':args[0],'fund_list':args[1]}})
#         pass
#
#     # 盘后处理函数，结束之后调用,用于计算每日收益，alpha，beta等
#     # @lazyproperty
#     # @lru_cache(maxsize=128)
#     def handle_data(self, log=False):
#         # 构造收益矩阵，矩阵中行为日期，列包含持仓市值，资金余额，alpha，beta等
#         df_returns = self.data[self.data['flag'].isna() == False].copy()
#         # df_returns['nav']=0
#         # df_returns['nav']=df_returns['nav'].astype('object')
#         # 将data按照flag划分为若干个时间区间，按照我们对flag的定义，每有一次交易时flag会+1，如果没有交易则不变，那么每个flag区间内持仓是一样的
#         # 分别计算每个flag内持仓的市值和总资产，用于进行后续收益率，风险的计算
#         flags = df_returns['flag'].unique()
#         df_returns['nav'] = 0
#         df_returns['nav'] = df_returns['nav'].astype('object')
#         for flag in flags:
#             begin_date = df_returns[df_returns['flag'] == flag].index[0]
#             end_date = df_returns[df_returns['flag'] == flag].index[-1]
#             ###第一个指标，持仓市值###
#             # 计算持仓市值
#             fund_list = list(df_returns.loc[begin_date]['fund_list'].keys())
#             #             print("现在看market_value,基金是",fund_list)###############################################
#             if (len(fund_list) == 0):
#                 continue
#             # 持仓基金列表对应的持仓数量
#             nums = list(df_returns.loc[begin_date]['fund_list'].values())
#             navs = Cal_Fundlist_NetValue(fund_list, self.fund_pool_data,begin_date, end_date)
#             valid_index = []
#             # 将返回的基金净值转换为numpy以便切片
#             d = np.array(navs.values.T)
#             i = 0
#
#             for t in navs.index:
#                 # 将返回的时间转换为字符串型
#                 idx = t.strftime("%Y-%m-%d")
#
#                 # 情况1:形如下列形式,多余1只基金，多个返回日期
#                 # .ErrorCode=0
#                 # .Codes=[000051.OF,020011.OF]
#                 # .Fields=[NAV]
#                 # .Times=[20210104,20210105]
#                 # .Data=[[1.7652,1.7972],[1.2286,1.2511]]
#                 if (d.shape[0] >= 2):
#                     market_value = np.dot(nums, d[:, i])
#                     df_returns.at[idx, 'nav'] = d[:, i]
#
#                 ##情况2:形如下列形式，只有一只基金，有多个返回日期
#                 # .ErrorCode=0
#                 # .Codes=[000051.OF]
#                 # .Fields=[NAV]
#                 # .Times=[20210104,20210105]
#                 # .Data=[[1.7652,1.7972]]
#                 if (d.shape[0] == 1 and len(list(navs.index)) > 1):
#                     market_value = np.dot(nums, d[0][i])
#                     df_returns.at[idx, 'nav'] = [d[0][i]]
#
#                 ##情况3，形如下列形式：多余1只基金，1个返回日期
#                 # .ErrorCode=0
#                 # .Codes=[000051.OF,020011.OF]
#                 # .Fields=[NAV]
#                 # .Times=[20210104]
#                 # .Data=[[1.7652,1.2286]]
#                 if (d.shape[0] == 1 and len(list(navs.index)) == 1):
#                     market_value = np.dot(nums, d[0])
#                     df_returns.at[idx, 'nav'] = d[0]
#                 df_returns.loc[idx, 'market_value'] = market_value
#                 i = i + 1
#                 # if (t.strftime("%Y-%m-%d") in df_returns.index)
#
#         ###第三个指标，总资产，为每日持仓市值与资金余额相加###
#         df_returns['total_assets'] = df_returns.loc[:, ['init_base', 'market_value']].sum(axis=1)
#         df_returns.dropna(inplace=True)
#         df_returns=df_returns.date_index()
#         return df_returns

def get_fund_nav_from_factor_group(begin_date, end_date, fund_code_group_input):
    '''
    根据因子分组列表数据框，提取基金池净值数据框
    fund_code_group_input：数据框，
    index是日期，columns是基金分组名称（可以是1、2、3，也可以是价值、成长这种）
    要求fund_code_group_input的每一个元素的资产代码的列表，可以是字符串格式也可以直接是列表格式
    '''
    if type(fund_code_group_input.iloc[-1, -1]) == str:
        fund_code_group_input = fund_code_group_input.applymap(parse_string_to_list)
    fund_code_group_input = fund_code_group_input[begin_date:end_date]

    fund_pool_group_list = list(set(extract_lists(fund_code_group_input)))
    fund_pool_group_data_nav = get_fund_pool_navdata(fund_pool_group_list, begin_date, end_date, fq=True)

    return fund_pool_group_data_nav
# # %%这个是无循环回测，基本上可以覆盖前面的class了。甚至可以作为一个标杆，套用到个股因子和行业因子
# class fund_backTest():
#     def __init__(self, begin_date, end_date, fund_code_group_input, freq='q', fund_pool_group_data_nav=None):
#         '''
#         fund_code_group_input是数据框，index为因子时间，列名无要求，但数据框的每一个元素应该是列表（或字符串格式的列表）
#         用于存放每一个因子日期对应的基金代码
#         fund_pool_group_data_nav是可选参数，不传入则在class中取数据，传入则直接用传入的数据。要求数据框
#         '''
#
#         if str(type(fund_pool_group_data_nav)) != "<class 'pandas.core.frame.DataFrame'>":  # 如果参数这里没传，则根据fund_code_group_input的代码集合提取净值数据，否则使用传入的净值数据
#             fund_pool_group_data_nav=get_fund_nav_from_factor_group(begin_date, end_date, fund_code_group_input)
#
#         freq = freq.upper()
#         TRADT_END = fund_pool_group_data_nav.index.astype('str')[-1]
#         RPT_END = fund_code_group_input.index.astype('str')[-1]
#
#         if end_date < min(TRADT_END, RPT_END):
#             end_date = end_date
#         if end_date > RPT_END:
#             if end_date > TRADT_END:
#                 end_date = TRADT_END
#
#         fund_pool_group_data_ret = fund_pool_group_data_nav.pct()[begin_date:end_date]
#         sample = fund_code_group_input.copy()
#
#         if freq == 'Q':
#             date_map = trade_and_calendar(begin_date, end_date, 'm')
#             date_map = date_map[date_map.trade_date <= end_date]
#             date_map.calendar_date = date_map.calendar_date.shift(1)
#             # 《公开募集证券投资基金信息披露管理办法》规定，季报在季度结束之日起15个工作日内披露完毕
#             date_map = date_map[pd.Index(date_map.calendar_date).month.isin([3, 6, 9, 12])].dropna()
#             sample = sample.loc[date_map.calendar_date.tolist(), :]
#         elif freq == '6M':
#             date_map1 = trade_and_calendar(begin_date, end_date, 'm')
#             date_map1 = date_map1[date_map1.trade_date <= end_date]
#             date_map1.calendar_date = date_map1.calendar_date.shift(2)
#             # 《公开募集证券投资基金信息披露管理办法》规定，半年报在上半年结束之日起2个月内披露完毕，年报在每年结束之日起90日内披露完毕
#             date_map1 = date_map1[pd.Index(date_map1.calendar_date).month.isin([6])].dropna()
#             date_map2 = trade_and_calendar(begin_date, end_date, 'm')
#             date_map2 = date_map2[date_map2.trade_date <= end_date]
#             date_map2.calendar_date = date_map2.calendar_date.shift(3)
#             date_map2 = date_map2[pd.Index(date_map2.calendar_date).month.isin([12])].dropna()
#             date_map = pd.concat([date_map1, date_map2]).sort_values('trade_date')
#             sample = sample.loc[date_map.calendar_date.tolist(), :]
#
#         sample_new = sample.reset_index().col(['Date', 'Funds'])
#         all_funds = set(extract_lists(sample))
#
#         # MASK用于存放因子分组的0-1掩码，index不一定是交易日
#         MASK = pd.DataFrame(0, index=sample_new['Date'], columns=list(all_funds))
#         MASK = sample.iloc[:, 0].explode().str.get_dummies().sum(level=0)
#
#         # 去除重复的列
#         MASK = MASK.loc[:, ~MASK.columns.duplicated()]
#
#         # 针对特定的频率，进行重采样。
#         fund_pool_group_data_ret_resample = fund_pool_group_data_ret.loc[date_map.trade_date.tolist(), :]
#
#         MASK_trade_index = MASK.copy()
#         MASK_trade_index.index = fund_pool_group_data_ret_resample.index
#
#         # mask_df用于存时间序列为交易日序列的0-1掩码
#         mask_df = pd.DataFrame(index=fund_pool_group_data_ret.index)
#         mask_df = pd.merge(mask_df, MASK_trade_index, left_index=True, right_index=True, how='left')
#         mask_df.fillna(method='ffill', inplace=True) #这太草率了
#         mask_df.dropna(inplace=True)
#
#         useful_ret_data = fund_pool_group_data_ret.loc[mask_df.index, mask_df.columns]
#         weight_df = mask_df.apply(lambda x: x / sum(x), axis=1)  # axis=1很重要，保证是按行运算。这里有个大问题，如果这样x/sum(x)之后，岂不是成了每日再平衡？这不科学
#         portfolio_return = useful_ret_data.fillna(0).values * weight_df
#
#         net_value = pd.DataFrame(np.cumprod(portfolio_return.sum(1) + 1))
#         net_value.columns = sample.columns
#
#         self.nav = net_value
#         self.mask_df = mask_df
#         self.useful_ret_data = useful_ret_data
#         self.weight_df = weight_df
#         self.portfolio_return = portfolio_return
#         self.date_map = date_map
#         self.fund_code_group_input = fund_code_group_input
#         self.fund_pool_group_data_ret_resample = fund_pool_group_data_ret_resample
class fund_backTest():
    def __init__(self, begin_date, end_date, fund_code_group_input, freq='q', fund_pool_group_data_nav=None):
        '''
        fund_code_group_input是数据框，index为因子时间，列名无要求，但数据框的每一个元素应该是列表（或字符串格式的列表）
        用于存放每一个因子日期对应的基金代码
        fund_pool_group_data_nav是可选参数，不传入则在class中取数据，传入则直接用传入的数据。要求数据框
        '''

        if str(type(
                fund_pool_group_data_nav)) != "<class 'pandas.core.frame.DataFrame'>":  # 如果参数这里没传，则根据fund_code_group_input的代码集合提取净值数据，否则使用传入的净值数据
            fund_pool_group_data_nav = get_fund_nav_from_factor_group(begin_date, end_date, fund_code_group_input)

        freq = freq.upper()
        TRADT_END = fund_pool_group_data_nav.index.astype('str')[-1]
        RPT_END = fund_code_group_input.index.astype('str')[-1]

        if end_date < min(TRADT_END, RPT_END):
            end_date = end_date
        if end_date > RPT_END:
            if end_date > TRADT_END:
                end_date = TRADT_END

        fund_pool_group_data_ret = fund_pool_group_data_nav.pct()[begin_date:end_date]
        sample = fund_code_group_input.copy()

        if freq == 'Q':
            date_map = trade_and_calendar(begin_date, end_date, 'm')
            date_map = date_map[date_map.trade_date <= end_date]
            date_map.calendar_date = date_map.calendar_date.shift(1)
            # 《公开募集证券投资基金信息披露管理办法》规定，季报在季度结束之日起15个工作日内披露完毕
            date_map = date_map[pd.Index(date_map.calendar_date).month.isin([3, 6, 9, 12])].dropna()
            sample = sample.loc[date_map.calendar_date.tolist(), :]
        elif freq == '6M':
            date_map1 = trade_and_calendar(begin_date, end_date, 'm')
            date_map1 = date_map1[date_map1.trade_date <= end_date]
            date_map1.calendar_date = date_map1.calendar_date.shift(2)
            # 《公开募集证券投资基金信息披露管理办法》规定，半年报在上半年结束之日起2个月内披露完毕，年报在每年结束之日起90日内披露完毕
            date_map1 = date_map1[pd.Index(date_map1.calendar_date).month.isin([6])].dropna()
            date_map2 = trade_and_calendar(begin_date, end_date, 'm')
            date_map2 = date_map2[date_map2.trade_date <= end_date]
            date_map2.calendar_date = date_map2.calendar_date.shift(3)
            date_map2 = date_map2[pd.Index(date_map2.calendar_date).month.isin([12])].dropna()
            date_map = pd.concat([date_map1, date_map2]).sort_values('trade_date')
            sample = sample.loc[date_map.calendar_date.tolist(), :]

        sample_new = sample.reset_index().col(['Date', 'Funds'])
        all_funds = set(extract_lists(sample))

        # MASK用于存放因子分组的0-1掩码，index不一定是交易日
        MASK = pd.DataFrame(0, index=sample_new['Date'], columns=list(all_funds))
        MASK = sample.iloc[:, 0].explode().str.get_dummies().sum(level=0)

        # 去除重复的列
        MASK = MASK.loc[:, ~MASK.columns.duplicated()]

        # 针对特定的频率，进行重采样。
        fund_pool_group_data_ret_resample = fund_pool_group_data_ret.loc[date_map.trade_date.tolist(), :]

        MASK_trade_index = MASK.copy()
        MASK_trade_index.index = fund_pool_group_data_ret_resample.index

        # mask_df用于存时间序列为交易日序列的0-1掩码
        mask_df = pd.DataFrame(index=fund_pool_group_data_ret.index)
        mask_df = pd.merge(mask_df, MASK_trade_index, left_index=True, right_index=True, how='left')
        # mask_df.fillna(method='ffill', inplace=True)
        # mask_df.dropna(inplace=True)

        useful_ret_data = fund_pool_group_data_ret.loc[mask_df.index, mask_df.columns]
        weight_df = mask_df.apply(lambda x: x / sum(x),axis=1)  # axis=1很重要，保证是按行运算。

        # weight_df是调仓日的权重
        change_position_date_list = date_map.trade_date.apply(lambda x: str(x)[:10]).tolist()

        useful_ret_data = useful_ret_data[change_position_date_list[0]:]
        weight_df = weight_df[change_position_date_list[0]:]

        useful_ret_data = useful_ret_data.fillna(0)

        nav_data = pd.DataFrame(index=useful_ret_data.index, columns=useful_ret_data.columns, data=np.nan)
        nav_data.iloc[0, :] = 1 * weight_df.iloc[0, :]

        for i, date in enumerate(useful_ret_data.index):
            if i == 0:
                1
            else:
                if str(date)[:10] in change_position_date_list:
                    nav_data.iloc[i, :] = (nav_data.iloc[i - 1, :].sum()) * (
                                useful_ret_data.iloc[i, :] + 1).values * weight_df.iloc[i, :].values
                    # nav_data.iloc[i, :] = (nav_data.iloc[i - 1, :].sum()) * weight_df.iloc[i, :].values #这句话是保证调仓日收盘之后各个资产权重相等，现实中做不到
                else:
                    nav_data.iloc[i, :] = (useful_ret_data.iloc[i, :] + 1).values * nav_data.iloc[i - 1, :].values

        net_value = nav_data.sum(1).to_frame().col([fund_code_group_input.columns[0]])

        self.nav = net_value
        self.mask_df = mask_df
        self.useful_ret_data = useful_ret_data
        self.weight_df = weight_df
        #         self.portfolio_return = portfolio_return
        self.date_map = date_map
        self.fund_code_group_input = fund_code_group_input
        self.fund_pool_group_data_ret_resample = fund_pool_group_data_ret_resample
        self.holding_data = nav_data
class FundBacktestGroup():
    def __init__(self, begin_date, end_date, fund_code_group_input, freq='q', fund_pool_group_data_nav=None):
        '''
        分组回测类
        '''
        if type(fund_code_group_input.iloc[-1, -1]) == str:
            fund_code_group_input = fund_code_group_input.applymap(parse_string_to_list)
        group_nav_list=[]
        for i in tqdm(fund_code_group_input.columns):
            fund_bt=fund_backTest(begin_date,end_date,fund_code_group_input[[i]],freq,fund_pool_group_data_nav)
            group_nav_list.append(fund_bt.nav)
        group_nav=pd.concat(group_nav_list,axis=1)
        self.group_nav=group_nav
        self.ret_risk=group_nav.pct().dropna().ret_risk(0,'d').str_index()



