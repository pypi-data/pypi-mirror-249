# from macronpy.basic_package import *
from macronpy.macro import *
import pandas as pd
from pandas.core.base import PandasObject #用于为pandas增加函数
from macronpy.eco_analysis import eco
from macronpy.database_connect import *
from macronpy.plotly_plot import *


start_date='2005-01-01'
end_date=today()
# from plotly_plot import *
#%%资产相关函数#####################################################################################################################################
#%%日期序列
def wsd(ID_list,name_list,start='',end='',idtype="close",freq="D",uni=False,fill=''):

    if str(type(name_list))=="<class 'str'>":
        name_list_copy=[name_list]
    else :
        name_list_copy=name_list
    # if (str(type(ID_list))=="<class 'str'>") and (',' not in ID_list):
    #     name_list=[ID_list]

    # if start=='':
    #     start=start_date
    #
    # if end=='':
    #     end=end_date

    if fill!='':
        df = w.wsd(ID_list, idtype, start, end, "Period=" + freq + ";Days=Alldays", "Fill=" + fill, usedf=True)[1]
    else:
        df = w.wsd(ID_list, idtype, start, end, "Period=" + freq , usedf=True)[1]

    Index=pd.to_datetime(df.index,format="%Y-%m-%d")
    df.set_index(Index,inplace=True,drop=True)
    df.columns=name_list_copy
    if uni==True:
        for i in range(df.shape[1]):
            df.iloc[:,i]=df.iloc[:,i]/df.iloc[0,i]        
    #返回的df索引为时间，列为资产
    return df
#%%生成交易日或日历日的索引
def day_ts_index(start_date, end_date, freq, trade=False):
    '''
    返回一个只有日期序列索引的空【数据框】
    【作用】用于后续merge操作，把这个空数据框作为merge的第一个参数，实现日期vlookup
    '''
    # 日期格式必须是字符串，否则需要在这里转换成字符串！！！
    if str(type(start_date)) != "<class 'str'>":
        start = datetime_to_str(start_date)
    else:
        start = start_date

    if str(type(end_date)) != "<class 'str'>":
        end = datetime_to_str(end_date)
    else:
        end = end_date

    if trade:
        date_index_df = pd.DataFrame(index=w.tdays(beginTime=start, endTime=end, period=freq).Data[0])
    else:
        date_index_df = pd.DataFrame(index=pd.date_range(start=start, end=end, freq=freq))

    return date_index_df
#%%股债相对价值
def ERP(equity_code, equity_name, bond_code='S0059749', bond_name='国债-10Y', start='', end='',idtype='pe_ttm'):
    '''
    计算方式：100/PE-rf，数值越小股越贵
    equity_code,equity_name,bond_code,bond_name：equity_code和equity_name是列表或单字符串格式，债的全是字符串格式
    idtype：默认是pe_ttm。或者，dividendyield2，即用股息率衡量的股债性价比
    '''
    if start == '':
        start = start_date

    if end == '':
        end = end_date
    if type(equity_code) == str:
        equity_code = [equity_code]
    if type(equity_name) == str:
        equity_name = [equity_name]

    bond = eco(bond_code, bond_name, start=start)
    equity_pe = wsd(equity_code, equity_name, idtype='pe_ttm', start=start, end=end)

    equity_ep = 100 / equity_pe

    calculate_df = merge([equity_ep, bond],how='inner')
    # calculated = calculate_df.apply(lambda x: x[bond_name] - x, axis=1)
    calculated = calculate_df.apply(lambda x: x -x[bond_name], axis=1)

    erp = calculated[equity_name]
    #     equity_pe['1/pe']=100/equity_pe[equity_name]#注意这里是用100作为分子，不是1
    #     erp=pd.concat([equity_pe,bond],join='outer',axis=1)
    #     erp_name='ERP:'+equity_name+'/'+bond_name
    #     erp[erp_name]=erp[bond_name]-erp['1/pe']
    erp.fillna(method='ffill', inplace=True)

    return erp
#%%股债收益差
def ERP2(equity_code, equity_name, bond_code, bond_name, start='', end=''):
    '''
    计算方式：Rf-股息率
    equity_code,equity_name,bond_code,bond_name：全是字符串格式
    '''
    if start == '':
        start = start_date

    if end == '':
        end = end_date

    bond = eco(bond_code, [bond_name], start=start)
    equity_dvdyield = wsd(equity_code, [equity_name], idtype='dividendyield2', start=start, end=end)
    erp = pd.concat([equity_dvdyield, bond], join='outer', axis=1)
    erp_name = '股债收益差:' + equity_name + '/' + bond_name
    erp[erp_name] = erp[bond_name] - erp[equity_name]
    erp.fillna(method='ffill', inplace=True)

    return erp[[erp_name]]
#%%滚动均值标准差时间序列计算函数
def mean_std_ts(df,window=0,window_name=''):
    '''
    df：dataframe或series，只能含有一列
    '''
    df_copy=df.copy()

    df_copy['均值（'+window_name+'）']=df.rolling(window).mean()
    df_copy['+1 标准差（'+window_name+'）']=df.rolling(window).mean()+df.rolling(window).std()
    df_copy['-1 标准差（'+window_name+'）']=df.rolling(window).mean()-df.rolling(window).std()
    df_copy['+1.5 标准差（'+window_name+'）']=df.rolling(window).mean()+1.5*df.rolling(window).std()
    df_copy['-1.5 标准差（'+window_name+'）']=df.rolling(window).mean()-1.5*df.rolling(window).std()
    df_copy['+2 标准差（'+window_name+'）']=df.rolling(window).mean()+2*df.rolling(window).std()
    df_copy['-2 标准差（'+window_name+'）']=df.rolling(window).mean()-2*df.rolling(window).std()
    
    return df_copy
#%%全样本均值标准差
def mean_std_ts_full(df):
    '''
    df：dataframe或series，只能含有一列
    '''
    df_copy = df.copy()

    df_copy['均值'] = df.mean()[0]
    df_copy['+1 标准差'] = df.mean()[0] + df.std()[0]
    df_copy['-1 标准差'] = df.mean()[0] - df.std()[0]
    df_copy['+1.5 标准差'] = df.mean()[0] + 1.5 * df.std()[0]
    df_copy['-1.5 标准差'] = df.mean()[0] - 1.5 * df.std()[0]
    df_copy['+2 标准差'] = df.mean()[0] + 2 * df.std()[0]
    df_copy['-2 标准差'] = df.mean()[0] - 2 * df.std()[0]

    return df_copy
#%%历史百分位
def quantile(df,name=''):
    '''
    【准确性有待继续核实】
    '''
    df_copy=df.copy()
    df_copy.sort_index(ascending=True,inplace=True)
    Index=pd.to_datetime(df_copy.index,format="%Y-%m-%d")
    df_copy.set_index(Index,inplace=True,drop=True)
    
    result=100*df_copy.rank(pct=True,ascending=True)
    
    start_day=str(result.index[0])
    start_day=start_day[:10]
    end_day=str(result.index[len(result)-1])
    end_day=end_day[:10]
    
    result=result.tail(1)
    result.sort_values(by=result.index[0],axis=1,inplace=True,ascending=False)
    result=result.T
    result.columns=[name+'相对分位('+start_day+'至'+end_day+')']
    return result
#%%价格时间序列数据求月平均收益率
def month_average_ret(df):
    '''
    df是一个N*1的数据框，N表示样本容量
    返回的结果是价格时间序列数据求【月平均收益率】，单位%
    【注意】df的数据要求必须是月频！
    如果要年化，计算结果应该 乘以 12
    '''
    return round(100*(df.iloc[len(df)-1,0]/df.iloc[0,0]-1)/len(df),2)
#%%区间涨跌幅
def interval_ret(df):
    '''
    和month_average_ret的算法类似，只不过统计的是区间涨跌幅
    '''
    return round(100 * (df.iloc[len(df) - 1, 0] / df.iloc[0, 0] - 1) , 2)
#%%年收益函数
def annualy_ret(data):
    '''
    输入：资产价格数据框（月度、季度、年度）
    输出：不管什么频率的数据，总是输出本年末相对上年末的资产价格同比
    '''
    data_cal=data.copy()
    period_index=data_cal.index.to_period()
    
    if period_index.dtype=='period[A-DEC]':
        diff_para=1
    elif period_index.dtype=='period[Q-DEC]':
        diff_para=4
    elif period_index.dtype=='period[M]':
        diff_para=12
    
    data_cal=(data_cal-data_cal.shift(diff_para))/data_cal.shift(diff_para)
    
    data_cal=data_cal.resample('A').last()
    
    return data_cal
#%%收益率面板各元素年化
def ann_return(data,freq='M'):
    '''
    收益率面板各元素年化
    数据序列【每一个元素】转化成年度收益率（复利法），适用于每个元素是对应时间内的收益率
    '''
    if freq=='D':
        period='daily'
    elif freq=='W':
        period='weekly'
    elif freq=='M':
        period='monthly'
    elif freq=='Q':
        period='quarterly'
    elif freq=='Y':
        period='yearly'
    
    data_copy=data.copy()
    data_copy=data_copy.applymap(lambda x:empyrical.annual_return(pd.Series(x), period=period, annualization=None))
    
    return data_copy
