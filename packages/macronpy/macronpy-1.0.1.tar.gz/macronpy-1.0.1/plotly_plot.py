# from macronpy.basic_package import *
from macronpy.macro import *
import macronpy
import pandas as pd
# from macronpy.macro import merge
from pandas.core.base import PandasObject  # 用于为pandas增加函数
# %%plotly画图系列函数##############################################################################################################################
# %%plotly画图
# 导入plotly
import plotly
import plotly.express as px
from plotly import graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.io as pio
from IPython.display import Image
import kaleido #用于将plotly的图存为png
import numpy as np
pio.renderers.default = 'notebook'
from datetime import datetime
# from plotly.offline import init_notebook_mode, iplot
# init_notebook_mode(connected=True)#解决jupyterlab不显示plotly图
# 设定全局参数，使得导入包之后默认不做图
return_plot = True
# 与streamlit交互
# import streamlit as st
config = dict({'displayModeBar': False, 'showTips': False})
# 定义一个隐藏Plotly logo的JavaScript函数
js_hide_logo = '''
function() {
  var img = document.querySelector(".modebar-group .plotlyjsicon");
  img.style.display = "none";
}
'''
# 添加一个自定义按钮来隐藏Plotly logo
custom_button = {
    'buttons': [
#         {
#             'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
# #             'label': 'Play',
#             'method': 'animate'
#         },
    ],
    'direction': 'left',
    'pad': {'r': 10, 't': 10},
    'showactive': False,
    'type': 'buttons',
    'x': 0.1,
    'xanchor': 'right',
    'y': 1.1,
    'yanchor': 'top'
}
hide_logo=dict(modebar={'orientation': 'v', 'bgcolor': 'white'},updatemenus=[custom_button])
# # 定义一个隐藏"double click to rezoom"提示框的JavaScript函数
# js_hide_rezoom_prompt = '''
# function(gd) {
#   var buttons = gd._fullLayout._modeBar.querySelectorAll('.modebar-btn');
#   buttons.forEach(function(btn) {
#     if (btn.getAttribute('data-title') === 'Double click to rezoom') {
#       btn.style.display = 'none';
#     }
#   });
# }
# '''
# # 添加一个自定义按钮来隐藏"double click to rezoom"提示框
# custom_button2 = {
#     # 'label': 'Hide Prompt',
#     'active': 'relayout',
#     'args': ['modebar.buttonsToRemove', ['reset'], js_hide_rezoom_prompt],
# }
# hide_prompt=dict(modebar={'orientation': 'v', 'bgcolor': 'white'},updatemenus=[custom_button2])

def stplt(plotly_go):
    '''
    用于简化在streamlit中作图的流程
    '''
    return st.plotly_chart(plotly_go, config=config)
#%%剪贴板函数
def myclip(filename):
    import win32con
    from PIL import Image
    import win32clipboard as w
    from io import BytesIO
    from urllib import request
    # 读取本地图片内容
    def getLocalImageData(path):
        img = Image.open(path)
        output = BytesIO()  # BytesIO实现了在内存中读写bytes
        img.convert("RGB").save(output, "BMP") #以RGB模式保存图像
        data = output.getvalue()[14:]
        output.close()
        return data
    # 把 Pillow/PIL Image object 塞入剪贴板
    def getPILImageData(img):
        output = BytesIO()  # BytesIO实现了在内存中读写bytes
        img.convert("RGB").save(output, "BMP") #以RGB模式保存图像
        data = output.getvalue()[14:]
        output.close()
        return data
    # 把图片内容塞入剪贴板
    def setImageDataToClipboard(data):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_DIB, data)
        w.CloseClipboard()
    data=getLocalImageData(filename)
    setImageDataToClipboard(data)
def cl(fig):
    fig.write_image('a.png')
    return myclip('a.png')
# 解决单元格中不显示图像的问题
# pio.renderers.default = "plotly_mimetype+notebook"
# # Set notebook mode to work in offline
# import plotly.offline as pyo
# pyo.init_notebook_mode()
def merge_for_plotly(df_list, how='outer', col=None):
    '''
    col：【列表格式】merge之后的新数据框的列名称，如果不写，则啥也不做
    '''
    merged = reduce(lambda left, right: pd.merge(left,
                                                 right,
                                                 left_index=True,
                                                 right_index=True,
                                                 how=how,
                                                 suffixes=(None, " ")), df_list)
    merged.sort_index(ascending=True, inplace=True)
    if col != None:
        merged.columns = col
    return merged


# 导入配色方案
try:
    color_scheme = pd.read_excel(r'C:\Users\niupeiyi\AppData\Roaming\Microsoft\AddIns\【图表配色方案】.xlsm', sheet_name='图表')
except:
    color_scheme = pd.read_excel(r'C:\Users\13312\AppData\Roaming\Microsoft\AddIns\【图表配色方案】.xlsm', sheet_name='图表')
color_scheme = color_scheme['RGB值'].to_list()
color_scheme2 = [x.replace('RGB', 'RGBA') for x in color_scheme]
color_scheme2 = [x.replace(")", ",0.4)") for x in color_scheme2]
# layout中：plot_bgcolor为作图区域背景色；mirror为显示作图区域轮廓。hovermode的取值为 ['x', 'y', 'closest', False, 'x unified', 'y unified']其中一个，用于动态显示数据。hoverlabel中的bgcolor调节的是悬浮颜色
# 如果想让图四周有框线，在xaxis yaxis yaxis2 里面分别加一句话：mirror=True
lo = go.Layout(
    xaxis=dict(color='RGB(0,0,0)', showgrid=False, title='', ticks="outside", ticklen=5, tickfont=dict(size=14),
               linewidth=1, linecolor='RGB(0,0,0)', showline=True,
               showspikes=False,
               spikemode='marker+across',
               spikesnap='data',
               spikedash='dash',
               rangemode='tozero',
               zeroline=False),
    yaxis=dict(anchor='x', color='RGB(0,0,0)', showgrid=False, title='', tickformat='1', ticks="outside", ticklen=None,
               tickfont=dict(size=14), linewidth=1, linecolor='RGB(0,0,0)', zeroline=False, zerolinewidth=1,
               zerolinecolor='rgb(0,0,0)', rangemode='normal', autorange=True, automargin=True),
    yaxis2=dict(color='RGB(0,0,0)', showgrid=False, title='', tickformat='1', ticks="outside", ticklen=None,
                tickfont=dict(size=14), linewidth=1, linecolor='RGB(0,0,0)', zeroline=False, showline=True,
                rangemode='normal', overlaying='y', side="right", autorange=True, automargin=True),
    yaxis3=dict(anchor='free', color='RGB(0,0,0)', showgrid=False, title='', tickformat='1', ticks="outside",
                ticklen=40, tickfont=dict(size=14, color='RGB(128,128,128)'), tickcolor='rgba(255,255,255,0)',
                linewidth=0, linecolor='RGB(0,0,0)', overlaying='y', zeroline=False, showline=False, rangemode='normal',
                side="right", autorange=True, automargin=True, position=1),
    yaxis4=dict(anchor='free', color='RGB(0,0,0)', showgrid=False, title='', tickformat='1', ticks="outside",
                ticklen=80, tickfont=dict(size=14, color='RGB(128,128,128)'), tickcolor='rgba(255,255,255,0)',
                linewidth=0, linecolor='RGB(0,0,0)', overlaying='y', zeroline=False, showline=False, rangemode='normal',
                side="right", autorange=True, automargin=True, position=1),
    width=700,
    height=400,
    font=dict(family="Arial, KaiTi"),
    plot_bgcolor='rgba(0,0,0,0)',
    title=None,
    showlegend=True,
    legend_title='',
    legend_orientation='h',
    #     legend=dict(font=dict(family="Microsoft YaHei",color='RGB(0,0,0)',size=13),bgcolor='rgba(0,0,0,0)',yanchor='top',xanchor='center',x = 0.5, y= 1.15,borderwidth=0),#x=0.22,y=1.1),
    #    legend=dict(font=dict(family="Arial",color='RGB(0,0,0)',size=13),bgcolor='rgba(0,0,0,0)',xanchor='center',x = 0.5,borderwidth=0),#x=0.22,y=1.1),
    #    legend=dict(font=dict(family="Arial",color='RGB(0,0,0)',size=13),bgcolor='rgba(0,0,0,0)',yanchor='top',xanchor='center',x = 0.5, y= 1.15,borderwidth=0),
    legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), bgcolor='rgba(0,0,0,0)',
                xanchor='center', x=0.5, borderwidth=0),

    hovermode='x',
    #     hoverlabel=dict(bgcolor='rgba(242,242,242,0.4)',font_size=13),
    hoverlabel=dict(font_size=12, font_family="Arial, KaiTi"),
    colorway=color_scheme,
    margin=dict(l=30, r=30, b=30, t=30, pad=0),
    modebar_remove=['zoom', 'zoomin', 'zoomout', 'pan', 'toImage', 'Autoscale', 'resetscale', 'logomark', 'logo'],
)
def create_matrix_layout_with_multiple_axes(num_axes, color_scheme):
    # 创建空列表来存储x轴和y轴的设置
    axes_settings = []

    # 循环创建x轴和y轴的设置
    for i in range(num_axes):
        axis_settings = dict(
            color='RGB(0,0,0)',
            showgrid=False,
            title='',
            ticks="outside",
            ticklen=5,
            tickfont=dict(size=14),
            linewidth=1,
            linecolor='RGB(0,0,0)',
            showline=True,
            showspikes=False,
            spikemode='marker+across',
            spikesnap='data',
            spikedash='dash',
            # rangemode='tozero',
            rangemode=None,
            zeroline=False
        )
        axes_settings.append(axis_settings)

    # 创建layout
    layout = go.Layout(
        xaxis=axes_settings[0],  # 使用第一个x轴设置
        yaxis=axes_settings[0],  # 使用第一个y轴设置
        font=dict(family='Arial, KaiTi'),
        hoverlabel=dict(font_size=12, font_family="Arial, KaiTi"),
        colorway=color_scheme,
        plot_bgcolor='rgba(0,0,0,0)',
        title=None,
        showlegend=False,
        hovermode='closest',
    )

    # 根据x和y的套数设置多个x轴和y轴
    for i in range(1, num_axes):
        layout[f'xaxis{i+1}'] = axes_settings[i]
        layout[f'yaxis{i+1}'] = axes_settings[i]
    return layout
lo_matrix_sp = go.Layout(
    xaxis=dict(color='RGB(0,0,0)', showgrid=False, title='', ticks="outside", ticklen=5, tickfont=dict(size=14),
               linewidth=1, linecolor='RGB(0,0,0)', showline=True,
               showspikes=False,
               spikemode='marker+across',
               spikesnap='data',
               spikedash='dash',
               rangemode='tozero',
               zeroline=False),
    yaxis=dict(anchor='x', color='RGB(0,0,0)', showgrid=False, title='', tickformat='1', ticks="outside", ticklen=None,
               tickfont=dict(size=14), linewidth=1, linecolor='RGB(0,0,0)', zeroline=False, zerolinewidth=1,
               zerolinecolor='rgb(0,0,0)', rangemode='normal', autorange=True, automargin=True),
    # width=700,
    # height=400,
    font=dict(family='Arial, KaiTi'),
    plot_bgcolor='rgba(0,0,0,0)',
    title=None,
    showlegend=False,
    # legend_title='',
    # legend_orientation='h',
    #     legend=dict(font=dict(family="Microsoft YaHei",color='RGB(0,0,0)',size=13),bgcolor='rgba(0,0,0,0)',yanchor='top',xanchor='center',x = 0.5, y= 1.15,borderwidth=0),#x=0.22,y=1.1),
    #    legend=dict(font=dict(family="Arial",color='RGB(0,0,0)',size=13),bgcolor='rgba(0,0,0,0)',xanchor='center',x = 0.5,borderwidth=0),#x=0.22,y=1.1),
    #    legend=dict(font=dict(family="Arial",color='RGB(0,0,0)',size=13),bgcolor='rgba(0,0,0,0)',yanchor='top',xanchor='center',x = 0.5, y= 1.15,borderwidth=0),
    #     legend=dict(font=dict(family="Arial",color='RGB(0,0,0)',size=13),bgcolor='rgba(0,0,0,0)',xanchor='center',x = 0.5,borderwidth=0),

    hovermode='closest',
    #     hoverlabel=dict(bgcolor='rgba(242,242,242,0.4)',font_size=13),
    hoverlabel=dict(font_size=12, font_family="Arial, KaiTi"),
    colorway=color_scheme,
    # margin=dict(l=30,r=30,b=30,t=30,pad=0),
    modebar_remove=['zoom', 'zoomin', 'zoomout', 'pan', 'toImage', 'Autoscale', 'resetscale', 'logomark', 'logo'],
)
try:
    shade_color = pd.read_excel(r'C:\Users\niupeiyi\AppData\Roaming\Microsoft\AddIns\【图表配色方案】.xlsm', sheet_name='阴影')
except:
    shade_color = pd.read_excel(r'C:\Users\13312\AppData\Roaming\Microsoft\AddIns\【图表配色方案】.xlsm', sheet_name='阴影')
shade_color = shade_color['RGB值'].to_list()


