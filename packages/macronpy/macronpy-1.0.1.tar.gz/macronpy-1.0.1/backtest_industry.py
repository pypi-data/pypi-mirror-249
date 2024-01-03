from macronpy.asset_analysis import *
from macronpy.database_connect import *
from macronpy.eco_analysis import *
from macronpy.macro import *
from macronpy.plotly_plot import *
from macronpy.port_model import *
from macronpy.dbmake import *

#%%行业轮动
#打分变量
def generate_mask(factor_df_list,rule_list,top_num=5):
    '''
    factor_df_list：因子数据框
    rule_list：升序降序规则列表，如[1,0]，表示第一个因子按照升序打分（因子值越大分越高），第二个因子按照降序打分（因子值越大分越低）
    【返回值】mask，series，bool值，表示多维度打分相加之后的得分在前 top_num 个资产
    '''
    cross_section_rank_factor=[]
    for i in range(len(factor_df_list)):

        factor_i=factor_df_list[i]
        #rank_factor_i 保存因子i的得分，是一个series
        rank_factor_i=factor_i.rank(ascending=rule_list[i])
        cross_section_rank_factor.append(rank_factor_i)
        # display(rank_factor_i)
        if i ==0:
            score=rank_factor_i
        else:
            score=score+rank_factor_i

    mask=score.isin(list(score.sort_values(ascending=False)[:top_num]))

    cross_section_rank_factor_df=pd.concat(cross_section_rank_factor,axis=1)
    cross_section_rank_factor_df.columns=['factor_'+str(i) for i in range(1,len(factor_df_list)+1)]
    cross_section_rank_factor_df['rank_sum']=cross_section_rank_factor_df.sum(1)
    cross_section_rank_factor_dict={factor_i.name.strftime("%Y-%m-%d"):cross_section_rank_factor_df}
    # display(cross_section_rank_factor_dict)
    return mask,cross_section_rank_factor_dict
#持仓生成函数
def mask2hold(mask_df):
    '''
    将mask_df映射为持仓数据框
    mask_df，是多因子打分体系下的资产bool变量，index为资产名称，columns为日期
    此函数将适配每一个日期资产数量相同的情况，以及资产数量不同的情况
    此函数应该配合mask_df_list.append(mask.to_frame())和mask_df=pd.concat(mask_df_list,axis=1)语句使用
    '''
    # display(mask_df.std())

    if len(set(round(mask_df.std(),4)))==1:#每一个日期资产数量相同的情况
        holding_df = mask_df.apply(lambda x: mask_df.index[x].tolist())
    else:
        # display(mask_df.apply(lambda x: mask_df.index[x].tolist()))
        holding_df = mask_df.apply(lambda x: mask_df.index[x].tolist()).to_frame().applymap(lambda x:"、".join(x)).col(['策略持仓'])
        # 确定行业的数量
        max_industries = holding_df['策略持仓'].str.count('、').max() + 1

        # 将持仓列拆分成多个列
        col_names = [f'行业{i+1}' for i in range(max_industries)]
        holding_df[col_names] = holding_df['策略持仓'].str.split('、', expand=True)
        holding_df.drop('策略持仓',axis=1,inplace=True)
        holding_df=holding_df.T
        holding_df.index=range(holding_df.shape[0])
        holding_df.fillna("",inplace=True)
    return holding_df