#%%价格涨跌幅
def pct(data,start='',end=''):
    import datetime
    if start=='':
        # start=start_date
        start=datetime.datetime.strptime(start, "%Y-%m-%d")
    else:
        start=datetime.datetime.strptime(start, "%Y-%m-%d")
        
    if end=='':
        # end=end_date
        end=datetime.datetime.strptime(end, "%Y-%m-%d")
    else:
        end=datetime.datetime.strptime(end, "%Y-%m-%d")
      
    data_copy=data.copy()
    Index=pd.to_datetime(data_copy.index,format="%Y-%m-%d")
    data_copy.set_index(Index,inplace=True,drop=True)
    data_copy.sort_index(ascending=True)
    
    
    # if start<data_copy.index[0] or end>data_copy.index[len(data_copy)-1]:
    #     return print('请检查时间区间！')
    # else:
    #     data_copy=data_copy.loc[start:end]
    #     data_for_sort=pd.DataFrame((data_copy.tail(1).values/data_copy.head(1)-1).values,columns=data_copy.columns)
    #     data_sorted=data_for_sort.sort_values(by=0,axis=1,ascending=False)
    #     data_sorted=data_sorted.T
    #
    #     start=datetime.datetime.strftime(start, "%Y-%m-%d")
    #     end=datetime.datetime.strftime(end, "%Y-%m-%d")
    #
    #     data_sorted.columns=[start+' 至 '+end+' 涨跌幅']
    #     data_sorted=round(data_sorted,2)
    #     return data_sorted



    data_copy = data_copy.loc[start:end]
    data_for_sort = pd.DataFrame((data_copy.tail(1).values / data_copy.head(1) - 1).values,
                                 columns=data_copy.columns)
    data_sorted = data_for_sort.sort_values(by=0, axis=1, ascending=False)
    data_sorted = data_sorted.T

    start = datetime.datetime.strftime(start, "%Y-%m-%d")
    end = datetime.datetime.strftime(end, "%Y-%m-%d")

    data_sorted.columns = [start + ' 至 ' + end + ' 涨跌幅']
    data_sorted = round(data_sorted, 4)
    return data_sorted

#%%分组计算中位数
def group_cut_median(data_input,bins,target):
    '''
    分组，然后计算组内的中位数。组区间为（左开，右闭]
    data_input：数据框，有一个或多个指标列
    bins:形如[1,3,5,7,9]
    target:字符串，表示分组基准
    【返回值】数据框，索引为分组区间
    '''
    data_copy=data_input.copy()
    data_copy['分组']=pd.cut(data_copy[target],bins)
    grouped_data=data_copy.groupby('分组').median()
    #组别转换成字符串，为了作直方图
    grouped_data.index=grouped_data.index.astype('str')
    return grouped_data
#%%分组计算个数
def group_cut_count(data_input,bins,target):
    '''
    分组，然后计算组内的计数。组区间为（左开，右闭]
    data_input：数据框，有一个或多个指标列
    bins:形如[1,3,5,7,9]
    target:字符串，表示分组基准
    【返回值】数据框，索引为分组区间
    '''
    data_copy=data_input.copy()
    data_copy['分组']=pd.cut(data_copy[target],bins)
    grouped_data=data_copy.groupby('分组').count()
    #组别转换成字符串，为了作直方图
    grouped_data.index=grouped_data.index.astype('str')
    return grouped_data
#%%策略的风险收益特征函数
def return_risk_df_func(ret_series,risk_free,strategy_name,period):
    '''
    策略的风险收益特征函数
    ret_series是series类型！！！是策略的收益率时间序列
    strategy_name是字符串,用于给生成的dataframe添加列的名称！！！
    risk_free是小数格式，如0.03
    【返回值】数据框，索引为['累计收益率','年化收益率','年化波动率','夏普比','最大回撤']，列名为策略名称
    '''
    # 判断数据频率，用于年化等操作
    if period=='d':
        annualization=252
    elif period=='w':
        annualization=52
    elif period=='m':
        annualization=12
    elif period=='q':
        annualization=4     
    
    #累计收益
    cum_returns=round(100*(empyrical.cum_returns(ret_series,starting_value=1)[-1]-1),2)  #这里取最后一个数
    #年化收益  注意period参数
    annual_return=round(100*(empyrical.annual_return(ret_series,annualization=annualization)),2)
    #年化波动率  注意period参数
    annual_volatility=round(100*(empyrical.annual_volatility(ret_series,annualization=annualization)),2)
    #夏普比  注意period参数
    sharpe_ratio=round(empyrical.sharpe_ratio(ret_series,risk_free=risk_free,annualization=annualization),2)
    #最大回撤
    max_drawdown=round(100*(empyrical.max_drawdown(ret_series)),2)
    #卡玛比率
    calmar=round((empyrical.calmar_ratio(ret_series,annualization=annualization)),2)
    #把结果构造成数据框
    return_sigma_df=pd.DataFrame({strategy_name:
                                  [cum_returns,
                                   annual_return,
                                   annual_volatility,
                                   sharpe_ratio,
                                   max_drawdown,
                                   calmar]},
                                 index=['累计收益率（%）','年化收益率（%）','年化波动率（%）','夏普比','最大回撤（%）','卡玛比'])
    
    return return_sigma_df  
#%%多策略收益率生成业绩评价表格
#这函数有问题啊！！！
def ret_risk(ret_df,risk_free,period):
    '''
    多策略收益率生成业绩评价表格
    ret_df:数据框，索引：时间；列名：不同策略名称
    risk_free是小数格式，如0.03
    period：'d'、'w'、'm'、'q'
    【返回值】数据框，行：业绩评价指标；列：不同策略名称
    '''
    #数据按时间升序排序


    ret_df_copy=ret_df.sort_index(ascending=True)
    
    data_output_list=[]
    for i in ret_df_copy.columns:
        data_output_list.append(return_risk_df_func(ret_df_copy[i],risk_free,i,period))
    data_output=pd.concat(data_output_list,1)
    return data_output.T
PandasObject.ret_risk=ret_risk
#单资产回报率序列最大回撤信息表
def max_draw_down_table(ret_series):
    '''
    生成最大回撤对应起始、终止日期、回撤时间长度的表格
    ret_series:【pd.Series格式】资产价格收益率，注意千万不能是价格水平值序列！
    '''
    xs = ret_series.values
    returns = xs
    returns_array = np.asanyarray(returns)

    cumulative = np.empty(
        (returns.shape[0] + 1,) + returns.shape[1:],
        dtype='float64',
    )
    cumulative[0] = start = 100
    unit_values = empyrical.cum_returns(returns_array, starting_value=start, out=cumulative[1:])

    i = np.argmax(np.maximum.accumulate(unit_values) - unit_values)  # end of the period
    j = np.argmax(unit_values[:i])  # start of period

    max_drawdown = -1 * abs(100 * (unit_values[i] / unit_values[j] - 1))

    max_drawdown_start = ret_series.index[j]
    max_drawdown_end = ret_series.index[i]

    output_table = pd.DataFrame(
        {'起始': [max_drawdown_start], '终止': [max_drawdown_end], '最大回撤': [round(max_drawdown, 2)], '回撤时间': [abs(i - j)]})
    output_table
    return output_table
#%%做风险收益散点图
def sc_ret_risk(ret_df,risk_free,period,hline=True,vline=True):
    '''
    根据收益率序列，做不同策略的风险收益对比散点图
    ret_df:数据框，索引：时间；列名：不同策略名称
    risk_free是小数格式，如0.03
    period：'d'、'w'、'm'、'q'
    hline、vline：默认是True，表示给图添加横线、竖线作为辅助线
    '''

    #生成风险收益特征表格，存入multi_ret_risk_dataframe
    multi_ret_risk_dataframe=ret_risk(ret_df, risk_free, period)
    #是否要加横线、竖线（平均值）
    if hline==True and vline==True:
        hline=multi_ret_risk_dataframe.loc['年化收益率',:].mean()
        vline=multi_ret_risk_dataframe.loc['年化波动率',:].mean()
    #画图
    multi_ret_risk_dataframe.T.sc(x='年化波动率',y='年化收益率',
                     text=list(multi_ret_risk_dataframe.columns),
                     hline=hline,
                     vline=vline)
PandasObject.sc_ret_risk = sc_ret_risk
#%%PE分位数跨资产比较
def pe_quantile_compare(taa_object,date_range_list,plot=True,s=3):
    '''
    PE分位数跨资产比较
    taa_object为taa的实例，必须是存的pe数据，否则会报错
    date_range_list：形如[['2009-01-01','2022-01-01'],['2012-01-01','2022-01-01']]的嵌套列表，最早的起始日期不能早于taa_pbject的起始日期
    plot如果设置成False，返回的是数据而不是作图
    '''

    compare=pd.concat(
        [quantile(taa_object.pe[date_range_list[0][0]:date_range_list[0][1]], 'PE'),
         quantile(taa_object.pe[date_range_list[1][0]:date_range_list[1][1]], 'PE')],
        join='inner', axis=1)
    if plot==True:
        return compare.p(mode='markers+lines', index_ascending=0, s=s)
    else:
        return compare
