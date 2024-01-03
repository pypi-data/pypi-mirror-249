from macronpy.basic_package import *
import pandas as pd
from macronpy.plotly_plot import *
from pandas.core.base import PandasObject #用于为pandas增加函数
import datetime

#%%基本算法########################################################################################################################################
#%%幂指数求和
def power_sum(x,start,n):
    '''
    幂指数求和，例如，2^1+2^2+2^3+2^4,此处x=2,start=1,n=4
    '''
    _s=0
    for k in range(start,n+1):
        _s=_s+x**k
    return _s
###################################################################################################################################################


#




#%%列表操作########################################################################################################################################
#%%循环替换列表中的字符
def list_str_replace(input,before,after):
    '''
    input:待替换列表
    before:原先的字符，列表格式！
    after:替换后的字符，列表格式！
    '''
    output=[]
    for i in input:
        for j in range(len(before)):
            #核心操作：替换字符串
            i=i.replace(before[j],after[j])
        output.append(i)
    return output
def col_str_replace(df,before,after):
    '''
    结合col和list_str_replace，加入了Pandas方法
    '''
    col_name=df.columns.tolist()
    return df.col(list_str_replace(col_name,before,after))
PandasObject.col_str_replace=col_str_replace
def index_str_replace(df,before,after):
    '''
    结合index和list_str_replace，加入了Pandas方法
    '''
    df_copy=df.copy()
    index_name=df_copy.index.tolist()
    df_copy.index=list_str_replace(index_name,before,after)
    return df_copy
PandasObject.index_str_replace=index_str_replace

#%%列表去重保序
def deduplicate_list(list_sample):
    '''
    列表去重保序
    '''
    series = pd.Series(list_sample)
    deduplicated_series = series.drop_duplicates()

    # 将去重后的Series转换回列表
    deduplicated_list = deduplicated_series.tolist()

    return deduplicated_list
#%%在一个列表中删除另一个列表
def diff_of_two_list(lst1,lst2):
    '''
    在列表lst1中删除列表lst2
    '''
    diff_list=[]
    for item in lst1:
        if item not in lst2:
            diff_list.append(item)
    return diff_list
#%%嵌套列表展开
def unfold_list(list_input):
    '''
    对于列表形如 list_1 = [[1, 2], [3, 4, 5], [6, 7], [8], [9]] 
    转化成列表 list_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    '''
    list_output=sum(list_input,[])
    return list_output
#%%列表中的元素重复N次
def repeat_in_list(list_input,N):
    '''
    [1,2,3]变为[1,1,2,2,3,3]
    '''
    list_output=[val for val in list_input for i in range(N)]
    return list_output
#%%两个列表元素错位拼接
def cuo_wei_conc_list(list1,list2):
    '''
    举例：list1=[1,1,1],list2=[2,2,2],输出[1,2,1,2,1,2]
    '''
    out_list=[]
    for i in range(len(list1)):
        out_list.append(list1[i])
        out_list.append(list2[i])
    return out_list
#%%按列表中的元素顺序排序
def sort_by_list(data_frame,key,list_custom):
    '''
    把dataframe中的某一列按照列表中的元素排序
    key：字符串，表示排序目标基准列的列名
    list_custom：提供顺序的列表
    返回排序好的新数据框
    '''
    df=data_frame.copy()
    # 设置成“category”数据类型
    df[key] = df[key].astype('category')
    # inplace = True，使 recorder_categories生效
    df[key]=df[key].cat.reorder_categories(list_custom)
    # inplace = True，使 df生效
    df.sort_values(key, inplace=True)
    return df
#%%把dataframe所有的数据的列表的所有元素取出来，存成一个大列表
def extract_lists(data):
    '''
    pandas的数据框，全部元素要么是空值，要么是列表。把所有的数据的列表的所有元素取出来，存成一个大列表
    举例说明
    # 创建示例数据框
    data = {'A': [[1, 2, 3], np.nan, [4, 5]], 'B': [[6, 7], [8, 9], [10, 11]]}
    df = pd.DataFrame(data)

    # 提取所有列表元素并存储为一个大列表
    all_lists = extract_lists(df)

    print(all_lists)
    结果输出：[1, 2, 3, 6, 7, 8, 9, 4, 5, 10, 11]
    '''
    result = []
    for value in data.values.flatten():
        if isinstance(value, list):
            result.extend(value)
        elif pd.isnull(value):
            continue
    return result
##################################################################################################################################################
#%%返回今天的yyyy-mm-dd字符串
def today():
    '''
    【返回值】'yyyy-mm-dd'，今天的日期
    '''
    return datetime.datetime.now().strftime('%Y-%m-%d')
TODAY=today()
def yearstart():
    return str(datetime.datetime.now().year)+'-01-01'
def yearend():
    return str(datetime.datetime.now().year)+'-12-31'





#%%日期操作########################################################################################################################################
#%%日期前推一天
def last_day(Ymd=TODAY,num=1):
    import datetime
    #如果Ymd传入的时候不是Timestamp，是字符串，那么要做格式转化
    if str(type(Ymd))!="<class 'pandas._libs.tslibs.timestamps.Timestamp'>":
        dayA= datetime.datetime.strptime(Ymd, '%Y-%m-%d')
    else:
        dayA=Ymd

    delta=datetime.timedelta(days=num)

    dayB=dayA-delta
    return dayB.strftime('%Y-%m-%d')