# %%WIND提取数据画图
def pl(ID_list, name_list, start='', end='', lead=0, lead_time=0, r=[], fill='', return_plot=False):
    '''
    lead是整数，一般是1或者2，表示第几个指标要领先
    lead_time是整数
    fill默认为空，如果要传入参数，从'ffill'和'bfill'里选一个传
    '''
    if start == '':
        start = start_date

    if end == '':
        end = end_date

    r_copy = r
    if type(r_copy) == int:
        r_copy = [r_copy]
    name_list_copy = name_list.copy()

    # 提取经济数据
    eco_data = w.edb(ID_list, start, end, usedf=True)[1]
    eco_data.columns = name_list

    # 升序排序时间索引
    eco_data.sort_index(ascending=True, inplace=True)

    # 填补缺失值
    if fill != '':
        eco_data.fillna(method=fill)

    # 数据指标数赋值给num_of_col
    num_of_col = len(name_list)
    # 生成左轴右轴参数列表
    yaxis_list = ['y1'] * num_of_col

    if lead_time > 0:
        name_list_copy[lead - 1] = name_list_copy[lead - 1] + "-领先" + str(lead_time) + "期"
        eco_data[[eco_data.columns[lead - 1]]] = eco_data[[eco_data.columns[lead - 1]]].shift(lead_time)

        # 用传入参数替换yaxis_list中原先设定的y1参数
    if r_copy != []:
        for k in r_copy:
            # 根据指标名称分右轴
            #             right_index=name_list.index(k)
            #             yaxis_list[right_index]='y2'
            #             name_list_copy[right_index]=name_list_copy[right_index]+'（右）'
            # 根据指标序号，注意，传入函数参数的时候是从1开始
            yaxis_list[k - 1] = 'y2'
            name_list_copy[k - 1] = name_list_copy[k - 1] + '（右）'

            # 循环生成trace
    trace_list = []
    for i in range(num_of_col):
        trace_list.append(go.Scatter(x=eco_data.index,
                                     y=eco_data.iloc[:, i],
                                     mode='lines',
                                     yaxis=yaxis_list[i],
                                     name=name_list_copy[i],
                                     hovertemplate="%{x|%Y-%m-%d}<br>%{y}",
                                     connectgaps=True))  # 注意这里的connectgaps=True！
    fig_data = trace_list
    fig = go.Figure(data=fig_data, layout=lo)
    if return_plot == False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig


# %%pl的另一个版本
def plt(ID_list, name_list, start='', end='', lead=[0, 0], r=[], y2re=False, fill='', legend_right=0, s='',
        connectgaps=True, uni=False, period_df=None, period=None, mode='lines', index_ascending=1):
    '''
    这个函数运行起来会更慢
    '''
    # 提取经济数据
    eco_data = w.edb(ID_list, start, end, usedf=True)[1]
    eco_data.columns = name_list
    # 调用p
    p(eco_data, start, end, lead, r, y2re, fill, legend_right, s, connectgaps, uni, period_df, period, mode,
      index_ascending)


# %%直接画图
def df_merge(df_list, how='outer', col=None):
    '''
    col：【列表格式】merge之后的新数据框的列名称，如果不写，则啥也不做
    '''
    merged = reduce(lambda left, right: pd.merge(left,
                                                 right,
                                                 left_index=True,
                                                 right_index=True,
                                                 how=how,
                                                 suffixes=(None, " ")), df_list)
    merged.sort_index(ascending=True, inplace=True)
    if col != None:
        merged.columns = col
    return merged