#%%两阶段DCF模型求PE的估计值
def PE_from_DCF_two_stage(g1_df,g,wacc,n1,n2,name):
    '''
    两阶段DCF模型求PE的估计值    
    g1_df:roe*(1-股利分配率),roe和股利分配率均采用TTM的数据，dataframe类型，单列
    g:TV如果采用永续增长模型，那么TV=(1+g)/(r-g)，g)，但是实际中永续增长的假设过于严格，一般选择固定年限n2 ，常见取值在20-30年之间；自行给出假设，数值型
    wacc:加权平均资本成本，计算PE时分母要用到，自行给出假设，数值型
    n1:第一阶段持续时间，自行给出假设，数值型
    n2:第二阶段持续时间，自行给出假设，数值型    
    name:对应的中文名，比如，明显低估、低估
    '''
    stage1=g1_df.apply(lambda x:power_sum(((1+x)/(1+wacc)),1,n1),1)
    stage2_part1=((g1_df+1)/(1+wacc))**n1
    TV=power_sum(((1+g)/(1+wacc)),1,n2)
    stage2=stage2_part1*TV
    PE=stage1+stage2
    PE.columns=[name]
    return PE
#%%根据资产涨跌幅顺序生成占优顺序
def asset_ret_sort(final_data,Phase_list,Asset_list):
    '''
    Asset_Statistic需要调用的函数，根据资产涨跌幅顺序生成占优顺序
    '''
    final_data['资产表现']=""
    for phase in Phase_list:
        sort_df=final_data.loc[phase,Asset_list]
        sort_df.sort_values(ascending=False,inplace=True)
        sorted_name=">".join(sort_df.index.tolist())
        final_data.loc[phase,'资产表现']=sorted_name
    return final_data


# %%投资时钟的资产统计
def Asset_Statistic(Phase_data, Phase_list, Asset_data, Asset_list):
    '''参数说明
    Phase_data是阶段划分的df，索引为yyyy-mm-dd格式的时间戳
    Phase_list是“阶段”的具体名称，列表格式
    Asset_data是资产回报率的数据，索引为yyyy-mm-dd格式的时间戳
    Asset_list是资产的具体名称，列表格式
    '''
    Phase_data_copy = Phase_data.copy()
    Phase_data_copy.columns=['阶段']
    Phase_data_copy = pd.merge(left=Phase_data_copy, right=Asset_data * 100, left_index=True, right_index=True,
                               how='inner')
    Phase_data_copy['资产表现'] = ""
    Phase_data_copy['最佳资产'] = ""
    for i in Phase_data_copy.index:
        Phase_data_copy_sort_df = Phase_data_copy.loc[i, Asset_list]
        Phase_data_copy_sort_df.sort_values(ascending=False, inplace=True)
        sorted_name_concrete = ">".join(Phase_data_copy_sort_df.index.tolist())
        Phase_data_copy['资产表现'][i] = sorted_name_concrete
        Phase_data_copy['最佳资产'][i] = Phase_data_copy_sort_df.index.tolist()[0]

    # 生成虚拟变量列
    Phase_data_copy[Phase_list] = ""
    # 填充虚拟变量列
    for phase_dummy_name in Phase_list:
        Phase_data_copy[phase_dummy_name] = Phase_data_copy['阶段'].apply(lambda x: 1 if x == phase_dummy_name else 0)

    Phase_data_copy;

    final_data = Phase_data_copy.groupby('阶段').sum()

    final_data = round(final_data, 2)

    sum_phase = []
    for phase in Phase_list:
        sum_phase.append(final_data.loc[phase, phase])
    sum_phase_df = pd.DataFrame({'全部时长': sum_phase}, index=final_data.index.tolist())

    final_data = pd.concat([final_data[Asset_list], sum_phase_df], axis=1)
    final_data;
    final_data.columns.name = '阶段'

    final_data = asset_ret_sort(final_data, Phase_list, Asset_list)
    final_data.index = final_data.index.astype('str')

    # final_data['资产表现']=""
    # for phase in Phase_list:
    #     sort_df=final_data.loc[phase,Asset_list]
    #     sort_df.sort_values(ascending=False,inplace=True)
    #     sorted_name=">".join(sort_df.index.tolist())
    #     final_data.loc[phase,'资产表现']=sorted_name

    # 这里注意要写copy，不然是在等号右边的数据框上操作！
    final_data_monthavg = final_data.copy()

    for u in Asset_list:
        final_data_monthavg[u] = final_data_monthavg[u] / final_data_monthavg['全部时长']

    # final_data_monthavg.drop('全部时长',inplace=True,axis=1)
    final_data_monthavg = round(final_data_monthavg, 2)
    final_data_monthavg.columns.name = '阶段'

    final_data_monthavg.index = final_data_monthavg.index.astype('str')

    # 返回值说明：
    # 返回的是一个列表，三个元素分别是总和回报率统计、平均回报率统计、数据明细
    return [final_data, final_data_monthavg, Phase_data_copy]
#%%投资时钟历史阶段的划分统计开始、终止时间窗口
def period_start_end(period_df,phase_list=None):
    '''
    用于把投资时钟历史阶段的划分统计开始、终止时间窗口，便于做复盘和提取start、end用于其他函数操作
    BBQ_stage的结果可以作为period_df的输入
    phase_list是“阶段”的具体名称，列表格式
    period_df是一个dataframe，index是日期戳，可以有多列也可以有一列，但列中必须包含字段“阶段”，阶段是和时间对应的阶段名称
    比如，阶段是1,2,3,4,5,6这种数字，也可以是“复苏”，“过热”，“滞胀”，“衰退”这种字符串
    '''
    if phase_list==None:
        phase_list = list(set(period_df.iloc[:, 0]))
    phase_name=period_df.columns[0]
    phase_detail=[]
    for phase in phase_list:
        phase_start=[]
        phase_end=[]

        #处理起始
        if period_df.iloc[0,0]==phase and period_df.iloc[1,0]==phase:
            phase_start.append(str(period_df.index[0])[:7])
        elif period_df.iloc[0,0]==phase and period_df.iloc[1,0]!=phase:
            phase_start.append(str(period_df.index[0])[:7])
            phase_end.append(str(period_df.index[0])[:7])

        for i in range(1,period_df.shape[0]-1):
            if period_df.iloc[i-1,0]!=phase and period_df.iloc[i,0]==phase and period_df.iloc[i+1,0]!=phase:
                phase_start.append(str(period_df.index[i])[:7])
                phase_end.append(str(period_df.index[i])[:7])
            elif period_df.iloc[i-1,0]!=phase and period_df.iloc[i,0]==phase and period_df.iloc[i+1,0]==phase:
                phase_start.append(str(period_df.index[i])[:7])
            elif period_df.iloc[i-1,0]==phase and period_df.iloc[i,0]==phase and period_df.iloc[i+1,0]!=phase:
                phase_end.append(str(period_df.index[i])[:7])

        #处理终止
        if period_df.iloc[-2,0]==phase and period_df.iloc[-1,0]==phase:
            phase_end.append(str(period_df.index[-1])[:7])
        elif period_df.iloc[-2,0]!=phase and period_df.iloc[-1,0]==phase:
            phase_start.append(str(period_df.index[-1])[:7])
            phase_end.append(str(period_df.index[-1])[:7])   

        phase_df=pd.DataFrame({phase_name:phase,'起始':phase_start,'结束':phase_end})
        phase_detail.append(phase_df)

    phase_detail=pd.concat(phase_detail)
    phase_detail.sort_values(by='起始',ascending=True,inplace=True)
    phase_detail.index=range(len(phase_detail))
    # phase_detail.set_index('阶段',inplace=True)
    # phase_detail.index.name=None
    # phase_detail.columns.name='阶段'

    return phase_detail
# def period_cycle_count():


#%%定义一系列用于指导战术资产配置的类

#%%基本信息
class basic:
    def __init__(self, group, freq,rf=0.00):
        # 属性
        file = 'D:\\Documents And Settings\\niupeiyi\\桌面\\资产配置研究\\' + '【大类资产】.xlsx'

        # 频率
        self.freq = freq

        # 无风险利率
        self.rf = rf

        # 资产类别
        self.group = group

        # 基本信息
        basic_info = pd.read_excel(file, sheet_name=group)
        self.info = basic_info
        self.code = basic_info['代码'].tolist()
        self.name = basic_info['名称'].tolist()

