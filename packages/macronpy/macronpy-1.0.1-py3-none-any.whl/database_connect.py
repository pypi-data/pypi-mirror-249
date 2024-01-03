from macronpy.macro import *
from macronpy.basic_package import *
import pandas as pd
from typing import List
#%%Oracle连接Wind底层数据库#####################################################################################################################################
try :
    wdb = cx_Oracle.connect('hqreader','Hqreader#2022','172.20.0.113:1521/winddb')
except:
    wdb=1
try :
    jydb = cx_Oracle.connect('mdm','mdmqaz','172.20.0.121:1521/emdm')
except:
    jydb=1
try :
    crdb = cx_Oracle.connect('ZHGLB','DbTM%UIbb0','172.20.0.84:1521/newdpdb')
except:
    crdb=1
# # %%中再资产数据映射
# cramc_indicator_info_position = getdata("d:\\Documents And Settings\\niupeiyi\\桌面\\工作文件\\【账户数据分析】\\【组合部数据系统】",
#                                         '组合管理部接口数据字典.xlsx',
#                                         'V_ZHGLB_POSITION_DATA（持仓信息）', header=0, index=False)
# cramc_indicator_info_trade = getdata("d:\\Documents And Settings\\niupeiyi\\桌面\\工作文件\\【账户数据分析】\\【组合部数据系统】",
#                                      '组合管理部接口数据字典.xlsx',
#                                      'V_ZHGLB_TRADE_MOVEMENT（交易信息）', header=0, index=False)
# cramc_indicator_info_cash = getdata("d:\\Documents And Settings\\niupeiyi\\桌面\\工作文件\\【账户数据分析】\\【组合部数据系统】",
#                                      '组合管理部接口数据字典.xlsx',
#                                      'v_zhglb_diff_balance（资金调拨记录表）', header=0, index=False)
# def crmap():
#     '''
#     展示映射表
#     '''
#     print("持仓表")
#     display(cramc_indicator_info_position)
#     print("交易表")
#     display(cramc_indicator_info_trade)
#     print("现金表")
#     display(cramc_indicator_info_cash)
#
# def crcn(data, table='position'):
#     '''
#     中再数据库的英文字段改成中文
#     '''
#     if table == 'position':
#         table_map = cramc_indicator_info_position
#     elif table == 'trade':
#         table_map = cramc_indicator_info_trade
#     elif table=='cash':
#         table_map = cramc_indicator_info_cash
#
#     data_col = data.columns.tolist()
#     # display(table_map)
#     # display(data_col)
#     table_map['名称']=table_map['名称'].str.upper()
#     col_cn = sort_by_list(table_map[table_map['名称'].isin(data_col)], '名称', data_col)['注释'].tolist()
#     data_new = data.copy()
#     data_new.columns = col_cn
#     return data_new
#
#
# PandasObject.crcn = crcn
#
#
# def cren(list_cn, table='position'):
#     '''
#     中文名的中再字段列表转成英文
#     '''
#     if table == 'position':
#         table_map = cramc_indicator_info_position
#     elif table == 'trade':
#         table_map = cramc_indicator_info_trade
#     elif table == 'cash':
#         table_map = cramc_indicator_info_cash
#     # display(table_map)
#     # print(list_cn)
#     col_en = sort_by_list(table_map[table_map['注释'].isin(list_cn)], '注释', list_cn)['名称'].tolist()
#     return col_en
#
#