def p(df, start='', end='', lead=[0, 0], ry=False, r=[], r2=[], r3=[], ds=[],
      area=[], stack=False, percent=False, bar=[],yre=False,
      y2re=False, fill='', legend_right=0, s='', height=None, width=None,
      connectgaps=True,
      uni=False, period_df=None, period=['上行','下行'],
      mode='lines', index_ascending=1, font_size='',
      ycomma=False,ypct=None, y2pct=None,yhide=False,xhide=False,
      vline='', hline='', vline2='', hline2='', line_group_color=['green', 'red'], d0=False, dec=None,
      trend_line=False, trend_start=None, layout=lo, color=color_scheme, color_repeat=0,color_group=0,
      title='', return_plot=return_plot,img=False):
    '''
    【默认做时间序列折线图】
    df：如果是一个dataframe，则直接画图；如果是一个dataframe组成的list，则把他们merge之后再画图
    start和end：如果只需要start，直接写一个参数；但如果只需要end，需要在end前面写上''，用于占位，否则只写一个就只会被当成是start
    lead：双元素列表，第一个元素表示第几个指标要领先，第二个表示领先多少期。要么是空列表，要么一起传入两个参数，只传一个参数会报错
    ry：只做右轴。注意，当ry=1的时候，必须要r=[], r2=[], r3=[]
    r:整数或列表，表示第几个指标要放在次1坐标轴
    r2、r3:整数或列表，表示第几个指标要放在次2、3坐标轴（外侧）
    ds:整数或列表，表示第几个指标要做成虚线
    area:整数或列表，表示第几个指标要做成面积图。但如果取值'all'，则全部都是面积图
    y2re：True or False，是否要把次1坐标轴逆序
    s=1,2,3,4 对应4种尺寸
    fill：默认为空，如果要传入参数，从'ffill'和'bfill'里选一个传
    legend_right：图例位于右侧
    uni：True or False，是否把指标净值化处理，多用于资产价格等序列数据
    period_df是一个dataframe，index是日期戳，可以有多列也可以有一列，但列中可以包含字段“阶段”，阶段是和时间对应的阶段名称
    比如，阶段是1,2,3,4,5,6这种数字，也可以是“复苏”，“过热”，“滞胀”，“衰退”这种字符串
    vline：字符串或列表，画一条或一组垂直线
    hline：字符串或列表，画一条或一组水平线
    d0:TRUE or False，表示是否在最新的数据旁边加文字注释数值
    trend_line:bool，趋势线
    font_size：图表全部元素字体大小
    color_repeat：整数，设定颜色的重复次数
    color_group:整数，设定分组颜色
    '''

    if color_repeat != 0:
        color_list = repeat_in_list(color, color_repeat)
    else:
        color_list = color
    layout.colorway = color_list

    if color_group != 0:
        color_list = color[:color_group]*100
    else:
        color_list = color
    layout.colorway = color_list

    if str(type(df)) == "<class 'list'>":
        df_copy = df_merge(df)
    elif str(type(df)) == "<class 'pandas.core.series.Series'>":
        df_copy = pd.DataFrame(df)
    else:
        df_copy = df.copy()

    if start != '':
        df_copy = df_copy[start:]
    if end != '':
        df_copy = df_copy[:end]

    if uni == True:
        for i in range(df_copy.shape[1]):
            df_copy.iloc[:, i] = df_copy.iloc[:, i] / df_copy.iloc[0, i]
    if percent:
        df_copy=df_copy.apply(lambda x:x/x.sum(),axis=1)
    r_copy = r
    r2_copy = r2
    r3_copy = r3
    ds_copy = ds
    area_copy = area

    # 升序排序时间索引
    if index_ascending == 1:
        if type(df_copy.index[0])!=str and type(df_copy.index[0])!=tuple:
            df_copy.sort_index(ascending=True, inplace=True)


    if type(r_copy) == int:
        r_copy = [r_copy]
    if type(r2_copy) == int:
        r2_copy = [r2_copy]
    if type(r3_copy) == int:
        r3_copy = [r3_copy]
    if type(ds_copy) == int:
        ds_copy = [ds_copy]
    if type(area_copy) == int:
        area_copy = [area_copy]
    if str(type(hline)) != "<class 'list'>":
        hline = [hline]
    if str(type(vline)) != "<class 'list'>":
        vline = [vline]
    if str(type(hline2)) != "<class 'list'>":
        hline2 = [hline2]
    if str(type(vline2)) != "<class 'list'>":
        vline2 = [vline2]

    num_of_col = df_copy.shape[1]
    name_list_copy = df_copy.columns.to_list()
    yaxis_list = ['y1'] * num_of_col

    # if ry == True and r == [] and r2 == [] and r3 == []:
    #     # lo['yaxis']=dict(anchor='x',color='RGB(0,0,0)',showgrid=False,title='',tickformat='1',ticks="outside",ticklen=None,tickfont=dict(size=14),linewidth=1,linecolor='RGB(0,0,0)',zeroline=False,zerolinewidth=1, zerolinecolor='rgb(0,0,0)',rangemode='normal',autorange=True,automargin=True)
    #     lo['yaxis'] = None
    #     # lo['yaxis'].side='right'
    #     # lo['xaxis']=dict(anchor='free')
    #     yaxis_list = ['y2'] * num_of_col

    if str(type(period_df))!="<class 'NoneType'>":
        period=list(set(period_df.iloc[:,0].dropna()))

    dash_list = [None] * num_of_col
    area_list = ['none'] * num_of_col
    area_stack_parameter_list = [None] * num_of_col
    if area_copy == 'all':
        area_copy = [x + 1 for x in range(num_of_col)]

    mode_list = [mode] * num_of_col

    # 填补缺失值
    if fill != '':
        df.fillna(method=fill)

    if lead[1] != 0:
        name_list_copy[lead[0] - 1] = name_list_copy[lead[0] - 1] + "-领先" + str(lead[1]) + "期"
        df_copy[[df_copy.columns[lead[0] - 1]]] = df_copy[[df_copy.columns[lead[0] - 1]]].shift(lead[1])

    if r_copy != []:
        for k in r_copy:
            # 根据指标名称分右轴
            #             right_index=name_list.index(k)
            #             yaxis_list[right_index]='y2'
            #             name_list_copy[right_index]=name_list_copy[right_index]+'（右）'
            # 根据指标序号，注意，传入函数参数的时候是从1开始
            yaxis_list[k - 1] = 'y2'
            if y2re == False:
                name_list_copy[k - 1] = name_list_copy[k - 1] + '（右）'
            else:
                name_list_copy[k - 1] = name_list_copy[k - 1] + '（右，逆序）'
    else:
        for k in r_copy:
            yaxis_list[k - 1] = 'y1'
    if r2_copy != []:
        for n in r2_copy:
            # 根据指标名称分右轴
            #             right_index=name_list.index(k)
            #             yaxis_list[right_index]='y2'
            #             name_list_copy[right_index]=name_list_copy[right_index]+'（右）'
            # 根据指标序号，注意，传入函数参数的时候是从1开始
            yaxis_list[n - 1] = 'y3'
            name_list_copy[n - 1] = name_list_copy[n - 1] + '（右2）'
    if r3_copy != []:
        for n in r3_copy:
            yaxis_list[n - 1] = 'y4'
            name_list_copy[n - 1] = name_list_copy[n - 1] + '（右3）'
    if ds_copy != []:
        for d in ds_copy:
            dash_list[d - 1] = 'dot'

    if area_copy != []:
        for area in area_copy:
            if stack == True:
                area_list[area - 1] = None
                mode_list[area - 1] = 'none'
                area_stack_parameter_list[area - 1] = 'one'
            else:
                area_list[area - 1] = 'tozeroy'
                mode_list[area - 1] = 'none'
                area_stack_parameter_list[area - 1] = None
    else:
        pass

    # 循环生成trace
    trace_list = []
    if str(type(df_copy.index)) == "<class 'pandas.core.indexes.multi.MultiIndex'>":
        layer_length = len(df_copy.index.levels)
        df_index = []
        for i in range(layer_length):
            df_index.append(df_copy.index.get_level_values(i).tolist())
    else:
        df_index = df_copy.index.tolist()

    for i in range(num_of_col):

        if 'markers' in mode:
            trace_list.append(go.Scatter(x=df_index, y=df_copy.iloc[:, i], mode=mode_list[i], fill=area_list[i],
                                         stackgroup=area_stack_parameter_list[i],
                                         yaxis=yaxis_list[i],
                                         name=name_list_copy[i]))  # ,marker=dict(symbol='circle-open')))
        else:
            trace_list.append(go.Scatter(x=df_index, y=df_copy.iloc[:, i], mode=mode_list[i], fill=area_list[i],
                                         stackgroup=area_stack_parameter_list[i],
                                         yaxis=yaxis_list[i], name=name_list_copy[i],
                                         # hovertemplate="%{x|%Y-%m-%d}<br>%{y}", connectgaps=connectgaps,
                                        connectgaps=connectgaps,hoverinfo='text+x',hovertext=df_copy.iloc[:, i],#这里很奇怪，如果设置hoverinfo和hovertext，x轴的游标将会消失，这个太奇怪了

                                         line=dict(dash=dash_list[i])))

    fig_data = trace_list
    fig = go.Figure(data=fig_data, layout=lo)
    # fig.update_traces(hovertemplate="%{y}")
    fig.update_layout(legend={'traceorder': 'normal'})

    if str(type(df_copy.index)) == "<class 'pandas.core.indexes.multi.MultiIndex'>":
        fig.update_layout(legend=dict(yanchor='top', xanchor='center', x=0.5, y=1.15, borderwidth=0))

    # 最新值的标签显示
    if d0 == True:

        # 最新的数据是否显示文字数值
        for i, d in enumerate(fig.data):
            d_y = d.y
            d_x = d.x
            if dec != None:
                text_number = round(d_y[~pd.isna(d_y)][-1], dec)
            else:

                text_number = d_y[~pd.isna(d_y)][-1]
            fig.add_scatter(x=[pd.DataFrame(d_y, index=d_x).dropna().index[-1]], y=[d_y[~pd.isna(d_y)][-1]],
                            mode='text',
                            text=text_number,
                            textfont=dict(color=color_list[i], size=14),
                            textposition='middle right',
                            marker=dict(color=color_list[i]),
                            legendgroup=d.name,
                            showlegend=False,
                            hovertemplate="%{x|%Y-%m-%d}<br>%{y}",
                            yaxis=yaxis_list[i], name=name_list_copy[i])

    # 添加趋势线
    if trend_line == True:
        if trend_start == None:
            trend_start = str(df_copy.index[-1])[:10]
        df = df_copy.copy().dropna()
        from sklearn.linear_model import LinearRegression

        for j in range(len(df.columns.tolist())):
            i = df.columns.tolist()[j]
            # extract the data from the data frame for the time trend
            trend_data = df[df.index >= trend_start].loc[:, i]

            # fit the linear regression model
            x = np.array(range(len(trend_data))).reshape(-1, 1)
            y = trend_data.values
            model = LinearRegression().fit(x, y)

            # add the trend line to the data frame
            trend_line = model.predict(x)
            # display(trend_data)
            trend_data = pd.DataFrame(trend_data)
            trend_data["trend_line"] = trend_line
            trend_data["trend_line"] = trend_data["trend_line"] + trend_data.iloc[0, 0] - trend_data.iloc[0, 1]
            #     display(trend_data)
            # merge the trend data with the original data frame
            df_with_trend = pd.concat([df, trend_data["trend_line"]], axis=1)
            df_with_trend = df_with_trend.fillna(method="ffill")
            fig.add_trace(
                go.Scatter(x=df_with_trend.index, y=df_with_trend['trend_line'], mode='lines', name=i + '：趋势线',
                           line=dict(dash='dot', color=color_list[j])))

    # 如果period_df,period都传入了参数则调用plot_shade函数
    if str(type(period_df)) != "<class 'NoneType'>":
        period_df_copy = period_df.copy()
        period_df_copy.columns = ['阶段']
        df_copy[period] = np.nan
        for k in range(len(period)):
            # 这里主要是加图例，并不是在图里加柱子，加柱子要到后面plot_shade的调用！
            trace_list.append(
                go.Bar(x=df_copy.index, y=df_copy[period[k]], name=period[k], marker_color=shade_color[k]))
        fig_data = trace_list
        fig = go.Figure(data=fig_data, layout=lo)
        # 图的横轴起始时间
        start_x = df_copy.index[0]
        end_x = df_copy.index[-1]
        fig.update_layout({'xaxis': {'range': [str(start_x.year) + '-' + str(start_x.month) + '-' + str(start_x.day),
                                               str(end_x.year) + '-' + str(end_x.month) + '-' + str(end_x.day)]}})
        # 加柱子在这里
        fig = plot_shade(fig, period_df_copy, period)

    # 特别调整
    if str(type(df_copy.index[0])) == "<class 'str'>" or str(type(df_copy.index[0])) == "<class 'int'>":
        fig.update_layout(legend=dict(yanchor='top', xanchor='center', x=0.5, y=1.15, borderwidth=0))

    fig.update_layout(width=600, height=330)

    fig["layout"].update(go.Layout(height=height, width=width))

    if s == 0:
        fig.update_layout(width=600)
    elif s == 1:
        fig.update_layout(width=700)
    elif s == 2:
        fig.update_layout(width=800)
    elif s == 3:
        fig.update_layout(width=1000, height=600)
    elif s == 4:
        fig.update_layout(width=1300, height=700)

    # 用于根据传入参数调整图例的左右位置
    if legend_right != 0:
        try:
            if r_copy != []:
                fig.update_layout(legend_orientation=None, width=width,  # width=700
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13),
                                              x=1.365,
                                              bgcolor='rgba(0,0,0,0)'))
            else:
                fig.update_layout(legend_orientation=None, width=width,  # width=700
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.22,
                                              bgcolor='rgba(0,0,0,0)'))
        except:
            if r_copy != []:
                fig.update_layout(legend_orientation=None, width=700,  # width=700
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13),
                                              x=1.365,
                                              bgcolor='rgba(0,0,0,0)'))
            else:
                fig.update_layout(legend_orientation=None, width=700,  # width=700
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.22,
                                              bgcolor='rgba(0,0,0,0)'))

    # 逆序坐标轴
    if y2re != False:
        fig.update_layout(yaxis2=dict(autorange="reversed"))
    if yre != False:
        fig.update_layout(yaxis=dict(autorange="reversed"))

    # 改变图的白色边缘宽度
    fig.update_layout(margin=dict(l=0, b=15, t=15))

    # 左轴0刻度线取代x轴，前提是用于左轴作图的数据最小值小于零
    if r_copy != [] and ry == False:
        df_copy_for_y1 = df_copy.drop(list(df_copy.columns[[i - 1 for i in r_copy]]), axis=1)
    else:
        df_copy_for_y1 = df_copy
    # elif ry==True:
    #     df_copy_for_y1=df_copy

    try:
        if min(df_copy_for_y1.min()) < 0:
            fig.update_layout(yaxis=dict(zeroline=True, zerolinewidth=1, autorange=True),
                              xaxis=dict(showline=False, ticks=""))
        # elif ry==True and min(df_copy_for_y1.min()) < 0:
        #     fig.update_layout(yaxis2=dict(zeroline=True, zerolinewidth=1, zerolinecolor=0,autorange=True),
        #                       yaxis=dict(showgrid=False,title='',tickformat=None,ticks=None,ticklen=None,tickfont=None,tickcolor=None,linewidth=None),
        #                       xaxis=dict(showline=False, ticks=""))
    except:
        pass

    if type(df_index[0]) != str and type(df_index[0]) != list:
        # 加垂直线
        if vline != '':
            for xi in vline:
                fig.add_vline(x=xi, line_width=1, line_dash="dash", line_color=line_group_color[0])
        # 加水平线
        if hline != '':
            for yi in hline:
                fig.add_hline(y=yi, line_width=1, line_dash="dash", line_color=line_group_color[0])
        # 加垂直线2
        if vline2 != '':
            for xi in vline2:
                fig.add_vline(x=xi, line_width=1, line_dash="dash", line_color=line_group_color[1])
        # 加水平线2
        if hline2 != '':
            for yi in hline2:
                fig.add_hline(y=yi, line_width=1, line_dash="dash", line_color=line_group_color[1])

    # x轴文本格式
    if str(type(df.index[0])) == "<class 'str'>":
        fig.update_layout(xaxis={'type': 'category'})
        # 双线条调整轴的颜色
    # if num_of_col==2  and  r==2 :
    #     fig.update_layout(yaxis=dict(linecolor=color_list[0],tickcolor=color_list[0],tickfont=dict(color=color_list[0])),
    #                       yaxis2=dict(linecolor=color_list[1],tickcolor=color_list[1],tickfont=dict(color=color_list[1])))
    # #三线条轴内卷版本
    # if num_of_col==3  and  r==2 and r2==3 :
    #     fig.update_layout(yaxis=dict(linecolor=color_list[0],tickcolor=color_list[0],tickfont=dict(color=color_list[0])),
    #                       yaxis2=dict(linecolor=color_list[1],tickcolor=color_list[1],tickfont=dict(color=color_list[1])),
    #                       yaxis3=dict(linecolor=color_list[2],tickfont=dict(color=color_list[2])))
    if r_copy != [] and len(r_copy) == 1 and r2_copy == []:

        if r_copy[0] > 0:
            r_i = r_copy[0]
        else:
            r_i = num_of_col + r_copy[0]
        fig.update_layout(
            yaxis=dict(linecolor=color_list[0], tickcolor=color_list[0], tickfont=dict(color=color_list[0])),
            yaxis2=dict(linecolor=color_list[r_i - 1], tickcolor=color_list[r_i - 1],
                        tickfont=dict(color=color_list[r_i - 1])))
    # 三线条轴内卷版本
    if r_copy != [] and len(r_copy) == 1 and r2_copy != [] and len(r2_copy) == 1:
        if r_copy[0] > 0:
            r_i = r_copy[0]
        else:
            r_i = num_of_col + r_copy[0]
        if r2_copy[0] > 0:
            r2_i = r2_copy[0]
        else:
            r2_i = num_of_col + r2_copy[0]
        fig.update_layout(
            yaxis=dict(linecolor=color_list[0], tickcolor=color_list[0], tickfont=dict(color=color_list[0])),
            yaxis2=dict(linecolor=color_list[r_i - 1], tickcolor=color_list[r_i - 1],
                        tickfont=dict(color=color_list[r_i - 1])),
            yaxis3=dict(linecolor=color_list[r2_i - 1], tickfont=dict(color=color_list[r2_i - 1])))
    # 四线条轴内卷版本
    if r_copy != [] and len(r_copy) == 1 and r2_copy != [] and len(r2_copy) == 1 and r3_copy != [] and len(r3_copy) == 1:
        if r_copy[0] > 0:
            r_i = r_copy[0]
        else:
            r_i = num_of_col + r_copy[0]
        if r2_copy[0] > 0:
            r2_i = r2_copy[0]
        else:
            r2_i = num_of_col + r2_copy[0]
        if r3_copy[0] > 0:
            r3_i = r3_copy[0]
        else:
            r3_i = num_of_col + r3_copy[0]

        fig.update_layout(
            yaxis=dict(linecolor=color_list[0], tickcolor=color_list[0], tickfont=dict(color=color_list[0])),
            yaxis2=dict(linecolor=color_list[r_i - 1], tickcolor=color_list[r_i - 1],
                        tickfont=dict(color=color_list[r_i - 1])),
            yaxis3=dict(linecolor=color_list[r2_i - 1], tickfont=dict(color=color_list[r2_i - 1])),
            yaxis4=dict(linecolor=color_list[r3_i - 1], tickfont=dict(color=color_list[r3_i - 1])))
    # 更改图元素字体大小
    if font_size != '':
        fig.update_layout(xaxis=dict(tickfont=dict(size=font_size)),
                          yaxis=dict(tickfont=dict(size=font_size)),
                          yaxis2=dict(tickfont=dict(size=font_size)),
                          yaxis3=dict(tickfont=dict(size=font_size)),
                          legend=dict(font=dict(size=font_size)))
    if title!='':
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,  # 将标题放置在 x 轴的中心
                'y': 0.98  # 将标题放置在 y 轴的顶部
            })

    # 日期x轴的密度
    # 确定时间跨度和密度
    # delta = df_copy.index.max() - df_copy.index.min()
    # if delta >= pd.Timedelta(days=365):
    #     date_format = '%Y'
    # elif delta >= pd.Timedelta(days=30):
    #     date_format = '%Y-%m'
    # else:
    #     date_format = '%Y-%m-%d'
    # fig.update_layout(xaxis=dict(tickformat=date_format))
    if ycomma:
        fig.update_layout(yaxis=dict(tickformat=","))
    if ypct:
        fig.update_layout(yaxis=dict(tickformat=".0%")) #参照bar的format改
    if y2pct:
        fig.update_layout(yaxis2=dict(tickformat=".0%")) #参照bar的format改

    if ry == True and r == [] and r2 == [] and r3 == []:
        fig.update_layout(yaxis={'side': 'right'})

    if yhide==True:
        fig.update_layout(
            yaxis=dict(showline=False, showticklabels=False, showgrid=False, tickcolor='rgba(0,0,0,0)'),
            yaxis2=dict(showline=False, showticklabels=False, showgrid=False, tickcolor='rgba(0,0,0,0)'),
            yaxis3=dict(showline=False, showticklabels=False, showgrid=False, tickcolor='rgba(0,0,0,0)'),
            yaxis4 = dict(showline=False, showticklabels=False, showgrid=False, tickcolor='rgba(0,0,0,0)'))
        fig.update_layout(yaxis=dict(zeroline=False))
    if xhide==True:
        fig.update_layout(
            xaxis=dict(showline=False, showticklabels=True, showgrid=False, tickcolor='rgba(0,0,0,0)'))

    # 添加自定义按钮到模式栏中
    fig.update_layout(hide_logo)
    # fig.update_layout(hide_prompt)
    # cl(fig)

    if return_plot == False and img==False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    elif return_plot == True and img==False:
        return fig

    elif return_plot == False and img==True:
        # 使用plotly.io.to_image将图表转换为PNG图像
        img_bytes = pio.to_image(fig, scale=1,format='jpg',engine='auto')

        # 使用IPython.display.Image将图像嵌入Notebook中
        return Image(img_bytes)