#%%大类资产class
class taa:
    '''
    TAA战术资产配置，用于观察大类资产的基础特征，包括价格、估值、盈利、拥挤度等
    group：【大类资产】具体类别，可以取值：宽基指数、价值成长、中信风格、中信行业、国债指数
    idtype：WDS的指标，默认为S_DQ_CLOSE，表示资产的收盘价
    tb：WDS的数据表，需要根据group的类别调整。
    tb对于WDS的来说，宽基指数是一张表（AIndexEODPrices），中信的风格和行业是一张表（AIndexWindIndustriesEOD）
    注意，self.basic.info.name中的名称顺序可能会和后面的不太一样
    '''

    def __init__(self, group, freq, start , end ,idtype='S_DQ_CLOSE',tb='AIndexEODPrices',rf=0.00):

        #定义指标列表
        indicator=['S_DQ_CLOSE',
                   'PE_TTM',
                   'NET_PROFIT_GROWTH_RATE']


        #对不同的大类资产的不同指标做一个数据表的映射字典！！！
        tb_map_dict_price=dict(宽基指数='AIndexEODPrices',
                               价值成长='AIndexEODPrices',
                               中信风格='AIndexWindIndustriesEOD',
                               中信行业='AIndexWindIndustriesEOD',
                               申万行业='ASWSIndexEOD',
                               国债指数='CBIndexEODPrices')

        tb_map_dict_pe=dict(宽基指数='AIndexValuation',
                            价值成长='AIndexValuation',
                            中信风格='AIndexValuation',
                            中信行业='AIndexValuation',
                            申万行业='AIndexValuation')

        tb_map_dict_profit=dict(宽基指数='AIndexFinancialderivative',
                                价值成长='AIndexFinancialderivative',
                                中信风格='AIndexFinancialderivative',
                                中信行业='AIndexFinancialderivative',
                                申万行业='AIndexFinancialderivative')


        #为taa添加类basic的属性
        self.basic=basic(group,freq,rf)

        attribute_list=['price','uni','ret','pct','ret_risk','pe','profit']


        if idtype==indicator[0]:

            if self.basic.group=='全球资产':
                self.price = wsd(self.basic.code,
                                 self.basic.name,
                                 start,
                                 end,
                                 idtype,
                                 freq)
            else:
                self.price=tsd(self.basic.code,
                               start,
                               end,
                               indicator=idtype,
                               tb=tb_map_dict_price[self.basic.group],
                               db=wdb,
                               freq=self.basic.freq,
                               how='last')

            if self.basic.group!='申万行业':

                self.price.columns = list_str_replace(self.price.columns.tolist(),
                                                ['(中信)', '(风格.中信)'],
                                                ['', ''])
            else:
                self.price.columns = self.basic.name

            # 净值
            self.uni = self.price / self.price.iloc[0, :]
            # 收益率
            self.ret = self.price.pct_change()

            # 阶段涨跌幅，单位%
            self.pct = 100 * pct(self.price, start, end)

            # 风险收益特征
            self.ret_risk = ret_risk(self.ret, risk_free=self.basic.rf, period=self.basic.freq)

            #拥挤度 1月均线比6月均线，注意只有日度数据采才有这个属性
            if freq=='D' or 'd':
                self_crowd=self.price.rolling(21).mean()/self.price.rolling(125).mean()
                self.crowd=100*self_crowd.rank(pct=True,ascending=True)#这个算法其实并不对，要改！！！！！！

        elif idtype==indicator[1]:

            # pe_ttm序列数据
            self.pe=tsd(self.basic.code,
                           start,
                           end,
                           indicator=idtype,
                           tb=tb_map_dict_pe[self.basic.group],
                           db=wdb,
                           freq=self.basic.freq,
                           how='last')

            # self.pe = wsd(self.basic.code,self.basic.name,start,end,idtype,freq)
        #
        elif idtype==indicator[2]:
            # 归母净利润同比序列数据

            self.profit=tsd_rpt(self.basic.code,
                           start,
                           end,
                           indicator=idtype,
                           tb=tb_map_dict_profit[self.basic.group],
                           db=wdb,
                           freq=self.basic.freq,
                           how='last')

            # self.profit = wsd(self.basic.code,self.basic.name,start,end,idtype,freq)

        #替换对应属性的数据框的列名称中不想要的字符串
        for att in attribute_list:
            try :
                df_final=eval("self."+att)
                df_final.columns=list_str_replace(df_final.columns.tolist(),
                                                    ['(中信)','(风格.中信)'],
                                                    ['',''])
            except :
                pass
#热力图函数，用于阶段收益率的数据框
#这个函数本来是写在invest_clock类的属性里的，但是方法函数似乎无法调用，所以就给拿外面来了。
def re_li_tu(data_input, axis=0, cmap='Blues'):
    df_copy = data_input.copy()
    df_copy['全部时长'] = df_copy['全部时长'].astype('str')
    df_copy['全部轮次'] = df_copy['全部轮次'].astype('str')
    return df_copy.rlt(1)
#%%投资时钟class
class invest_clock():
    '''
    投资时钟类，基于taa类或价格序列数据框的计算结果
    【注意】asset频率要求必须是月频！！！！！！
    period_df和period两个参数和画图函数p()中的一样
    '''
    #属性部分-----------------------------------------------------------------------------
    def __init__(self,asset,period_df,period):
    # def __init__(self,asset,period_df):

        # period=[str(x) for x in period]

        if str(type(asset))=="<class 'macronpy.asset_analysis.taa'>":

            price_df=asset.price
            ret_df=asset.ret
            ret_df_name=asset.basic.name

        elif str(type(asset))=="<class 'pandas.core.frame.DataFrame'>":

            price_df=asset
            ret_df=asset.pct_change()
            ret_df_name=asset.columns.tolist()

        self.price=price_df
        self.ret=ret_df
        self.asset_name=ret_df_name


        #基本的三个属性，取自Asset_Statistic的三个返回值
        self.ret_phs_tot,\
        self.ret_phs_avg,\
        self.ret_phs_detail=Asset_Statistic(period_df,
                                    period,
                                    ret_df,
                                    ret_df_name)

        #利用period_start_end函数，转换成阶段分组
        period_group = period_start_end(period_df,period)

        ###self.period_group存的是区间内月均收益率，注意month_average_ret函数
        for i in ret_df_name:
            period_group[i] = period_group.apply(lambda x: month_average_ret(price_df[[i]][x['起始']:x['结束']]), 1)
        period_group['阶段'] = period_group['阶段'].astype('str')

        self.period_group=period_group
        self.period_group.set_index('阶段',inplace=True)
        self.period_group.index.name = None
        self.period_group.columns.name='阶段'

        ###利用period_start_end函数，转换成阶段分组，区间涨跌幅！！！
        period_group2 = period_start_end(period_df,period)

        # self.period_group2存的是区间涨跌幅，注意interval_ret函数
        for i in ret_df_name:
            period_group2[i] = period_group2.apply(lambda x: interval_ret(price_df[[i]][x['起始']:x['结束']]), 1)
        period_group2['阶段'] = period_group2['阶段'].astype('str')

        self.period_group2=period_group2
        self.period_group2.set_index('阶段',inplace=True)
        self.period_group2.index.name = None
        self.period_group2.columns.name='阶段'

        #定义aaa、bbb、ccc、ddd，用于计算eee、fff、ggg
        aaa = self.period_group2.copy()
        ind = aaa.index
        aaa['轮次'] = round(aaa.reset_index()[['index', '起始']].groupby(aaa.reset_index()[['index', '起始']]['index']).rank(method='first',ascending=False).set_index(ind)['index'], 0).astype('int')
        aaa = aaa[[aaa.columns.tolist()[-1]] + aaa.columns.tolist()[:-1]]

        bbb = round(aaa.reset_index()[['index'] + ret_df_name].groupby('index').mean(), 2)
        bbb.index.name = None

        ccc = asset_ret_sort(bbb, [str(x) for x in period], ret_df_name)

        ddd = round(aaa.reset_index()[['index', '轮次']].groupby('index').last(), 2)
        ddd.index.name = None
        ddd.rename(columns={'轮次': '全部轮次'}, inplace=True)


        period_str=[str(x) for x in period]
        #eee：“区间涨跌幅”的平均数
        self.ret_phs_avg.index = self.ret_phs_avg.index.astype('str')
        eee = merge([ddd, self.ret_phs_avg[['全部时长']], ccc])
        #新增属性：interval_avg
        self.interval_avg=eee
        self.interval_avg=self.interval_avg.loc[period_str,:]

        #fff：self.ret_phs_avg的变体，这里替换掉原先的self.ret_phs_avg
        fff = merge([eee[['全部轮次', '全部时长']], self.ret_phs_avg.drop('全部时长', 1)])
        self.ret_phs_avg=fff
        self.ret_phs_avg = self.ret_phs_avg.loc[period_str, :]

        #ggg：self.ret_phs_tot的变体，这里替换掉原先的self.ret_phs_tot
        ggg = merge([eee[['全部轮次', '全部时长']], self.ret_phs_tot.drop('全部时长', 1)])
        self.ret_phs_tot=ggg
        self.ret_phs_tot = self.ret_phs_tot.loc[period_str, :]


    #方法函数-----------------------------------------------------------------------------

    #宏观阶段-饼形图
    def phs_pie(self):
        pie(self.ret_phs_avg.index,
            self.ret_phs_avg['全部时长'],
            rotation=180,
            textinfo=None,
            sort=False)

    #【柱形图】
    #分阶段资产月平均收益率
    def ret_phs_avg_bar(self):
        bar(self.ret_phs_avg.iloc[:, 2:-1])
    #分阶段资产月总和收益率
    def ret_phs_tot_bar(self):
        bar(self.ret_phs_tot.iloc[:, 2:-1])
    #分阶段资产期间涨跌幅平均数
    def interval_avg_bar(self):
        bar(self.interval_avg.iloc[:, 2:-1])

    #【表格热力图】
    #分阶段资产月平均收益率
    def ret_phs_avg_rlt(self,axis=0, cmap='Blues'):
        return re_li_tu(self.ret_phs_avg,axis=axis, cmap=cmap)

    #分阶段资产月总和收益率
    def ret_phs_tot_rlt(self,axis=0, cmap='Blues'):
        return re_li_tu(self.ret_phs_tot,axis=axis, cmap=cmap)
    #分阶段资产期间涨跌幅平均数
    def interval_avg_rlt(self,axis=0, cmap='Blues'):
        return re_li_tu(self.interval_avg,axis=axis, cmap=cmap)