#%%日期前推一个季度
def last_quarter(Ymd=TODAY):
    '''
    找到当前‘yyyy-mm-dd’日期最近的【上一个】一个季度末的日期，比如输入‘2022-12-30’，输出'2022-09-30'
    '''
    # 如果Ymd传入的时候不是Timestamp，是字符串，那么要做格式转化
    if str(type(Ymd))!="<class 'pandas._libs.tslibs.timestamps.Timestamp'>":
        dayA= pd.Timestamp(Ymd)
    else:
        dayA=Ymd
    # date = pd.Timestamp(dayA)
    quarter_end = dayA - pd.offsets.QuarterEnd()
    last_quarter_end = quarter_end - pd.offsets.QuarterEnd()
    last_quarter_end_date = pd.date_range(start=last_quarter_end, end=quarter_end, freq='D')[-1]
    return last_quarter_end_date.strftime('%Y-%m-%d')
#%%这个有问题，要好好改！
def next_quarter(Ymd=TODAY):
    '''
    找到当前‘yyyy-mm-dd’日期最近的【下一个】一个季度末的日期，比如输入‘2022-12-30’，输出'2023-03-31'
    '''
    # 如果Ymd传入的时候不是Timestamp，是字符串，那么要做格式转化
    if str(type(Ymd))!="<class 'pandas._libs.tslibs.timestamps.Timestamp'>":
        dayA= pd.Timestamp(Ymd)
    else:
        dayA=Ymd
    # date = pd.Timestamp(dayA)
    quarter_end = dayA + pd.offsets.QuarterEnd()
    next_quarter_end = quarter_end + pd.offsets.QuarterEnd()
    next_quarter_end_date = pd.date_range(start=quarter_end, end=next_quarter_end, freq='D')[-1]
    return next_quarter_end_date.strftime('%Y-%m-%d')
#%%数据框索引从非datetime设置成datetime
def date_index(data):
    '''
    添加为了pandas方法
    数据框索引从非datetime设置成datetime
    多应用于从Excel直接复制时间序列数据set_index之后，index的类型是字符串的情况
    '''
    data_copy=data.copy()
    if str(type(data_copy.index[0]))=="<class 'str'>":
        Index=pd.to_datetime(data_copy.index,format="%Y-%m-%d")
    elif str(type(data_copy.index[0])) in ("<class 'int'>","<class 'numpy.int64'>"):
        Index = pd.to_datetime(data_copy.index.astype('str'), format="%Y-%m-%d")
    else:
        Index = pd.to_datetime(data_copy.index, format="%Y-%m-%d")
    out=data_copy.set_index(Index)
    return out
PandasObject.date_index=date_index
def long_index(data):
    '''
    添加为了pandas方法
    数据框索引从datetime设置成yyyymmdd的long
    '''
    data_copy=data.copy()
    Index = data_copy.index.strftime('%Y%m%d')
    out=data_copy.set_index(Index)
    return out
PandasObject.long_index=long_index
def str_index(data,left=None):
    '''
    索引转化为字符串格式
    left是切片参数，如果是日期索引，left=4，则切片yyyy，7则切片yyyy-mm
    '''
    df=data.copy()
    df.index=df.index.astype('str')
    if left!=None:
        df.index = df.index.str[:left]
    return df
PandasObject.str_index=str_index
def str_col(data):
    '''
    索引转化为字符串格式
    '''
    df=data.copy()
    df.columns=df.columns.astype('str')
    return df
PandasObject.str_col=str_col
#%%从datetime类型转成str
def datetime_to_str(datetime_var):
    import datetime
    str_p=datetime.datetime.strftime(datetime_var,'%Y-%m-%d')
    return str_p
def datetime_index_to_str(df):
    df_copy=df.copy()
    df_index=df.index
    b=pd.DataFrame(index=df_index)
    b['索引']=b.index
    b['索引']=b['索引'].apply(lambda x:datetime_to_str(x))
    b.index=b['索引']
    df_copy.index=b.index
    df_copy.index.name=df.index.name
    return df_copy
PandasObject.datetime_index_to_str = datetime_index_to_str
#%%从yyyymmdd长字符转换成yyyy-mm-dd的datetime
def long_to_dt(long_date_df,col=False,ymd="%Y-%m-%d"):
    '''
    从yyyymmdd长字符转换成yyyy-mm-dd的datetime
    long_date_df：单列数据框，必须是数据框！元素形如yyyymmdd的长字符串
    col：二值变量
    【返回值】吧yyyymmdd转换成datetime输出
    '''
    import datetime
    col_name = list(long_date_df.columns)
    if col==False:
        #这里要求long_date_df单列
        date_df = long_date_df.applymap(str).applymap(lambda s: "{}-{}-{}".format(s[:4],s[4:6],s[6:]) if s[0] in ['0','1','2','3','4','5','6','7','8','9'] else np.nan)
        date_df=date_df.applymap(lambda x:datetime.datetime.strptime(x, ymd))
        # date_df.iloc[:,0] = [datetime.datetime.strptime(x, ymd) for x in date_df.iloc[:,0]]
        return date_df
    else :
        #这里long_date_df不必单列
        if ymd=="%Y-%m-%d":
            new_col=[x[:4]+'-'+x[4:6]+'-'+x[6:] for x in col_name]
        elif ymd=="%Y-%m":
            new_col = [x[:4] + '-' + x[4:6]  for x in col_name]
        elif ymd=="%Y":
            new_col = [x[:4]  for x in col_name]
        long_date_df_copy=long_date_df.copy()
        long_date_df_copy.columns=new_col
        long_date_df_copy = long_date_df_copy.applymap(lambda x: datetime.datetime.strptime(x, ymd))
        # long_date_df_copy.iloc[:, 0] = [datetime.datetime.strptime(x, ymd) for x in long_date_df_copy.iloc[:, 0]]
        return long_date_df_copy