#行业因子有效性测试
class IndustryFactorTest():
    '''
    旨在服务于行业轮动回测框架，以行业指数为基础资产
    本class着眼于测试单个行业因子有效性。将行业因子设置5分组。考察组之间的单调性
    本class没有比较基准的参数
    【NOTE】行业针对申万一级2021特别定制
    '''

    def __init__(self, factor_data, basic_ret, basic_price, start, end, freq='m'):
        '''
        类初始化函数
        factor_data：因子数据框
        ret_data：资产回报率数据框
        basic_price：基准价格
        '''

        # 定义holding_uniform，空dataframe，用于保存每一个行业的累计资金
        # 这里要格外注意的是，收益率数据和因子数据的行业是一致的，列的顺序是一致的。不然算不出来正确的结果
        factor_df = factor_data.copy()
        ret_df = basic_ret.copy()
        ret_df = ret_df[factor_df.columns]

        holding_uniform1 = pd.DataFrame(0.0, index=factor_df[start:end].index, columns=factor_df.columns)
        holding_uniform1.iloc[0]=1 / holding_uniform1.shape[1]
        holding_uniform2 = pd.DataFrame(0.0, index=factor_df[start:end].index, columns=factor_df.columns)
        holding_uniform2.iloc[0]=1 / holding_uniform2.shape[1]
        holding_uniform3 = pd.DataFrame(0.0, index=factor_df[start:end].index, columns=factor_df.columns)
        holding_uniform3.iloc[0]=1 / holding_uniform3.shape[1]
        holding_uniform4 = pd.DataFrame(0.0, index=factor_df[start:end].index, columns=factor_df.columns)
        holding_uniform4.iloc[0]=1 / holding_uniform4.shape[1]
        holding_uniform5 = pd.DataFrame(0.0, index=factor_df[start:end].index, columns=factor_df.columns)
        holding_uniform5.iloc[0]=1 / holding_uniform5.shape[1]

        for i in range(holding_uniform1.shape[0]-1):
            date_i    = holding_uniform1.index.tolist()[i]
            date_i_F1 = holding_uniform1.index.tolist()[i + 1]
            p = ret_df.loc[date_i_F1] + 1
            # if i == 0:
            #     cash1, cash2, cash3, cash4, cash5 = 1, 1, 1, 1, 1
            # else:
            #     date_i_L1 = holding_uniform1.index.tolist()[i - 1]
            #     cash1 = (holding_uniform1.loc[date_i_L1] * p).sum()
            #     cash2 = (holding_uniform2.loc[date_i_L1] * p).sum()
            #     cash3 = (holding_uniform3.loc[date_i_L1] * p).sum()
            #     cash4 = (holding_uniform4.loc[date_i_L1] * p).sum()
            #     cash5 = (holding_uniform5.loc[date_i_L1] * p).sum()

            cash1 = (holding_uniform1.loc[date_i] * p).sum()
            cash2 = (holding_uniform2.loc[date_i] * p).sum()
            cash3 = (holding_uniform3.loc[date_i] * p).sum()
            cash4 = (holding_uniform4.loc[date_i] * p).sum()
            cash5 = (holding_uniform5.loc[date_i] * p).sum()

                # mask：打分变量
            # 举例，(fa.iloc[i].rank(ascending=False) <= 5)，表示按照当前时点的行业景气度排名。按照景气度降序排序，最高的排名1
            mask1 = (factor_df.loc[date_i].rank(ascending=False) <= 6)
            mask2 = (factor_df.loc[date_i].rank(ascending=False) >= 7)  & (factor_df.loc[date_i].rank(ascending=False) <= 12)
            mask3 = (factor_df.loc[date_i].rank(ascending=False) >= 13) & (factor_df.loc[date_i].rank(ascending=False) <= 18)
            mask4 = (factor_df.loc[date_i].rank(ascending=False) >= 19) & (factor_df.loc[date_i].rank(ascending=False) <= 24)
            mask5 = (factor_df.loc[date_i].rank(ascending=False) >= 25) & (factor_df.loc[date_i].rank(ascending=False) <= 31)

            #     display("这是mask:",mask.to_frame())
            holding_uniform1.loc[date_i_F1] = (cash1 / mask1.sum() * mask1)  # 每一个调仓期末的资金分配。1/mask.sum() * mask表示资金分配。holding_uniform的每一个日期都是相同的，表示这些钱平均分布在对应的行业上，用于再投资
            holding_uniform2.loc[date_i_F1] = (cash2 / mask2.sum() * mask2)
            holding_uniform3.loc[date_i_F1] = (cash3 / mask3.sum() * mask3)
            holding_uniform4.loc[date_i_F1] = (cash4 / mask4.sum() * mask4)
            holding_uniform5.loc[date_i_F1] = (cash5 / mask5.sum() * mask5)

        equity_uniform1 = holding_uniform1.sum(1).nameas('G1')
        equity_uniform2 = holding_uniform2.sum(1).nameas('G2')
        equity_uniform3 = holding_uniform3.sum(1).nameas('G3')
        equity_uniform4 = holding_uniform4.sum(1).nameas('G4')
        equity_uniform5 = holding_uniform5.sum(1).nameas('G5')

        self.equity_uniform = merge([equity_uniform1, equity_uniform2, equity_uniform3, equity_uniform4, equity_uniform5]).round(2)
        self.ret_risk = ret_risk(self.equity_uniform.mg(basic_price).pct().dropna(), 0, freq)
