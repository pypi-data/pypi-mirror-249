from macronpy.basic_package import *
from macronpy.macro import *
from macronpy.plotly_plot import *
from macronpy.database_connect import *
import warnings
warnings.filterwarnings("ignore")
indicator_info=getdata("D:\\Users\\niupeiyi\\资产配置研究\\0资产配置系统\\taamacro",
                       '宏观指标库.xlsm', '指标信息', header=0,index=False)
indicator_info.ffill(inplace=True)
indicator_info.drop_duplicates(subset=['指标ID'],inplace=True)
indicator_info.dropna(axis=1,how='any',inplace=True)
#美国衰退
recession=getdata("D:\\Users\\niupeiyi\\资产配置研究\\【宏观经济分析】\\000数据库\\000全球宏观数据库\\美国\\NBER衰退",'NBER衰退区间.xlsx','NBER衰退区间',header=0,index=False,usecols='A:B').dropna().applymap(lambda x:x.strftime("%Y-%m-%d"))
recession=gen_period_df_single(calendar_date_pd(str(recession.iloc[0,0])[:10],today(),'m','last'),recession.values,'衰退')
#美国加息周期
rate_hike=getdata("D:\\Users\\niupeiyi\\资产配置研究\\【宏观经济分析】\\000数据库\\000全球宏观数据库\\美国\\加息周期",'加息周期.xlsx','Sheet1',header=0,index=True,usecols='A:B')

#美联储数据库初始化
FRED=Fred(api_key='eccad1b316461826e992d61f339bfcf6')

# haver数据库
import Haver
# Haver.direct('on')
Haver.path('C:\DLX\DATA')
# hd1 =hv(['HMTORR@USECON'])
def hvd(indicator_id,database,id_name=True):
    '''
    取haver数据的快捷函数
    indicator_id：列表形式的指标id，字符串也可以
    database:字符串，数据库名称
    id_name：是否把列名改为指标名称，默认为True
    '''
    data=Haver.data(indicator_id,database,dates=True)
    if type(indicator_id)==str:
        indicator_id=[indicator_id]
    if id_name:
        name_list=Haver.metadata(indicator_id,database)['descriptor'].tolist()
        data.columns=name_list
    return data
def transform_data(input_list):
    '''
    把 ACPISP@USECON 这种代码格式转换为 USECON:ACPISP
    '''
    output_list = []
    for item in input_list:
        parts = item.split('@')
        if len(parts) == 2:
            output_list.append(f'{parts[1]}:{parts[0]}')
    return output_list
def hv(indicator_list,id_name=True):
    '''
    便捷的取数据函数,indicator_list必须是'ACPISP@USECON' 或者['ACPISP@USECON']这种
    id_name=True，默认是取数据的指标名称
    预感结合终端那个复制到剪贴板的操作，这个函数会用的很频繁，因为非常方便
    '''
    if type(indicator_list)==str:
        indicator_list=[indicator_list]

    indicator_id=transform_data(indicator_list)

    return_data=Haver.data(indicator_id,dates=True)

    if id_name:
        name_list=Haver.metadata(indicator_id)['descriptor'].tolist()
        return_data.columns=name_list

    return return_data
# hd1 = hv.data(['LRMANUA'],'USECON',startdate='2012-02-15',frequency='m',dates=True)
#%%正月初一的日期
def spring_day(start=2000,end=int(today()[:4])):
    '''
    春节日列表（正月初一）
    '''
    return spring_date_list(start, end)
#%%春节日所在月的月末列表
def spring_month(start=2000,end=int(today()[:4])):
    '''
    春节日所在月的月末列表
    '''
    return month_end(spring_day(start,end))
#%%经济分析相关函数################################################################################################################################
#%%提取经济数据
def eco(ID_list,name_list=None,start='',end='',freq='',how='',fill=''):
    '''
    freq='M'、'Q'、'Y'
    how='mean'、'first'、'last'
    freq和how载传入参数时要么都写，要么都不写
    fill默认为空，如果要传入参数，从'ffill'和'bfill'里选一个传
    '''
    # if start=='':
    #     start=start_date
    #
    # if end=='':
    #     end=end_date

    if str(type(name_list))=="<class 'str'>":
        name_list_copy=[name_list]
    else:
        name_list_copy = name_list

    eco_data=w.edb(ID_list,start, end,usedf=True)[1]
    if fill!='':
        eco_data.fillna(method=fill)

    if name_list!=None:
        eco_data.columns=name_list_copy


    Index=pd.to_datetime(eco_data.index,format="%Y-%m-%d")
    eco_data.set_index(Index,inplace=True)
    
    if freq!='' and how!='':
        if how=='mean':
            eco_data=eco_data.resample(freq).mean()
        elif how=='first':
            eco_data=eco_data.resample(freq).first()
        elif how=='last':
            eco_data=eco_data.resample(freq).last()
        
    return eco_data
#本地经济指标库数据提取
def edb(ID_list, start='', end='', freq='', how='', fill=''):
    '''
    edb函数和w.edb不一样，这个是自己写的。用于简化eco函数提取指标的流程。函数中，indicator_info这个数据框需要在用的时候定义
    ID_list:指标ID，可以是字符串拼接或列表
    '''
    try:

        if type(ID_list) == str and ',' in ID_list:
            eco_code_list = ID_list.split(",")
        elif type(ID_list) == str:
            eco_code_list = [ID_list]
        else:
            eco_code_list = ID_list
        # print(eco_code_list)
        name_list = sort_by_list(indicator_info[indicator_info['指标ID'].isin(eco_code_list)], '指标ID', eco_code_list)['指标名称'].tolist()
        # print(name_list)
        return eco(eco_code_list, name_list, start=start, end=end, freq=freq, how=how, fill=fill)
    except Exception as e:
        print(e)
        print('指标库里无此指标，请从EDB查询并改用eco函数')