def long2dt(df,colname,ymd="%Y-%m-%d",inplace=False):
    '''
    将long_to_dt集成为对象
    colname：字符串或列表
    默认inplace=True，即修改原数据框
    【note】其实一句话就能解决：df['起始日期'] = pd.to_datetime(df['起始日期'], format='%Y%m%d')
    '''
    if str(type(colname))=="<class 'str'>":
        colname_list=[colname]
    else:
        colname_list=colname

    if inplace==True:
        data=df
    else:
        data = df.copy()
    long_date_df=data[colname_list]
    data[colname_list]=long_to_dt(long_date_df)
    if inplace==False:
        return data
    else:
        pass
PandasObject.long2dt=long2dt
def dt2long(df,colname,ymd="%Y%m%d",inplace=False):
    '''
    long2dt的反函数
    ymd是吧日期戳转换成的long目标格式
    '''
    import datetime
    if str(type(colname))=="<class 'str'>":
        colname_list=[colname]
    else:
        colname_list=colname

    if inplace==True:
        data=df
    else:
        data = df.copy()

    data[colname_list]=data[colname_list].applymap(lambda x:datetime.datetime.strftime(x, ymd))

    if inplace==False:
        return data
    else:
        pass
PandasObject.dt2long=dt2long
#%%从yyyymmdd长字符转换成yyyy-mm-dd的str
def long_to_str(long_date_df):
    '''
    从yyyymmdd长字符转换成yyyy-mm-dd的datetime
    long_date_df：单列数据框，必须是数据框！元素形如yyyymmdd的长字符串
    【返回值】吧yyyymmdd转换成datetime输出
    '''
    col_namne=long_date_df.columns.tolist()
    date_df = long_date_df.applymap(str).applymap(lambda s: s[:4]+'-'+s[4:6]+'-'+s[6:])
    return date_df
#%%从yyyy-mm-dd长字符转换成yyyy-mm-dd的datetime
#现在这个不工作。。。需要找时间调整一下！！！！！！！！！
def str_to_dt(long_date_df,ymd="%Y-%m-%d"):
    '''
    从yyyy-mm-dd长字符转换成yyyy-mm-dd的datetime
    long_date_df：单列数据框，必须是数据框！元素形如yyyy-mm-dd的长字符串
    【返回值】把yyyy-mm-dd转换成datetime输出
    '''
    date_df = long_date_df.applymap(str).applymap(lambda s: "{}-{}-{}".format(s[0:4],s[5:7],s[8:10]))
    date_df = date_df.applymap(lambda x: datetime.datetime.strptime(x, ymd))
    return date_df
def str2long(df,colname,inplace=False):
    '''
    yyyy-mm-dd的字符串列转化成yyyymmdd
    '''
    import datetime
    if str(type(colname))=="<class 'str'>":
        colname_list=[colname]
    else:
        colname_list=colname

    if inplace==True:
        data=df
    else:
        data = df.copy()

    data[colname_list]=data[colname_list].applymap(lambda x:''.join(x.split('-')))

    if inplace==False:
        return data
    else:
        pass
PandasObject.str2long=str2long
#%%前推计算当前日期【date_str】推【month_offset】个月的第【nth_week】个周【weekday】
def calculate_previous_nth_weekday(date_str, month_offset, nth_week, weekday):
    '''
    计算当前日期【date_str】推【month_offset】个月的第【nth_week】个周【weekday】
    在计算期货合约移仓的时候用到的
    举例：

    date_str = '2023-07-08'
    month_offset = -1
    nth_week = 4
    weekday = 'friday'  # 星期五，可以使用 "monday", "tuesday", ...等

    result = calculate_previous_nth_weekday(date_str, month_offset, nth_week, weekday)
    print(result)
    2023-06-16
    '''
    # 将日期字符串转换为日期时间格式
    current_date = pd.to_datetime(date_str)
    month_offset=-1*month_offset+1
    # 计算目标月份的第一天
    target_month_first_day = current_date - pd.DateOffset(months=month_offset) + pd.offsets.MonthBegin(0)

    # 计算目标月份的最后一天
    target_month_last_day = target_month_first_day + pd.offsets.MonthEnd(0)

    # 生成目标月份的所有日期
    dates_in_month = pd.date_range(target_month_first_day, target_month_last_day)

    # 映射星期几的参数值到0-6的范围
    weekday_mapping = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }

    # 将星期几参数值转换为小写字母
    weekday = weekday.lower()

    # 筛选出目标星期几的日期
    target_weekdays = dates_in_month[dates_in_month.weekday == weekday_mapping[weekday]]

    # 获取目标星期几的第nth_week个日期
    target_date = target_weekdays[nth_week - 1]

    return target_date.date()