#%%宏观场景切割类，分为两个层次，1）切割宏观场景的有效性；2）切割后的宏观场景对资产收益率区分度的有效性
#目前完成了层次1的构建，层次2有待完善
class macro_stage:
    '''
    divide_data：宏观变量时间序列，每一列为划分好的状态，比如“宽”、“紧”，列名为简写变量名，如“货币”、“信用”
    basic_clock_list：形如['货币宽+信用紧','货币宽+信用宽','货币紧+信用宽','货币紧+信用紧']的列表，之所以要手工写入，是因为顺序很重要！
    basic_clock_var：形如['货币','信用']的【双元素】列表，顺序也很重要！
    cut_var：切割变量，字符串类型，比如'盈利'
    '''
    def __init__(self,divide_data,basic_clock_list,basic_clock_var,cut_var):

        divide = divide_data.copy()

        #宏观变量列表
        macro_var=divide.columns.tolist()

        #生成宏观变量描述版数据框
        for i in macro_var:
            divide[i]=str(i)+divide[i]

        divide['计数'] = 1

        #以货币信用为例，这里basic_clock_var_name表示“货币信用”
        basic_clock_var_name=''.join(basic_clock_var)
        divide[basic_clock_var_name] = divide[basic_clock_var[0]] + '+' + divide[basic_clock_var[1]]

        pivot=divide.pivot_table(index=cut_var,columns=basic_clock_var_name,values='计数',aggfunc='sum')


        pivot=pivot[basic_clock_list]
        pivot=round(100*(pivot/pivot.sum()),1)
        pivot=pivot.T
        pivot.index.name,pivot.columns.name=None,None

        self.cut_result=pivot

    #类方法

    #切割结果作图
    def cut_result_bar(self):
        bar(self.cut_result,stack=1,hline=50)
#股票申万一级行业名称
def stock_industry(drop_industry=[]):
    '''
    提取全部股票的申万一级行业名称
    【返回值】三列的dataframe，第一列为股票代码，第二列为股票简称，第三列为申万一级行业简称。索引为数值
    '''
    sql1 = "select S_INFO_WINDCODE,SW_IND_CODE,ENTRY_DT from wind.AShareSWIndustriesClass"

    # stockname_swcode:股票名 对应 申万代码
    stockname_swcode = pd.read_sql(sql1, wdb)

    stockname_swcode = stockname_swcode.sort_values(by='ENTRY_DT',
                                                    ascending=True).drop_duplicates(subset=['S_INFO_WINDCODE'],
                                                                                    keep='last')

    stockname_swcode['SW_IND_CODE'] = stockname_swcode['SW_IND_CODE'].apply(lambda x: x[:4])

    sw_code_list = stockname_swcode.SW_IND_CODE.drop_duplicates().tolist()

    sw_code_str = "\',\'".join(sw_code_list)

    sql2 = "select INDUSTRIESCODE,INDUSTRIESNAME,LEVELNUM from wind.AShareIndustriesCode"

    # swcode_swname：申万代码 对应 申万名
    swcode_swname = pd.read_sql(sql2, wdb)

    # 剔除部分行业
    if drop_industry != []:
        swcode_swname = swcode_swname[~swcode_swname['INDUSTRIESNAME'].isin(drop_industry)]

    swcode_swname['INDUSTRIESCODE'] = swcode_swname['INDUSTRIESCODE'].apply(lambda x: x[:4])

    swcode_swname = swcode_swname[swcode_swname['INDUSTRIESCODE'].isin(sw_code_list)].query("LEVELNUM==2")

    # stockname_swname：股票名 对应 申万名。上面两个都是中介
    stockname_swname = pd.merge(left=stockname_swcode,
                                right=swcode_swname,
                                left_on='SW_IND_CODE',
                                right_on='INDUSTRIESCODE', how='inner')[['S_INFO_WINDCODE',
                                                                         'INDUSTRIESNAME']].set_index('S_INFO_WINDCODE')

    sql3 = "select S_INFO_WINDCODE,S_INFO_NAME from wind.AShareDescription"

    stock_code_name = pd.read_sql(sql3, wdb)
    stock_code_name = stock_code_name.set_index('S_INFO_WINDCODE')

    stockcode_name_swname = merge([stock_code_name, stockname_swname])
    stockcode_name_swname = stockcode_name_swname.reset_index()
    return stockcode_name_swname
#股票分组的类
class stock_group:
    '''
    股票分组的类，主要用于考察不同行业的财务数据聚合,数据频率：【季度】
    属性：财务数据分组求和、分组求和后求同比

    '''
    def __init__(self,code_list,start,end,indicator,tb,cn_name='',drop_industry=[]):
        #code_list如果是空，传入''或者['']，那么tsd_rpt返回的是全部A股，当然后面要剔除没用的
        # try_data的形态：行为日期（季度频率），列为各个股票的中文简称
        try_data = tsd_rpt(code_list, start, end, indicator, tb)
        #定义哪些股票需要剔除
        col_cleared = diff_of_two_list(list(try_data.columns), [x for x in list(try_data.columns)
                                                                if ('(退市)' in x)
                                                                or ('(IPO终止)' in x)
                                                                or ('*ST' in x)
                                                                or ('ST' in x)
                                                                or ('PT' in x)
                                                                or (x[0] == 'N')
                                                                or (x[0] == 'C')
                                                                or ('(已借壳)' in x)
                                                                or ('-U' in x)
                                                                or ('-W' in x)
                                                                or ('-UW' in x)
                                                                or ('B' in x)])
        #剔除需要剔除的股票（如果有）
        try_data = try_data[col_cleared]

        # #求和，然后单位换算为：亿元
        # try_data_sum = (try_data.sum(1) / 100000000)
        # try_data_sum = pd.DataFrame(try_data_sum, columns=[indicator])
        # try_data_sum.columns.name, try_data_sum.index.name = None, None
        # # try_data_sum = try_data_sum[:'2022-03-31']
        #
        # #计算年度同比
        # try_data_yoy = 100 * (try_data_sum / try_data_sum.shift(4) - 1)
        # try_data_yoy.columns.name, try_data_yoy.index.name = None, None

        #try_data2用于后续的行业分组求和的过程
        try_data2 = try_data.T

        stockcode_name_swname=stock_industry(drop_industry=drop_industry)
        stockcode_name_swname = stockcode_name_swname.reset_index().set_index('S_INFO_NAME')

        industry_sum = merge([try_data2, stockcode_name_swname[['INDUSTRIESNAME']]], 'inner').groupby('INDUSTRIESNAME').sum()
        # industry_sum = industry_sum.T.iloc[:-1, :]
        industry_sum = industry_sum.T
        industry_sum.columns.name, industry_sum.index.name = None, None

        industry_yoy = 100 * (industry_sum / industry_sum.shift(4) - 1)
        industry_yoy.columns.name, industry_yoy.index.name = None, None

        #求和，然后单位换算为：亿元
        try_data_sum = (industry_sum.sum(1) / 100000000)
        try_data_sum = pd.DataFrame(try_data_sum, columns=[indicator])
        try_data_sum.columns.name, try_data_sum.index.name = None, None
        # try_data_sum = try_data_sum[:'2022-03-31']

        #计算年度同比
        try_data_yoy = 100 * (try_data_sum / try_data_sum.shift(4) - 1)
        try_data_yoy.columns.name, try_data_yoy.index.name = None, None

        if cn_name!='':
            try_data_sum.columns=[cn_name]
            self.all_sum=try_data_sum
            try_data_yoy.columns=[cn_name]
            self.all_yoy=try_data_yoy
        else :
            self.all_sum=try_data_sum
            self.all_yoy=try_data_yoy

        self.industry_sum=industry_sum
        self.industry_yoy=industry_yoy
        self.stock_data=try_data