#%%交叉相关系数
def crosscorr(lag,lead,n,lagmax):#计算时间差相关系数,n为样本容量,tl为最大滞后期,x为自变量列，y为因变量列
    
    '''lag和lead均为series类型！！！    
    【NOTE】lead为需要滞后的变量，即，直观上，lead领先lag maxrou 期为最优
    把想要滞后的变量放在lead的位置上
    '''
    
    x=lag.copy()
    y=lead.copy()
    x.sort_index(ascending=False,inplace=True)
    y.sort_index(ascending=False,inplace=True)
      
    tl=lagmax+1 
    
    corrlist_positive=[]#注意这里是谁领先谁！！
    dataframe1=pd.DataFrame(list(zip(x,y)))
    
    for i in range(tl):
        dataframe_new1=pd.DataFrame(list(zip(x,dataframe1.iloc[:,1].shift(-1*i))))
        varmatrix1=dataframe_new1.iloc[:n,:].corr()
        rou1=varmatrix1.iloc[1,0]
        corrlist_positive.append(rou1)
  
    corrlist_negative=[]#注意这里是谁领先谁！！
    dataframe2=pd.DataFrame(list(zip(x,y))) 
     
    for j in range(1,tl):
        dataframe_new2=pd.DataFrame(list(zip(x,dataframe2.iloc[:,1].shift(j))))
        varmatrix2=dataframe_new2.iloc[:n,:].corr()
        rou2=varmatrix2.iloc[1,0]
        corrlist_negative.append(rou2)    
    
    corrlist_negative.reverse()#倒序排列列表！！！
     
    corrlist=corrlist_negative+corrlist_positive
    
    list_index=[k for k in range(-1*lagmax,tl)]
    
    corrdf=pd.DataFrame(corrlist,index=list_index,columns=['不同'+lead.name+'领先期数对应的交叉相关系数'])
    maxrou=corrdf['不同'+lead.name+'领先期数对应的交叉相关系数'].max()
    optimal_lag=corrdf['不同'+lead.name+'领先期数对应的交叉相关系数'].idxmax()    
    
    #第一个返回值：最优滞后期；第二个返回值：最优相关系数；第三个返回值：滞后期及相关系数数据框
    return optimal_lag,maxrou,corrdf
#%%交叉相关分析系数
def crosscorr_analysis(sample,lagmax=12,return_plot=False):
    '''
    sample两列，这里考察的是第二列领先第一列
    '''

    cross_corr_df=[]
    
    for i in range(1,sample.shape[1]):
        cross_corr_data=crosscorr(sample.iloc[:,0],sample.iloc[:,i],len(sample),lagmax)[2]
        cross_corr_df.append(cross_corr_data)
    
    #生成交叉相关系数dataframe，并作为返回值返回
    cross_corr_df=pd.concat(cross_corr_df,axis=1)
    return bar(cross_corr_df,return_plot=return_plot)
PandasObject.cca=crosscorr_analysis #注意这里类方法用的是简写
#%%指标库最优滞后期及领先滞后阶数选择函数
def find_opt_leadlag(data):
    '''
    data的第一列是被领先指标，后面的列都是备选领先指标。时间索引无需降序排序
    '''
    crosscorr_list_n=[]
    crosscorr_list_rou=[]
    
    for i in range(1,data.shape[1]):
        output=crosscorr(data.iloc[:,0],data.iloc[:,i],len(data),12)
        crosscorr_list_n.append(output[0])
        crosscorr_list_rou.append(output[1])
    
    result=pd.DataFrame({'指标名称':data.columns.tolist()[1:],'领先阶数':crosscorr_list_n,'时差相关系数':crosscorr_list_rou})
    
    result['时差相关系数']=result['时差相关系数'].apply(lambda x:round(x,4))
    
    return result
#%%HP滤波函数
#%%HP滤波
def hp(hp_data,freq):
    '''
    hp_data_input要求是一个series
    freq是'y'、'q'、'm'
    '''
    if str(type(hp_data))=="<class 'pandas.core.frame.DataFrame'>":
        hp_data_input=hp_data.iloc[:,0]
    else:
        hp_data_input=hp_data


    if freq=='y':
        lamb=100
    elif freq=='q':
        lamb=1600
    elif freq=='m':
        lamb=14400
    
    cycle,trend=sm.tsa.filters.hpfilter(hp_data_input, lamb=lamb)
    #返回df类型的数据
    df=pd.DataFrame([trend,cycle]).T
    df.columns=[hp_data_input.name+'_trend',hp_data_input.name+'_cycle']
    return df

PandasObject.hp=hp
#%%hp滤波趋势项
def hp_trend(hp_data,freq):
    '''
    hp_data_input要求是一个series
    '''
    if str(type(hp_data))=="<class 'pandas.core.frame.DataFrame'>":
        hp_data_input=hp_data.iloc[:,0]
    else:
        hp_data_input=hp_data
    
    hp_data_input.dropna(inplace=True)

    if freq=='y':
        lamb=100
    elif freq=='q':
        lamb=1600
    elif freq=='m':
        lamb=14400
    
    cycle,trend=sm.tsa.filters.hpfilter(hp_data_input, lamb=lamb)
    #返回df类型的数据
    cycle=pd.DataFrame(cycle)
    trend=pd.DataFrame(trend)
    df=pd.merge(trend,cycle,left_index=True,right_index=True,how='inner')
    df.columns=[hp_data_input.name+'_trend',hp_data_input.name+'_cycle']
    return df[[df.columns[0]]]