#%%农历春节正月初一的列表
from lunardate import LunarDate
def spring_date_list(start,end):
    '''
    返回农历春节正月初一的列表，每一个元素是yyyy-mm-dd的字符串
    '''
    start = str(start[:4])
    end = str(end[:4])
    date_list=[str(LunarDate(x, 1, 1, False).toSolarDate())[:10] for x in range(int(start),int(end)+1)]
    return date_list
#%%寻找月末日期
def month_end(date_list):
    '''
    根据日期列表，找到每一个日期当月最后一天的日历日（不是交易日）
    '''
    #from pandas.tseries.offsets import MonthEnd
    date_final=[str(pd.to_datetime(x, format="%Y-%m-%d") + MonthEnd(0))[:10] for x in date_list]
    return date_final
#农历日期改公历
def solar2lunar(date):
    '''
    农历日期改公历，date:yyyy-mm-dd
    '''
    date_str=str(date)[:10]
    year,month,day=int(date_str[:4]),int(date_str[5:7]),int(date_str[8:10])
    lunar_date=LunarDate.fromSolarDate(year,month,day)
    lunar_date=f'''{lunar_date.year}-{lunar_date.month:02d}-{lunar_date.day:02d}'''
    return lunar_date
#公历日期改农历
def lunar2solar(date):
    '''
    公历日期改农历，date:yyyy-mm-dd
    '''
    date_str=str(date)[:10]
    year,month,day=int(date_str[:4]),int(date_str[5:7]),int(date_str[8:10])
    solar_date=str(LunarDate(year,month,day).toSolarDate())[:10]
    return solar_date
def lunar_index(df):
    '''
    数据框index从公历改为农历
    '''
    data=df.copy()
    data.index=pd.DataFrame(index=data.index).reset_index().applymap(solar2lunar).set_index('index').id0nm().index
    return data
PandasObject.lunar_index=lunar_index
def solar_lunar_map():
    '''
    映射公历日期农历日期
    solar字段：str,yyyy-mm-dd,公历日期
    lunar字段：str,yyyy-mm-dd,农历日期
    solar从2000年1月1日开始
    '''
    solar_lunar_map=pd.DataFrame(index=pd.date_range('2000-01-01',today(),freq='d')).reset_index().col('solar')
    solar_lunar_map=solar_lunar_map.applymap(lambda x:str(x)[:10])
    solar_lunar_map['lunar']=solar_lunar_map[['solar']].applymap(solar2lunar)
    return solar_lunar_map
##################################################################################################################################################









#%%数据框相关操作###################################################################################################################################
#%%Df冻结窗格   
from ipywidgets import interact, IntSlider
from IPython.display import display
def freeze_header(df, num_rows=30, num_columns=24, step_rows=1,
                  step_columns=1):
    """
    Freeze the headers (column and index names) of a Pandas DataFrame. A widget
    enables to slide through the rows and columns.

    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame to display
    num_rows : int, optional
        Number of rows to display
    num_columns : int, optional
        Number of columns to display
    step_rows : int, optional
        Step in the rows
    step_columns : int, optional
        Step in the columns

    Returns
    -------
    Displays the DataFrame with the widget
    """
    @interact(last_row=IntSlider(min=min(num_rows, df.shape[0]),
                                 max=df.shape[0],
                                 step=step_rows,
                                 description='rows',
                                 readout=False,
                                 disabled=False,
                                 continuous_update=True,
                                 orientation='horizontal',
                                 slider_color='purple'),
              last_column=IntSlider(min=min(num_columns, df.shape[1]),
                                    max=df.shape[1],
                                    step=step_columns,
                                    description='columns',
                                    readout=False,
                                    disabled=False,
                                    continuous_update=True,
                                    orientation='horizontal',
                                    slider_color='purple'))
    def _freeze_header(last_row, last_column):
        display(df.iloc[max(0, last_row-num_rows):last_row,max(0, last_column-num_columns):last_column])
#%%日期索引的数据集批量合并的常用函数
def merge(df_list,how='outer',col=None):
    '''
    col：【列表格式】merge之后的新数据框的列名称，如果不写，则啥也不做
    '''
    merged=reduce(lambda left,right:pd.merge(left,
                                      right,
                                      left_index=True,
                                      right_index=True,
                                      how=how,
                                      suffixes=(None," ")),df_list)
    merged.sort_index(ascending=True,inplace=True)
    if col!=None:
        merged.columns=col
    return merged
def mg(dataframe1,dataframe2,how='outer'):
    '''
    懒人函数，数据框连着写merge，多用于时间序列索引！！！
    '''
    if str(type(dataframe2))=="<class 'list'>":
        df = merge([dataframe1]+dataframe2, how=how)
    elif str(type(dataframe2))=="<class 'pandas.core.frame.DataFrame'>":
        df=merge([dataframe1,dataframe2],how=how)
    else :
        print("检查数据类型！")
    return df
