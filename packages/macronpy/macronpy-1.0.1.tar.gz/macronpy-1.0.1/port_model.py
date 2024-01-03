from macronpy.basic_package import *
#最后一个遗留问题，当price_freq=rebalance_freq='M'的时候，程序报错index=0
class RiskParity():
    '''
    风险平价的class。基于资产价格序列得到优化结果，包含各资产的权重
    '''
    def __init__(self,price_df,price_freq='D',rebalance_freq='M',method=None,half=False):
        '''
        初始化函数
        price_df：大类资产价格序列，一定是价格而不是收益率
        freq：频率
        mehod：取值'pca'或者'lasso'
        half：True或者False
        '''

        price_freq = price_freq.upper()
        rebalance_freq = rebalance_freq.upper()

        # 计算协方差矩阵
        def calculate_cov_matrix(dataframe, price_freq=price_freq):
            """
            计算协方差矩阵
            freq：'D','W','M','Q','Y'
            """
            # display(dataframe)
            dataframe = dataframe / dataframe.loc[str(dataframe.index[0])[:10], :] * 100  # 统一缩放到100为基点
            returns_dataframe = (dataframe - dataframe.shift(1)) / dataframe.shift(1)  # 简单收益率
            # returns_dataframe = np.log(dataframe/dataframe.shift(1)) # 对数收益率
            returns_dataframe.dropna(axis='index', inplace=True)  # 删除空数据

            freq_upper = price_freq.upper()
            time_span_dict = {'D': 252, 'W': 52, 'M': 12, 'Q': 4, 'Y': 1}
            time_span = time_span_dict[freq_upper]
            one_cov_matrix = returns_dataframe.cov() * time_span

            return np.matrix(one_cov_matrix)

        # 返回训练样本数据
        def get_train_set(change_time, df, price_freq=price_freq):
            """
            返回训练样本数据
            freq：'D','W','M','Q','Y'
            """
            # change_time: 调仓时间
            freq_upper = price_freq.upper()
            # 时间跨度字典
            time_span_dict = {'D': 252, 'W': 52, 'M': 12, 'Q': 4, 'Y': 1}
            time_span = time_span_dict[freq_upper]
            df = df.loc[df.index < change_time]
            df = df.iloc[-time_span:]  # 每个调仓前 time_span 个交易日

            return df

            # 标准风险平价下的风险贡献
        def calculate_risk_contribution(weight, one_cov_matrix):
            weight = np.matrix(weight)
            sigma = np.sqrt(weight * one_cov_matrix * weight.T)
            # 边际风险贡献 Marginal Risk Contribution (MRC)
            MRC = one_cov_matrix * weight.T / sigma
            # 风险贡献 Risk Contribution (RC)
            RC = np.multiply(MRC, weight.T)
            return RC

        # 定义优化问题的目标函数，即最小化资产之间的风险贡献差
        def naive_risk_parity(weight, parameters):
            # weight: 待求解的资产权重,
            # parameters: 参数列表
            # parameters[0]: 协方差矩阵
            # parameters[1]: 风险平价下的目标风险贡献度向量

            one_cov_matrix = parameters[0]
            RC_target_ratio = parameters[1]
            # RC_target为风险平价下的目标风险贡献，一旦参数传递以后，RC_target就是一个常数，不随迭代而改变
            sigma_portfolio = np.sqrt(weight * one_cov_matrix * np.matrix(weight).T)  # 组合波动率
            RC_target = np.asmatrix(np.multiply(sigma_portfolio, RC_target_ratio))  # 目标风险贡献
            # RC_real是 每次迭代以后最新的真实风险贡献，随迭代而改变
            RC_real = calculate_risk_contribution(weight, one_cov_matrix)
            sum_squared_error = sum(np.square(RC_real - RC_target.T))[0, 0]
            return sum_squared_error

        # 根据资产预期目标风险贡献度来计算各资产的权重
        def calculate_portfolio_weight(one_cov_matrix, risk_budget_objective, df):
            '''
            约束条件的类型只有'eq'和'ineq'两种
            eq表示约束方程的返回结果为0
            ineq表示约束方程的返回结果为非负数
            '''
            # df是资产价格统一基期后的数据框！
            num = df.shape[1]
            x0 = np.array([1.0 / num for _ in range(num)])  # 初始资产权重
            bounds = tuple((0, 1) for _ in range(num))  # 取值范围(0,1)

            cons_1 = ({'type': 'eq', 'fun': lambda x: sum(x) - 1},)  # 权重和为1
            RC_set_ratio = np.array([1.0 / num for _ in range(num)])  # 风险平价下每个资产的目标风险贡献度相等
            optv = sco.minimize(risk_budget_objective, x0,
                                args=[one_cov_matrix, RC_set_ratio], method='SLSQP',
                                bounds=bounds, constraints=cons_1)
            return optv.x

        def get_weight_matrix(df, rebalance_freq = rebalance_freq, method=None, half=False):
            """返回资产权重矩阵"""

            period_type = rebalance_freq
            df_weight = df.resample(period_type).last()

            #     df_weight = df_weight[df_weight.index>='2008-12-31']

            for i in range(len(df_weight.index)):
                change_time = df_weight.index[i]

                # next_change_time = df_weight.index[i+1]

                train_set = get_train_set(change_time, df=df,price_freq=price_freq)
                # display(train_set)
                # 是否使用半衰协方差矩阵
                if half == True:
                    one_cov_matrix = calculate_half_cov_matrix(train_set)
                else:
                    one_cov_matrix = calculate_cov_matrix(train_set,price_freq=price_freq)
                # 是否使用主成分分析
                if method == 'pca':
                    df_weight.iloc[i] = calculate_portfolio_weight(one_cov_matrix, pca_risk_parity, df)
                elif method == 'lasso':
                    df_weight.iloc[i] = calculate_portfolio_weight(one_cov_matrix, lasso_risk_parity, df)
                else:
                    df_weight.iloc[i] = calculate_portfolio_weight(one_cov_matrix, naive_risk_parity, df)
                # backtest_set = get_backtest_set(change_time,next_change_time,df)
                # df_weight.iloc[i] = calculate_portfolio_weight(one_cov_matrix)
            return df_weight

        # 基于主成分分析的风险平价下的风险贡献
        def calculate_risk_contribution_pca(weight, one_cov_matrix):
            weight = np.matrix(weight)
            sigma = np.sqrt(weight * one_cov_matrix * weight.T)
            # 奇异值分解，其中uv=I ,u,v是特征向量矩阵，是正交阵，d是对角矩阵，对角元素是特征值，tr(d)=tr(one_cov_matrix)
            u, d, v = np.linalg.svd(one_cov_matrix)
            a = v * weight.T
            b = v * (one_cov_matrix * weight.T)
            # 风险贡献 Risk Contribution (RC)
            RC = np.multiply(a, b)
            RC = RC / sigma
            return RC

        # 定义优化问题的目标函数，即最小化资产之间的风险贡献差
        def pca_risk_parity(weight, parameters):
            # weight: 待求解的资产权重,
            # parameters: 参数列表
            # parameters[0]: 协方差矩阵
            # parameters[1]: 风险平价下的目标风险贡献度向量
            one_cov_matrix = parameters[0]
            RC_target_ratio = parameters[1]
            # RC_target为风险平价下的目标风险贡献，一旦参数传递以后，RC_target就是一个常数，不随迭代而改变
            sigma_portfolio = np.sqrt(weight * one_cov_matrix * np.matrix(weight).T)  # 组合波动率
            RC_target = np.asmatrix(np.multiply(sigma_portfolio, RC_target_ratio))  # 目标风险贡献
            # RC_real是 每次迭代以后最新的真实风险贡献，随迭代而改变
            RC_real = calculate_risk_contribution_pca(weight, one_cov_matrix)
            sum_squared_error = sum(np.square(RC_real - RC_target.T))[0, 0]
            return sum_squared_error

        #生成风险平价优化后的权重矩阵，这个asset_weight_df是这个class的核心结果
        asset_weight_df=get_weight_matrix(price_df.copy(),rebalance_freq,method,half)

        # 用资产原始序列的日期替换调仓日的序列
        if rebalance_freq=='Y':
            asset_weight_df.index = price_df.groupby([price_df.index.year]).tail(1).index
        elif rebalance_freq=='Q':
            asset_weight_df.index = price_df.groupby([price_df.index.year,price_df.index.quarter]).tail(1).index
        elif rebalance_freq=='M':
            asset_weight_df.index = price_df.groupby([price_df.index.year, price_df.index.month]).tail(1).index

        self.asset_weight=asset_weight_df