PandasObject.hp_trend=hp_trend
#%%hp滤波周期项
def hp_cycle(hp_data,freq):
    '''
    hp_data_input要求是一个series
    '''
    if str(type(hp_data))=="<class 'pandas.core.frame.DataFrame'>":
        hp_data_input=hp_data.iloc[:,0]
    else:
        hp_data_input=hp_data
    
    hp_data_input.dropna(inplace=True)

    if freq=='y':
        lamb=100
    elif freq=='q':
        lamb=1600
    elif freq=='m':
        lamb=14400
    
    cycle,trend=sm.tsa.filters.hpfilter(hp_data_input, lamb=lamb)
    #返回df类型的数据
    cycle=pd.DataFrame(cycle)
    trend=pd.DataFrame(trend)
    df=pd.merge(trend,cycle,left_index=True,right_index=True,how='inner')
    df.columns=[hp_data_input.name+'_trend',hp_data_input.name+'_cycle']
    return df[[df.columns[1]]]
PandasObject.hp_cycle=hp_cycle
#%%OECD两步滤波
def oecd_filter(hp_data_input,freq):
    first_cycle_get=hp_cycle(hp_data_input,freq)
    second_trend_get=hp_trend(first_cycle_get,freq)
    #返回df类型的数据
    return pd.DataFrame(second_trend_get)
#%%线性回归去线性趋势
import pandas as pd
import numpy as np
import statsmodels.api as sm
import pandas as pd
import numpy as np
import statsmodels.api as sm


def detrend(df):
    '''
    data: 输入的时间序列数据，必须包含一个时间索引和一个时间序列值列。
    返回去除时间趋势后的时间序列数据。
    【线性回归法】
    '''
    res = []
    for i in range(df.shape[1]):
        data = df.iloc[:, [i]]
        y = data.values
        x = np.arange(len(data))

        # Add a constant term to the x variable for the intercept in the regression
        x = sm.add_constant(x)

        # Fit the linear regression model
        model = sm.OLS(y, x)
        results = model.fit()

        # Get the trend line values
        trend_line = results.predict()

        # Subtract the trend line from the original time series to detrend it
        detrended = y - trend_line.reshape(-1, 1)  # 将trend_line转换为二维数组

        # Create a new DataFrame with the detrended values
        detrended_data = pd.DataFrame(detrended, index=data.index, columns=[data.columns[0] + '_detrend'])

        res.append(detrended_data)

    return pd.concat(res, axis=1)
PandasObject.detrend = detrend
#%%针对【流量】经济数据精心设计的插值函数
def fill_flow_2m(dataframe):
    '''
    【数据框】特定的月频经济数据
    针对【流量】的1-2月合并发布的中国经济数据的【累计值】（一般是工业利润等经营效益指标），精心设计的插值函数
    【返回】插值法补齐1月数据。注意！！!返回的是【当月值】，不再是累计值了
    '''
    return dataframe.resample('M').last().diff().interpolate()
PandasObject.fill_flow_2m=fill_flow_2m
#%%针对【存量】经济数据精心设计的插值函数
def fill_stock_2m(dataframe):
    '''
    【数据框】特定的月频经济数据
    针对【存量】1-2月合并发布的中国经济数据（一般是工业库存等资产负债科目），精心设计的插值函数，插值法补齐1月数据
    【返回】插值法补齐1月数据（仍然是存量）
    '''
    return dataframe.resample('M').last().interpolate()
PandasObject.fill_stock_2m=fill_stock_2m
#%%针对1-2月连续但因为春节错期有跳点的中国经济数据精心设计的插值函数
def fill_1m_2m(dataframe):
    '''
    【数据框】特定的月频经济数据
    针对1-2月连续但因为春节错期有跳点的中国经济数据（一般是工业增加值、M1等），精心设计的插值函数，插值法修匀1-2月数据
    【返回】插值法修匀1-2月数据（使用1月和2月的平均值，这样会导致一月、二月的数据相等，但是问题不大）
    '''
    y_list=[]
    for x in dataframe.index:
        if x.month!=1 and x.month!=2:
            y=dataframe.loc[x,dataframe.columns[0]]
        else:
            import datetime
            month1=datetime.datetime(x.year,2,1)-datetime.timedelta(days=1)
            month2=datetime.datetime(x.year,3,1)-datetime.timedelta(days=1)
            y=(dataframe.loc[month1,dataframe.columns[0]]+dataframe.loc[month2,dataframe.columns[0]])/2
        y_list.append(y)
    return pd.DataFrame(y_list,index=dataframe.index,columns=dataframe.columns)
PandasObject.fill_1m_2m=fill_1m_2m
#%%季度累计差分变为单季
def diff_flow_q(dataframe):
    '''
    以人均可支配收入累计值为例，处理这种季度累计数据为当季度值
    '''
    def calculate_quarterly_value(column):
        y_list = []
        for x in dataframe.index:
            try:
                if x.month == 3:
                    y = column[x]
                else:
                    import datetime
                    month1 = x
                    month2 = datetime.datetime(x.year, x.month - 2, 1) - datetime.timedelta(days=1)
                    y = (column[month1] - column[month2])
            except:
                y = column[x]

            y_list.append(y)
        return pd.Series(y_list, index=dataframe.index)

    result = dataframe.apply(calculate_quarterly_value)

    return result
PandasObject.diff_flow_q=diff_flow_q
#%%月度累计差分变为单月
def diff_flow_m(dataframe):
    '''
    以商品房销售累计值为例，处理这种月度累计数据为当月度值
    NOTE：不含1月，数据应该是2月开始！
    '''
    def calculate_monthly_value(column):
        y_list = []
        for x in dataframe.index:
            try:
                if x.month == 2:
                    y = column[x]
                else:
                    import datetime
                    month1 = x
                    month2 = datetime.datetime(x.year, x.month, 1) - datetime.timedelta(days=1)
                    y = (column[month1] - column[month2])
            except:
                y = column[x]

            y_list.append(y)
        return pd.Series(y_list, index=dataframe.index)

    result = dataframe.apply(calculate_monthly_value)

    return result