PandasObject.mg=mg
#%%从Excel读取数据（读WIND导出的EDB数据最为常见）
def getdata(cd,name,sheet='Sheet1',header=1,usecols=None,start='',end='',index=True,print=False):
    '''
    cd:形如cd='C:\\Users\\13312\\Desktop\\'，要人为加转义字符！！！
    name：文件名
    sheet：工作表名
    默认header=1，把Excel表中的【第二行】作为dataframe的列名
    usecols：形如"A:F",用于读取指定的列
    '''
    df = pd.read_excel(cd + '\\' + name, sheet_name=sheet, header=header, usecols=usecols)

    if index==True:
        df.set_index(df.columns[0],inplace=True)
    df.sort_index(ascending=True,inplace=True)
    df.index.name=None

#    col=df.columns.tolist()
#    for i in range(len(col)):
#        if '.1' in col[i]:
#            col[i]=col[i].replace('.1','')
#    df.columns=col
    if print==True:
        print(df.columns.tolist())
#
    if start!='':
        df=df[start:]
    if end!='':
        df=df[:end]
    
    return df
#%%查看数据框的列名
def varli(df,v=False):
    varli_col=list(df.columns)
    if v==False:
        return varli_col
    else:
        return print(varli_col)
PandasObject.varli = varli
#%%按照日期字段分组，找到每一个日期字段组内，某个字段数值最大的5个样本
def df_nlargest(df,date_var,sort_var,num=5,top=True):
    '''
    按照【日期字段】【分组】，找到每一个日期【组内】，某个字段数值【最大的5个样本】
    df:SQL结构数据，包含日期字段和数值型待排序字段
    【返回值】经过筛选并排序后的dataframe
    '''
    data=df.copy()
    if top==True:
        result=data.groupby(date_var).apply(lambda x:x.nlargest(num,sort_var)).reset_index(drop=True).sort_values(by=[date_var,sort_var],ascending=[True,False])
    else:
        result=data.groupby(date_var).apply(lambda x:x.nsmallest(num,sort_var)).reset_index(drop=True).sort_values(by=[date_var,sort_var],ascending=[True,True])
    return result
PandasObject.df_nlargest=df_nlargest
def add_trendline(df,fit_start, trend_start ):
    '''
    fit_start：趋势线训练集起点
    trend_start：趋势线训练集终点、趋势线的起点
    '''
    df_copy = df.copy()
    if trend_start is None:
        trend_start = str(df_copy.index[-1])[:10]
    df = df_copy.copy().dropna()
    from sklearn.linear_model import LinearRegression

    for j in range(len(df.columns.tolist())):
        i = df.columns.tolist()[j]
        # Extract the data from the data frame for training and testing
        train_data = df[(df.index >= fit_start) & (df.index < trend_start)].loc[:, i]
        test_data = df[df.index >= trend_start].loc[:, i]

        # Fit the linear regression model
        x_train = np.array(range(len(train_data))).reshape(-1, 1)
        y_train = train_data.values
        model = LinearRegression().fit(x_train, y_train)

        # Generate trend line for the testing period
        x_test = np.array(range(len(train_data), len(train_data) + len(test_data))).reshape(-1, 1)
        trend_line = model.predict(x_test)

        # Add the trend line to the data frame
        trend_data_full = pd.DataFrame(test_data)
        trend_data_full["trend_line"] = trend_line
        trend_data_full["trend_line"] = trend_data_full["trend_line"] + trend_data_full.iloc[0, 0] - trend_data_full.iloc[0, 1]

        # Merge the trend data with the original data frame
        df_with_trend = pd.concat([df, trend_data_full["trend_line"]], axis=1)
        df_with_trend = df_with_trend.fillna(method="ffill")
        df_with_trend.rename(columns={'trend_line': i + '：趋势线'}, inplace=True)

    return df_with_trend
PandasObject.add_trendline=add_trendline
#%%热力图
def rlt(df,axis=0,cmap='Blues',dec=2):
    '''
    热力图，返回的不是数据框，不能参与后续运算！
    axis=0，默认是纵向着色，取1则是横向着色
    '''
    return df.style.set_precision(dec).background_gradient(cmap=cmap,axis=axis)
PandasObject.rlt = rlt
#%%季度序列求同比
def yoy(df,var_for_yoy,all=False):
    '''
    var_for_yoy是一个列表
    '''
    df_copy=df.copy()
    df_copy.sort_index(ascending=True,inplace=True)
    if all==False:
        try:
            df_copy[var_for_yoy]=100*(df_copy[var_for_yoy]/df_copy[var_for_yoy].shift(4)-1)
        except:
            pass
    else:
        df_copy=100*(df_copy/df_copy.shift(4)-1)
    return df_copy
PandasObject.yoy = yoy
#%%直接更改数据框的名称
def col(dataframe,col_name_new=[]):
    '''
    直接更改数据框的名称，返回改名后的数据框
    '''
    if str(type(col_name_new))=="<class 'str'>":
        col_name_new=[col_name_new]
    if col_name_new==[]:
        return dataframe
    else:
        df=dataframe.copy()
        df.columns=col_name_new
        return df
PandasObject.col=col
#%%直接更改数据框的索引名称
def indx(dataframe,index_name_new=[]):
    '''
    直接更改数据框的名称，返回改名后的数据框
    '''
    if str(type(index_name_new))=="<class 'str'>":
        index_name_new=[index_name_new]
    if index_name_new==[]:
        return dataframe
    else:
        df=dataframe.copy()
        df.index=index_name_new
        return df
