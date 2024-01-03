from macronpy.asset_analysis import *
from macronpy.database_connect import *
from macronpy.eco_analysis import *
from macronpy.macro import *
from macronpy.plotly_plot import *
from macronpy.port_model import *
from macronpy.dbmake import *


#%%多资产回测策略框架
# 定义 account 类，作用是根据每日多资产的回报率计算账户净值，并记录净值和调仓记录
class MultiAssetAccount():
    """
    Account 类定义，模拟账户的各种行为。MultiAssetAccount是用于简单再平衡。
    如果希望根据自定义仓位进行再平衡，使用StrategyAccount
    """
    def __init__(self, daily_series,  # 收益率序列
                 asset_initial_ratio=[0.5,0.5],  # 初始权重
                 asset_target_ratio=[0.5,0.5],  # 目标权重
                 rebalance_ratio=0.55, rebalance_freq='month', rebalance_rule='定期-月'):
        """
        类初始化函数，记录初始账户各资产的比例以及账户净值
        初始账户净值为1
        """
        n_asset = daily_series.shape[1]
        asset_list = []
        for i in range(n_asset):
            asset_list.append('asset' + str(i + 1))

        self.asset_list = asset_list

        self.rebalance_rule = rebalance_rule
        #定期调仓所用到的参数
        freq = rebalance_freq
        globals()['last_tradeday_' + freq] = []
        for i in range(1, len(daily_series.index)):
            if eval('daily_series.index[i].' + freq) != eval('daily_series.index[i-1].' + freq):
                globals()['last_tradeday_' + freq].append(daily_series.index[i - 1])


        balance_ratio_dict = {}
        for i in range(len(asset_list)):
            setattr(self, 'asset' + str(i + 1) + '_ratio', asset_initial_ratio[i])
            balance_ratio_dict['asset' + str(i + 1)] = asset_target_ratio[i]

        self.balance_ratio = balance_ratio_dict
        #         self.rebalance_threshold = rebalance_ratio          # 调仓阈值
        self.net_value = 1  # 初始账户净值
        self.rebalance_record = {}  # 记录策略调仓记录，检查用途；
        self.balance = {}  # 记录账户策略表现净值

    def rebalance(self):
        """
        账户再平衡，将各资产比例调整回目标比例
        """
        for i in range(len(self.asset_list)):
            setattr(self, 'asset' + str(i + 1) + '_ratio', self.balance_ratio['asset' + str(i + 1)])

    def update_ratio(self, daily_series):
        """
        根据每日收益率数据更新各资产持仓比例和策略净值；
        daily_series: 每日两种资产的收益率，pandas series
        """
        s = 0  # s：求和算子。用于记录总资产净值
        # 各资产净值
        for i in range(len(self.asset_list)):
            setattr(self, 'asset' + str(i + 1) + '_net',
                    eval('self.' + 'asset' + str(i + 1) + '_ratio') * self.net_value * (
                                1 + daily_series['asset' + str(i + 1)]))
            s = s + eval('self.' + 'asset' + str(i + 1) + '_net')
        self.net_value = s

        # 更新各资产仓位比例
        for i in range(len(self.asset_list)):
            setattr(self, 'asset' + str(i + 1) + '_ratio',
                    eval('self.' + 'asset' + str(i + 1) + '_net') / self.net_value)
        #             locals()['asset'+str(i+1)+'_ratio']=locals()['asset'+str(i+1)+'_net']/self.net_value

        # 记录收益进来之后的更新后的账户净值
        self.balance[daily_series.name] = self.net_value  # daily_series.name 为日期

    def check_rebalance(self, daily_series):
        """
        检查账户是否需要再平衡
        """

        #         ['限值','定期','ERP']
        if self.rebalance_rule == '买入持有':
            return False
        #         elif self.rebalance_rule=='限值':
        #             if (self.stock_ratio >= self.rebalance_threshold) or (self.bond_ratio >= self.rebalance_threshold):
        #                 return True
        elif self.rebalance_rule == '定期-月':
            if daily_series.name in last_tradeday_month:
                return True
        elif self.rebalance_rule == '定期-季':
            if daily_series.name in last_tradeday_quarter:
                return True
        elif self.rebalance_rule == 'ERP':
            if (daily_series.name in ERP_signal_day):
                return True
        else:
            return False

    def data_in(self, daily_series):
        """
        是我们策略的主逻辑；
        处理每天进来的新数据；
        根据当日涨跌幅数据计算账户变动
        此方法设计作为参数传递给pandas.apply()函数
        daily_series: series，单日各资产的收益率，index为asset1、asset2等等
        【返回】与 daily_series 结构相同的 series，分别是stock 和 bond 比例更新以后的结果
        """
        # 更新各资产持仓比例和账户净值，记录账户净值
        self.update_ratio(daily_series)
        # 检查是否 rebalance
        if self.check_rebalance(daily_series):
            # 记录调仓日期和调仓前的各资产比例

            asset_ratio_for_record_dict = {}
            for i in range(len(self.asset_list)):
                asset_ratio_for_record_dict['asset' + str(i + 1)] = eval('self.' + 'asset' + str(i + 1) + '_ratio')
            self.rebalance_record[daily_series.name] = asset_ratio_for_record_dict
            # 调仓到目标比例
            self.rebalance()
        else:
            pass

        asset_ratio_for_record_dict = {}
        for i in range(len(self.asset_list)):
            asset_ratio_for_record_dict['asset' + str(i + 1)] = eval('self.' + 'asset' + str(i + 1) + '_ratio')

        return pd.Series(asset_ratio_for_record_dict, name=daily_series.name)