PandasObject.diff_flow_m=diff_flow_m
#定基经济数据季调函数
def eco_level_sa(df,year_range=5,back_adj=2020,mode=12):
    '''
    对月度的经济数据水平值做季节性调整，使用季节性均值法
    比如，中国:工业增加值:定基指数，就可以用这个
    返回值：单列dataframe，原指标的季调指标
    '''
    ecodata=df.copy()
    ecodata['TTM']=ecodata.rolling(mode).sum() # mode=12 or 11
    col_name=ecodata.columns[0]
    ecodata['季节性指数']=ecodata[col_name]/ecodata['TTM']

    ecodata['年份']=ecodata.index.year
    ecodata['月份']=ecodata.index.month

    ecodata_seasfactor=ecodata.pivot('年份','月份','季节性指数').rolling(year_range).mean().bfill().apply(lambda x:np.nan if x.name>=back_adj else x,axis=1).ffill().unstack().to_frame().col('季调因子').reset_index()
    # display(ecodata_seasfactor)
    ecodata_seasfactor['date']=pd.to_datetime(ecodata_seasfactor['年份'].astype(str) + '-' + ecodata_seasfactor['月份'].astype(str) + '-1')+pd.offsets.MonthEnd()
    ecodata_seasfactor=ecodata_seasfactor.set_index('date').drop(['年份','月份'],axis=1).sort_index()
    ecodata_res=ecodata[[col_name]].mg(ecodata_seasfactor)
    ecodata_res[col_name+'定基季调']=ecodata_res[col_name]/ecodata_res['季调因子']
    return ecodata_res[[col_name+'定基季调']]
PandasObject.eco_level_sa=eco_level_sa
#%%优势分析函数
def Dominance_Analysis(sample,Lag_list=None,isp=0):
    '''
    sample的第一列为被解释变量
    解释变量个数至少为2，但是如果为2，不会返回每个变量贡献R2的数据框，只能看图
    '''
    sample_copy=sample.copy()
    sample_copy.sort_index(ascending=True,inplace=True)
    
    var=sample_copy.columns.tolist()
    
    if Lag_list==None:
        Lag_list=[0]*(len(var)-1)    
     
    #生成predictor_lag，用于存放经过滞后的数据，predictor_lag自身用于后面的pd.concat
    predictor_lag=[]
    predictor_lag.append(sample_copy.iloc[:,0])
    for i in range(len(Lag_list)):
        predictor_lag.append(sample_copy.iloc[:,i+1].shift(Lag_list[i]))
    
    sample_new=pd.concat(predictor_lag,axis=1)
    #做优势分析的时候需要剔除数据中的空值
    sample_new.dropna(inplace=True)
    
    dominance_regression=Dominance(data=sample_new,target=var[0],objective=1)

    incr_variable_rsquare=dominance_regression.incremental_rsquare()

    result=dominance_regression.dominance_stats()
    
    #画图
    if isp!=0:
        dominance_regression.plot_incremental_rsquare()
    
    Total_Dominance=result.iloc[:,(result.shape[1]-2):(result.shape[1]-1)]
    #返回值Total_Dominance是一个dataframe，是各个解释变量贡献的R2
    return Total_Dominance
#%%时间序列区间中枢
def zhongshu_basic(df,start,end):
    '''
    单区间中枢（平均值
    '''
    import datetime
    df[[start+'至'+end]]=""
    mean=df.iloc[:,0][start:end].mean()
    for i in range(len(df)):
        if (df.index[i]>=datetime.datetime.strptime(start,'%Y-%m-%d')) & (df.index[i]<=datetime.datetime.strptime(end,'%Y-%m-%d')):
            df.loc[df.index[i],start+'至'+end]=mean         
    return df
def zhongshu(df,interval_list):
    '''
    对但时间序列生成不同区间的中枢（平均值）
    df：【单列】数据框
    interval_list：区间双层列表，区间首尾相接
    例如：[['2001-01-31','2006-12-31'],['2007-01-31','2011-12-31']]
    【返回值】：原始数据单列+区间为列名的中枢列
    '''
    df_list=[]
    
    for interval_i in interval_list:
        df_list.append(zhongshu_basic(df,interval_i[0],interval_i[1]))
        
    df_final=pd.concat(df_list,axis=1)
    df_final=df_final.T.drop_duplicates().T
    
    return df_final
PandasObject.zhongshu=zhongshu
#%%傅里叶正弦波拟合
def sinfunc(t, A, w, p, c):
    """Raw function to be used to fit data.

    Parameters
    ----------
    t :
        Voltage array
    A :
        Amplitude
    w :
        Angular frequency
    p :
        Phase
    c :
        Constant value

    Returns
    -------
    __ :
        Formed fit function with provided values.

    """
    return A * np.sin(w*t + p) + c
def initial_guess(data_x, data_y):
    data_x = np.array(data_x)
    data_y = np.array(data_y)
    freqz = np.fft.rfftfreq(len(data_x), (data_x[1] - data_x[0]))  # uniform spacing
    freq_y = abs(np.fft.rfft(data_y))
    guess_freq = abs(freqz[np.argmax(freq_y[1:]) + 1])  # exclude offset peak
    guess_amp = np.std(data_y) * 2. ** 0.5
    guess_offset = np.mean(data_y)
    guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])
    return guess