#
#
# def generate_sql_cramc(select_fields: List[str], filter_conditions: List[str], start: str, end: str,
#                        frequency: str, calendar=False, table='position') -> str:
#     '''
#     特别针对中再数据库涉及的sql语句生成函数
#     '''
#     start_date = start
#     end_date = end
#     select_fields_en = cren(select_fields, table)
#     filter_conditions_new = list_str_replace(filter_conditions, select_fields, cren(select_fields, table))
#     # 将起始日期和截止日期转换成datetime对象
#     if calendar == False:
#         filter_dates = trade_date_wind(start_date, end_date, frequency, 'last').index.tolist()
#     else:
#
#         filter_dates = calendar_date_pd(start_date, end_date, freq=frequency, how='last').index.tolist()
#
#     if table == 'position':
#         table_name = 'V_ZHGLB_POSITION_DATA'
#     elif table == 'trade':
#         table_name = 'V_ZHGLB_TRADE_MOVEMENT'
#     elif table == 'cash':
#         table_name = 'v_zhglb_diff_balance'
#
#     if len(filter_dates) < 1000:
#         # 将日期格式化为字符串
#         filter_dates_str = [d.strftime('%Y-%m-%d')[:4] + d.strftime('%Y-%m-%d')[5:7] + d.strftime('%Y-%m-%d')[8:10] for
#                             d in
#                             filter_dates]
#
#         # 构建 SQL 语句
#         sql = "SELECT " + ", ".join(select_fields_en) + "\n"
#         sql += f"FROM {table_name}\n"
#         sql += "WHERE CALC_DATE IN (\n"
#         sql += "    " + ",\n    ".join("TO_DATE('{}', 'YYYY-MM-DD')".format(date) for date in filter_dates_str) + "\n"
#         sql += ")"
#     else:
#         start_long = start_date[:4] + start_date[5:7] + start_date[8:10]
#         end_long = end_date[:4] + end_date[5:7] + end_date[8:10]
#
#         # 构建 SQL 语句
#         sql = "SELECT " + ", ".join(select_fields_en) + "\n"
#         sql += f"FROM {table_name}\n"
#         sql += f"WHERE CALC_DATE between   TO_DATE('{start_long}', 'YYYY-MM-DD')   and  TO_DATE('{end_long}', 'YYYY-MM-DD')  \n"
#
#     if filter_conditions_new:
#         sql += "\n    AND " + "\n    AND ".join(filter_conditions_new)
#     return sql
#
#
# def crdata(select_fields, filter_conditions, start_date=last_day(TODAY), end_date=TODAY, frequency='d', calendar=False,
#            table='position'):
#     '''
#     中再组合部专属取数据函数，很酷的，未来会持续完善
#     select_fields：字段名，形如['日期', '委托人', '管理人','资产大类一级','证券名称','市值']
#     filter_conditions：筛选条件，形如["管理人 in  ('外部委托')"]，里面的每一个字符串满足sql语法
#     start_date：默认昨天
#     end_data：默认今天。默认的日期其实是取的昨天的数据，因为白天取数据的时候今天的还没更新
#     frequency：频率参数，默认'd'，可以是'm','q','y'
#     table：'position'或者'trade'或者'cash'，对应持仓表和交易表和现金表
#     【NOTE】table参数一旦指定，就必须和select_fields中的字段兼容。否则在cren这个函数调用的过程中会报错
#     '''
#     data_result = pd.read_sql(generate_sql_cramc(select_fields, filter_conditions, start_date, end_date, frequency, calendar, table), crdb)
#     data_result = data_result.crcn(table)
#     return data_result
# def crwtr():
#     '''
#     委托人列表
#     '''
#     return ['中再集团','2 财再(China PropertyRe)','3 寿再(China LifeRe)','4 大地(China Continent)','9 寿再香港(China LifeRe - HK)']
# def crglr():
#     '''
#     管理人列表
#     '''
#     return ['5 资产(CRAMC)','中再资产香港子公司','外部委托']
#%%万得数据库sql取数据函数
#半年的还有待继续探索！超过1000的要照着cramc的那个改一下
def generate_sql_wdb(table_name, date_str, select_fields: List[str], filter_conditions: List[str], start_date: str,
                     end_date: str,
                     frequency: str, calendar=False) -> str:
    '''
    特别针对wind数据库涉及的sql语句生成函数
    date_str：日期标识，这里填入参数之后，select_fields中可以省略日期字段
    '''
    start=start_date
    end=end_date
    frequency=frequency.upper()
    # 将起始日期和截止日期转换成datetime对象
    if calendar == False:
        filter_dates = trade_date_wind(start_date, end_date, frequency, 'last').index.tolist()
    else:
        filter_dates = pd.date_range(start_date, end_date, freq=frequency).tolist()
    # print(filter_dates)
    # 将日期格式化为字符串
    filter_dates_str = [d.strftime('%Y-%m-%d')[:4] + d.strftime('%Y-%m-%d')[5:7] + d.strftime('%Y-%m-%d')[8:10] for d in
                        filter_dates]

    select_fields = [date_str] + select_fields

    # 构建 SQL 语句
    sql = "SELECT " + ", ".join(select_fields) + "\n"
    sql += "FROM wind." + table_name + "\n"
    sql += "WHERE " + date_str + " IN (\n"
    sql += "    " + ",\n    ".join(date for date in filter_dates_str) + "\n"
    sql += ")"
    if filter_conditions:
        sql += "\n    AND " + "\n    AND ".join(filter_conditions)
    return sql
def wdsdata(table_name,date_str,select_fields, filter_conditions,
            start_date, end_date, frequency,calendar=False,db=wdb):
    '''
    WDS取数据函数，很酷的，未来会持续完善
    calendar：默认是FALSE，即交易日。TRUE的话是日历日
    '''
    data_result=pd.read_sql(generate_sql_wdb(table_name,date_str,select_fields, filter_conditions, start_date, end_date, frequency,calendar),db)
    return data_result

def trade_date_wind(start, end, freq='d', how='last'):
    '''
    利用WDS数据库生成交易日序列
    how：'first'或'last'，默认last
    '''
    trade_date_sql = "select TRADE_DAYS,S_INFO_EXCHMARKET from wind.AShareCalendar order by 1"
    trade_date_wind = pd.read_sql(trade_date_sql, wdb)
    trade_date_wind_basic = trade_date_wind.query("S_INFO_EXCHMARKET=='SSE'").drop_duplicates()[['TRADE_DAYS']]
    trade_date_wind_basic = trade_date_wind_basic.long2dt('TRADE_DAYS').set_index('TRADE_DAYS')
    freq = freq.upper()
    if how == 'last':
        # 日
        if freq == 'D':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.month,
                 trade_date_wind_basic.index.day]).tail(1)
        # 周
        elif freq == 'W':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.month,
                 trade_date_wind_basic.index.week]).tail(1)
        # 月
        elif freq == 'M':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.month]).tail(1)
        # 季
        elif freq == 'Q':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.quarter]).tail(1)
        # 半年
        elif freq == '6M':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.quarter]).tail(1)
            trade_date = trade_date.loc[trade_date.index.month.isin([6, 12])]
        # 年
        elif freq == 'Y':
            trade_date = trade_date_wind_basic.groupby([trade_date_wind_basic.index.year]).tail(1)

    elif how == 'first':
        # 日
        if freq == 'D':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.month,
                 trade_date_wind_basic.index.day]).head(1)
        # 周
        elif freq == 'W':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.month,
                 trade_date_wind_basic.index.week]).head(1)
        # 月
        elif freq == 'M':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.month]).head(1)
        # 季
        elif freq == 'Q':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.quarter]).head(1)

        # 半年
        elif freq == '6M':
            trade_date = trade_date_wind_basic.groupby(
                [trade_date_wind_basic.index.year, trade_date_wind_basic.index.quarter]).head(1)
            trade_date = trade_date.loc[trade_date.index.month.isin([1, 7])]
        # 年
        elif freq == 'Y':
            trade_date = trade_date_wind_basic.groupby([trade_date_wind_basic.index.year]).head(1)

    trade_date.index.name = None
    return trade_date[start:end]
    # return trade_date