class stock_group2:
    '''
    stock_group是单指标类
    stock_group2是双指标类，计算指标1和指标2相除之后的新指标
    indicator_list是一个双元素列表，第一个为指标分子，第二个为指标分母
    cn_name_list是一个双元素列表，第一个为指标分子-中文名，第二个为指标分母-中文名
    '''
    def __init__(self,code_list,start,end,indicator_list,tb_var,cn_name_list=['',''],drop_industry=[]):

        if str(type(tb_var))=="<class 'str'>":
            tb=[tb_var,tb_var]
        else:
            tb=tb_var

        self.cn_name_list=cn_name_list

        #分子类
        stock_group_fenzi=stock_group(code_list,start,end,indicator_list[0],tb[0],cn_name_list[0],drop_industry)
        #分母类
        stock_group_fenmu=stock_group(code_list,start,end,indicator_list[1],tb[1],cn_name_list[1],drop_industry)

        stock_group_fenzi_all_sum_copy = stock_group_fenzi.all_sum.copy()
        stock_group_fenmu_all_sum_copy = stock_group_fenmu.all_sum.copy()

        #这些属性顾名思义，纯属原始数据搬运。单位都是亿元
        ####注意！！在基本的类中应该换算单位！！！！！！！！
        self.all_fz=stock_group_fenzi_all_sum_copy
        self.all_fz_yoy=100*(self.all_fz/self.all_fz.shift(4)-1)
        self.all_fz=(self.all_fz)/(10**8)

        self.all_fm=stock_group_fenmu_all_sum_copy
        self.all_fm_yoy = 100 * (self.all_fm / self.all_fm.shift(4) - 1)
        self.all_fm=(self.all_fm)/(10**8)

        self.industry_fz=stock_group_fenzi.industry_sum
        self.industry_fz_yoy=100 * (self.industry_fz / self.industry_fz.shift(4) - 1)
        self.industry_fz=(self.industry_fz)/(10**8)

        self.industry_fm=stock_group_fenmu.industry_sum
        self.industry_fm_yoy = 100 * (self.industry_fm / self.industry_fm.shift(4) - 1)
        self.industry_fm=(self.industry_fm)/(10**8)

        #谁比谁，字符串定义好
        ratio_name=cn_name_list[0]+'/'+cn_name_list[1]

        stock_group_fenzi_all_sum_copy.columns = [cn_name_list[0]]
        stock_group_fenmu_all_sum_copy.columns = [cn_name_list[1]]

        self.all_ratio=pd.DataFrame((stock_group_fenzi_all_sum_copy.values)/(stock_group_fenmu_all_sum_copy.values),columns=[ratio_name],index=stock_group_fenzi_all_sum_copy.index)
        self.all_ratio.columns=[ratio_name]

        #注意这里，分行业的列名要用行业名！！！不需要修改原有的名称
        self.industry_ratio=stock_group_fenzi.industry_sum/stock_group_fenmu.industry_sum

        #重要指标的中位数
        self.all_fz_median=pd.DataFrame(self.all_fz.median(),columns=[self.all_fz.columns[0]+' 中位数']).sort_values(by=self.all_fz.columns[0]+' 中位数',ascending=False)
        self.all_fm_median=pd.DataFrame(self.all_fm.median(),columns=[self.all_fm.columns[0]+' 中位数']).sort_values(by=self.all_fm.columns[0]+' 中位数',ascending=False)
        self.industry_fz_median=pd.DataFrame(self.industry_fz.median(),columns=[self.all_fz.columns[0]+' 中位数']).sort_values(by=self.all_fz.columns[0]+' 中位数',ascending=False)
        self.industry_fm_median=pd.DataFrame(self.industry_fm.median(),columns=[self.all_fm.columns[0]+' 中位数']).sort_values(by=self.all_fm.columns[0]+' 中位数',ascending=False)
        self.industry_ratio_median=pd.DataFrame(self.industry_ratio.median(),columns=[ratio_name+' 中位数']).sort_values(by=ratio_name+' 中位数',ascending=False)


        #个股原始数据，调用的时候小心，速度较慢。单位：元
        self.stock_data_fz = stock_group_fenzi.stock_data
        self.stock_data_fm = stock_group_fenmu.stock_data

    def p_all_fzfm(self):
        return merge([self.all_fz,self.all_fm]).p(r=2)
    def p_all_fzfm_yoy(self):
        return merge([self.all_fz_yoy,self.all_fm_yoy]).p(r=2)
    def p_ind_fzfm(self,ind):
        ind_fzfm=merge([self.industry_fz[[ind]], self.industry_fm[[ind]]])
        ind_fzfm.columns=[self.cn_name_list[0],self.cn_name_list[1]]
        return ind_fzfm.p(r=2)
    def p_ind_fzfm_yoy(self,ind):
        ind_fzfm_yoy=merge([self.industry_fz_yoy[[ind]],self.industry_fm_yoy[[ind]]])
        ind_fzfm_yoy.columns=[self.cn_name_list[0],self.cn_name_list[1]]
        return ind_fzfm_yoy.p(r=2)
#%%资产面板排序
class asset_panel_sort:
    '''
    资产面板排序的类，输入面板，index为日期，column为标的
    属性是按照数值排序，以及数值对应的变量排序
    这个的目的是用于投资组合分组。也可以看到之前投资时钟的思想，这个相对更简洁
    '''
    def __init__(self,data):

        data_panel=data.copy()
        data_panel.reset_index(inplace=True)
        data_panel_melted=data_panel.melt(id_vars='index')
        data_panel_melted['sort_id']=data_panel_melted['value'].groupby(data_panel_melted['index']).rank(method='first',ascending=False)
        data_panel_melted['sort_id']=data_panel_melted['sort_id'].astype('int')

        #这俩段排序的代码是核心
        #数值
        data_panel_value_sorted=data_panel_melted.pivot_table(index='index',
                                                              columns='sort_id',
                                                              values='value')
        data_panel_value_sorted.index.name,data_panel_value_sorted.columns.name=None,None
        #名称
        data_panel_name_sorted=pd.DataFrame(data_panel_melted.pivot_table(index='index',
                                                                          columns='sort_id',
                                                                          values='variable',
                                                                          aggfunc=lambda x:' '.join(str(v) for v in x)))
        data_panel_name_sorted.index.name,data_panel_name_sorted.columns.name=None,None

        self.value_sorted=data_panel_value_sorted
        self.name_sorted=data_panel_name_sorted

#事件时间点区间收益统计表
# def event_interval_pct(date_list, date_name, asset_frame, interval=[20, 40, 60, 120], basic_asset=''):
#     '''
#     date_list：待考察日期列表
#     date_name：日期事件名称，字符串
#     asset_frame：目标资产价格数据框
#     interval：列表，存放待考察区间的天数
#     basic_asset：默认是空，如果要计算和基准的超额收益，则传入基准资产的价格数据框。需要是单列数据框！
#     【返回值】第一列，时间点；第二列，区间xx日涨跌幅；后续列，不同资产收益统计
#     '''
#     import datetime
#     asset_frame_pct_all = []
#     for date_i in date_list:
#         asset_frame_pct_list = []
#         for day in interval:
#             asset_frame_i = asset_frame.loc[date_i:w.tdaysoffset(day, beginTime=date_i).Data[0][0], :]
#             # print(w.tdaysoffset(day, beginTime=date_i).Data[0][0])
#             asset_frame_i_pct = pd.DataFrame(100 * (asset_frame_i.iloc[-1, :] / asset_frame_i.iloc[0, :] - 1),
#                                              columns=[str(day) + '日后']).T
#
#             if str(type(basic_asset)) == "<class 'pandas.core.frame.DataFrame'>":
#                 basic_asset_i = basic_asset.loc[date_i:w.tdaysoffset(day, beginTime=date_i).Data[0][0], :]
#                 basic_asset_i_pct = pd.DataFrame(100 * (basic_asset_i.iloc[-1, :] / basic_asset_i.iloc[0, :] - 1),
#                                                  columns=[str(day) + '日后']).T
#
#                 asset_frame_i_pct = pd.DataFrame(asset_frame_i_pct.values - basic_asset_i_pct.values,
#                                                  columns=asset_frame.columns, index=asset_frame_i_pct.index)
#
#             asset_frame_pct_list.append(asset_frame_i_pct)
#
#         asset_frame_pct = pd.concat(asset_frame_pct_list)
#         asset_frame_pct[date_name] = date_i
#         asset_frame_pct_all.append(asset_frame_pct)
#
#     asset_frame_pct_all = round(pd.concat(asset_frame_pct_all), 2)
#     asset_frame_pct_all = asset_frame_pct_all.reset_index()
#
#     if str(type(basic_asset)) == "<class 'pandas.core.frame.DataFrame'>":
#         asset_frame_pct_all.rename(columns={'index': '区间超额涨跌幅'}, inplace=True)
#         asset_frame_pct_all = asset_frame_pct_all.set_index([date_name, '区间超额涨跌幅'])
#     else:
#         asset_frame_pct_all.rename(columns={'index': '区间涨跌幅'}, inplace=True)
#         asset_frame_pct_all = asset_frame_pct_all.set_index([date_name, '区间涨跌幅'])
#     return asset_frame_pct_all
def event_interval_pct(date_list0, date_name, asset_frame, freq='d', interval=[20, 40, 60, 120], basic_asset=''):
    '''
    date_list0：待考察日期列表
    date_name：日期事件名称，字符串
    asset_frame：目标资产价格数据框
    interval：列表，存放待考察区间的天数
    freq：'d','m'
    basic_asset：默认是空，如果要计算和基准的超额收益，则传入基准资产的价格数据框。需要是单列数据框！
    【返回值】第一列，时间点；第二列，区间xx日涨跌幅；后续列，不同资产收益统计
    '''
    if freq == 'd':
        freq_name = '日后'
    #         date_offset=[date_i+pd.offsets.CustomBusinessDay(day) for date_i in interval]
    elif freq == 'm':
        freq_name = '月后'
    #         date_offset=[date_i+pd.offsets.BusinessMonthEnd(day) for date_i in interval]

    if str(type(date_list0[0])) == "<class 'str'>":
        import datetime
        date_list = [datetime.datetime.strptime(x, "%Y-%m-%d") for x in date_list0]
    else:
        date_list = date_list0

    asset_frame_pct_all = []
    for date_i in date_list:

        asset_frame_pct_list = []
        for day in interval:
            # print(day)
            # print((asset_frame.index.tolist()).index(date_i))
            # print((asset_frame.index.tolist()).index(date_i) + day)
            day_offset_i = asset_frame.index.tolist()[(asset_frame.index.tolist()).index(date_i) + day]
            asset_frame_i = asset_frame.loc[date_i:day_offset_i, :]
            asset_frame_i_pct = pd.DataFrame(100 * (asset_frame_i.iloc[-1, :] / asset_frame_i.iloc[0, :] - 1),
                                             columns=[str(day) + freq_name]).T

            if str(type(basic_asset)) == "<class 'pandas.core.frame.DataFrame'>":
                basic_asset_i = basic_asset.loc[date_i:day_offset_i, :]
                basic_asset_i_pct = pd.DataFrame(100 * (basic_asset_i.iloc[-1, :] / basic_asset_i.iloc[0, :] - 1),
                                                 columns=[str(day) + freq_name]).T

                asset_frame_i_pct = pd.DataFrame(asset_frame_i_pct.values - basic_asset_i_pct.values,
                                                 columns=asset_frame.columns, index=asset_frame_i_pct.index)

            asset_frame_pct_list.append(asset_frame_i_pct)

        asset_frame_pct = pd.concat(asset_frame_pct_list)
        asset_frame_pct[date_name] = date_i
        asset_frame_pct_all.append(asset_frame_pct)

    asset_frame_pct_all = round(pd.concat(asset_frame_pct_all), 2)
    asset_frame_pct_all = asset_frame_pct_all.reset_index()

    if str(type(basic_asset)) == "<class 'pandas.core.frame.DataFrame'>":
        asset_frame_pct_all.rename(columns={'index': '区间超额涨跌幅'}, inplace=True)
        asset_frame_pct_all = asset_frame_pct_all.set_index([date_name, '区间超额涨跌幅'])
    else:
        asset_frame_pct_all.rename(columns={'index': '区间涨跌幅'}, inplace=True)
        asset_frame_pct_all = asset_frame_pct_all.set_index([date_name, '区间涨跌幅'])
    return asset_frame_pct_all