PandasObject.indx=indx
#%%数据框增加结尾字符
def coladd(dataframe,col_add=''):
    '''
    数据框增加结尾字符
    '''
    df=dataframe.copy()
    df.columns=[x+col_add for x in df.columns.tolist()]
    return df
PandasObject.coladd=coladd
#计算两列的差
def col_dif(dataframe, order=1, pct=False):
    '''
    计算两列的差（或百分比），并对新的变量重命名
    dataframe：只有两列的数据框，计算这两列指标的差（或百分比）
    order：取值为1时，数据框的第一列为被减数，第二列为减数。取值为-1，则相反
    pct: 是否计算百分比，当为True时，计算 (第一列/第二列 - 1)
    【返回值】只有1列的数据框，保存计算好的两列差或百分比，列名为x1-x2（或x1/x2-1）
    '''
    df = dataframe.copy()
    var = list(df.columns)
    period = -1 * order
    if order == 1:
        first, second = 0, 1
    elif order == -1:
        first, second = 1, 0

    if pct:
        result = (df[var[first]] / df[var[second]] - 1).to_frame().rename(columns={0: var[first] + '/' + var[second] + '-1'})
    else:
        result = df.diff(axis=1, periods=period).iloc[:, [first]].rename(columns={var[first]: var[first] + '-' + var[second]})

    return result
PandasObject.col_dif=col_dif
def col_sum(dataframe):
    '''
    计算两列的和，并对新的变量重命名
    dataframe：只有两列的数据框，计算这两列指标的商
    【返回值】只有1列的数据框，保存计算好的两列商，列名为x1+x2
    '''
    df = dataframe.copy()
    var = list(df.columns)

    first, second = 0, 1

    result = df.iloc[:, first] + df.iloc[:, second]
    result=pd.DataFrame(result,columns=[var[first] + '+' + var[second]])
    return result
PandasObject.col_sum = col_sum
# 计算两列的商
def col_div(dataframe, order=1):
    '''
    计算两列的商，并对新的变量重命名
    dataframe：只有两列的数据框，计算这两列指标的商
    order：取值为1时，数据框的第一列为分子，第二列为分母。取值为-1，则相反
    【返回值】只有1列的数据框，保存计算好的两列商，列名为x1/x2
    '''
    df = dataframe.copy()
    var = list(df.columns)
    if order == 1:
        first, second = 0, 1
    elif order == -1:
        first, second = 1, 0
    result = df.iloc[:, first] / df.iloc[:, second]
    result=pd.DataFrame(result,columns=[var[first] + '/' + var[second]])
    return result
PandasObject.col_div = col_div
def col_mul(dataframe):
    '''
    计算两列的乘积，并对新的变量重命名
    dataframe：只有两列的数据框，计算这两列指标的乘积
    【返回值】只有1列的数据框，保存计算好的两列积，列名为x1*x2
    '''
    df = dataframe.copy()
    var = list(df.columns)

    first, second = 0, 1

    result = df.iloc[:, first] * df.iloc[:, second]
    result=pd.DataFrame(result,columns=[var[first] + '*' + var[second]])
    return result
PandasObject.col_mul = col_mul

#%%对单列的滞后项进行计算，像Excel那样
def col_inner_lag(df, col, lag_list, how='mean'):
    shifted_cols = [df[col].shift(lag) for lag in lag_list]

    if how == 'mean':
        result = pd.concat(shifted_cols, axis=1).mean(axis=1)
    elif how == 'sum':
        result = pd.concat(shifted_cols, axis=1).sum(axis=1)
    else:
        raise ValueError("Invalid value for 'how'. Use 'mean' or 'sum'.")

    return result
PandasObject.col_inner_lag = col_inner_lag
#%%指标列原地求和
def col_inplace_sum(df, list1, list2):
    '''
    根据list1中的多个列进行求和，并将求和结果替换原有的list1列，然后将求和结果放置在list1的位置，并给这些新列取名为list2中的元素
    dataframe: 输入的数据框
    list1: 需要求和的指标列名的列表
    list2: 求和后的新列名，只能是一个元素的列表
    '''
    dataframe=df.copy()
    if len(list2) != 1:
        raise ValueError("list2 must have exactly one element.")

    sum_result = dataframe[list1].sum(axis=1)
    sum_column_name = list2[0]

    # 求和后的新列放在原有list1的位置
    dataframe.insert(dataframe.columns.get_loc(list1[0]), sum_column_name, sum_result)

    # 删除原有list1的指标列
    dataframe.drop(list1, axis=1, inplace=True)
    return dataframe
PandasObject.col_inplace_sum=col_inplace_sum
#%%把列格式改成字符串
def col2str(df):
    '''
    日期列变为str
    '''
    import datetime
    data=df.copy()
    data.columns=[datetime.datetime.strftime(x,"%Y-%m-%d") for x in df.columns]
    return data
PandasObject.col2str=col2str
#工作文件读取#########################################################################################################################
import shelve
# %%用于shelve剔除的预定义变量
yu_ding_yi = ['In', 'NamespaceMagics', 'Out', '_', '_1', '_2', '_3', '_Jupyter', '__', '___', '__builtin__',
              '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', '_dh', '_getshapeof',
              '_getsizeof', '_i', '_i1', '_i2', '_i3', '_i4', '_ih', '_ii', '_iii', '_nms', '_oh', 'exit',
              'get_ipython', 'getsizeof', 'json', 'np', 'quit', 'var_dic_list', 'shelve']