#%%多资产策略子类，继承了父类MultiAssetAccount
class MultiAssetStrategy(MultiAssetAccount):
    def __init__(self, asset_initial_ratio, asset_target_ratio, daily_series, rebalance_ratio=0.55, rebalance_freq='Q',
                 rebalance_rule='限值', strategy_name='再平衡策略'):
        # 初始化父类
        MultiAssetAccount.__init__(self, daily_series=daily_series, asset_initial_ratio=asset_initial_ratio,
                            asset_target_ratio=asset_target_ratio, rebalance_ratio=rebalance_ratio,
                            rebalance_freq=rebalance_freq, rebalance_rule=rebalance_rule)

        daily_series_copy = daily_series.copy()
        daily_series_copy.columns = self.asset_list
        # 资产仓位
        self.portfolio_ratio = daily_series_copy.apply(self.data_in, axis=1)
        self.portfolio_ratio.columns = daily_series.columns
        # 调仓记录
        self.rebalance_record = pd.DataFrame(self.rebalance_record).T
        # 账户净值
        self.net_value = pd.Series(self.balance, name=strategy_name)
# %%多资产回测策略框架【StrategyAccount是自由回测版本】。传入什么样的调仓参数数据框就在什么时间点调仓，调仓权重由数据框参数决定
class StrategyAccount():
    """
    Account 类定义，模拟账户的各种行为
    """

    def __init__(self, daily_series,  # 收益率序列
                 target_weight_df,  # 目标权重
                 asset_initial_ratio=[0.5, 0.5]):  # 初始权重
        """
        类初始化函数，记录初始账户各资产的比例以及账户净值
        初始账户净值为1
        target_weight_df：目标权重数据框。index为升序排列的时间索引，columns为各资产名称
        """
        n_asset = daily_series.shape[1]
        asset_list = ['asset' + str(i + 1) for i in range(n_asset)]
        self.asset_list = asset_list
        self.daily_series = daily_series
        self.daily_series.columns = asset_list

        target_weight_data = target_weight_df.copy()
        target_weight_data.columns = ['asset' + str(i + 1) + '_ratio' for i in range(n_asset)]
        self.target_weight_data = target_weight_data

        #         balance_ratio_dict = {}
        for i in range(len(asset_list)):
            setattr(self, 'asset' + str(i + 1) + '_ratio', asset_initial_ratio[i])
        #             balance_ratio_dict['asset' + str(i + 1)] = asset_target_ratio[i]

        #         self.balance_ratio = balance_ratio_dict
        self.net_value = 1  # 初始账户净值
        self.rebalance_record = {}  # 记录策略调仓记录，检查用途；
        self.balance = {}  # 记录账户策略表现净值

    def rebalance(self, daily_series):
        """
        账户再平衡，将各资产比例调整为目标比例
        """
        for i in range(len(self.asset_list)):
            setattr(self,
                    'asset' + str(i + 1) + '_ratio',
                    self.target_weight_data.loc[daily_series.name, 'asset' + str(i + 1) + '_ratio'])

    def update_ratio(self, daily_series):
        """
        根据每日收益率数据更新各资产持仓比例和策略净值；
        daily_series: 每日两种资产的收益率，pandas series
        """
        s = 0  # s：求和算子。用于记录总资产净值
        # 各资产净值
        for i in range(len(self.asset_list)):
            setattr(self, 'asset' + str(i + 1) + '_net',
                    eval('self.' + 'asset' + str(i + 1) + '_ratio') * self.net_value * (
                            1 + daily_series['asset' + str(i + 1)]))
            s = s + eval('self.' + 'asset' + str(i + 1) + '_net')
        self.net_value = s

        # 更新各资产仓位比例
        for i in range(len(self.asset_list)):
            setattr(self, 'asset' + str(i + 1) + '_ratio',
                    eval('self.' + 'asset' + str(i + 1) + '_net') / self.net_value)
        #             locals()['asset'+str(i+1)+'_ratio']=locals()['asset'+str(i+1)+'_net']/self.net_value

        # 记录收益进来之后的更新后的账户净值
        self.balance[daily_series.name] = self.net_value  # daily_series.name 为日期

    def check_rebalance(self, daily_series):
        """
        检查账户是否需要再平衡
        """

        if (daily_series.name in self.target_weight_data.index.tolist()):
            return True
        else:
            return False

    def data_in(self, daily_series):
        """
        是我们策略的主逻辑；
        处理每天进来的新数据；
        根据当日涨跌幅数据计算账户变动
        此方法设计作为参数传递给pandas.apply()函数
        daily_series: series，单日各资产的收益率，index为asset1、asset2等等
        【返回】与 daily_series 结构相同的 series，分别是stock 和 bond 比例更新以后的结果
        """

        # 更新各资产持仓比例和账户净值，记录账户净值
        self.update_ratio(daily_series)

        # 检查是否 rebalance
        if self.check_rebalance(daily_series):
            # if判断结果为True，表示到了调仓日
            # 记录调仓日期和调仓前的各资产比例

            asset_ratio_for_record_dict = {}
            for i in range(len(self.asset_list)):
                asset_ratio_for_record_dict['asset' + str(i + 1)] = eval('self.' + 'asset' + str(i + 1) + '_ratio')
            self.rebalance_record[daily_series.name] = asset_ratio_for_record_dict
            # 调仓到目标比例
            self.rebalance(daily_series)
        else:
            pass

        asset_ratio_for_record_dict = {}
        for i in range(len(self.asset_list)):
            asset_ratio_for_record_dict['asset' + str(i + 1)] = eval('self.' + 'asset' + str(i + 1) + '_ratio')

        return pd.Series(asset_ratio_for_record_dict, name=daily_series.name)
##########################################################################################################################################################################################
# %%多资产策略子类，继承了父类StrategyAccount
class StrategyBackTest(StrategyAccount):
    def __init__(self, daily_series, asset_initial_ratio, target_weight_df, strategy_name='再平衡策略'):
        ret_df = daily_series.copy()
        self.asset_name_list = target_weight_df.columns.tolist()
        # 初始化父类
        StrategyAccount.__init__(self, daily_series=ret_df, asset_initial_ratio=asset_initial_ratio,
                                 target_weight_df=target_weight_df)

        daily_series_copy = ret_df.copy()
        daily_series_copy.columns = self.asset_list
        # 资产仓位
        self.portfolio_ratio = daily_series_copy.apply(self.data_in, axis=1)
        self.portfolio_ratio.columns = self.asset_name_list
        # 调仓记录
        self.rebalance_record = pd.DataFrame(self.rebalance_record).T
        # 账户净值
        self.net_value = pd.Series(self.balance, name=strategy_name)