PandasObject.p = p
# %%画堆积柱形图+折线图
def p_stackbar_line(df, lines=[], start='', end='', lead=0, lead_time=0, r=[], fill='', legend_right=0, width=600,
                    height=330,
                    return_plot=return_plot):
    '''
    【同时做堆积柱形图和折线图】
    df：如果是一个dataframe，则直接画图；如果是一个dataframe组成的list，则把他们merge之后再画图
    start和end：如果只需要start，直接写一个参数；但如果只需要end，需要在end前面写上''，用于占位，否则只写一个就只会被当成是start
    lead：整数，一般是1或者2，表示第几个指标要领先。0表示最后一个指标
    lead_time：整数
    fill：默认为空，如果要传入参数，从'ffill'和'bfill'里选一个传
    '''

    if str(type(df)) == "<class 'list'>":
        df_copy = merge(df)
    else:
        df_copy = df.copy()

    if start != '':
        df_copy = df_copy[start:]
    if end != '':
        df_copy = df_copy[:end]

    r_copy = r

    if type(lines) == str:
        lines = [lines]
    if not lines:
        lines = [df.columns.tolist()[0]]
    # 升序排序时间索引
    df_copy.sort_index(ascending=True, inplace=True)

    df_for_lines = df_copy[lines]
    df_copy.drop(lines, axis=1, inplace=True)

    if type(r_copy) == int:
        r_copy = [r_copy]

    num_of_col = df_copy.shape[1]
    name_list_copy = df_copy.columns.to_list()
    yaxis_list = ['y1'] * num_of_col

    # 填补缺失值
    if fill != '':
        df.fillna(method=fill)

    if lead_time > 0:
        name_list_copy[lead - 1] = name_list_copy[lead - 1] + "-领先" + str(lead_time) + "期"
        df_copy[[df_copy.columns[lead - 1]]] = df_copy[[df_copy.columns[lead - 1]]].shift(lead_time)

    if r_copy != []:
        for k in r_copy:
            # 根据指标序号，注意，传入函数参数的时候是从1开始
            yaxis_list[k - 1] = 'y2'
            name_list_copy[k - 1] = name_list_copy[k - 1] + '（右）'

    trace_list = []

    # 这一行是画折线
    for line in lines:
        trace_list.append(go.Scatter(x=df_copy.index, y=df_for_lines[line], mode='lines', yaxis='y1', name=line))

    for i in range(num_of_col):
        if str(type(df_copy.index[0])) == "<class 'str'>" or str(type(df_copy.index[0])) == "<class 'int'>":
            trace_list.append(
                go.Scatter(x=df_copy.index, y=df_copy.iloc[:, i], mode='markers+lines', yaxis=yaxis_list[i],
                           name=name_list_copy[i]))
        else:
            trace_list.append(go.Bar(x=df_copy.index, y=df_copy.iloc[:, i], yaxis=yaxis_list[i], name=name_list_copy[i],
                                     hovertemplate="%{x|%Y-%m-%d}<br>%{y}"))

    fig_data = trace_list
    fig = go.Figure(data=fig_data, layout=lo)

    # 添加自定义按钮到模式栏中
    fig.update_layout(hide_logo)

    # 用于根据传入参数调整图例的左右位置
    if legend_right != False:
        try:
            if r_copy != []:
                fig.update_layout(legend_orientation=None, width=width,
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.365,
                                              bgcolor='rgba(0,0,0,0)'))
            else:
                fig.update_layout(legend_orientation=None, width=width,
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.22,
                                              bgcolor='rgba(0,0,0,0)'))
        except:
            if r_copy != []:
                fig.update_layout(legend_orientation=None, width=700,
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.365,
                                              bgcolor='rgba(0,0,0,0)'))
            else:
                fig.update_layout(legend_orientation=None, width=700,
                                  legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.22,
                                              bgcolor='rgba(0,0,0,0)'))

    if str(type(df_copy.index[0])) == "<class 'str'>" or str(type(df_copy.index[0])) == "<class 'int'>":
        fig.update_layout(legend=dict(yanchor='top', xanchor='center', x=0.5, y=1.15, borderwidth=0))

    # 注意，barmode不能设定为stack，那样会掩盖负数
    fig.update_layout(barmode='relative', legend_traceorder='normal')

    # 改变图的白色边缘宽度
    fig.update_layout(margin=dict(l=0, r=10, b=15, t=15))

    # 左轴0刻度线取代x轴，前提是用于左轴作图的数据最小值小于零
    if r_copy != []:
        df_copy_for_y1 = df_copy.drop(list(df_copy.columns[[i - 1 for i in r_copy]]), axis=1)
    else:
        df_copy_for_y1 = df_copy
    if min(df_copy_for_y1.min()) < 0:
        fig.update_layout(yaxis=dict(zeroline=True, zerolinewidth=1, autorange=True),
                          xaxis=dict(showline=False, ticks=""))

    fig.update_layout(width=width, height=height)

    #     cl(fig)
    if return_plot == False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig
PandasObject.p_stackbar_line = p_stackbar_line
# %%画简易事件研究图
def p_event(df_input, T, interval, col_name=False,vline=True, hline='', s='', norm=False, return_data=False,return_plot=return_plot):
    '''
    【做事件研究图】
    df：Series或者DataFrame，但只能有一列，【强调】时间不能有间断点，否则需要自行填充好
    T：形如['2022-01-11','2022-02-10']的单/多元素列表
    interval：形如[-5,5]的双元素列表
    col_name:自定义列名。默认是FALSE，或者传入字符串列表参数
    vline：bool型，在T处加垂直虚线
    hline：数值型，画一条水平线
    s：调整大小
    '''
    df = df_input.copy()

    if len(T[0]) == 10:
        freq = 'd'
    elif len(T[0]) == 7:
        freq = 'm'
    elif len(T[0]) == 4:
        freq = 'y'
    if vline == True:
        vline = 0

    # 补充df的区间
    back_na = pd.DataFrame(data=np.nan,
                           index=pd.date_range(start=df.index[-1],
                                               periods=500,
                                               freq=freq,
                                               inclusive='right'),
                           columns=df.columns)
    front_na = pd.DataFrame(data=np.nan,
                            index=pd.date_range(end=df.index[0],
                                                periods=500,
                                                freq=freq,
                                                inclusive='left'),
                            columns=df.columns)

    df = pd.concat([front_na, df, back_na], axis=0)

    if str(type(df)) == "<class 'pandas.core.frame.DataFrame'>":
        indicator_name = list(df.columns)
    elif str(type(df)) == "<class 'pandas.core.series.Series'>":
        indicator_name = [df.name]

    t_list = []
    # for i in range(interval[0], interval[1] + 1):
    #     if i < 0:
    #         t_list.append('T' + str(i))
    #     elif i > 0:
    #         t_list.append('T+' + str(i))
    #     else:
    #         t_list.append('T')
    for i in range(interval[0], interval[1] + 1):
        if i < 0:
            t_list.append(i)
        elif i > 0:
            t_list.append(i)
        else:
            t_list.append(0)
    # 数据日期索引转换成字符串列表
    df_input_index_list = [datetime.strftime(x, "%Y-%m-%d") for x in df.index]

    T_list = []
    for t in T:
        t0_index = df_input_index_list.index(t)

        T_list.append(df_input_index_list[t0_index - abs(interval[0]):t0_index + interval[1] + 1])

    data_reshaped = []
    for Ti in T_list:
        data_reshaped.append(df[(str(Ti[0])[:10]):(str(Ti[-1])[:10])])

    for data_new in data_reshaped:
        data_new.index = t_list

    column_of_data_reshaped = [indicator_name[0] + ' (T=' + T[0] + ')']
    for t in T[1:]:
        column_of_data_reshaped.append('(T=' + t + ')')

    df_final = pd.concat(data_reshaped, axis=1)
    df_final.columns = column_of_data_reshaped

    # 使用T时刻的数据标准化
    # df_final_value_at_T = df_final.loc['T', :]
    df_final_value_at_T = df_final.loc[0, :]
    df_norm = df_final.copy() / df_final_value_at_T

    if norm == True:
        df_final = df_norm

    if col_name!=False:
        df_final.columns=col_name
    if return_data==False:
        return p(df_final, index_ascending=0, vline=vline, hline=hline, s=s, return_plot=return_plot)
    else:
        return df_final
    # if vline == True:
    #     # return p(df_final, index_ascending=0, vline='T', s=s)
    #     return p(df_final, index_ascending=0, vline=0, s=s,return_plot=return_plot)
    # else:
    #     return p(df_final, index_ascending=0, s=s,return_plot=return_plot)
PandasObject.p_event = p_event


# %%核密度曲线图
def p_kde(df, return_plot=return_plot):
    '''
    【做核密度曲线图】
    df：要求是数据框
    '''
    fig = ff.create_distplot([df[c] for c in df.columns[::-1]], df.columns[::-1], show_hist=False, show_rug=False,
                             colors=color_scheme)
    fig.update_layout(lo)
    fig.update_layout(width=600, height=330)
    # cl(fig)
    if return_plot == False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig
PandasObject.p_kde = p_kde

# %%WIND提取数据画季节图
def season(ID_list, name_list, start='', end='', f=0):
    '''
    【做季节图，利用WIND数据库】
    f即front，意思是向前推几年，0的话就是推0年，也就是只画今年的一条线
    '''

    if start == '':
        start = start_date

    if end == '':
        end = end_date

    # season2是置信带+近5年均值

    data = w.edb(ID_list, start, end, "Fill=Previous", usedf=True)[1]
    data.columns = name_list

    current_year = datetime.datetime.now().year
    start_year_data = str(current_year - 6) + '-12-31'

    data_copy = data.copy()
    data_copy['Year'] = data_copy.index.astype(str).str[:4]
    data_copy['Month'] = data_copy.index.astype(str).str[5:7]
    data_copy['Day'] = 1
    data_copy['Date'] = pd.to_datetime(data_copy[['Year', 'Month', 'Day']])
    data_copy.set_index('Date', drop=True, inplace=True)
    data_copy.sort_index(inplace=True)
    data_copy = data_copy[start_year_data:]

    data_pivot = pd.pivot_table(data_copy, values=data.columns[0], index=['Month'],
                                columns=['Year'], aggfunc=np.sum)
    #     display(data_pivot)
    data_pivot['Max'] = data_pivot.iloc[:, :5].max(axis=1)
    data_pivot['Min'] = data_pivot.iloc[:, :5].min(axis=1)
    data_pivot['近5年均值'] = data_pivot.iloc[:, :5].mean(axis=1)

    fig = go.Figure()
    months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

    # 定义统计量的tracelist
    trace_list_statistic = []
    trace_list_statistic.append(
        go.Scatter(x=months, y=data_pivot['Max'], name='近5年最大值', fill=None, mode='lines', line_color='#EDEDED',
                   showlegend=False))
    trace_list_statistic.append(go.Scatter(x=months, y=data_pivot['Min'], name='近5年最小值', fill='tonexty', mode='lines',
                                           # fill area between trace0 and trace1
                                           line_color='#EDEDED', showlegend=False))
    trace_list_statistic.append(
        go.Scatter(x=months, y=data_pivot['近5年均值'], name='近5年均值', line=dict(color='black', width=3, dash='10px')))

    # 定义数据的tracelist
    trace_list_data = []

    rangelist = range(5, 4 - f, -1)

    for i in rangelist:
        trace_list_data.append(
            go.Scatter(x=months, y=data_pivot.iloc[:, i], name=data_pivot.columns[i], line=dict(width=2.5)))

    trace_list = trace_list_statistic + trace_list_data

    fig_data = trace_list
    fig = go.Figure(data=fig_data, layout=lo)
    #    fig.update_layout(title_text=data.columns[0],title_x=0.5)

    # fig.show()
    return fig


PandasObject.season = season


# %%直接画季节图
def seas(data, f=0, return_data=False, return_plot=return_plot):
    '''
    【做季节图】
    data：数据框类型，可以是月频数据，也可以不是月频，不是的话会自动加总降频为月。只能有一列！！！
    f即front，意思是向前推几年，0的话就是推0年，也就是只画今年的一条线
    '''
    # season2是置信带+近5年均值
    import datetime

    date_index_var = pd.to_datetime(data.index)
    # 非季度数据
    if date_index_var.inferred_freq != 'Q-DEC':  # 判断

        current_year = datetime.datetime.now().year
        start_year_data = str(current_year - 6) + '-12-31'

        data_copy = data.copy()
        data_copy['Year'] = data_copy.index.astype(str).str[:4]
        data_copy['Month'] = data_copy.index.astype(str).str[5:7]
        data_copy['Day'] = 1
        data_copy['Date'] = pd.to_datetime(data_copy[['Year', 'Month', 'Day']])
        data_copy.set_index('Date', drop=True, inplace=True)
        data_copy.sort_index(inplace=True)
        data_copy = data_copy[start_year_data:]

        data_pivot = pd.pivot_table(data_copy, values=data.columns[0], index=['Month'],
                                    columns=['Year'], aggfunc=np.sum)
        #     display(data_pivot)
        data_pivot['Max'] = data_pivot.iloc[:, :5].max(axis=1)
        data_pivot['Min'] = data_pivot.iloc[:, :5].min(axis=1)
        data_pivot['近5年均值'] = data_pivot.iloc[:, :5].mean(axis=1)

        data_pivot.index.name = None
        data_pivot.columns.name = None

        months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        data_pivot.index = months

        fig = go.Figure()
        # 定义统计量的tracelist
        trace_list_statistic = []
        trace_list_statistic.append(
            go.Scatter(x=months, y=data_pivot['Max'], name='近5年最大值', fill=None, mode='lines', line_color='#EDEDED',
                       showlegend=False))
        trace_list_statistic.append(
            go.Scatter(x=months, y=data_pivot['Min'], name='近5年最小值', fill='tonexty', mode='lines',
                       # fill area between trace0 and trace1
                       line_color='#EDEDED', showlegend=False))
        trace_list_statistic.append(
            go.Scatter(x=months, y=data_pivot['近5年均值'], name='近5年均值', line=dict(color='black', width=3, dash='10px')))

        # 定义数据的tracelist
        trace_list_data = []

        rangelist = range(5, 4 - f, -1)

        for i in rangelist:
            trace_list_data.append(
                go.Scatter(x=months, y=data_pivot.iloc[:, i], name=data_pivot.columns[i], line=dict(width=2.5)))

        trace_list = trace_list_statistic + trace_list_data

        fig_data = trace_list
        fig = go.Figure(data=fig_data, layout=lo)
        fig.update_layout(title_text=data.columns[0], title_x=0.5)
        config = dict({'displayModeBar': False, 'showTips': False})

        if return_data == False:
            if return_plot == False:
                config = dict({'displayModeBar': False, 'showTips': False})
                fig.show(config=config)
            else:
                # 添加自定义按钮到模式栏中
                llo=dict(modebar={'orientation': 'v', 'bgcolor': 'white'},
                    updatemenus=[custom_button])
                fig.update_layout(llo)
                return fig
        else:
            return data_pivot

    else:  # 季度数据
        data_copy = data.copy()
        data_copy['月份'] = date_index_var.month
        data_copy['年度'] = date_index_var.year
        data_copy = data_copy.pivot_table(index='月份', columns='年度', values=data.columns[0])
        data_copy.index = ['Q1', 'Q2', 'Q3', 'Q4']
        data_copy.index.name = None
        data_copy.columns.name = None
        if return_data == False:
            # data_copy.iloc[:, -1 * f:].p()
            return data_copy.iloc[:, -1 * f:].p(mode='lines+markers', return_plot=return_plot, vline=-1)
            # display(data_copy)
        else:
            return data_copy