# %%保存当前工作空间
def save_workspace(name_of_workplace, globals_passthrough, dir_list, yu_ding_yi=yu_ding_yi):
    '''
    globals_passthrough的位置务必填写globals()
    dir_list的位置务必填写dir()
    举个例子：save_workspace('美股研究',globals(),dir())，这样就可以了，在本地存了三个文件
    '''
    used_var = diff_of_two_list(dir_list, yu_ding_yi)
    my_shelf = shelve.open(name_of_workplace, 'n')  # 'n' for new
    for key in used_var:
        try:
            my_shelf[key] = globals_passthrough[key]
        except:
            1
    my_shelf.close()
# %%读取工作空间
def read_workspace(name_of_workplace, globals_passthrough):
    '''
    第二个参数填写globals()就可以
    '''
    with shelve.open(name_of_workplace) as data:
        for key in data:
            try:
                globals_passthrough[key] = data[key]
            except:
                1
######################################################################################################################################
#%%降序排序快速
def sortd(dataframe,ascending=False):
    '''
    对数据框按列降序排序，满足日常需求。单列或多列
    sortd里面的d表示down，即降序
    '''
    df=dataframe.copy()
    return df.sort_values(by=df.columns.tolist(),ascending=ascending)
PandasObject.sortd = sortd

#%%列表连接成字符串
def join_list(list_input,pare=False):
    '''
    连接列表元素形成字符串，便于放到SQL中查询
    '''
    a = list_input
    b = "','".join(a)
    b = "'" + b + "'"
    if pare==True:
        b="("+b+")"
    return b
#%%百分比
def pct(df,periods = 1,fill_method = 'pad',limit = None,freq = None):
    '''
    简化pct_change
    '''
    return df.pct_change(periods = periods,fill_method = fill_method,limit = limit,freq = freq)
PandasObject.pct = pct
#%%百分比例
def pp(df):
    '''
    百分比例，针对时间序列数据，计算每一个指标在所有指标里的占比
    '''
    return df.apply(lambda x: x / x.sum(), axis=1)
PandasObject.pp = pp
# #%%去除行列的名称
# def index_name_none(dataframe):
#     '''
#     去除行列的名称
#     '''
#     df=dataframe.copy()
#     df.index.name=None
#     df.columns.name=None
#     return df
# PandasObject.index_name_none = index_name_none
def nameas(series,name=None):
    '''
    为series赋名
    '''
    series_copy=series.copy()
    series_copy.name=name
    return series_copy
PandasObject.nameas = nameas
#%%把数据框列里面的指标做领先滞后处理
def lead(df,lead_setting=[0, 0]):
    '''
    把数据框列里面的指标做领先滞后处理
    lead：双元素列表，第一个元素表示第几个指标要领先，第二个表示领先多少期。要么是空列表，要么一起传入两个参数，只传一个参数会报错
    '''
    df_copy = df.copy()
    df_copy.sort_index(inplace=True,ascending=True)
    name_list_copy = df_copy.columns.to_list()

    if lead_setting[1] != 0:
        name_list_copy[lead_setting[0] - 1] = name_list_copy[lead_setting[0] - 1] + "_领先" + str(lead_setting[1]) + "期"
        df_copy[[df_copy.columns[lead_setting[0] - 1]]] = df_copy[[df_copy.columns[lead_setting[0] - 1]]].shift(lead_setting[1])
    return df_copy.col(name_list_copy)
PandasObject.lead=lead
def h(data,n=5):
    '''
    查看头几行，懒人
    '''
    return data.head(n)
PandasObject.h=h
def t(data,n=5):
    '''
    查看尾几行，懒人
    '''
    return data.tail(n)
PandasObject.t=t
def uni(df):
    '''
    归一化
    '''
    df_copy=df.copy()
    df_copy.sort_index(ascending=True,inplace=True)
    for i in range(df_copy.shape[1]):
        df_copy.iloc[:, i] = df_copy.iloc[:, i] / df_copy.iloc[0, i]
    return df_copy
PandasObject.uni=uni
#%%移除索引的名称
def index0name(df):
    # 如果 df 的索引是多级的，将其全部重置为 None
    if isinstance(df.index, pd.MultiIndex):
        new_index = pd.MultiIndex.from_tuples([None] * len(df.index))
        df.index = new_index
    else:
        df.index.name = None

    # 如果 df 的列名是多级的，将其全部重置为 None
    if isinstance(df.columns, pd.MultiIndex):
        new_columns = pd.MultiIndex.from_tuples([None] * len(df.columns))
        df.columns = new_columns
    else:
        df.columns.name = None

    return df