class IndustryFactorCorr():
    '''
    利用纯多头因子收益率，计算因子间的相关性
    '''
    def __init__(self, factor_data_list, rule_list,basic_ret, basic_price, start, end, freq='m',factor_name=[]):
        factor_uniform_list=[]
        for i in range(len(factor_data_list)):
            factor_data_i=factor_data_list[i]
            rule_i=rule_list[i]
            facrot_test_class_i=IndustryFactorTest(factor_data_i, basic_ret, basic_price, start, end, freq=freq)
            rule_map={1:'G1',0:'G5'}
            factor_uniform_list.append(facrot_test_class_i.equity_uniform[[rule_map[rule_i]]])

        if factor_name != []:
            factor_uniform = pd.concat(factor_uniform_list, axis=1).col(factor_name)
        else:
            factor_uniform = pd.concat(factor_uniform_list, axis=1).col(['factor'+str(i) for i in range(len(factor_data_list))])
        self.factor_uniform=factor_uniform
        self.factor_ret=factor_uniform.pct()
        self.factor_corr=factor_uniform.pct().corr().round(3)
#多因子打分行业轮动策略
# 多因子打分行业轮动策略
class IndustryStrategy():
    '''
    多因子打分行业轮动策略
    本class着眼于行业多因子打分的回测
    factor_df_list：因子数据框列表。如果是单因子，就填写[data]
    rule_list：因子打分规则。1表示升序打分，也就是数值越大分越高。如果是单因子，就填写[1]或者[0]
    ret_data：资产回报率数据框
    basic_price：基准价格
    【NOTE】因子数据框、回报率数据框、基准价格，这三类数据的结构都是dataframe，并且，列名应该都是一样的！不一样一定会报错
    factor_name：列表，可以不传参数。但是因子名称一定要按顺序！
    '''

    def __init__(self, factor_dataframe_list, rule_list, basic_ret, basic_price, start, end, freq='m', top_num=5,
                 factor_name=[]):
        '''
        类初始化函数

        '''
        # 定义holding_uniform，空dataframe，用于保存每一个行业的累计资金
        # 这里要格外注意的是，收益率数据和因子数据的行业是一致的，列的顺序是一致的。不然算不出来正确的结果
        # factor_df=allocation_ratio_m.copy()
        factor_df_list = []
        for i in range(len(factor_dataframe_list)):
            factor_i = factor_dataframe_list[i]
            factor_df_list.append(factor_i[factor_dataframe_list[0].columns])

        ret_df = basic_ret.copy()

        # 把收益率的列顺序统一成因子的列顺序
        ret_df = ret_df[factor_df_list[0].columns]

        mask_df_list = []
        rank_score_df_list = []

        # 生成空数据框，用于保存净值
        holding_uniform = pd.DataFrame(0.0, index=factor_df_list[0][start:end].index, columns=factor_df_list[0].columns)
        holding_uniform.iloc[0] = 1 / holding_uniform.shape[1]

        # 生成空字典，用于存放每一期的多因子得分结果字典
        rank_factor_dict_all_date = dict()

        for i in range(holding_uniform.shape[0] - 1):
            # date_i表示本月末时点，date_i_F1表示下一个月末时点
            # date_i_L1 = holding_uniform.index.tolist()[i - 1]
            date_i = holding_uniform.index.tolist()[i]
            date_i_F1 = holding_uniform.index.tolist()[i + 1]

            p = ret_df.loc[date_i_F1] + 1

            cash = (holding_uniform.loc[date_i] * p).sum()
            # mask：打分变量
            # 举例，(fa.iloc[i].rank(ascending=False) <= 5)，表示按照当前时点的行业景气度排名。按照景气度降序排序，最高的排名1
            #     mask = (factor_df.loc[date_i].rank(ascending=False) <= 5)
            factor_df_list_date_i = []
            for j in range(len(factor_df_list)):
                factor_df_list_date_i.append(factor_df_list[j].loc[date_i])  # 每一个调仓期初，应当用上一个调仓期末对应的因子数据

            mask, rank_factor_dict_date_i = generate_mask(factor_df_list_date_i, rule_list, top_num)
            holding_uniform.loc[date_i_F1] = (cash / mask.sum() * mask)  # 每一个调仓期末的资金分配。1/mask.sum() * mask表示资金分配。holding_uniform的每一个日期都是相同的，表示这些钱平均分布在对应的行业上，用于再投资

            # display(holding_uniform.loc[date_i_F1])

            mask_df_list.append(mask.to_frame())
            rank_score_df_list.append(rank_factor_dict_date_i[date_i.strftime("%Y-%m-%d")][['rank_sum']].sortd().col(date_i.strftime("%Y-%m-%d")))
            #             display(rank_score_df_list[-1])
            # display(rank_factor_dict_date_i)
            rank_factor_dict_all_date[date_i.strftime("%Y-%m-%d")] = rank_factor_dict_date_i[date_i.strftime("%Y-%m-%d")]
            # display(mask)

        # 补齐最新一期持仓
        factor_df_list_last = []
        for k in range(len(factor_df_list)):
            factor_df_list_last.append(factor_df_list[k].loc[holding_uniform.index.tolist()[-1]])

        mask_last, rank_factor_dict_last = generate_mask(factor_df_list_last, rule_list, top_num)
        mask_last = mask_last.to_frame()
        date_last = list(rank_factor_dict_last.keys())[0]
        mask_df_list.append(mask_last)
        rank_score_df_list.append(rank_factor_dict_last[date_last][['rank_sum']].sortd().col(date_last))
        rank_factor_dict_all_date[date_last] = rank_factor_dict_last[date_last]

        self.equity_uniform = holding_uniform.sum(1).nameas('策略净值').to_frame().mg(basic_price).dropna().uni().round(2)

        self.mask_df = pd.concat(mask_df_list, axis=1)
        self.holding_df = mask2hold(self.mask_df)

        self.rank_sum_df = pd.concat(rank_score_df_list, axis=1)
        last_date = self.rank_sum_df.columns.tolist()[-1]
        self.rank_sum_df = self.rank_sum_df.sort_values(last_date, ascending=False)

        self.ret_risk = ret_risk(self.equity_uniform.pct().dropna(), 0, freq)
        self.excess_ret = (100 * (self.equity_uniform.dropna().uni().resample('y').last().pct().col_dif().col('年超额收益（%）'))).round(2)
        self.rank_factor_dict_all_date = rank_factor_dict_all_date
        # 调整因子名称，如果有的话
        if factor_name != []:
            for each_date in list(self.rank_factor_dict_all_date.keys()):
                self.rank_factor_dict_all_date[each_date].columns = factor_name + ['rank_sum']