def calendar_date_pd(start, end, freq='d', how='last'):
    '''
    利用pd生成日期序列
    '''
    if start!=end:
        date_basic=pd.DataFrame(index=pd.date_range(start, end,freq='d'))
        freq = freq.upper()
        if how == 'last':
            # 日
            if freq == 'D':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.month,
                     date_basic.index.day]).tail(1)
            # 周
            elif freq == 'W':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.month,
                     date_basic.index.week]).tail(1)
            # 月
            elif freq == 'M':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.month]).tail(1)
            # 季
            elif freq == 'Q':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.quarter]).tail(1)
            # 半年
            elif freq == '6M':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.quarter]).tail(1)
                final_date = final_date.loc[final_date.index.month.isin([6, 12])]
            # 年
            elif freq == 'Y':
                final_date = date_basic.groupby([date_basic.index.year]).tail(1)

        else:
            # 日
            if freq == 'D':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.month,
                     date_basic.index.day]).head(1)
            # 周
            elif freq == 'W':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.month,
                     date_basic.index.week]).head(1)
            # 月
            elif freq == 'M':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.month]).head(1)
            # 季
            elif freq == 'Q':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.quarter]).head(1)
                final_date = final_date.loc[final_date.index.month.isin([1,4,7,10])]

            # 半年
            elif freq == '6M':
                final_date = date_basic.groupby(
                    [date_basic.index.year, date_basic.index.quarter]).head(1)
                final_date = final_date.loc[final_date.index.month.isin([1, 7])]
            # 年
            elif freq == 'Y':
                final_date = date_basic.groupby([date_basic.index.year]).head(1)

        final_date.index.name = None
        return final_date[start:end]
    else:
        df=pd.DataFrame(index=[pd.date_range(start=start, periods=10,freq='d')[0]])
        return df
def trade_and_calendar(start, end, freq='d', how=['last', 'last']):
    '''
    【返回值】数据框格式，是交易日和对应日历日的并列时间戳
    '''
    date_far = pd.date_range(start=end, periods=10, freq=freq)[-1].strftime("%Y-%m-%d")

    if how == 'first' or how == 'last':
        how = [how, how]
    df = merge([day_ts_index(start, date_far, freq, 1, how[0]).reset_index().col('trade_date'),
                day_ts_index(start, date_far, freq, 0, how[1]).reset_index().col('calendar_date')], how='outer')
    df = df[(df.trade_date <= end) | (df.calendar_date <= end)]
    return df
#%%数据框时间索引在交易日和日历日之间转换
def index_trade_calendar_convert(df, to_trade_date=True, freq='q', how=['last', 'last']):
    '''
    注：这个函数只能用一次。
    如果从交易日转换到日历日，比这个函数更好用的是resample！更直接！
    如果是从日历日转换到交易日，那么这个函数将会起到作用
    '''
    trade_calendar_df = trade_and_calendar(df.index.min(), df.index.max(), freq=freq, how=how)
    #     display(trade_calendar_df)
    if to_trade_date:
        mapped_index = trade_calendar_df.set_index('calendar_date')['trade_date']
    else:
        mapped_index = trade_calendar_df.set_index('trade_date')['calendar_date']

    df_mapped = df.copy()
    df_mapped.index = df_mapped.index.map(mapped_index)
    return df_mapped
PandasObject.index_trade_calendar_convert=index_trade_calendar_convert
def last_trade_day(date=today()):
    '''
    返回距离输入日期最近的上一个交易日
    '''
    return trade_date_wind(last_day(date,10),date).index[-2].strftime("%Y-%m-%d")
def get_closed_trade_date(date, offset=-1):
    '''
    date：str,yyyy-mm-dd格式
    返回距离输入日期最近的N个交易日
    offset<0，日期向前推；offset>0，日期向后推
    注，如果日期是一个日历日周末，这个函数给出的结果和wind插件会有所不同，这块之后调整下
    '''
    if type(date)!=str:
        date=str(date)[:10]
    if ('-' not in date) and (len(date)==8):
        DATE=date[:4]+"-"+date[4:6]+"-"+date[6:8]
    elif ('-'  in date) and (len(date)==10):
        DATE=date

    if offset < 0:
        trade_date_list = trade_date_wind(last_day(DATE, (abs(offset) + 5) * 2), DATE)
        date_bound=offset-1
    elif offset > 0:
        trade_date_list = trade_date_wind(DATE, last_day(DATE, -1 * ((abs(offset) + 5) * 2)))
        date_bound=offset
    # print(trade_date_list)
    return trade_date_list.index[date_bound].strftime("%Y-%m-%d")