PandasObject.seas = seas


# 高级季节图
def seasuper(df, scope='m', f=5):
    '''
    超级季节图，可以做比seas的月度/季度频率更高频的，比如日频、周频的
    f:取最近几年。默认f=5，即做包含今年在内的5年的曲线
    scope：横轴的刻度线数目，'d','w','m'
    '''
    if scope == 'm':
        tickformat = '%m'
        nticks = 12
        xaxis_dtick = None
    elif scope == 'w' or scope == 'd':
        tickformat = "%W"
        xaxis_dtick = 86400000 * 7 * 2
        nticks = None
    # elif scope=='q':
    #     tickformat = "%Q"
    #     nticks = 4
    #     xaxis_dtick=4


    df_copy = df.copy()
    name = list(df.columns)[0]
    df_copy['year'] = df_copy.index.year
    year_list = df_copy['year'].drop_duplicates().tolist()
    df_seas_list = []
    # display(df)
    for year in year_list[-1 * f:]:
        df_seas_list.append(pd.DataFrame(df[str(year)+'-01-01':str(year)+'-12-31']).reset_index(drop=True).rename(columns={name: str(year)}))

    merged = merge_for_plotly(df_seas_list)
    full_date = merged.dropna(axis=1).columns[0]
    merged.index = df.loc[str(full_date),:].index.tolist()

    return merged.p(return_plot=True).update_layout(title_text=name, title_x=0.5, title_y=0.98,
                                                    title_font=dict(size=13), xaxis=dict(tickformat=tickformat),
                                                    xaxis_dtick=xaxis_dtick).update_traces(
        hovertemplate='%{x|%m-%d}<br>%{y}').update_xaxes(nticks=nticks)


PandasObject.seasuper = seasuper


# %%WIND提取数据画子图
def spl(ID_list, name_list, start='', end='', d=[], r=[], fill=''):
    '''
    d代表down，即下面的图
    fill默认为空，如果要传入参数，从'ffill'和'bfill'里选一个传
    '''
    if start == '':
        start = start_date

    if end == '':
        end = end_date

    r_copy = r
    if type(r_copy) == int:
        r_copy = [r_copy]

    df = w.edb(ID_list, start, end, usedf=True)[1]
    df.columns = name_list

    # 填补缺失值
    if fill != '':
        df.fillna(method=fill)

    d_copy = d.copy()
    d_copy = [i - 1 for i in d_copy]

    num_of_col = df.shape[1]
    name_list_copy = df.columns.to_list()
    yaxis_list = [False] * num_of_col

    if r_copy != []:
        for k in r_copy:
            # 根据指标名称分右轴
            #             right_index=name_list.index(k)
            #             yaxis_list[right_index]='y2'
            #             name_list_copy[right_index]=name_list_copy[right_index]+'（右）'
            # 根据指标序号，注意，传入函数参数的时候是从1开始
            yaxis_list[k - 1] = True
            name_list_copy[k - 1] = name_list_copy[k - 1] + '（右）'

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                        specs=[[{"secondary_y": True}], [{"secondary_y": True}]])

    fig["layout"].update(go.Layout({
        'colorway': color_scheme,
        'font': {'family': 'Microsoft YaHei'},
        'height': 600,
        'hoverlabel': {'font': {'size': 13}},
        'hovermode': 'closest',
        'legend': {'font': {'color': 'RGB(0,0,0)', 'family': 'Microsoft YaHei', 'size': 13},
                   'orientation': 'h',
                   'title': {'text': ''},
                   'xanchor': 'center',
                   'x': 0.5},
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'showlegend': True,
        'xaxis': {'color': 'RGB(0,0,0)',
                  'anchor': 'y',
                  'domain': [0.0, 0.94],
                  'matches': 'x2',
                  'showticklabels': False,
                  'tickfont': {'size': 13}},
        'xaxis2': {'color': 'RGB(0,0,0)',
                   'anchor': 'y3',
                   'domain': [0.0, 0.94],
                   'showticklabels': True,
                   'ticks': "outside",
                   'linewidth': 1,
                   'linecolor': 'RGB(0,0,0)',
                   'tickfont': {'size': 13}},
        'yaxis': {'color': 'RGB(0,0,0)',
                  'anchor': 'x',
                  'domain': [0.525, 1.0],
                  'showticklabels': True,
                  'ticks': "outside",
                  'linewidth': 1,
                  'linecolor': 'RGB(0,0,0)',
                  'tickfont': {'size': 13}},
        'yaxis2': {'color': 'RGB(0,0,0)',
                   'anchor': 'x',
                   'overlaying': 'y',
                   'side': 'right',
                   'showticklabels': True,
                   'ticks': "outside",
                   'linewidth': 1,
                   'linecolor': 'RGB(0,0,0)',
                   'tickfont': {'size': 13}},
        'yaxis3': {'color': 'RGB(0,0,0)',
                   'anchor': 'x2',
                   'domain': [0.0, 0.475],
                   'showticklabels': True,
                   'ticks': "outside",
                   'linewidth': 1,
                   'linecolor': 'RGB(0,0,0)',
                   'tickfont': {'size': 13}},
        'yaxis4': {'color': 'RGB(0,0,0)',
                   'anchor': 'x2',
                   'overlaying': 'y3',
                   'side': 'right',
                   'showticklabels': True,
                   'ticks': "outside",
                   'linewidth': 1,
                   'linecolor': 'RGB(0,0,0)',
                   'tickfont': {'size': 13}}}))

    for i in range(num_of_col):
        if i not in d_copy:
            fig.add_trace(
                go.Scatter(x=df.index, y=df.iloc[:, i], mode='lines', name=name_list_copy[i], connectgaps=True,
                           hovertemplate="%{x|%Y-%m-%d}<br>%{y}"), row=1, col=1, secondary_y=yaxis_list[i])
        else:
            fig.add_trace(
                go.Scatter(x=df.index, y=df.iloc[:, i], mode='lines', name=name_list_copy[i], connectgaps=True,
                           hovertemplate="%{x|%Y-%m-%d}<br>%{y}"), row=2, col=1, secondary_y=yaxis_list[i])

    config = dict({'displayModeBar': False, 'showTips': False})
    # fig.show(config=config)
    return fig


PandasObject.spl = spl


# %%直接画子图0，目前弃用状态
# def sp0(data,start='',end='',d=[],r=[],fill='',small=0):
#     '''
#     d代表down，即下面的图
#     fill默认为空，如果要传入参数，从'ffill'和'bfill'里选一个传
#     '''
#     df=data.copy()
#     if str(type(df))=="<class 'list'>":
#         df=merge(df)
#     else:
#         df=df.copy()

#     if start!='':
#         df=df[start:]
#     if end!='':
#         df=df[:end]

#     r_copy=r
#     if type(r_copy)==int:
#         r_copy=[r_copy]

#     d_copy=d.copy()
#     d_copy=[i - 1 for i in d_copy]


#     #填补缺失值
#     if fill!='':
#         df.fillna(method=fill)


#     num_of_col=df.shape[1]
#     name_list_copy=df.columns.to_list()
#     yaxis_list=[False]*num_of_col

#     if r_copy!=[]:
#         for k in r_copy:
#         #根据指标名称分右轴
# #             right_index=name_list.index(k)
# #             yaxis_list[right_index]='y2'
# #             name_list_copy[right_index]=name_list_copy[right_index]+'（右）'
#             #根据指标序号，注意，传入函数参数的时候是从1开始
#             yaxis_list[k-1]=True
#             name_list_copy[k-1]=name_list_copy[k-1]+'（右）'

#     fig=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing = 0.05 ,specs=[[{"secondary_y": True}], [{"secondary_y": True}]])

#     fig["layout"].update(go.Layout({
#         'colorway': color_scheme,
#         'font': {'family': 'Microsoft YaHei'},
#         'height': 600,
#         'hoverlabel': { 'font': {'size': 13}},
#         'hovermode': 'closest',
#         'legend': {'font': {'color': 'RGB(0,0,0)', 'family': 'Microsoft YaHei', 'size': 13},
#                    'orientation': 'h',
#                    'title': {'text': ''},
#                    'xanchor':'center',
#                    'x':0.5},
#         'plot_bgcolor': 'rgba(0,0,0,0)',
#         'showlegend': True,
#         'xaxis': {'color':'RGB(0,0,0)',
#                   'anchor': 'y',
#                   'domain': [0.0, 0.94],
#                   'matches': 'x2',
#                   'showticklabels': False,
#                   'tickfont':{'size':13}},
#         'xaxis2': {'color':'RGB(0,0,0)',
#                    'anchor': 'y3',
#                    'domain': [0.0, 0.94],
#                    'showticklabels': True,
#                    'ticks':"outside",
#                    'linewidth':1,
#                    'linecolor':'RGB(0,0,0)',
#                    'tickfont':{'size':13}},
#         'yaxis': {'color':'RGB(0,0,0)',
#                   'anchor': 'x',
#                   'domain': [0.525, 1.0],
#                   'showticklabels': True,
#                   'ticks':"outside",
#                   'linewidth':1,
#                   'linecolor':'RGB(0,0,0)',
#                   'tickfont':{'size':13}},
#         'yaxis2': {'color':'RGB(0,0,0)',
#                    'anchor': 'x',
#                    'overlaying': 'y',
#                    'side': 'right',
#                    'showticklabels': True,
#                    'ticks':"outside",
#                    'linewidth':1,
#                    'linecolor':'RGB(0,0,0)',
#                    'tickfont':{'size':13}},
#         'yaxis3': {'color':'RGB(0,0,0)',
#                    'anchor': 'x2',
#                    'domain': [0.0, 0.475],
#                    'showticklabels': True,
#                    'ticks':"outside",
#                    'linewidth':1,
#                    'linecolor':'RGB(0,0,0)',
#                    'tickfont':{'size':13}},
#         'yaxis4': {'color':'RGB(0,0,0)',
#                    'anchor': 'x2',
#                    'overlaying': 'y3',
#                    'side': 'right',
#                    'showticklabels': True,
#                    'ticks':"outside",
#                    'linewidth':1,
#                    'linecolor':'RGB(0,0,0)',
#                    'tickfont':{'size':13}}}))


#     for i in range(num_of_col):
#         if i not in d_copy :
#             fig.add_trace(go.Scatter(x=df.index,y=df.iloc[:,i],mode='lines',name=name_list_copy[i],connectgaps=True,hovertemplate="%{x|%Y-%m-%d}<br>%{y}"),row=1,col=1,secondary_y=yaxis_list[i])
#         else:
#             fig.add_trace(go.Scatter(x=df.index,y=df.iloc[:,i],mode='lines',name=name_list_copy[i],connectgaps=True,hovertemplate="%{x|%Y-%m-%d}<br>%{y}"),row=2,col=1,secondary_y=yaxis_list[i])

#     if small==1:
#         fig["layout"].update(go.Layout(width=800))
#     elif small==2:
#         fig["layout"].update(go.Layout(width=1000))