def sin_cycle(case_df):
    '''
    生成周期性序列的正弦波
    case_df：单列的dataframe，索引为时间序列
    '''
    case_df = date_index(case_df)
    #用向量空间生成x向量
    x_data = np.linspace(0, 100, num=len(case_df))
    #调用initial_guess函数生成初始值guess_p0以用于迭代
    guess_p0 = initial_guess(x_data, case_df.iloc[:, 0])
    #拟合
    params, params_covariance = sco.curve_fit(sinfunc, x_data, case_df.iloc[:, 0], p0=guess_p0)
    sin_fitted = pd.DataFrame(sinfunc(x_data, params[0], params[1], params[2], params[3]),
                         index=case_df.index,
                         columns=['傅里叶拟合'])
    df_final=pd.concat([case_df, sin_fitted], axis=1)
    return df_final
#%%B-B算法划分周期阶段，参考cif包中的算法，进行了一定的修改
def BBQ_stage(df, showPlots = False, savePlots = None, nameSuffix = '',wide=9):
    
    """
    Find local maxima/minima in df. Mark all point which are higher/lower than their 5 nearest neighbours.
    
    Parameters
    -----
    df: pandas.DataFrame
        pandas DataFrame (with one column)
    showPlots: bool
        show plots?
    savePlots: str or None
        path where to save plot
    nameSuffix: str
        plot name suffix used when savePlots != None
        
    Returns
    -----
    indicator: pandas.DataFrame
        dataframe with local extremes marked as -1 (troughs) or 1 (peaks) or 0 otherwise
        
    """
    
    dataShifted = pd.DataFrame(index = df.index)
    
    for i in range(-1*wide, wide):
        
        dataShifted = pd.concat([dataShifted, df.shift(i).rename(columns = {df.columns[0]: 'shift_' + str(i)})], axis = 1)
        
    dataInd = pd.DataFrame(0, index = df.index, columns = df.columns)
    dataInd[dataShifted['shift_0'] >= dataShifted.drop('shift_0', axis = 1).max(axis = 1)] = 1
    dataInd[dataShifted['shift_0'] <= dataShifted.drop('shift_0', axis = 1).min(axis = 1)] = -1
    
    # No extremes near the beginning/end of the series
    
    dataInd[:wide] = 0
    dataInd[-1*wide:] = 0
    
#     if showPlots or savePlots:
        
#         plotIndicator(df, dataInd, showPlots = showPlots, savePlots = savePlots, nameSuffix = nameSuffix)
    
    return dataInd
#%%BBQ_stage辅助函数
def replace_one_zero(x,col_name):
    if x[col_name]==1:
        return int(1)
    elif x[col_name]==-1:
        return int(0)
#%%BBQ_stage的数据进行清洗
def BBQ(df,wide=12,phase=['上行','下行']):
    '''
    利用BBQ_stage和replace_one_zero两个函数生成阶段划分，用于传入p的函数中做折线图阴影
    【注意】这个目前还存在bug，可能会存在划分不准确的情况！！！需要人工校验！！！
    '''
    dataInd=BBQ_stage(df,wide=wide)
    col_name=df.columns.tolist()[0]
    dataInd[phase[0]] = dataInd.apply(lambda x: replace_one_zero(x,col_name), 1)
    dataInd.fillna(method='bfill', inplace=True)
    dataInd.fillna(0, inplace=True)

    dataInd[phase[1]]=dataInd[phase[0]].apply(lambda x:0 if x==1 else 1,1)
    dataInd['阶段']=dataInd.apply(lambda x:phase[0] if x[phase[0]]==1 else phase[1],1)
    dataInd.drop([col_name,phase[0],phase[1]],axis=1,inplace=True)

    return dataInd
#%%利用动态因子模型生成隐含因子
class DFM:
    '''
    动态因子模型
    data_input：输入数据，需要降维成因子的多指标时间序列dataframe
    k_factors：潜在因子个数
    max_factor_order：最大滞后期
    smoothed：平滑与否，bool值
    '''
    #定义类属性
    def __init__(self,data_input,k_factors,max_factor_order,smoothed=True):

        self.data_input=data_input
        self.data_norm=(self.data_input-self.data_input.mean())/self.data_input.std()
        self.k_factors=k_factors
        self.max_factor_order=max_factor_order
        self.smoothed=smoothed

        #定义动态因子模型基础函数
        #【注意】用于做动态因子模型的数据data_dfm必须是经过标准化的！！！
        def Dynamic_Factor_Model(data_dfm, k_factors, factor_order, smoothed=smoothed):
            model_dfm = tsa.DynamicFactor(data_dfm, k_factors=k_factors, factor_order=factor_order, error_order=0,
                                          error_cov_type="scalar")
            initial_res_dfm = model_dfm.fit(method='powell', disp=False, maxiter=300)
            res_dfm = model_dfm.fit(initial_res_dfm.params, method='lbfgs', disp=False, maxiter=300)
            #     这里要用summary显示一下回归结果
            #     print(res_dfm.summary())
            #     注意：函数的返回值是两个元素！！！！！
            if smoothed:
                return pd.Series(pd.np.sign(res_dfm.params[:data_dfm.shape[1]].sum()) * res_dfm.factors.smoothed[0],
                                 index=data_dfm.index), res_dfm.summary()
            else:
                return pd.Series(pd.np.sign(res_dfm.params[:data_dfm.shape[1]].sum()) * res_dfm.factors.filtered[0],
                                 index=data_dfm.index), res_dfm.summary()


        def run_dfm(data_norm,k_factors,max_factor_order):

            dflist = []
            df_ic_list = []

            for i in range(-1, max_factor_order):

                a = i + 1

                b, c = Dynamic_Factor_Model(data_dfm=data_norm, k_factors=k_factors, factor_order=a)
                dflist.append(b)

                d = c.as_text
                IC_namelist = ['aic', 'bic', 'hqic']
                IC_value = [re.findall('AIC(.*?)\\n', str(d))[0].strip(),
                            re.findall('BIC(.*?)\\n', str(d))[0].strip(),
                            re.findall('HQIC(.*?)\\n', str(d))[0].strip()]

                IC_df = pd.DataFrame(data=IC_value, index=IC_namelist, columns=['L' + str(a)])
                df_ic_list.append(IC_df)

            data_of_different_lag = pd.concat(dflist, axis=1)
            data_of_different_lag.columns = ['L' + str(x + 1)  for x in range(-1, max_factor_order)]
            data_of_different_lag.index.name = None

            ic_of_different_lag = pd.concat(df_ic_list, axis=1)
            ic_of_different_lag = ic_of_different_lag.astype('float')

            return data_of_different_lag,ic_of_different_lag,c

        self.data_output,self.ic_table,self.result_report=run_dfm(data_norm=self.data_norm,
                                 k_factors=self.k_factors,
                                 max_factor_order=self.max_factor_order)
        self.ic_plot=self.ic_table.T.p(return_plot=True)