#%%ERP模型
def ERP_model(equity_code, equity_name, window=2 * 252, alpha=0.05, freq='d', interval=[20, 40, 60, 120],
              idtype='pe_ttm'):
    '''
    【ERP胜率赔率模型】
    equity_code：权益资产代码列表
    equity_name：权益资产名称列表
    window：滚动分位数的窗口期
    alpha：置信度，一般为0.05
    freq：数据频率，默认为'd'
    interval：列表，存放待考察区间的天数
    【返回值】数据框，存放不同持仓周期的“获得正收益概率”，以及“小于0平均收益率”。注意，这里的收益率不是年化的，是区间收益率
    '''
    import datetime
    erp = ERP(equity_code, equity_name, idtype=idtype).dropna()
    erp_quantile = erp.rolling(window).rank(pct=True, ascending=True).dropna()
    asset_df = wsd(equity_code, equity_name).dropna()

    # 设定门槛日期，用于限制回测时间点的上限
    threshold_date = [datetime.datetime.strftime(x, "%Y-%m-%d") for x in asset_df.index.tolist()][
        -1 * interval[-1]]  # -120这里是参数

    result_table_df = []
    for asset in asset_df.columns.tolist():
        erp_i = erp_quantile[[asset]]

        asset_df_i = asset_df[[asset]]

        # 置信区间
        min_value = min(erp_i.iloc[-1, 0] * (1 - alpha), erp_i.iloc[-1, 0] * (1 + alpha))
        max_value = max(erp_i.iloc[-1, 0] * (1 - alpha), erp_i.iloc[-1, 0] * (1 + alpha))

        # 筛选出历史上ERP在目标区间内的日期，存为列表

        date_list = erp_i[(erp_i >= min_value) & (erp_i <= max_value)].dropna().index.tolist()
        date_list = [datetime.datetime.strftime(date, "%Y-%m-%d") for date in date_list]

        valid_date_list = [x for x in date_list if x < threshold_date]

        pct_data_try = event_interval_pct(valid_date_list, 'ERP分位点', asset_df_i, freq, interval)
        pct_data_try_mean = pct_data_try.groupby('区间涨跌幅', sort=False).mean()
        pct_data_try_dummy = pct_data_try.applymap(lambda x: 1 if x > 0 else 0)
        WinRate = pct_data_try_dummy.groupby('区间涨跌幅').apply(lambda x: x.sum() / x.count())
        WinRate = WinRate.loc[pct_data_try.loc[date_list[0]].index.tolist()]
        WinRate = (100 * (WinRate.T)).round(1)
        negative_map = pct_data_try.applymap(lambda x: x if x < 0 else np.nan)
        negative_mapped = negative_map.applymap(lambda x: x if x < 0 else np.nan).groupby('区间涨跌幅').mean().applymap(
            lambda x: x if x < 0 else '未亏损过')
        negative_mapped = negative_mapped.loc[pct_data_try.loc[date_list[0]].index.tolist()]
        negative_mapped = negative_mapped.T.round(1)
        table_merged = merge([WinRate, negative_mapped])
        table_merged.columns = [
            repeat_in_list(['获得正收益概率'], WinRate.shape[1]) + repeat_in_list(['小于0平均收益率'], WinRate.shape[1]),
            WinRate.columns.tolist() * 2]
        result_table_df.append(table_merged)

    result_table = pd.concat(result_table_df)

    return result_table
#%%基金仓位估计
def fund_position_est(fund_index_price, basic_price, start_date, end_date, window=60):
    '''
    fund_index_price：基金指数数据框时序
    basic_price：基准指数数据框时序
    window：滚动回归的窗口长度，默认是60
    '''
    ret = merge([fund_index_price, basic_price]).pct_change()
    fund_name = fund_index_price.columns.tolist()
    basic_name = basic_price.columns.tolist()[0]
    import statsmodels.api as sm
    from statsmodels.regression.rolling import RollingOLS

    result = []
    for fund_name_i in fund_name:
        mod = RollingOLS.from_formula(fund_name_i + '~' + basic_name + '-1', data=ret[[fund_name_i, basic_name]],
                                      window=window)  # 不含截距项的回归
        rres = mod.fit()
        position_estimate = rres.params
        position_estimate.columns = [fund_name_i]
        result.append(position_estimate)
    result_df = merge(result)
    return result_df
def ttm(df,yoy=False):
    '''
    季度数据TTM，主要是季报的数据，通常wind底层数据库的季报数据不是TTM，是从年初开始累计的
    '''
    name=df.columns[0]
    df_copy=df.copy()
    df_copy['delta']=df_copy[name].diff()
    df_copy['index_judge']=df.index.month==3
    df_copy['x2']=df_copy.apply(lambda x:x[name] if x['index_judge']==True else x['delta'],axis=1)
    df_copy['x2']=df_copy['x2'].rolling(4).sum()
    df_copy=df_copy[['x2']]
    df_copy.columns=[name]
    if yoy==True:
        return df_copy.pct_change(4)
    else:
        return df_copy
PandasObject.ttm=ttm

#%%投资组合VaR与CVaR(ES)
def getData(tickers, start_date, end_date):
    df = wsd(','.join(tiuckers), 'close', start_date, end_date, '', usedf=True)

    retMat = df.pct_change()
    retMean = retMat.mean()

    covMat = retMat.covMat()
    return retMat, retMean, covMat
def calVar(tickers, weight, iniInv=100000000, start_date='2019-12-31', end_date='2021-12-31', conLevel=0.05, varDay=15):
    retMat, retMean, covMat = getData(tickers, start_date, end_date)

    portMean = retMean.dot(weightts)
    portStdev = np.sqrt(weights.T.dot(covMat).dot(weights))

    cutoffVar = norm.ppf(1 - conLevel) * portStdev - portMean
    VaRd1 = iniInv * cutoofVar

    cutoffES = conLevel ** -1 * norm.pdf(norm.ppf(conLevel)) * portStdev - portMean
    CvaRd1 = iniInv * cutoffES

    return VaRd1, CvaRd1