#     config = dict({'displayModeBar':False,'showTips':False})
#     fig.show(config=config)
# %%直接画子图
def sp(df, start='', end='', d=[], p=[], r=[], ds=[],fill='', s=1,
       height=None, width=None, period_df=None,  period=['上行','下行'], ea=False,
       return_plot=return_plot):
    '''
    p代表position，即每一个指标在哪个图，比如，如果有6个指标，则p=[1,1,2,2,3,3]
    r代表让第几个指标放在右轴
    s=1,2,3,4,5 对应不同的宽度尺寸
    fill默认为空，如果要传入参数，从'ffill'和'bfill'里选一个传
    ea：全称each，如果p没有传入参数且ea=1，全部指标自动做单个子图
    '''
    r_copy = r
    if type(r_copy) == int:
        r_copy = [r_copy]

    if str(type(df)) == "<class 'list'>":
        df_copy = merge(df)
    else:
        df_copy = df.copy()

    if start != '':
        df_copy = df_copy[start:]
    if end != '':
        df_copy = df_copy[:end]

    if d != [] and p == []:
        p = [1] * (df_copy.shape[1])
        for down in d:
            p[down - 1] = 2

    if str(type(period_df))!="<class 'NoneType'>":
        period=list(set(period_df.iloc[:,0].dropna()))

    # 简化做单图的参数传入方式
    if p == [] :
        ea=True
        p = [x for x in range(1, df_copy.shape[1] + 1)]

    # 用n来判断应当让函数做几个子图
    n = max(p)

    p_copy = p.copy()

    # 填补缺失值
    if fill != '':
        df_copy.fillna(method=fill)

    num_of_col = df_copy.shape[1]
    name_list_copy = df_copy.columns.to_list()
    yaxis_list = [False] * num_of_col

    #虚线
    ds_copy = ds
    dash_list = [None] * num_of_col
    if type(ds_copy) == int:
        ds_copy = [ds_copy]
    if ds_copy != []:
        for d in ds_copy:
            dash_list[d - 1] = 'dot'



    if r_copy != []:
        for k in r_copy:
            # 根据指标名称分右轴
            #             right_index=name_list.index(k)
            #             yaxis_list[right_index]='y2'
            #             name_list_copy[right_index]=name_list_copy[right_index]+'（右）'
            # 根据指标序号，注意，传入函数参数的时候是从1开始
            yaxis_list[k - 1] = True
            name_list_copy[k - 1] = name_list_copy[k - 1] + '（右）'

    spec_list = []
    for i in range(n):
        spec_list.append([{"secondary_y": True}])

    fig = make_subplots(rows=n, cols=1, shared_xaxes=True, vertical_spacing=(0.05 - 0.005 * (n - 2)), specs=spec_list)
    #     fig=make_subplots(rows=n,cols=1,shared_xaxes=True,vertical_spacing = 0.05)

    fig["layout"].update(go.Layout({
        'colorway': color_scheme,
        'font': {'family': 'Arial, KaiTi'},
        'height': 200 * n + 200,
        'hoverlabel': {'font': {'size': 13}},
        'hovermode': 'closest',
        'legend': {'font': {'color': 'RGB(0,0,0)', 'family': 'Arial, KaiTi', 'size': 13},
                   'orientation': 'h',
                   'title': {'text': ''}},
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'showlegend': True,
        'xaxis': {'color': 'RGB(0,0,0)',
                  'anchor': 'y',
                  'matches': 'x2',
                  'showgrid': False,
                  'showticklabels': False,
                  'tickfont': {'size': 13}},
        'yaxis': {'color': 'RGB(0,0,0)',
                  'anchor': 'x',
                  'showgrid': False,
                  'showticklabels': True,
                  'ticks': "outside",
                  'linewidth': 1,
                  'linecolor': 'RGB(0,0,0)',
                  'tickfont': {'size': 13},
                  'zeroline': False},
        'yaxis2': {'color': 'RGB(0,0,0)',
                   'anchor': 'x',
                   'overlaying': 'y',
                   'side': 'right',
                   'showgrid': False,
                   'showticklabels': True,
                   'ticks': "outside",
                   'linewidth': 1,
                   'linecolor': 'RGB(0,0,0)',
                   'tickfont': {'size': 13},
                   'zeroline': False}}))

    # 生成x轴
    xaxis_dict = []
    for i in range(2, n + 1):
        xaxis_dict.append({'xaxis' + str(i): {'color': 'RGB(0,0,0)',
                                              'anchor': 'y' + str(int(2 * i - 1)),
                                              'matches': 'x',
                                              'linewidth': 1,
                                              'showline': False,
                                              'linecolor': 'RGB(0,0,0)',
                                              'showgrid': False,
                                              'showticklabels': False,
                                              'tickfont': {'size': 13}}})
    xaxis_dict[n - 2]['xaxis' + str(int(n))]['showticklabels'] = True
    xaxis_dict[n - 2]['xaxis' + str(int(n))]['showline'] = True
    xaxis_dict[n - 2]['xaxis' + str(int(n))]['ticks'] = 'outside'

    # 生成y轴
    yaxis_dict = []
    for i in range(3, 2 * n + 1):
        if i % 2 == 0:
            yaxis_dict.append({'yaxis' + str(i): {'color': 'RGB(0,0,0)',
                                                  'anchor': 'x' + str(int(i / 2)),
                                                  'overlaying': 'y' + str(i - 1),
                                                  'side': 'right',
                                                  'showgrid': False,
                                                  'showticklabels': True,
                                                  'ticks': "outside",
                                                  'linewidth': 1,
                                                  'linecolor': 'RGB(0,0,0)',
                                                  'tickfont': {'size': 13},
                                                  'zeroline': False}})
        else:
            yaxis_dict.append({'yaxis' + str(i): {'color': 'RGB(0,0,0)',
                                                  'anchor': 'x' + str(int((i + 1) / 2)),
                                                  'showgrid': False,
                                                  'showticklabels': True,
                                                  'ticks': "outside",
                                                  'linewidth': 1,
                                                  'linecolor': 'RGB(0,0,0)',
                                                  'tickfont': {'size': 13},
                                                  'zeroline': False}})

    for j in range(2, n + 1):
        fig["layout"].update(go.Layout(xaxis_dict[j - 2]))

    for j in range(3, 2 * n + 1):
        fig["layout"].update(go.Layout(yaxis_dict[j - 3]))

    for i in range(num_of_col):
        fig.add_trace(go.Scatter(x=df_copy.index, y=df_copy.iloc[:, i], mode='lines', name=name_list_copy[i],
                                 hovertemplate="%{x|%Y-%m-%d}<br>%{y}", connectgaps=True,line=dict(dash=dash_list[i])), row=p[i], col=1,
                      secondary_y=yaxis_list[i])
        if yaxis_list[i] == False and min(df_copy.iloc[:, [i]].min()) < 0:
            fig["layout"].update(go.Layout(
                {'yaxis' + str(p[i] * 2 - 1): {'zeroline': True, 'zerolinecolor': 'Black', 'zerolinewidth': 1}}))
            fig["layout"].update(go.Layout({'xaxis' + str(p[i]): {'showline': False, 'ticks': ''}}))

    # 如果period_df,period都传入了参数则调用plot_shade函数
    if str(type(period_df)) != "<class 'NoneType'>":
        period_df_copy = period_df.copy()
        period_df_copy.columns = ['阶段']
        df_copy[period] = np.nan
        for k in range(len(period)):
            fig.add_trace(go.Bar(x=df_copy.index, y=df_copy[period[k]], name=period[k], marker_color=shade_color[k]))

        # 图的横轴起始时间
        start_x = df_copy.index[0]
        end_x = df_copy.index[-1]
        fig.update_layout({'xaxis': {'range': [str(start_x.year) + '-' + str(start_x.month) + '-' + str(start_x.day),
                                               str(end_x.year) + '-' + str(end_x.month) + '-' + str(end_x.day)]}})
        fig = splot_shade(fig, period_df, period)

    # 改变图的白色边缘宽度
    # fig["layout"].update(margin=dict(l=60,r=15,b=None,t=50))

    fig["layout"].update(
        go.Layout(legend=dict(bgcolor='rgba(0,0,0,0)', xanchor='center', x=0.47, y=-0.05, borderwidth=None)))

    if s == 1:
        fig["layout"].update(go.Layout(width=800))
    elif s == 2:
        fig["layout"].update(go.Layout(width=900))
    elif s == 3:
        fig["layout"].update(go.Layout(width=1000))
    elif s == 4:
        fig["layout"].update(go.Layout(width=1100))
    elif s == 5:
        fig["layout"].update(go.Layout(width=1200))

    if width != None:
        fig["layout"].update(go.Layout(width=width))
    if height != None:
        fig["layout"].update(go.Layout(height=height))
    # cl(fig)
    if return_plot == False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig


PandasObject.sp = sp


# %%子图阴影，之后也要用chatGPT优化一下
def splot_shade(splot, period_df, period):
    '''
    splot为plotly对象，是利用splo2函数生成的子图
    period_df_copy是一个dataframe，index是日期戳，可以有多列也可以有一列，但列中必须包含字段“阶段”，阶段是和时间对应的阶段名称。
    比如，阶段是1,2,3,4,5,6这种数字，也可以是“复苏”，“过热”，“滞胀”，“衰退”这种字符串
    shade_color是阴影颜色，这个在plotly包导入的时候定义好
    '''
    shape_dict = []

    period_df_copy = period_df.copy()
    # 这句话要注释！！！否则会剔除NA，从而把单阶段阴影搞成连续的，就不对了。
    # period_df_copy.dropna(inplace=True)

    for i in range(len(period_df_copy.index.tolist())):
        if i != len(period_df_copy.index.tolist()) - 1:
            if pd.isna(period_df_copy['阶段'][i]) == False:
                shape_dict.append(dict(type='rect', xref='x', yref='paper',
                                       x0=str(period_df_copy.index[i])[:10], x1=str(period_df_copy.index[i + 1])[:10],
                                       y0=0, y1=1,
                                       fillcolor=shade_color[period.index(period_df_copy['阶段'][i])],
                                       opacity=0.30, layer="below",
                                       line_width=0))
            else:
                pass
        else:
            break
    splot.update_layout(shapes=shape_dict)
    # config = dict({'displayModeBar':False,'showTips':False})
    # splot.show(config=config)
    return splot


# %%单图阴影
# def plot_shade(plot, period_df, period):
#     '''
#     plot为plotly对象，是利用plo函数生成的子图
#     period_df是一个dataframe，index是日期戳，可以有多列也可以有一列，但列中必须包含字段“阶段”，阶段是和时间对应的阶段名称。
#     比如，阶段是1,2,3,4,5,6这种数字，也可以是“复苏”，“过热”，“滞胀”，“衰退”这种字符串
#     shade_color是阴影颜色，这个在plotly包导入的时候定义好
#     '''
#     shape_dict = []
#
#     period_df_copy = period_df.copy()
#     # period_df_copy.dropna(inplace=True)
#
#     for i in range(len(period_df_copy.index.tolist())):
#         if i != len(period_df_copy.index.tolist()) - 1:
#             if pd.isna(period_df_copy['阶段'][i]) == False:
#                 shape_dict.append(dict(type='rect', xref='x', yref='paper',
#                                        x0=str(period_df_copy.index[i])[:10], x1=str(period_df_copy.index[i + 1])[:10],
#                                        y0=0, y1=1,
#                                        fillcolor=shade_color[period.index(period_df_copy['阶段'][i])],
#                                        opacity=0.30, layer="below",
#                                        line_width=0))
#             else:
#                 pass
#         else:
#             break
#     plot.update_layout(shapes=shape_dict)
#     plot.update_layout({'xaxis': {'range': [plot.layout.xaxis.range[0], plot.layout.xaxis.range[1]]}})
#     config = dict({'displayModeBar': False, 'showTips': False})
#     # plot.show(config=config)
#     return plot
import pandas as pd

# def plot_shade(plot, period_df, period, shade_color):
#     shape_dict = []
#
#     period_df_copy = period_df.copy()
#
#     for i in range(len(period_df_copy)):
#         current_stage = period_df_copy['阶段'][i]
#         next_stage = period_df_copy['阶段'].iloc[i + 1] if i + 1 < len(period_df_copy) else None
#
#         if not pd.isna(current_stage) and current_stage in period:
#             shape_dict.append(dict(
#                 type='rect',
#                 xref='x',
#                 yref='paper',
#                 x0=str(period_df_copy.index[i])[:10],
#                 x1=str(period_df_copy.index[i + 1])[:10] if next_stage is not None else str(period_df_copy.index[i])[:10],
#                 y0=0,
#                 y1=1,
#                 fillcolor=shade_color[period.index(current_stage)],
#                 opacity=0.30,
#                 layer="below",
#                 line_width=0
#             ))
#
#     plot.update_layout(shapes=shape_dict)
#     plot.update_layout({'xaxis': {'range': [plot.layout.xaxis.range[0], plot.layout.xaxis.range[1]]}})
#     config = dict({'displayModeBar': False, 'showTips': False})
#
#     return plot
# import pandas as pd
#
# def plot_shade(plot, period_df, period, shade_color):
#     shape_dict = []
#     period_df_copy = period_df.copy()
#     period_df_copy['日期'] = pd.to_datetime(period_df_copy.index)  # 转换时间字符串为日期对象
#
#     iterator = period_df_copy.iterrows()
#     _, prev_row = next(iterator)  # 获取第一个行，并作为前一行
#
#     for _, row in iterator:
#         current_stage = prev_row['阶段']
#         next_stage = row['阶段']
#
#         if not pd.isna(current_stage) and current_stage in period:
#             shape_dict.append(dict(
#                 type='rect',
#                 xref='x',
#                 yref='paper',
#                 x0=str(prev_row['日期'])[:10],
#                 x1=str(row['日期'])[:10],
#                 y0=0,
#                 y1=1,
#                 fillcolor=shade_color[period.index(current_stage)],
#                 opacity=0.30,
#                 layer="below",
#                 line_width=0
#             ))
#
#         prev_row = row  # 更新前一行为当前行
#
#     plot.update_layout(shapes=shape_dict)
#     plot.update_layout({'xaxis': {'range': [plot.layout.xaxis.range[0], plot.layout.xaxis.range[1]]}})
#     config = dict({'displayModeBar': False, 'showTips': False})
#
#     return plot
#%%单图阴影优化加速版
def plot_shade(plot, period_df, period):
    shape_dict = []
    period_df_copy = period_df.copy()
    period_df_copy['日期'] = pd.to_datetime(period_df_copy.index)  # 转换时间字符串为日期对象

    iterator = period_df_copy.iterrows()
    _, prev_row = next(iterator)  # 获取第一个行，并作为前一行

    for _, row in iterator:
        current_stage = prev_row['阶段']
        next_stage = row['阶段']

        if not pd.isna(current_stage) and current_stage in period:
            shape_dict.append(dict(
                type='rect',
                xref='x',
                yref='paper',
                x0=str(prev_row['日期'])[:10],
                x1=str(row['日期'])[:10],
                y0=0,
                y1=1,
                fillcolor=shade_color[period.index(current_stage)],
                opacity=0.30,
                layer="below",
                line_width=0
            ))

        prev_row = row  # 更新前一行为当前行

    plot.update_layout(shapes=shape_dict)
    plot.update_layout({'xaxis': {'range': [plot.layout.xaxis.range[0], plot.layout.xaxis.range[1]]}})
    config = dict({'displayModeBar': False, 'showTips': False})

    return plot

# %%生成阶段数据框
def gen_period_df_single(tsdata, interval, name=None):
    '''
    生成阶段数据框，用于传入p()中的period_df。只生成一个阶段
    tsdata：基础数据，数据框格式
    intertval：形如
    [['2008-11-01','2010-11-30'],
    ['2013-02-01','2014-10-31']]，嵌套列表，表示阶段的每一个区间
    name：阶段的名称，字符串格式
    '''
    if name==None:
        name='阶段'
    df_stage = pd.DataFrame(np.nan, index=tsdata.index, columns=['阶段'])
    for x in interval:
        df_stage.loc[x[0]:x[1], :] = name
    return df_stage


# %%修改阶段数据框
def gen_period_df_add(df_stage, interval, name):
    '''
    把gen_period_df_single函数生成的元素添加新的阶段，注意，这个会修改传入的df_stage
    '''
    for x in interval:
        df_stage.loc[x[0]:x[1], :] = name
    return df_stage