#%%概率模型
def logit_model(X, dummy_df):
    '''
    logit模型，典型的例子是用美债期限利差刻画衰退概率
    X:多时间序列变量数据框
    dummy_df:0-1变量时间序列数据框
    【返回值】X刻画的虚拟变量发生的概率时间序列，数据框
    '''
    import statsmodels.formula.api as smf
    data_set = merge([X.dropna(), dummy_df]).ffill().dropna()
    data_set.sort_index(ascending=True, inplace=True)
    prob_df = []
    for i in X.varli():
        logit = smf.logit(formula=dummy_df.varli()[0] + ' ~ ' + i, data=data_set)
        results = logit.fit().predict()
        probalibity = pd.DataFrame(results, columns=[i], index=data_set.index)
        prob_df.append(probalibity)
    prob_df = merge(prob_df)
    return prob_df
#%%概率模型（多变量拟合，而非多个单变量拟合logit_model）
def logit_model_multivar(X,dummy_df):
    '''
    logit模型，典型的例子是用美债期限利差等经济指标刻画衰退概率
    X:多时间序列变量数据框，和logit_model的要求是一样的
    dummy_df:0-1变量时间序列数据框
    '''
    import statsmodels.formula.api as smf
    data_set=merge([X.dropna(),dummy_df]).ffill().dropna()
    data_set.sort_index(ascending=True,inplace=True)
    varlist=X.varli()
    logit = smf.logit(formula=dummy_df.varli()[0]+' ~ '+"+".join(varlist), data = data_set)
    results = logit.fit().predict();
    probalibity=pd.DataFrame(results,columns=['logit模型预测'],index=data_set.index)
    return probalibity
class reg:
    '''
    线性回归的类，简化常规操作
    '''
    def __init__(self, data, dependent_variable=1, independent_variable=2, intercept=True):

        if (dependent_variable, independent_variable)==(1,2):
            dependent_variable=data.columns[0]
            independent_variable = data.columns[1]
        elif (dependent_variable, independent_variable)==(2,1):
            dependent_variable=data.columns[1]
            independent_variable = data.columns[0]

        if str(type(independent_variable)) == "<class 'str'>":
            independent_variables = [independent_variable]
        else:
            independent_variables = independent_variable

        self.data = data
        self.dependent_variable = dependent_variable
        self.independent_variables = independent_variables
        self.include_intercept = intercept
        self.coefficients = None
        self.residuals = None
        self.fitted_values = None
        self.predict_values = None
        self.summary = None
        self.run_regression()

    def run_regression(self):
        formula = f"{self.dependent_variable} ~ "

        formula += " + ".join(self.independent_variables)
        if  not self.include_intercept:
            formula += " -1 "
        model = sm.formula.ols(formula=formula, data=self.data)
        results = model.fit()
        self.coefficients =  pd.DataFrame(results.params,columns=['coefficients'])
        self.residuals = pd.DataFrame(results.resid,index=self.data.index,columns=['residuals'])
        self.fitted_values = pd.DataFrame(results.fittedvalues,index=self.data.index,columns=['fitted_values'])
        self.predict_values = pd.DataFrame(results.predict(self.data[self.independent_variables]),index=self.data[self.independent_variables].index,columns=['predict_values'])
        self.summary = results.summary()
        self.summary2 = results.summary2()

#%%循环求最优滞后期
from itertools import product
def Reg_model_nfactor(sample, var_num=3, maxlag=12):
    '''
    默认加截距项！
    '注意，sample的指标名称必须都是英文！'
    '''
    var = sample.columns.tolist()

    # 用于存储结果的列表
    p_values = [[] for _ in range(var_num)]
    lag_periods = [[] for _ in range(var_num)]
    AIC_list = []
    R2_list = []

    # 利用for循环遍历所有可能的滞后期
    for lag_combination in tqdm(product(range(maxlag), repeat=var_num)):
        # 构建滞后期的DataFrame
        lagged_data = pd.concat(
            [sample.iloc[:, 0]] + [sample.iloc[:, i].shift(lag) for i, lag in enumerate(lag_combination, start=1)],
            axis=1)
        # 构建模型公式
        formula = f"{var[0]} ~ {' + '.join(var[1:])}"
        # 执行回归
        reg = ols(formula=formula, data=lagged_data).fit()
        # 提取结果
        aic = reg.aic
        r2 = reg.rsquared
        p_values_var = [reg.pvalues.round(decimals=3)[i] for i in range(1, var_num + 1)]
        # 存储结果
        AIC_list.append(aic.round(decimals=2))
        R2_list.append(r2.round(decimals=2))
        for i in range(var_num):
            p_values[i].append(p_values_var[i])
            lag_periods[i].append(lag_combination[i])

    # 构建输出DataFrame
    output_columns = {var[i + 1]: lag_periods[i] for i in range(var_num)}
    output_columns.update({'p' + str(i + 1): p_values[i] for i in range(var_num)})
    output_columns.update({'AIC': AIC_list, 'R2': R2_list})
    output = pd.DataFrame(output_columns)
    return output