#%%沪深300映射行业权重及收益率
class hs300_cs_ts():
    '''
    沪深300映射行业权重及收益率
    hs300_weight_cs_ts、hs300_return_cs_ts
    '''

    def __init__(self, start_date, end_date):

        self.start = start_date
        self.end = end_date

        def hs300_data_sql(start, end):
            '''
            利用WDS提取沪深300的成分股权重，映射到中信一级行业。频率：日
            '''

            start = self.start[:4] + self.start[5:7] + self.start[8:10]
            end = end_date[:4] + end_date[5:7] + end_date[8:10]
            sql_hs300_weight = f'''
            select S_INFO_WINDCODE,S_CON_WINDCODE,TRADE_DT,I_WEIGHT,I_WEIGHT_15
            from wind.AIndexHS300CloseWeight  
            where TRADE_DT>={start} and TRADE_DT<={end}
            order by TRADE_DT
            '''
            hs300_weight = pd.read_sql(sql_hs300_weight, wdb)
            return hs300_weight

        self.ashare_stock_cs = asharestockcs()
        def hs300_weight_dataframe(start, end):
            # 由于申万行业的股票问题更多，所以这里我选择使用中信的行业分类。一致性更好

            hs300_weight_data = pd.merge(self.hs300_weight, self.ashare_stock_cs, left_on='S_CON_WINDCODE',right_on='S_INFO_WINDCODE', how='outer')
            hs300_weight_data = hs300_weight_data.drop(['S_INFO_WINDCODE_y'], axis=1).rename(columns={'S_INFO_WINDCODE_x': 'S_INFO_WINDCODE'})
            hs300_weight_data[['REMOVE_DT']] = hs300_weight_data[['REMOVE_DT']].fillna(today()[:4] + today()[5:7] + today()[8:10])

            hs300_weight_data['useful'] = hs300_weight_data.apply(lambda x: 1 if (float(x['ENTRY_DT']) <= float(x['TRADE_DT']) and float(x['REMOVE_DT']) >= float(x['TRADE_DT'])) else 0, axis=1)

            hs300_weight_data = hs300_weight_data.query("useful==1")
            hs300_weight_data = hs300_weight_data[['S_CON_WINDCODE', 'TRADE_DT', 'I_WEIGHT', 'I_WEIGHT_15', 'industry_cs1', 'industry_cs2']]
            hs300_weight_data.rename(columns={'I_WEIGHT_15': 'close'}, inplace=True)  # 这里的收盘价是不复权的价格
            return hs300_weight_data


        self.hs300_weight = hs300_data_sql(start_date, end_date)
        self.hs300_weight_data = hs300_weight_dataframe(start_date, end_date)
        self.hs300_weight_cs_ts = self.hs300_weight_data.groupby(['TRADE_DT', 'industry_cs1'])[['I_WEIGHT']].sum().reset_index().long2dt('TRADE_DT').pivot_table('I_WEIGHT','TRADE_DT','industry_cs1').fillna(0) / 100
        self.hs300_weight_cs_ts=self.hs300_weight_cs_ts.iloc[1:,:]

        def hs300_return_cs_ts_func(start, end, hs300_weight_data):
            df = hs300_weight_data.copy()

            df_lag = df.copy()
            df_lag = df_lag.long2dt('TRADE_DT').pivot_table('close', 'TRADE_DT', 'S_CON_WINDCODE')
            df_lag = df_lag.shift(1)
            df_lag = pd.DataFrame(df_lag.unstack()).reset_index().rename(columns={0: 'close'})
            df_lag.dt2long('TRADE_DT', inplace=True)
            df_lag = pd.merge(left=df_lag, right=df, on=['S_CON_WINDCODE', 'TRADE_DT'], how='left')
            df_lag = df_lag.drop('close_y', axis=1).rename(columns={'close_x': 'close'})
            df_lag = df_lag.rename(columns={'close': 'close_lag'})

            index_return_ts = pd.merge(df, df_lag[['S_CON_WINDCODE', 'TRADE_DT', 'close_lag']],on=['S_CON_WINDCODE', 'TRADE_DT'], how='outer').dropna(axis=0)
            index_return_ts['pct_chg'] = index_return_ts['close'] / index_return_ts['close_lag'] - 1
            index_return_ts = pd.DataFrame(index_return_ts.groupby(['TRADE_DT', 'industry_cs1']).apply(lambda x: sum(x['I_WEIGHT'] * x['pct_chg']) / sum(x['I_WEIGHT'])), columns=['pct']).reset_index()
            index_return_ts = index_return_ts.long2dt('TRADE_DT').pivot_table('pct', 'TRADE_DT', 'industry_cs1').fillna(0)
            return index_return_ts

        #hs300_return_cs_ts表示各个中信行业的沪深300成分股当日涨跌幅，不是贡献！！！！！！
        self.hs300_return_cs_ts = hs300_return_cs_ts_func(start_date, end_date, self.hs300_weight_data)
        # hs300_return_cs_ts表示各个中信行业的沪深300成分股当日涨跌幅贡献！！！！！！横向加总等于当天的沪深300指数整体涨跌幅
        self.hs300_return_cs_ts_contribute = self.hs300_return_cs_ts*self.hs300_weight_cs_ts

#%%Brinson分析框架
#存在问题有待继续完善
class Brinson_framework():
    '''
    Brinson基本框架
    '''

    def __init__(self, pf_data, bench_mark_weight, bench_mark_return):
        '''
        类初始化函数
        pf_data为持仓数据，SQL结构数据，至少包含字段：'市值','持仓日期','行业'。其中，行业是中信行业分类
        bench_mark_weight：沪深300（或者其他什么宽基指数）的样本股权重，按照行业聚合
        bench_mark_return：沪深300（或者其他什么宽基指数）的样本股收益率，按照行业聚合
        【注意】一定要确保pf_data和bench_mark的日期频率同频，比如，用公司持仓数据，那可以获得高频的日度数据，保证二者都是日度
        反之，如果是公募基金半年报，那要保证两者都是半年度的，需要手动调整一下基准指数权重和收益率的数据频率
        '''
        self.pf_data = pf_data
        self.bench_mark_weight = bench_mark_weight
        self.bench_mark_return = bench_mark_return

        def w_r_calculation(pf_data):
            '''
            · 函数功能：计算所持仓位的权重和收益矩阵
            · 输入变量：pf_data：使用读取函数读取到的数据
            · 输出变量：持仓的权重矩阵和收益矩阵，格式为DataFrame的list
            '''
            data_pivoted = pf_data.pivot_table('市值', '持仓日期', '行业', 'sum').fillna(0)
            p_w = data_pivoted.apply(lambda x: x / sum(x), axis=1)
            p_r = data_pivoted.pct_change().fillna(0)
            p_r = p_r.applymap(lambda x: 0 if x == np.inf else x)
            return [p_w, p_r]

        w_cal_result = w_r_calculation(pf_data)
        self.p_w = w_cal_result[0]
        self.p_r = w_cal_result[1]
class Brinson(Brinson_framework):
    '''
    正式的Brinson类，继承了Brinson_framework
    '''
    def __init__(self, pf_data, bench_mark_weight, bench_mark_return, start, end):
        Brinson_framework.__init__(self,
                                   pf_data=pf_data,
                                   bench_mark_weight=bench_mark_weight,
                                   bench_mark_return=bench_mark_return)
        b_w = self.bench_mark_weight
        b_r = self.bench_mark_return

        def Brinson_Multiple(p_w, p_r, b_w, b_r):
            p_w = p_w.loc[b_w.index, :]
            p_r = p_r.loc[b_r.index, :]
            # display(p_r.h())
            p_w[diff_of_two_list(b_w.columns, p_w.columns)] = 0
            p_r[diff_of_two_list(b_r.columns, p_r.columns)] = 0

            # 从基准权重和收益数据框中提取行业名称和交易日期
            sectors = b_w.columns
            td_dates = b_w.index

            # 定义 Brinson 归因模型的四个组成部分
            ticker = ['R_pp', 'R_pb', 'R_bp', 'R_bb']

            # 计算每个行业对基准和组合收益的贡献
            rp_contrib = p_w.values * p_r.values
            rb_contrib = b_w.values * b_r.values

            # 计算每个组成部分的单期收益
            single_R = np.zeros((len(td_dates), len(ticker)))
            #     print(rp_contrib.shape)
            single_R[:, 0] = np.sum(rp_contrib, axis=1)
            single_R[:, 1] = np.sum(p_w.values * b_r.values, axis=1)
            single_R[:, 2] = np.sum(b_w.values * p_r.values, axis=1)
            single_R[:, 3] = np.sum(rb_contrib, axis=1)

            # 计算每个组成部分的累积收益
            cum_R = np.cumprod(single_R + 1, axis=0)

            # 根据 Brinson 模型指定的方式，将组成部分相减得出最终归因结果
            Total_Excess_Return = cum_R[:, 0] - cum_R[:, 3]
            Time_Selection = cum_R[:, 1] - cum_R[:, 3]
            Stock_Selection = cum_R[:, 2] - cum_R[:, 3]
            Interactive_Effect = Total_Excess_Return - Stock_Selection - Time_Selection

            # 将归因结果合并成一个数据框并返回
            Outcome = pd.DataFrame({'总超额收益': Total_Excess_Return,
                                    '配置效应': Time_Selection,
                                    '择股效应': Stock_Selection,
                                    '交互效应': Interactive_Effect},
                                   index=td_dates)
            return Outcome.id0nm()

        self.result = Brinson_Multiple(self.p_w[start:end], self.p_r[start:end], b_w[start:end], b_r[start:end])