#%%生成阶段数据虚拟变量
def gen_period_dummy(start,end,freq):
    '''
    生成对应时间的阶段虚拟变量
    '''
    return 1
# %%柱形图。目前还没研究明白如何做双轴柱形图
def bar(df, r=[], legend_right=False, hline='', s='', stack=False, label=False, ypct=None,fmt=None, return_plot=return_plot,
        height=None, width=None, barwidth=None, meangap=False):
    '''
    【做柱形图】
    '''

    r_copy = r
    if type(r_copy) == int:
        r_copy = [r_copy]

    num_of_col = df.shape[1]
    name_list_copy = df.columns.to_list()
    yaxis_list = ['y1'] * num_of_col

    if fmt != None:
        label = True

    if fmt == '0.00':
        label_format = '%{text:.2f}'
    elif fmt == '0.0':
        label_format = '%{text:.1f}'
    elif fmt == '0':
        label_format = '%{text:.0f}'
    elif fmt == '0.00%':
        label_format = '%{text:.2%}'
    elif fmt == '0.0%':
        label_format = '%{text:.1%}'
    elif fmt == '0%':
        label_format = '%{text:.0%}'

    if r_copy != []:
        for k in r_copy:
            # 根据指标名称分右轴
            #             right_index=name_list.index(k)
            #             yaxis_list[right_index]='y2'
            #             name_list_copy[right_index]=name_list_copy[right_index]+'（右）'
            # 根据指标序号，注意，传入函数参数的时候是从1开始
            yaxis_list[k - 1] = 'y2'
            name_list_copy[k - 1] = name_list_copy[k - 1] + '（右）'
            # 循环生成trace
    trace_list = []
    # 判断索引是否是多层索引，从而决定是否做多层索引柱形图
    if str(type(df.index)) == "<class 'pandas.core.indexes.multi.MultiIndex'>":
        layer_length = len(df.index[0])
        df_index = []
        df_index_name = df.index.names
        if df_index_name == [None] * layer_length:
            df_index_name_list = ['level_' + str(x) for x in range(layer_length)]
        else:
            df_index_name_list = list(df_index_name)
        for i in range(layer_length):
            df_index.append(df.reset_index()[df_index_name_list[i]].tolist())
    else:
        df_index = df.index
    # print(df_index)

    for i in range(num_of_col):
        if label == True:
            text_i = df.iloc[:, i]
            textposition = 'outside'
            texttemplate_i = label_format
        else:
            text_i = None
            textposition = None
            texttemplate_i = None
        # display(pd.DataFrame(text_i))
        # if str(text_i)=='nan':
        #     text_i=''
        #     # texttemplate_i=None
        #     # textposition=None
        # else:
        #     text_i=text_i

        trace_list.append(go.Bar(x=df_index, y=df.iloc[:, i], yaxis=yaxis_list[i], name=name_list_copy[i], text=text_i,
                                 textposition=textposition, texttemplate=texttemplate_i, offsetgroup=i, width=barwidth))
    fig_data = trace_list
    fig = go.Figure(data=fig_data, layout=lo)
    # 添加自定义按钮到模式栏中
    fig.update_layout(hide_logo)
    fig.update_layout(yaxis=dict(zeroline=True, zerolinewidth=1, autorange=True), xaxis=dict(showline=False, ticks=""))
    fig.update_layout(legend=dict(yanchor='top', xanchor='center', x=0.5, y=1.15, borderwidth=0))
    if ypct:
        fig.update_layout(yaxis=dict(tickformat=".0%")) #参照bar的format改
    # 用于根据传入参数调整图例的左右位置
    if legend_right != False:
        if r_copy != []:
            fig.update_layout(legend_orientation=None, width=800,
                              legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.365,
                                          bgcolor='rgba(0,0,0,0)'))
        else:
            fig.update_layout(legend_orientation=None, width=800,
                              legend=dict(font=dict(family="Arial, KaiTi", color='RGB(0,0,0)', size=13), x=1.22,
                                          bgcolor='rgba(0,0,0,0)'))

    # 加水平线
    if hline != '':
        fig.add_hline(y=hline, line_width=1, line_dash="dash", line_color='black')

    fig["layout"].update(go.Layout(height=height, width=width))

    # 调整大小
    if s == 1:
        fig["layout"].update(go.Layout(height=600, width=800))
    elif s == 2:
        fig["layout"].update(go.Layout(height=700, width=900))
    elif s == 3:
        fig["layout"].update(go.Layout(height=800, width=1000))
    elif s == 4:
        fig["layout"].update(go.Layout(height=900, width=1100))
    elif s == 5:
        fig["layout"].update(go.Layout(height=1000, width=1200))

    if str(type(df.index[0])) == "<class 'str'>":
        fig.update_layout(xaxis={'type': 'category'})

    # 堆积柱形图
    if stack == True:
        fig.update_layout(barmode='relative', legend_traceorder='normal')

    if meangap == True:
        fig.update_layout(bargap=1, bargroupgap=1)
    # cl(fig)
    if return_plot == False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig
PandasObject.bar = bar
def bar_2color(df, width='', height='', label=False, fmt='0.00%'):
    '''
    上下双色图，要求传入的数据是单列！！！
    '''
    if fmt == '0.00':
        label_format = '%{text:.2f}'
    elif fmt == '0.0':
        label_format = '%{text:.1f}'
    elif fmt == '0':
        label_format = '%{text:.0f}'
    elif fmt == '0.00%':
        label_format = '%{text:.2%}'
    elif fmt == '0.0%':
        label_format = '%{text:.1%}'
    elif fmt == '0%':
        label_format = '%{text:.0%}'
    if fmt != None:
        label = True
    if label == True:
        text = df.iloc[:, 0]
        textposition = 'outside'
        texttemplate = label_format
    else:
        text = None
        textposition = None
        texttemplate = None

    df_copy = df.copy()
    df_copy["Color"] = np.where(df_copy[(df_copy.columns)[0]] < 0, 'red', 'blue')
    df_copy_bar = pd.DataFrame(index=df_copy.index).bar(return_plot=True)
    df_copy_bar.add_trace(go.Bar(x=df_copy.index, y=df_copy[(df_copy.columns)[0]], marker_color=df_copy["Color"],
                                 name=list(df_copy.columns)[0], text=text,
                                 textposition=textposition, texttemplate=texttemplate))
    if width != '':
        df_copy_bar.update_layout(width=width, height=height)

    # cl(df_copy_bar)
    return df_copy_bar
PandasObject.bar_2color = bar_2color
#%%堆积柱+折线
def bar_line(data_frame, line='' ,y2=True,width=700, height=400,return_plot=return_plot):
    '''
    data_frame：索引是字符串，列也是字符串，数据中有一列是其他列的相加
    主要为了做【堆积】柱形图和折线图的组合图
    '''
    # 提取索引和列
    index = data_frame.index.tolist()
    columns = data_frame.columns.tolist()

    # 创建图形对象
    fig = go.Figure()

    if y2==True:
        yaxis="y2"
    else:
        yaxis="y"

    line=data_frame.columns.tolist()[1] #默认是取第二列做折线
    # 绘制折线图
    if line in columns:
        fig.add_trace(go.Scatter(
            x=index,
            y=data_frame[line],
            name=line,
            yaxis=yaxis
        ))
    # 绘制柱形图
    for column in columns[::-1]:
        if column != line:
            fig.add_trace(go.Bar(
                x=index,
                y=data_frame[column],
                name=column
            ))
    # 创建布局

    fig.layout=lo
    fig.update_layout(
        barmode='stack',  # 堆积柱形图
        # yaxis=dict(title='柱形图'),  # 第一个y轴标签
        # yaxis2=dict(title='折线图', overlaying='y', side='right'),  # 第二个y轴标签
        # legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),  # 图例位置
    )

    fig.update_layout(width=width, height=height)

    fig.update_layout(legend=dict(yanchor='top', xanchor='center', x=0.5, y=1.15, borderwidth=0),
                      barmode='relative', legend_traceorder='reversed')
    # 添加自定义按钮到模式栏中
    fig.update_layout(hide_logo)
    # cl(fig)
    if return_plot == False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig
PandasObject.bar_line = bar_line
# %%饼形图
def pie(df, labels=None, values=None,
        textinfo='none', direction='clockwise',
        sort=False, rotation=0,
        legend_right=False, s='', width=600,height=600,
        showlegend=1,return_plot=return_plot):
    '''
    【做饼形图】
    labels：string
    values：string
    textinfo：字符串，取值如下
    The 'textinfo' property is a flaglist and may be specified
    as a string containing:
      - Any combination of ['label', 'text', 'value', 'percent'] joined with '+' characters
        (e.g. 'label+text')
        OR exactly one of ['none'] (e.g. 'none')
    '''

    # Check if the DataFrame has a single column and string index
    if len(df.columns) == 1 and df.index.dtype == 'object':
        labels = df.index
        values = df.iloc[:, 0]
    else:
        try:
            labels = df[labels]
        except:
            labels = df.reset_index()[labels]

        values = df[values]

    if showlegend==1:
        showlegend=True
    else:
        showlegend=False

    trace = [go.Pie(labels=labels, values=values, direction=direction, sort=sort, rotation=rotation, showlegend=showlegend, textinfo=textinfo)]
    fig = go.Figure(data=trace, layout=lo)
    fig.update_layout(width=width, height=height)
    # 添加自定义按钮到模式栏中
    fig.update_layout(hide_logo)
    if s == 1:
        fig.update_layout(width=700)
    elif s == 2:
        fig.update_layout(width=1000)
    elif s == 3:
        fig.update_layout(width=1000, height=600)
    elif s == 4:
        fig.update_layout(width=1300, height=700)

    if legend_right:
        fig.update_layout(legend=dict(xanchor='right', x=1.1, y=0, orientation='v'))
    else:
        fig.update_layout(legend=dict(yanchor='top', x=0.5, y=1.2, orientation='h'))
    # fig.update_layout(width=width,height=height)
    # cl(fig)
    if not return_plot:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig

PandasObject.pie = pie
from sklearn.decomposition import PCA
from scipy.optimize import leastsq
# 定义椭圆方程
# 定义椭圆方程
def ellipse_func(x, a, b, h, k, theta):
    return h + a * np.cos(theta) * np.cos(x) - b * np.sin(theta) * np.sin(x), k + a * np.cos(theta) * np.sin(x) + b * np.sin(theta) * np.cos(x)

def fit_ellipse(x, y):
    x_m, y_m = np.mean(x), np.mean(y)
    x_norm = x - x_m
    y_norm = y - y_m
    A = np.array([x_norm**2, x_norm*y_norm, y_norm**2, x_norm, y_norm]).T
    u, s, vh = np.linalg.svd(A)
    a, b = vh.T[:, -1] / np.sqrt(s[-1])
    theta = 0.5 * np.arctan2(2 * b, a - b)
    a, b = np.sqrt(s[-1]), np.sqrt(s[0])
    h, k = x_m - a * np.cos(theta), y_m - b * np.sin(theta)
    return a, b, h, k, theta