#%%计算数据框的余弦相似度，每一列看做一个独立的向量
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
def cosine_similarity(dataframe, metric=False):
    # 将数据框转换为 NumPy 数组
    if type(dataframe)==np.ndarray:
        vectors=dataframe.copy()
    else:
        vectors = dataframe.values
    # 计算余弦相似度矩阵
    similarity_matrix = cosine_similarity(vectors)
    if metric:
        # 构建相似度矩阵的数据框并返回
        similarity_df = pd.DataFrame(similarity_matrix, columns=dataframe.columns, index=dataframe.columns)
        return similarity_df
    else:
        # 计算综合余弦相似度
        composite_similarity = np.prod(similarity_matrix) ** (1.0 / len(vectors)) #几何平均，剔除向量个数的影响
        return round(composite_similarity,2)

#%%月度GDP拟合，基于工增和服务业生产指数
def GDP_month():
    '''
    使用产业占比加权法计算月度的GDP
    【返回值】'月度GDP同比（上年同期加权）'（2017年12月至今）、'月度GDP同比（当期数据加权）'的两列数据框(2016年12月至今)
    '''
    winddata_q = w.edb(['M5567901', 'M5567877', 'M5567878', 'M5567879', 'M5567876', 'M0001227'], "2007-12-31", today(),
                       "Fill=Previous", usedf=True)
    winddata_m = w.edb(['M0000545', 'M5767203'], "2007-12-31", today(), "Fill=Blank", usedf=True)

    basedatadf_q = winddata_q[1]
    basedatadf_m = winddata_m[1]

    namelist_q = ['第一产业实际GDP当季同比', '第一产业当季增加值', '第二产业当季增加值', '第三产业当季增加值', '名义GDP当季值', 'PPI同比']  # PPI纯属工具，目的是使季度的数能够填充
    namelist_m = ['工业增加值当月同比', '服务业生产指数当月同比']

    basedatadf_q.columns = namelist_q
    basedatadf_m.columns = namelist_m

    df_q = basedatadf_q

    df_q['第一产业当季增加值'] = df_q['第一产业当季增加值'] / df_q['名义GDP当季值']
    df_q['第二产业当季增加值'] = df_q['第二产业当季增加值'] / df_q['名义GDP当季值']
    df_q['第三产业当季增加值'] = df_q['第三产业当季增加值'] / df_q['名义GDP当季值']

    df_q.rename(columns=
                {'第一产业当季增加值': '第一产业当季增加值占比',
                 '第二产业当季增加值': '第二产业当季增加值占比',
                 '第三产业当季增加值': '第三产业当季增加值占比'}, inplace=True)

    df_q = df_q.drop('PPI同比', axis=1)  # axis=1一定要写，目的是删除列变量！
    df_q = df_q.shift(-2)  # -2表示向‘上’移动两行！！！
    df_q = df_q.fillna(method='ffill')

    # 把原先的索引变成新的列！
    df_q['时间'] = df_q.index
    df_q = df_q.reset_index(drop=True)

    # 行切片并生成新的dataframe：
    df_q_new = df_q[108:]

    # 重新排列df_q_new列的顺序：
    df_q_new = df_q_new[['时间', '第一产业实际GDP当季同比', '第一产业当季增加值占比', '第二产业当季增加值占比', '第三产业当季增加值占比', '名义GDP当季值']]

    # 对basedatadf_m中的服务业生产指数进行interpolat插值

    # SPI是服务业生产指数的简称
    SPI = basedatadf_m['服务业生产指数当月同比']
    SPI = pd.DataFrame(SPI)
    SPIadj = SPI.reset_index()

    # 切片
    SPIadj = SPIadj[108:]
    # 提取有取值的样本
    x = np.array(SPIadj[SPIadj['服务业生产指数当月同比'].notnull()].index)  # x为把有取值的样本对应的索引做成的一个数组
    y = np.array(SPIadj[SPIadj['服务业生产指数当月同比'].notnull()]['服务业生产指数当月同比'])  # y为把有取值的样本对应的数据做成的一个数组
    xnew = np.array(SPIadj.index)  # xnew这个必须是数，不能是日期！所以才需要在上面去掉索引，“FAIPriceIndexadj = FAIPriceIndex.reset_index()”

    # SPI也要先进行切片
    SPI = SPI[108:]

    # 拟合插值函数
    f3 = interp1d(x, y, kind='cubic')
    SPIadj = pd.DataFrame([f3(xnew)]).T
    SPIadj = SPIadj.set_index(SPI.index)
    SPI = SPI.join(SPIadj, how='outer')
    # SPI.columns = ['initial', 'linear', 'quadratic', 'cubic']

    SPIadj.columns = ['服务业生产指数当月同比(插值)']

    basedatadf_m = basedatadf_m.drop('服务业生产指数当月同比', axis=1)
    basedatadf_m = basedatadf_m[108:]

    df_m_new = pd.concat([basedatadf_m['工业增加值当月同比'], SPIadj['服务业生产指数当月同比(插值)']], axis=1)

    # 我们需要的有：df_m_new，df_q_new，df_q_new需要把时间设置成索引
    df_q_new.set_index('时间', inplace=True)
    # 下面开始计算月度GDP同比
    gdp_m = pd.DataFrame()
    gdp_m['月度GDP同比（上年同期加权）'] = df_q_new['第一产业实际GDP当季同比'].shift(12) * df_q_new['第一产业当季增加值占比'].shift(12) + df_m_new['工业增加值当月同比'] * df_q_new['第二产业当季增加值占比'].shift(12) + df_m_new['服务业生产指数当月同比(插值)'] * df_q_new['第三产业当季增加值占比'].shift(12)
    gdp_m['月度GDP同比（当期数据加权）'] = df_q_new['第一产业实际GDP当季同比'] * df_q_new['第一产业当季增加值占比'] + df_m_new['工业增加值当月同比'] * df_q_new['第二产业当季增加值占比'] + df_m_new['服务业生产指数当月同比(插值)'] * df_q_new['第三产业当季增加值占比']

    return gdp_m.date_index()