PandasObject.index0name=index0name
# def id0nm(dataframe):
#     '''
#     在处理多级索引的时候遇到了问题，需要后续调试
#     '''
#     df=dataframe.copy()
#     # 如果 df 的索引是多级的，将其全部重置为 None
#     if isinstance(df.index, pd.MultiIndex):
#         new_index = pd.MultiIndex.from_tuples([None] * len(df.index))
#         df.index = new_index
#     else:
#         df.index.name = None
#
#     # 如果 df 的列名是多级的，将其全部重置为 None
#     if isinstance(df.columns, pd.MultiIndex):
#         new_columns = pd.MultiIndex.from_tuples([None] * len(df.columns))
#         df.columns = new_columns
#     else:
#         df.columns.name = None
#
#     return df
# PandasObject.id0nm=id0nm
def id0nm(df):
    df_copy = df.copy()
    num_index_levels = df_copy.index.nlevels
    df_copy = df_copy.rename_axis(index=[None] * num_index_levels)

    num_column_levels = df_copy.columns.nlevels
    df_copy = df_copy.rename_axis(columns=[None] * num_column_levels)

    return df_copy
PandasObject.id0nm=id0nm
def zscore(dataframe):
    '''
    求时间序列索引的数据框的Zscore
    '''
    return  (dataframe-dataframe.mean()) / dataframe.std()
PandasObject.zscore = zscore

#%%返回参数变量的名称
import inspect


def store_variable_name(variable):
    """
    返回变量的名称
    # 示例调用
    my_variable = 10
    variable_name = store_variable_name(my_variable)
    print(variable_name)  # 输出 "my_variable"
    """
    frame = inspect.currentframe().f_back  # 获取调用栈帧
    local_vars = frame.f_locals  # 获取局部变量表
    for name, value in local_vars.items():
        if value is variable:
            return name

    return None


# 定义解析函数。把python中数值为列表的数据框存为Excel后再读取之后转化为原先的列表格式（否则列表在Excel中变成了字符串）
import ast
from ast import literal_eval
def parse_string_to_list(string):
    if isinstance(string, str):
        # 使用 literal_eval() 解析字符串为列表
        try:
            elements = literal_eval(string)
            return elements
        except (ValueError, SyntaxError):
            return None
    else:
        return None


import datetime

import sys
import pandas as pd
def varinspector(LOCALS):
    '''
    用法：varinspector(locals())
    这段代码目前有bug，只能写在jupyter里，不能从包中调用。之后一定要解决他。
    '''
    variables = list(LOCALS.keys())
    data = pd.DataFrame(columns=['Variable', 'Shape', 'Data Type', 'Memory', 'Unit'])

    for var in variables:
        try:
            if not var.startswith('_'):
                memory = sys.getsizeof(eval(var)) / (1024 ** 3)  # 转换为GB
                dtype = type(eval(var)).__name__  # 获取变量的数据类型

                # 获取变量的数据形状（根据变量类型进行适当处理）
                if isinstance(eval(var), pd.DataFrame):
                    shape = str(eval(var).shape)
                elif isinstance(eval(var), pd.Series):
                    shape = str(eval(var).shape)
                elif isinstance(eval(var), (list, tuple)):
                    shape = f"({len(eval(var))},)"
                else:
                    shape = ""

                unit = 'GB'

                data = data.append(
                    {'Variable': var, 'Shape': shape, 'Data Type': dtype, 'Memory': memory, 'Unit': unit},
                    ignore_index=True)
        except:
            pass

    data['Memory'] = data['Memory'].astype('float').round(3)
    data = data.sort_values(['Memory'], ascending=False)
    data.index = range(data.shape[0])
    print("总内存占用：",round(data.Memory.sum(),3),"GB")
    return data
#%%保存当前运行的jupyternotebook为html
def save_html(name):
    '''
    保存当前运行的jupyternotebook为html,不含代码的那种！
    '''
    import subprocess
    path = cd
    command = f'cd /d {path} && jupyter nbconvert --to html --no-input "{name}"'
    subprocess.call(command, shell=True)
#%%数据框连续操作，生成新列
def cal(data,exp="",varname=""):
    '''
    exp varname 都是字符串
    不定义新数据框，通过表达式直接在原有数据框上进行操作
    举例：score_sum是一个只含有'股票'仓位的数据框，希望生成债券仓位，则
    score_sum.cal("1-df['股票']","债券")
    【注意】这里的形参统一用"df"！！！写其他的，函数识别不出来
    返回的结果是生成好了的数据框
    '''
    df=data.copy()
    df[varname]=eval(exp)
    return df
PandasObject.cal=cal
def div_col(data,col_name):
    '''
    区别于col_div，div_col是把一个数据框的所有列除以某一列。
    【返回值】不含被除列的其他列的百分比
    '''
    df=data.copy().applymap(lambda x:np.nan)
    for col in df.columns.tolist():
        df.loc[:,col]=data.apply(lambda x:x[col]/x[col_name],axis=1).values
    df.drop(col_name,axis=1,inplace=True)
    # display(df)
    return df
PandasObject.div_col=div_col

def col_name_map(data_repo, idata_map, source_col, target_col):
    """
    根据提供的数据框中的映射关系，重命名 data_repo 中的列名。

    参数:
    - data_repo: DataFrame
    - idata_map: DataFrame
    - source_col: 字符串，源列名
    - target_col: 字符串，目标列名

    返回:
    - 重命名后的 DataFrame
    """
    # 将映射关系数据框转换为字典
    col_mapping = dict(zip(idata_map[source_col], idata_map[target_col]))

    # 根据映射重命名 data_repo 中的列
    data_repo_renamed = data_repo.rename(columns=col_mapping)

    return data_repo_renamed
PandasObject.col_name_map=col_name_map