# %%散点图
def sc(data, x=1, y=2, z=3, zlarge=1, sub='', subellipse=False,text='', fit=0,
       hline='', vline='', xy=False, y_x=False,
       text_size=12, lines=False, single_varmode=True, return_plot=return_plot,
       ycomma=False, xpercent=False, hollow=False):
    '''
    【做散点图】
    data：如果是一个dataframe，则直接画图；如果是一个dataframe组成的list，则把他们merge之后再画图。如果数据包含缺失值，函数自动剔除缺失值
    x：字符串或列表，横轴变量，通常只有一个元素
    y：字符串或列表，纵轴变量，通常有多个元素
    z：字符串或列表，气泡变量，通常只有一个元素
    sub：日期分割点，列表格式，'yyyy-mm-dd'
    text：列表，但如果取值index则直接是用索引作图
    fit:默认=0，不加拟合线；加拟合线
    hline：数值型，加水平虚线
    vline：数值型，加垂直虚线
    hollow：1则是空心点，默认实心点
    '''

    if x==1 and y==2:
        x=data.columns[0]
        y=data.columns[1]

    if str(type(data)) == "<class 'list'>":
        data_copy = merge(data)
    elif str(type(data)) == "<class 'pandas.core.series.Series'>":
        data_copy = pd.DataFrame(data)
    else:
        data_copy = data.copy()

    data_copy=data_copy.dropna()

    if str(type(x)) == "<class 'str'>":
        x_copy = [x]
    else:
        x_copy = x
    if str(type(y)) == "<class 'str'>":
        y_copy = [y]
    else:
        y_copy = y
    if str(type(z)) != "<class 'int'>":
        z_copy = data_copy[z]
    else:
        z_copy = z
    if text != '':
        if text == 'index':
            text = pd.Series(data.index.tolist())
        else:
            text = pd.Series(text)



    if lines == False:
        line_para = ''
    else:
        line_para = '+lines'

    if hollow:
        marker_mode = 'markers'
    else:
        marker_mode = 'markers+text'

    # 循环生成trace
    trace_list = []

    if sub != '':
        sub = [data_copy.index[0]] + sub + [data_copy.index[-1]]
        ellipse_shape_list=[]
        for i in range(len(y_copy)):

            for j in range(len(sub) - 1):
                # 提取数据子集
                data_subset = data[(data.index >= sub[j]) & (data.index < sub[j + 1])]

                # 使用主成分分析拟合椭圆
                pca = PCA(n_components=2)
                pca.fit(data_subset[[x_copy[0], y_copy[i]]])
                mean_x, mean_y = np.mean(data_subset[x_copy[0]]), np.mean(data_subset[y_copy[i]])
                eigenvalues, eigenvectors = pca.explained_variance_, pca.components_
                a, b = np.sqrt(eigenvalues[0]) * 2, np.sqrt(eigenvalues[1]) * 2
                angle_rad = np.arctan2(eigenvectors[0, 1], eigenvectors[0, 0])

                # 计算椭圆上的点
                theta = np.linspace(0, 2 * np.pi, 100)
                ellipse_x = mean_x + a * np.cos(theta) * np.cos(angle_rad) - b * np.sin(theta) * np.sin(angle_rad)
                ellipse_y = mean_y + a * np.cos(theta) * np.sin(angle_rad) + b * np.sin(theta) * np.cos(angle_rad)

                trace_list.append(
                    go.Scatter(x=data_subset[x_copy[0]], y=data_subset[y_copy[i]], mode=marker_mode + line_para,
                               name=y_copy[i] + "(" + str(sub[j])[:10] + "—" + str(sub[j + 1])[:10] + ")",
                               marker_size=zlarge * z_copy, text=text, textposition='middle right'))
                # 绘制椭圆形状
                ellipse_shape = {
                    'type': 'path',
                    'path': f'M {ellipse_x[0]}, {ellipse_y[0]} L {" L ".join([str(x) + "," + str(y) for x, y in zip(ellipse_x, ellipse_y)])} Z',
                    'fillcolor': color_scheme2[j],  # 不同数据子集用绿色填充椭圆阴影
                    'line': {
                        'color': color_scheme2[j],  # 椭圆边界线的颜色和透明度
                        'width': 0,
                    }
                }
                ellipse_shape_list.append(ellipse_shape)
                # layout = go.Layout(shapes=[ellipse_shape])
                # fig = go.Figure(data=[trace_list[-1]], layout=layout)
                # fig.show()
                if fit == 1:
                    # 利用sm的ols加入拟合曲线
                    x_range = np.linspace(data_copy[x_copy[0]][sub[j]:sub[j + 1]].min(), data_copy[x_copy[0]][sub[j]:sub[j + 1]].max(), 100)
                    x_range.reshape(100, 1)
                    reg = sm.OLS(data[y_copy[i]][sub[j]:sub[j + 1]],
                                 sm.add_constant(data[x_copy[0]][sub[j]:sub[j + 1]])).fit()
                    R2_adj = reg.rsquared_adj
                    trace_list.append(go.Scatter(x=x_range, y=reg.params[0] + x_range * reg.params[1], mode='lines',
                                                 name='线性(R2=' + str(round(R2_adj, 2)) + ")", line=dict(width=1.5)))

    else:
        for i in range(len(y_copy)):
            trace_list.append(
                go.Scatter(x=data_copy[x_copy[0]], y=data_copy[y_copy[i]], mode=marker_mode + line_para,
                           name=y_copy[i], marker_size=zlarge*z_copy, text=text, textfont=dict(size=text_size),
                           textposition='middle right'))
            if fit == 1:
                # 利用sm的ols加入拟合曲线
                x_range = np.linspace(data_copy[x_copy[0]].min(), data_copy[x_copy[0]].max(), 100)
                x_range.reshape(100, 1)
                reg = sm.OLS(data_copy[y_copy[i]], sm.add_constant(data_copy[x_copy[0]])).fit()
                R2_adj = reg.rsquared_adj
                trace_list.append(go.Scatter(x=x_range, y=reg.params[0] + x_range * reg.params[1], mode='lines',
                                             name='线性(R2=' + str(round(R2_adj, 2)) + ")", line=dict(width=1.5)))
    # 添加y=x对角线
    if y_x:
        x_range = np.linspace(data_copy[x_copy[0]].min(), data_copy[x_copy[0]].max(), 100)
        trace_list.append(go.Scatter(x=x_range, y=x_range, mode='lines', name='y=x', line=dict(color='black', dash='dash')))

    fig = go.Figure(data=trace_list, layout=lo)
    if subellipse!=False:
        fig.update_layout(shapes=ellipse_shape_list)
    # fig = go.Figure(data=trace_list)

    if hollow:
        fig.update_traces(marker=dict(symbol='circle-open', line_color='black'))
    # 添加自定义按钮到模式栏中
    fig.update_layout(hide_logo)
    if single_varmode==True:
        fig.update_layout(height=500, width=600, xaxis_title=dict(text=x_copy[0], font=dict(size=14)) , yaxis_title=dict(text=y_copy[0], font=dict(size=14)))
        fig.update_layout(showlegend=False)
    else:
        fig.update_layout(height=500, width=600, xaxis_title=dict(text=x_copy[0], font=dict(size=14)))
        fig.update_layout(legend=dict(y=-0.15))

    # 单独拟合线的颜色
    if fit == 1:
        color_scheme_2 = [item for s in color_scheme for item in [s] * 2]
        fig.update_layout(colorway=color_scheme_2)

    # 加水平线
    if hline != '':
        fig.add_hline(y=hline, line_width=1, line_dash="dash", line_color='black')
    # 加垂直线
    if vline != '':
        fig.add_vline(x=vline, line_width=1, line_dash="dash", line_color='black')

    if xy == True:
        fig.add_hline(y=0, line_width=1, line_dash="dash", line_color='black')
        fig.add_vline(x=0, line_width=1, line_dash="dash", line_color='black')

    if ycomma:
        fig.update_layout(yaxis=dict(tickformat=","))
    if xpercent:
        fig.update_layout(xaxis=dict(tickformat=".2%"))

    # cl(fig)
    if return_plot == False:
        config = dict({'displayModeBar': False, 'showTips': False})
        fig.show(config=config)
    else:
        return fig
PandasObject.sc = sc

# %%桑吉图
def sankey(dataframe, father, son, data, height=None, width=None):
    '''
    做桑吉图
    dataframe：必须是sql格式数据
    father：父类列名，要求字符串格式
    son：子类列名，要求字符串格式
    data：数据列名，要求字符串格式
    '''
    df = dataframe.copy()
    df = df[[father, son, data]]
    df = df.groupby([father, son])[data].sum().reset_index()
    df.columns = ['父类', '子类', '数据']


    labels = list(set(df["父类"].tolist() + df["子类"].tolist()))

    number = list(range(len(df) + 1))

    index = dict(list(zip(labels, number)))

    df["父类索引"] = df["父类"].map(index)
    df["子类索引"] = df["子类"].map(index)

    # 标签就是index字典中的key键
    label = list(index.keys())
    # 父类和子类
    source = df["父类索引"].tolist()
    target = df["子类索引"].tolist()
    # 流量的值
    value = df["数据"].tolist()

    # 生成绘图需要的字典数据

    nodes = np.unique(df[["父类", "子类"]], axis=None)
    nodes = pd.Series(index=nodes, data=range(len(nodes)))

    node = dict(label=nodes.index, color=[color_scheme[i % len(color_scheme)] for i in nodes])
    link = dict(source=nodes.loc[df["父类"]], target=nodes.loc[df["子类"]], value=value,
                color=[color_scheme2[i % len(color_scheme2)] for i in nodes.loc[df["父类"]]])

    data = go.Sankey(link=link, node=node)
    fig = go.Figure(data=data, layout=lo)

    fig["layout"].update(go.Layout(height=height, width=width))
    # cl(fig)
    fig.show(config=config)
PandasObject.sankey = sankey
def sankey2(dataframe, father, son, grandson, data, height=None, width=None,return_plot=return_plot):
    '''
    桑吉图，三层版本。多了一个孙类
    函数里面有groupby,因此dataframe的格式为SQL的基本数据格式就可，不需要自己groupby然后再传入函数
    '''
    df=dataframe.copy()
    df=df.groupby([father, son, grandson])[data].sum().reset_index()
    df.rename(columns={father:'lay1',son:'lay2',grandson:'lay3',data:'weight'},inplace=True)
    nodes = []
    for i in range(3):  # 修改处
        vales = df.iloc[:, i].unique()
        for value in vales:
            dic = {}
            dic['name'] = value
            nodes.append(dic)

    first = df.groupby(['lay1', 'lay2'])['weight'].sum().reset_index()
    second = df.iloc[:, 1:]
    first.columns = ['source', 'target', 'value']
    second.columns = ['source', 'target', 'value']
    result = pd.concat([first, second])

    linkes = []
    for i in result.values:
        dic = {}
        dic['source'] = i[0]
        dic['target'] = i[1]
        dic['value'] = i[2]
        linkes.append(dic)
    df = pd.DataFrame(linkes)

    # 调整数据结构
    labels = list(set(df["source"].tolist() + df["target"].tolist()))
    number = list(range(len(labels)))
    index = dict(list(zip(labels, number)))
    df["source_index"] = df["source"].map(index)
    df["target_index"] = df["target"].map(index)
    label = list(index.keys())
    source = df["source_index"].tolist()
    target = df["target_index"].tolist()
    value = df["value"].tolist()

    # 绘图需要的字典数据
    node = dict(label=label, pad=200, thickness=40, color=[color_scheme[i % len(color_scheme)] for i in number])
    link = dict(source=source, target=target, value=value,
                color=[color_scheme2[i % len(color_scheme2)] for i in df["source_index"].tolist()])

    data = go.Sankey(link=link, node=node)

    fig = go.Figure(data)
    fig = go.Figure(data=data, layout=lo)
    fig["layout"].update(go.Layout(height=height, width=width))
    if return_plot:
         return fig
    else:
        # cl(fig)
        fig.show(config=config)
PandasObject.sankey2 = sankey2
def radar(df, cols=None, text_col=None):
    '''
    空心雷达图，
    cols为list，指标列表，默认为数据框的列
    text_col为字符串，文字，默认为数据框的索引
    '''

    if cols is None:
        cols = df.columns.tolist()  # 使用数据框的列作为指标列表

    if text_col is None:
        text_col = df.index.name  # 使用数据框的索引作为文字列

    fig = go.Figure()

    for col in cols:
        # 添加起点和终点的重复值，以连接起点和终点
        values = df[col].tolist() + [df[col][0]]
        labels = df.index.tolist() + [df.index[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='none',
            name=col,
            mode='lines',
            line=dict(width=2)
        ))
    fig.layout = lo
    fig.update_layout(polar=dict(
        radialaxis=dict(visible=True, range=[0, df.max().max()], showgrid=False, showline=False),
        angularaxis=dict(showline=False),
        radialaxis_visible=True,
        radialaxis_showline=False,
        #         bgcolor='rgba(0, 0, 0, 0)'
    ), showlegend=True)
    # cl(fig)
    fig.show(config=config)
# 添加到Pandas的DataFrame对象中
PandasObject.radar = radar
#%%瀑布图
def waterfall(dataframe):
    '''
    dataframe格式：index为日期，但是只有一行。列为类别，不含合计列，作图的时候自动合计
    '''
    df=dataframe.copy()
    df=df.unstack().to_frame().reset_index().col(['列','行','数值'])
    # 创建瀑布图
    fig = go.Figure(go.Waterfall(
        name="列",
        orientation="v",
        measure=df["列"],
        x=df["列"],
        y=df["数值"],
        increasing=dict(marker_color=color_scheme[1]),
        decreasing=dict(marker_color=color_scheme[2]),connector={"line": {"color": "rgba(0, 0, 0, 0)"}}
    ))

    # 计算合计
    total = sum(df["数值"])

    # 添加合计数据点
    fig.add_trace(go.Bar(
        name="合计",
        x=["合计"],
        y=[total],
        marker=dict(color=color_scheme[0])
    ))
    fig.layout=lo
    fig.update_layout(showlegend=False)
    # 添加自定义按钮到模式栏中
    fig.update_layout(hide_logo)
    # fig.update_layout(hide_prompt)
    # cl(fig)
    return fig
PandasObject.waterfall=waterfall
#%%矩阵多图
import pandas as pd
from plotly.subplots import make_subplots


def matrix_sp(dataframe, row=2, col=2, ptype='p',parameter="",height=900, width=None,font_size=None):
    '''
    矩阵多图，row*col图的数量应该和数据框的列数量相等！
    ptype：子图的类型
    parameter：子图的参数，字符串里如果要传多个参数则用逗号隔开
    '''
    if type(ptype) == str:
        ptype = [ptype] * row * col
    df = dataframe.copy()

    # Check if the number of columns in the dataframe is less than row * col
    num_missing_cols = row * col - len(df.columns) + 1
    if num_missing_cols > 0:
        df[['' for i in range(num_missing_cols)]]=np.nan
    # display(df)
    varlist = list(df.columns)
    fig = make_subplots(rows=row, cols=col, subplot_titles=varlist)
    trace_list = []
    s = 0

    for i in range(row):
        for j in range(col):
            s = s + 1
            if s <= len(dataframe.columns):
                plot = eval(ptype[s - 1] + f'(df.iloc[:,[s-1]],return_plot=True,{parameter})')
                plot.update_layout(title_font=dict(size=font_size)) #这个没啥用，再检查一下
            else:
                plot = go.Figure()
                plot.update_layout({'showlegend': False})
                plot.update_xaxes(showticklabels=False)
                plot.update_yaxes(showticklabels=False)
                plot.update_layout({'annotations': []})
                plot.update_layout(title_text=None)
                plot.update_layout(title_font=dict(size=font_size))
            # plot = eval(ptype[s - 1] + '(df.iloc[:,[s-1]],return_plot=True)')

            plot = plot.update_layout(lo_matrix_sp)
            for k in range(len(plot.data)):
                plot_k = plot.data[k]

                fig.add_trace(plot_k, row=i + 1, col=j + 1)

    lo_matrix_sp_all = create_matrix_layout_with_multiple_axes(row * col, color_scheme)
    fig.update_layout(lo_matrix_sp_all)
    fig.update_layout(height=height, width=width, showlegend=False)
    # cl(fig)
    return fig
PandasObject.matrix_sp=matrix_sp