#%%社融历史月度同比数据测算
def TSF():
    '''
    社融历史月度同比数据测算
    '''
    socfinData = eco(['M5206731', 'M5525755', 'M5206730', 'M5541321', 'M5525763'],
                     ['中国:社会融资规模:新增人民币贷款:当月值', '中国:社会融资规模存量', '中国:社会融资规模:当月值', '中国:社会融资规模:当月值:初值',
                      '中国:社会融资规模存量:同比']).col_str_replace(["中国:"], [""])
    data2 = eco(['M0325576'], ['(停止)债券托管量:政府债券']).col_str_replace(["中国:", "(停止)"], ["", ""])
    data3 = eco(['M0043411'], ['中国:金融机构:财政存款余额']).col_str_replace(["中国:"], [""])
    data4 = eco(['M6179494'], ['中国:社会融资规模存量:政府债券']).col_str_replace(["中国:"], [""])
    socfinData.fillna(0, inplace=True)
    socfinData['社会融资规模存量'] = socfinData['社会融资规模存量'] * 10000
    socfinData['社融存量估算'] = 0

    tempvalue = 0
    for i in range(10, -1, -1):
        tempvalue += socfinData.iloc[i, 2]
        socfinData.iloc[i, 5] = socfinData.iloc[11, 1] - tempvalue
    for i in range(11, socfinData.shape[0]):
        if socfinData.iloc[i, 1] == 0:
            socfinData.iloc[i, 5] = socfinData.iloc[i, 2] + socfinData.iloc[i - 1, 5]
        else:
            socfinData.iloc[i, 5] = socfinData.iloc[i, 1]

    # data为社融相关表
    socfinData['社融存量估算-政府债调整'] = socfinData['社融存量估算'] + data2['债券托管量:政府债券'] - data3['金融机构:财政存款余额']
    socfinData['社融存量估算-政府债调整（未剔除财政存款）'] = socfinData['社融存量估算'] + data2['债券托管量:政府债券']
    socfinData['社融存量官方 同比'] = socfinData['社会融资规模存量'].pct_change(periods=12)
    socfinData['社融存量估算 同比'] = socfinData['社融存量估算'].pct_change(periods=12)
    socfinData['广义社融同比'] = socfinData['社融存量估算-政府债调整'].pct_change(periods=12)
    socfinData['广义社融同比（未剔除财政存款）'] = socfinData['社融存量估算-政府债调整（未剔除财政存款）'].pct_change(periods=12)

    socfinData.loc['2015-12-31':, '社融存量估算 同比'] = socfinData.loc['2015-12-31':, '社会融资规模存量:同比'] * 0.01
    socfinData.loc['2015-12-31':, '广义社融同比（未剔除财政存款）'] = socfinData.loc['2015-12-31':, '社会融资规模存量:同比'] * 0.01
    socfinData.loc['2017-01-31':, '社融存量估算-政府债调整'] = socfinData.loc['2017-01-31':, '社融存量估算'] - data3.loc['2017-01-31':,
                                                                                              '金融机构:财政存款余额']
    socfinData.loc['2017-01-31':, '社融存量估算-政府债调整（未剔除财政存款）'] = socfinData.loc['2017-01-31':, '社会融资规模存量']
    socfinData.loc['2017-01-31':, '广义社融同比'] = socfinData.loc['2017-01-31':, '社会融资规模存量:同比'] * 0.01

    return 100*socfinData[['广义社融同比']].col('社融同比')

def fed_single(id):
    '''
    提取美联储单一指标
    '''
    data=FRED.get_series(id).to_frame()
    data.columns=[id]
    return data
import pandas as pd

def fed(id, name="",):
    '''
    从美联储数据库提取一组指标
    id：形如"AAAA,BB"，用半角逗号分隔开
    name：形如"AAAA,BB"，用半角逗号分隔开。不写的话，则默认用id作为数据框的列名
    '''
    id_list = id.split(",")
    df_list = []
    idname_list=[]

    for identifier in id_list:
        df_list.append(fed_single(identifier))
        idname_list.append(FRED.search(identifier).query(f"id=='{identifier}'")['title'][0])

    res = pd.concat(df_list, axis=1)

    if name != "":
        name_list = name.split(",")
        res.columns = name_list
    else:
        res.columns = idname_list
    # display(res)
    # Infer frequency of the date index
    freq = pd.infer_freq(res.index)[:1]

    # Adjust the frequency of the date index
    if freq == "M":
        res=res.resample('M').last()
    elif freq == "Q":
        res=res.resample('Q').last()
    elif freq == "A":
        res=res.resample('Y').last()

    return res


def adf_test(dataframe, autolag='aic'):
    """
    Pass in a DataFrame with multiple time series columns,
    perform ADF tests for each column, and return a summary DataFrame.
    """
    # Initialize an empty DataFrame to store results
    results_df = pd.DataFrame(columns=['ADF test statistic', 'p-value', 'lags used', 'observations',
                                       'critical value (1%)', 'critical value (5%)', 'critical value (10%)'],
                              index=dataframe.columns)

    # Perform ADF tests for each column in the DataFrame
    for column in dataframe.columns:
        series = dataframe[column]
        result = adfuller(series.dropna(), autolag=autolag)

        # Fill in the results DataFrame with ADF test results
        results_df.loc[column] = [result[0], result[1], result[2], result[3],
                                  result[4]['1%'], result[4]['5%'], result[4]['10%']]

    return results_df.T