#%%返回一个只有日期序列索引的空数据框
def day_ts_index(start_date, end_date, freq, trade=False,how='last'):
    '''
    返回一个只有日期序列索引的空数据框
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
        # date_index_df = pd.DataFrame(index=w.tdays(beginTime=start, endTime=end, period=freq).Data[0])
        date_index_df = pd.DataFrame(index=trade_date_wind(start=start, end=end, freq=freq,how=how).index)
    else:
        date_index_df = pd.DataFrame(index=calendar_date_pd(start=start, end=end, freq=freq,how=how).index)

    return date_index_df
#%%生成数据框存对应频率的起点和终点
def start_end_df(start_date, end_date, freq, trade=False):
    '''
    【返回值】数据框，start,end两列，存对应频率的起点和终点
    '''
    start_df=day_ts_index(start_date, end_date, freq, trade=trade,how='first').reset_index().col('start')
    end_df=day_ts_index(start_date, end_date, freq, trade=trade,how='last').reset_index().col('end')
    result=pd.merge(start_df,end_df,left_index=True,right_index=True,how='inner')
    result=result.applymap(lambda x:x.strftime("%Y-%m-%d"))
    return result
#%%把day_ts_index生成的日期列索引空df转换成【长日期】list
def longdate_list(date_index_df):
    '''
    把day_ts_index生成的日期列索引空df转换成【长日期】list
    '''
    import datetime
    date_list=[datetime.datetime.strftime(x,"%Y-%m-%d")[:4]+datetime.datetime.strftime(x,"%Y-%m-%d")[5:7]+datetime.datetime.strftime(x,"%Y-%m-%d")[8:10] for x in date_index_df.index.tolist()]
    return date_list
#%%生成字符串拼接后的日期
def longdate_str(date_index_df):
    '''
    生成字符串拼接后的日期
    '''
    import datetime
    date_list=[datetime.datetime.strftime(x,"%Y-%m-%d")[:4]+datetime.datetime.strftime(x,"%Y-%m-%d")[5:7]+datetime.datetime.strftime(x,"%Y-%m-%d")[8:10] for x in date_index_df.index.tolist()]
    date_str="\',\'".join(date_list)
    return date_str
#%%把long日期yyyymmdd改成yyyy-mm-dd的字符串
def longdate2str(longdate):
    '''
    生成字符串拼接后的日期
    '''
    import datetime
    date_str=longdate[:4]+"-"+longdate[4:6]+"-"+longdate[6:8]
    return date_str
#%%多股票时间序列宽表
def tsd(code_list,
        start_date,
        end_date,
        indicator='S_DQ_CLOSE',
        tb='AShareEODPrices',
        db=wdb,
        freq='D',
        how='last'):
    '''
    利用Oracle连接Wind底层数据库提取股票相关数据，存为宽表，行为时间、列为股票
    【注意】默认只能个股，不能指数！指数的表要另行指定
    start、end:'yyyy-mm-dd'
    indicator:指标名称，从Wind字典复制
    【tb】:表名称，默认为AShareEODPrices，可传AShareEODPrices、AIndexEODPrices、AIndexWindIndustriesEOD、AIndexValuation、CBIndexEODPrices
    日期是日历日，非交易日数据用前一个交易日数据填充
    '''
    if str(type(code_list))!="<class 'str'>":
        code_str="\',\'".join(code_list)
    else:
        code_str=code_list

    #日期格式必须是字符串，否则需要在这里转换成字符串！！！
    if str(type(start_date))!="<class 'str'>":
        start=datetime_to_str(start_date)
    else:
        start=start_date

    if str(type(end_date))!="<class 'str'>":
        end=datetime_to_str(end_date)
    else:
        end=end_date

    
    start_long=start[:4]+start[5:7]+start[8:10]
    end_long=end[:4]+end[5:7]+end[8:10]

    date_index_ = pd.DataFrame(index=pd.date_range(start, end, freq=freq))
    # date_index_=eval("date_index_.resample('" + freq + "')." + how + "()")
    # #注意这里传入any的一定是长日期！！！
    date_list=[datetime.strftime(x,"%Y-%m-%d")[:4]+datetime.strftime(x,"%Y-%m-%d")[5:7]+datetime.strftime(x,"%Y-%m-%d")[8:10] for x in date_index_.index.tolist()]
    # date_str="\',\'".join(date_list)

    date_index_series = day_ts_index(start, end, freq, trade=True)
    date_str = longdate_str(date_index_series)

    try:

        time_mark='TRADE_DT'

        if len(date_list)<1000:
            sql="select s_info_windcode,"+indicator+","+time_mark+"  \n" \
            "from wind."+tb+"  \n" \
            "where s_info_windcode = any("+'\''+code_str+'\''+") \n" \
            "and "+time_mark+"= any("+'\''+date_str+'\''+") \n" \
            "order by s_info_windcode"
        else:
            sql="select s_info_windcode,"+indicator+","+time_mark+"  \n" \
            "from wind."+tb+"  \n" \
            "where s_info_windcode = any("+'\''+code_str+'\''+") \n" \
            "and "+time_mark+" between ("+'\''+start_long+'\''+") and ("+'\''+end_long+'\''+") \n" \
            "order by s_info_windcode"
        df = pd.read_sql(sql, db)
    except:
        time_mark = 'REPORT_PERIOD'
        if len(date_list)<1000:
            sql="select s_info_windcode,"+indicator+","+time_mark+"  \n" \
            "from wind."+tb+"  \n" \
            "where s_info_windcode = any("+'\''+code_str+'\''+") \n" \
            "and "+time_mark+"= any("+'\''+date_str+'\''+") \n" \
            "order by s_info_windcode"
        else:
            sql="select s_info_windcode,"+indicator+","+time_mark+"  \n" \
            "from wind."+tb+"  \n" \
            "where s_info_windcode = any("+'\''+code_str+'\''+") \n" \
            "and "+time_mark+" between ("+'\''+start_long+'\''+") and ("+'\''+end_long+'\''+") \n" \
            "order by s_info_windcode"
        df = pd.read_sql(sql, db)

    info_tb='WindCustomCode'

    sql2="select S_INFO_WINDCODE,S_INFO_NAME from wind."+info_tb+" where s_info_windcode = any("+'\''+code_str+'\''+") "
    

    df2=pd.read_sql(sql2,db)
    df3=pd.merge(df,df2,on='S_INFO_WINDCODE',how='inner')
    
    df3[[time_mark]]=long_to_dt(df3[[time_mark]])

    col=df3['S_INFO_NAME'].drop_duplicates().tolist()

    df3=df3.pivot_table(values=indicator,index=time_mark,columns='S_INFO_NAME',dropna=False) #这里的dropna参数的设定很重要！！！
    df3=df3[col]
    df3.index.name,df3.columns.name=None,None

    df3=date_index(df3)
    return df3
#%%这个tsd_rpt还是有问题的！！！有一些问题吧
def tsd_rpt(code_list,
            start,
            end,
            indicator='ST_BORROW',
            tb='AShareBalanceSheet',
            db=wdb,
            freq='Q',
            how='last',
            rpt_type='408001000'):
    '''
    利用Oracle连接Wind底层数据库提取股票相关数据，存为宽表，行为时间、列为股票
    【注意】默认只能个股，不能指数！指数的表要另行指定
    start、end:'yyyy-mm-dd'
    indicator:指标名称，从Wind字典复制
    tb:表名称，默认为AShareEODPrices
    日期是日历日，非交易日数据用前一个交易日数据填充
    rpt_type：报表类型。用A股财务数据的时候这个是主键！
    '''
    if str(type(code_list))!="<class 'str'>":
        code_str="\',\'".join(code_list)
    else:
        code_str=code_list

    if tb in ['AShareBalanceSheet',
              'AShareIncome',
              'AShareCashFlow',
              'AShareTTMAndMRQ',
              'AShareTTMHis','PITFinancialFactor']:

        info_tb='AShareDescription'

    elif tb=='AIndexFinancialderivative' :

        info_tb='AIndexDescription'

    start_long=start[:4]+start[5:7]+start[8:10]
    end_long=end[:4]+end[5:7]+end[8:10]

    if code_str!='':

        sql="select s_info_windcode,"+ indicator +",REPORT_PERIOD  \n" \
        "from wind."+tb+"  \n" \
        "where s_info_windcode = any("+'\''+code_str+'\''+") \n" \
        "and REPORT_PERIOD between ("+'\''+start_long+'\''+") and ("+'\''+end_long+'\''+") \n" \
        "and STATEMENT_TYPE ="+ rpt_type + " \n" \
        "order by s_info_windcode,REPORT_PERIOD"
        sql2="select S_INFO_WINDCODE,S_INFO_NAME from wind."+info_tb+" where s_info_windcode = any("+'\''+code_str+'\''+") "
    else : #如果code_list是个空列表，或者空字符串，那么定义下面这些sql
        sql="select s_info_windcode,"+ indicator +",REPORT_PERIOD  \n" \
        "from wind."+tb+"  \n" \
        "where REPORT_PERIOD between ("+'\''+start_long+'\''+") and ("+'\''+end_long+'\''+") \n" \
        "and STATEMENT_TYPE ="+ rpt_type + " \n" \
        "order by s_info_windcode,REPORT_PERIOD"
        sql2="select S_INFO_WINDCODE,S_INFO_NAME from wind."+info_tb

    df=pd.read_sql(sql,db)
    df2=pd.read_sql(sql2,db)
    df3=pd.merge(df,df2,on='S_INFO_WINDCODE',how='inner')


    df3[['REPORT_PERIOD']]=long_to_dt(df3[['REPORT_PERIOD']])

    col = df3['S_INFO_NAME'].drop_duplicates().tolist()
    df3=df3.pivot_table(indicator,'REPORT_PERIOD','S_INFO_NAME',dropna=False)
    df3=df3[col]
    df3.index.name,df3.columns.name=None,None
    df3=date_index(df3)
    
    #变频
    df4=eval("df3.resample('"+freq+"')."+how+"()")
    df4.sort_index(ascending=True, inplace=True)
    
    return df4
#%%提取指数历史成分股数据存为dataframe
def index_component(index_code,start,end,db=wdb):
    '''
    可以提沪深300，也可以提取其他宽基指数、行业指数
    '''
    start_long=start[:4]+start[5:7]+start[8:10]
    end_long=end[:4]+end[5:7]+end[8:10]

    sql  = "select s_info_windcode,s_con_windcode,trade_dt,i_weight from wind.AIndexHS300FreeWeight " \
    "where trade_dt between ("+'\''+start_long+'\''+") and ("+'\''+end_long+'\''+") and s_info_windcode = any("+'\''+index_code+'\''+") " \
    "order by trade_dt,i_weight"

    # sql2="select S_INFO_WINDCODE,S_INFO_NAME from wind."+'AShareDescription'+" where s_info_windcode = any("+'\''+code_str+'\''+") "

    df=pd.read_sql(sql,db)
    # df2 = pd.read_sql(sql2, db)
    # df3 = pd.merge(df, df2, on='S_INFO_WINDCODE', how='inner')

    return df
def stock_name(code_list,db=wdb):
    '''
    提取一系列股票的名称
    返回WDS的SQL结构数据
    '''
    if str(type(code_list)) != "<class 'str'>":
        code_str = "\',\'".join(code_list)
    else:
        code_str = code_list

    sql2="select S_INFO_WINDCODE,S_INFO_NAME from wind."+'AShareDescription'+" where s_info_windcode = any("+'\''+code_str+'\''+") "

    df2 = pd.read_sql(sql2, db)

    return df2
#%%中文名把代码列表转换为资产的中文名列表
#存在问题！！！！！可能有一些代码再WDS的表里查不到对应的中文简称！！！这个问题需要解决。
def code2name(code_list,db=wdb):
    '''
    通过sql查询对应的中文名把代码列表转换为资产的中文名列表
    '''
    if str(type(code_list))!="<class 'str'>":
        code_str="\',\'".join(code_list)
    else:
        code_str=code_list
    info_tb='WindCustomCode'
    sql_code_name="select S_INFO_WINDCODE,S_INFO_NAME from wind."+info_tb+" where s_info_windcode = any("+'\''+code_str+'\''+") "
    df_codename=pd.read_sql(sql_code_name,db)
    # display(df_codename)
    df_codename=sort_by_list(df_codename,'S_INFO_WINDCODE',code_list)
    name_list=df_codename['S_INFO_NAME'].tolist()
    return name_list
def code2name_df(code_list,db=wdb):
    '''
    通过sql查询对应的中文名把代码列表转换为资产的中文名列表
    '''
    if str(type(code_list))!="<class 'str'>":
        code_str="\',\'".join(code_list)
    else:
        code_str=code_list
    info_tb='WindCustomCode'
    sql_code_name="select S_INFO_WINDCODE,S_INFO_NAME from wind."+info_tb+" where s_info_windcode = any("+'\''+code_str+'\''+") "
    df_codename=pd.read_sql(sql_code_name,db)
    return df_codename


# A股申万行业映射（一级、二级、三级）
def asharestocksw(version='2021'):
    '''
    【返回值】包含S_INFO_WINDCODE、industry_sw1、industry_sw2、ENTRY_DT、REMOVE_DT、CUR_SIGN的数据框。随着时间的推移，CUR_SIGN的数据会变化，这一点要格外注意
    '''

    version_dict = {'2021': 'AShareSWNIndustriesClass', '2014': 'AShareSWIndustriesClass'}

    sql_ashare_sw1 = f'''
    select a.S_INFO_WINDCODE, a.SW_IND_CODE, b.INDUSTRIESNAME ,a.ENTRY_DT,a.REMOVE_DT,a.CUR_SIGN
    from wind.{version_dict[version]} a, wind.AShareIndustriesCode b 
    where substr(a.SW_IND_CODE,1,4)=substr(b.INDUSTRIESCODE,1,4) 
    and b.levelnum = '2' order by 1
    '''
    ashare_stock_sw1 = pd.read_sql(sql_ashare_sw1, wdb)

    sql_ashare_sw2 = f'''
    select a.S_INFO_WINDCODE, a.SW_IND_CODE, b.INDUSTRIESNAME ,a.ENTRY_DT,a.REMOVE_DT,a.CUR_SIGN
    from wind.{version_dict[version]} a, wind.AShareIndustriesCode b 
    where substr(a.SW_IND_CODE,1,6)=substr(b.INDUSTRIESCODE,1,6) 
    and b.levelnum = '3' order by 1
    '''
    ashare_stock_sw2 = pd.read_sql(sql_ashare_sw2, wdb)

    sql_ashare_sw2 = f'''
    select a.S_INFO_WINDCODE, a.SW_IND_CODE, b.INDUSTRIESNAME ,a.ENTRY_DT,a.REMOVE_DT,a.CUR_SIGN
    from wind.{version_dict[version]} a, wind.AShareIndustriesCode b 
    where substr(a.SW_IND_CODE,1,6)=substr(b.INDUSTRIESCODE,1,6) 
    and b.levelnum = '3' order by 1
    '''
    ashare_stock_sw2 = pd.read_sql(sql_ashare_sw2, wdb)

    sql_ashare_sw3 = f'''
    select a.S_INFO_WINDCODE, a.SW_IND_CODE, b.INDUSTRIESNAME ,a.ENTRY_DT,a.REMOVE_DT,a.CUR_SIGN
    from wind.{version_dict[version]} a, wind.AShareIndustriesCode b 
    where substr(a.SW_IND_CODE,1,8)=substr(b.INDUSTRIESCODE,1,8) 
    and b.levelnum = '4' order by 1
    '''
    ashare_stock_sw3 = pd.read_sql(sql_ashare_sw3, wdb)

    ashare_stock_sw = pd.merge(left=ashare_stock_sw1, right=ashare_stock_sw2,
                               on=['S_INFO_WINDCODE', 'ENTRY_DT'], how='outer')
    ashare_stock_sw.drop(['SW_IND_CODE_x', 'SW_IND_CODE_y', 'REMOVE_DT_y', 'CUR_SIGN_y'], axis=1, inplace=True)
    ashare_stock_sw.columns = list_str_replace(ashare_stock_sw.columns.tolist(), ['_x'], [''])
    ashare_stock_sw.rename(columns={'INDUSTRIESNAME': 'industry_sw1', 'INDUSTRIESNAME_y': 'industry_sw2'}, inplace=True)
    ashare_stock_sw = ashare_stock_sw[
        ['S_INFO_WINDCODE', 'industry_sw1', 'industry_sw2', 'ENTRY_DT', 'REMOVE_DT', 'CUR_SIGN']]

    ashare_stock_sw = pd.merge(left=ashare_stock_sw, right=ashare_stock_sw3,
                               on=['S_INFO_WINDCODE', 'ENTRY_DT'], how='outer')
    ashare_stock_sw.drop(['REMOVE_DT_y', 'CUR_SIGN_y', 'SW_IND_CODE'], axis=1, inplace=True)
    ashare_stock_sw.columns = list_str_replace(ashare_stock_sw.columns.tolist(), ['_x'], [''])
    ashare_stock_sw.rename(columns={'INDUSTRIESNAME': 'industry_sw3'}, inplace=True)
    ashare_stock_sw = ashare_stock_sw[
        ['S_INFO_WINDCODE', 'industry_sw1', 'industry_sw2', 'industry_sw3', 'ENTRY_DT', 'REMOVE_DT', 'CUR_SIGN']]

    ashare_stock_sw[['ENTRY_DT', 'REMOVE_DT']] = ashare_stock_sw[['ENTRY_DT', 'REMOVE_DT']].fillna(
        TODAY[:4] + TODAY[5:7] + TODAY[8:10])

    return ashare_stock_sw
#%%A股中信行业映射（一级、二级、三级）
def asharestockcs():
    '''
    【返回值】包含S_INFO_WINDCODE、industry_sw1、industry_sw2、ENTRY_DT、REMOVE_DT、CUR_SIGN的数据框。
    随着时间的推移，CUR_SIGN的数据会变化，这一点要格外注意
    把cur_sign=None的用TODAY的yyyymmdd填充
    '''
    sql_cs1 = '''
    select INDUSTRIESCODE,INDUSTRIESNAME,LEVELNUM from wind.AShareIndustriesCode 
    where substr(INDUSTRIESCODE,1,2)='b1' and levelnum=2
    '''
    cs1 = pd.read_sql(sql_cs1, wdb)
    cs1['cs1'] = cs1['INDUSTRIESCODE'].apply(lambda x: x[:4])

    sql_cs2 = '''
    select INDUSTRIESCODE,INDUSTRIESNAME,LEVELNUM from wind.AShareIndustriesCode 
    where substr(INDUSTRIESCODE,1,2)='b1' and levelnum=3
    '''
    cs2 = pd.read_sql(sql_cs2, wdb)
    cs2['cs2'] = cs2['INDUSTRIESCODE'].apply(lambda x: x[:6])

    sql_cs3 = '''
    select INDUSTRIESCODE,INDUSTRIESNAME,LEVELNUM from wind.AShareIndustriesCode 
    where substr(INDUSTRIESCODE,1,2)='b1' and levelnum=4
    '''
    cs3 = pd.read_sql(sql_cs3, wdb)
    cs3['cs3'] = cs3['INDUSTRIESCODE'].apply(lambda x: x[:8])

    sql_ashare_stock_cs = '''
    select S_INFO_WINDCODE,CITICS_IND_CODE,ENTRY_DT,REMOVE_DT,CUR_SIGN from wind.AShareIndustriesClassCITICS
    order by 1
    '''
    ashare_stock_cs = pd.read_sql(sql_ashare_stock_cs, wdb)
    ashare_stock_cs['cs1'] = ashare_stock_cs['CITICS_IND_CODE'].apply(lambda x: x[:4])
    ashare_stock_cs['cs2'] = ashare_stock_cs['CITICS_IND_CODE'].apply(lambda x: x[:6])
    ashare_stock_cs['cs3'] = ashare_stock_cs['CITICS_IND_CODE'].apply(lambda x: x[:8])

    ashare_stock_cs = pd.merge(left=ashare_stock_cs, right=cs1, on='cs1', how='outer')
    ashare_stock_cs.rename(columns={'INDUSTRIESNAME': 'industry_cs1'}, inplace=True)
    ashare_stock_cs = pd.merge(left=ashare_stock_cs, right=cs2, on='cs2', how='outer')
    ashare_stock_cs.rename(columns={'INDUSTRIESNAME': 'industry_cs2'}, inplace=True)
    ashare_stock_cs = pd.merge(left=ashare_stock_cs, right=cs3, on='cs3', how='outer')
    ashare_stock_cs.rename(columns={'INDUSTRIESNAME': 'industry_cs3'}, inplace=True)

    ashare_stock_cs = ashare_stock_cs[
        ['S_INFO_WINDCODE', 'industry_cs1', 'industry_cs2', 'industry_cs3', 'ENTRY_DT', 'REMOVE_DT', 'CUR_SIGN']]
    ashare_stock_cs[['ENTRY_DT', 'REMOVE_DT']] = ashare_stock_cs[['ENTRY_DT', 'REMOVE_DT']].fillna(TODAY[:4] + TODAY[5:7] + TODAY[8:10])
    ashare_stock_cs[['date_assist']] = ashare_stock_cs[['ENTRY_DT']].long2dt('ENTRY_DT')
    ashare_stock_cs.drop(['date_assist'], axis=1, inplace=True)

    return ashare_stock_cs
#%%A股行业映射
def dataset_add_industry(data, datename, codename, industry='cs'):
    '''
    持仓数据中的【A股】映射到行业，无法映射港股美股。
    【注意】目前的设定是，如果持仓中有非A股，那么最后的返回值是去会掉这些样本的。这个bug有待改进，特别是，针对港股也要加入行业映射
    data：SQL格式数据集，持仓基本数据
    [datename,codename]：列表，分别是持仓数据集的日期字段名、股票代码字段名
    industry：取值'cs' or 'sw'，行业类型
    '''
    if industry == 'cs':
        industry_df = asharestockcs()
    elif industry == 'sw':
        industry_df = asharestocksw('2021')

    industry_df[['REMOVE_DT']] = industry_df[['REMOVE_DT']].fillna(TODAY)

    if str(type(data[datename][0])) == "<class 'pandas._libs.tslibs.timestamps.Timestamp'>":
        industry_df.long2dt(['ENTRY_DT', 'REMOVE_DT'], inplace=True)

    dataset = pd.merge(data, industry_df, left_on=codename,right_on='S_INFO_WINDCODE', how='outer')

    if str(type(data[datename][0])) == "<class 'pandas._libs.tslibs.timestamps.Timestamp'>":
        dataset['useful'] = dataset.apply(lambda x: 1 if (x['ENTRY_DT'] <= x[datename] and x['REMOVE_DT'] >= x[datename]) else 0, axis=1)
    elif str(type(data[datename][0])) == "<class 'str'>":
        dataset['useful'] = dataset.apply(lambda x: 1 if (float(x['ENTRY_DT']) <= float(x[datename]) and float(x['REMOVE_DT']) >= float(x[datename])) else 0,axis=1)

    dataset = dataset.query("useful==1")
    # dataset.drop(['S_INFO_WINDCODE', 'ENTRY_DT', 'REMOVE_DT', 'CUR_SIGN', 'useful'], axis=1, inplace=True)
    dataset.drop(['ENTRY_DT', 'REMOVE_DT', 'CUR_SIGN', 'useful'], axis=1, inplace=True)
    dataset.rename(columns={'industry_cs1': '中信一级', 'industry_cs2': '中信二级', 'industry_cs3': '中信三级'}, inplace=True)
    return dataset
def dataset_add_name(data,codename='S_INFO_WINDCODE'):
    '''
    数据集的代码字段映射到中文简称
    【返回值】添加一个字段"stock_name"
    '''
    df=data.copy()
    code_list = list(set(df[codename]))
    sql_code_name="select S_INFO_WINDCODE,S_INFO_NAME from wind.WindCustomCode "
    d2=pd.read_sql(sql_code_name,wdb)
    d2.rename(columns={'S_INFO_WINDCODE': 'stock_code', 'S_INFO_NAME': 'stock_name'}, inplace=True)
    data2 = pd.merge(left=df, right=d2, left_on=codename, right_on='stock_code', how='left')
    data2.drop('stock_code', axis=1, inplace=True)
    return data2
def wss_sw_industry(code_list):
    '''
    迫不得已用wss写的取行业函数，之后研究一下如何用WDS实现，实际上已经用WDS实现了，只不过这个更灵活一些
    '''
    date=today()[:4]+today()[5:7]+today()[8:10]
    return w.wss(code_list,
                 "industry_sw_2021",
                 f"tradeDate={date};industryType=1",
                 usedf=True)[1].reset_index().col(['wind代码','申万行业'])

class EquityTradeProfit():
    '''
    利用组合部的持仓信息和交易信息，计算任意时间区间内，投资经理在个股上的操作获利情况
    使用场景：1）委外投资经理业绩归因；2）权益部投资经理操作分析；3）TAA配置型组合收益兑现计算。等等
    port：风格组合二级名称，例如：'财再-外委景顺长城'
    '''

    def __init__(self, label, port, start, end):
        # 交易数据
        data_trade = crdata(
            select_fields=['日期', '委托人', '管理人', '风格组合一级', '风格组合二级', '资产大类一级', '资产大类二级', '币种', '证券代码', '证券名称', '方向','交易数量', '交易金额', '成交价格'],
            filter_conditions=[f"{label} in  ('{port}')"],
            start_date=start, end_date=end, frequency='d', calendar=1, table='trade')
        # 持仓数据
        data_position = crdata(
            select_fields=['日期', '委托人', '管理人', '风格组合一级', '风格组合二级', '资产大类一级', '资产大类二级','资产大类三级', '币种', '证券代码', '证券名称', '市值', '数量','行业'],
            filter_conditions=[f"{label} in  ('{port}')"],
            start_date=start, end_date=end, frequency='d', calendar=1, table='position')

        profit = dict()
        for stock in list(set(data_position.query("资产大类一级=='权益类' ")['证券代码']) | set(data_trade.query("资产大类一级=='权益类' ")['证券代码'])):
            po = data_position.query(f"资产大类一级=='权益类' and 证券代码=='{stock}'")
            tr = data_trade.query(f"资产大类一级=='权益类' and 证券代码=='{stock}'")
            data_try = pd.merge(po, tr[['日期', '证券代码', '方向', '交易数量', '交易金额']], on=['日期', '证券代码'], how='left')
            # data_try.loc[0, '交易金额'] = data_try.loc[0, '市值']
            # data_try.loc[0, '方向'] = '买入'
            # data_try.loc[data_try.shape[0] - 1, '交易金额'] = -1 * data_try.loc[data_try.shape[0] - 1, '市值']
            # data_try.loc[data_try.shape[0] - 1, '方向'] = '卖出'
            if   data_try.loc[0,'方向']=='买入' and data_try.loc[data_try.shape[0] - 1,'方向']=='卖出':
                profit[stock] = -1 * data_try.query("方向 in ('买入','卖出')")[['交易金额']].sum()
            elif data_try.loc[0,'方向']=='买入' and data_try.loc[data_try.shape[0] - 1,'方向']!='卖出':
                profit[stock] = -1 * data_try.query("方向 in ('买入','卖出')")[['交易金额']].sum() + data_try.loc[data_try.shape[0] - 1, '市值']
            elif data_try.loc[0,'方向']!='买入' and data_try.loc[data_try.shape[0] - 1,'方向']=='卖出':
                profit[stock] = -1 * data_try.query("方向 in ('买入','卖出')")[['交易金额']].sum() -data_try.loc[0, '市值']
            elif data_try.loc[0,'方向']!='买入' and data_try.loc[data_try.shape[0] - 1,'方向']!='卖出':
                profit[stock] = -1 * data_try.query("方向 in ('买入','卖出')")[['交易金额']].sum() + data_try.loc[data_try.shape[0] - 1, '市值'] - data_try.loc[0, '市值']

            # profit[stock] = -1 * data_try.query("方向 in ('买入','卖出')")[['交易金额']].sum()+data_try.loc[data_try.shape[0] - 1, '市值']-data_try.loc[0, '市值']
            # profit[stock] = -1 * data_try.query("方向 in ('买入','卖出')")[['交易金额']].sum()
            # display(data_try.loc[data_try.shape[0] - 1, '交易金额'])


        profit_stock_basic = pd.DataFrame(profit).T.sortd()
        # display(profit_stock_basic)
        sw_name_df = wss_sw_industry(profit_stock_basic.index.tolist()).set_index('wind代码').index0name()

        # display(profit_stock_basic)
        # display(profit_stock_basic.index.tolist())
        # display(sw_name_df)
        stock_name_df = code2name_df(profit_stock_basic.index.tolist()).col(['证券代码', '证券名称'])

        profit_stock = profit_stock_basic.mg(stock_name_df.set_index('证券代码').index0name(),how='left').dropna().set_index('证券名称').index0name().sortd().col('净盈利')
        profit_industry = profit_stock_basic.mg(sw_name_df, how='left').groupby('申万行业').sum().index0name().sortd().col('净盈利')

        self.profit_stock = profit_stock
        self.profit_industry = profit_industry
        self.trade=data_trade
        self.position=data_position

#查看变量名称，展示前几行或后几行
def show_vars(var_list, row=5, head=True):
    for var in var_list:
        print(var)
        if head == True:
            display(data.head(row))
        else:
            display(data.tail(row))




