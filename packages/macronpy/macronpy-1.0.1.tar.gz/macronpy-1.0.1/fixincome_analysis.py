from macronpy.basic_package import *
from macronpy.macro import *
from macronpy.plotly_plot import *
import warnings

#%%新老券利差
def on_off_run_spread( sample_bond='230009.IB',issudate_start='2015-01-01',remainingmaturity_min=25,remainingmaturity_max=30):
    '''
    计算新老券利差
    '''
    T_bond_set=w.wset("f9sameissuer",f"windcode={sample_bond};containissue=on",usedf=True)[1]
    T_bond_set['期限']=T_bond_set.apply(lambda x:x['maturitydate'].year-x['issuedate'].year,axis=1)
    query_string=f'''期限=={remainingmaturity_max} and listingplace=='银行间' and ~secname.str.contains('续') and issuedate>'{issudate_start}' and remainingmaturity>='{remainingmaturity_min}' and  remainingmaturity<='{remainingmaturity_max}' '''
    T_bond_set_list_for_rank=T_bond_set.query(query_string)['windcode'].tolist()
    T_bond_set_for_rank_yield=w.wsd(T_bond_set_list_for_rank, "yield_cnbd", issudate_start, today(), "credibility=1",usedf=True)[1]
    bond_set_for_rank_yield_dataset=T_bond_set_for_rank_yield.unstack().to_frame().reset_index().col(['windcode','TRADE_DT','r'])
    bond_set_for_rank_yield_dataset=bond_set_for_rank_yield_dataset.merge(T_bond_set[['windcode','maturitydate']],on='windcode',how='left')

    TRADE_DT=trade_date_wind(issudate_start,today(),'d').reset_index().col('TRADE_DT')
    bond_set_for_rank_yield_dataset['TRADE_DT']=bond_set_for_rank_yield_dataset['TRADE_DT'].apply(lambda x:str(x)[:10])
    TRADE_DT['TRADE_DT']=TRADE_DT['TRADE_DT'].apply(lambda x:str(x)[:10])

    bond_set_for_rank_yield_dataset_merged=pd.merge(bond_set_for_rank_yield_dataset,TRADE_DT,on='TRADE_DT',how='left')
    bond_set_for_rank_yield_dataset[['TRADE_DT','maturitydate']]=bond_set_for_rank_yield_dataset[['TRADE_DT','maturitydate']].applymap(lambda x:pd.to_datetime(x,format="%Y-%m-%d"))
    bond_set_for_rank_yield_dataset['remainingmaturity']=bond_set_for_rank_yield_dataset['maturitydate']-bond_set_for_rank_yield_dataset['TRADE_DT']
    bond_set_for_rank_yield_dataset=bond_set_for_rank_yield_dataset.dropna()
    bond_set_for_rank_yield_dataset['rank']=bond_set_for_rank_yield_dataset.groupby(['TRADE_DT'])['remainingmaturity'].rank(ascending=False)

    bond_set_for_rank_yield_dataset_top3=bond_set_for_rank_yield_dataset.sort_values('TRADE_DT').query('rank in (1,2,3,4,5)')
    bond_set_for_rank_yield_dataset_top3['rank']=bond_set_for_rank_yield_dataset_top3['rank'].apply(lambda x:str(x)+'名')
    bond_set_for_rank_yield_dataset_top3_ts=bond_set_for_rank_yield_dataset_top3.pivot('TRADE_DT','rank','r')

    bond_set_for_rank_yield_dataset_top3_ts['1vs2']=bond_set_for_rank_yield_dataset_top3_ts['2.0名']-bond_set_for_rank_yield_dataset_top3_ts['1.0名']
    bond_set_for_rank_yield_dataset_top3_ts['1vs3']=bond_set_for_rank_yield_dataset_top3_ts['3.0名']-bond_set_for_rank_yield_dataset_top3_ts['1.0名']
    bond_set_for_rank_yield_dataset_top3_ts['1vs4']=bond_set_for_rank_yield_dataset_top3_ts['4.0名']-bond_set_for_rank_yield_dataset_top3_ts['1.0名']
    bond_set_for_rank_yield_dataset_top3_ts['1vs5']=bond_set_for_rank_yield_dataset_top3_ts['5.0名']-bond_set_for_rank_yield_dataset_top3_ts['1.0名']
    return bond_set_for_rank_yield_dataset_top3_ts
#%%现金流折现
def PV(cash_df,t0,start,end,step):
    '''
    现金流折现
    cash_df：index为日期yyyy-mm-dd，columns为1列，表示现金流
    t0：折现时点，yyyy-mm-dd表示的字符串
    start\end：模拟的起点和重点，step：步长
    比如：start=0.001、 end=0.051、 step=0.000001，最后的曲线就是这样的分布
    '''
    cash_flows=cash_df.copy().col('Cash Flow')
    T0=pd.Timestamp(int(t0[:4]), int(t0[5:7]), int(t0[8:10]))
    # 生成折现率序列
    discount_rates = np.array(np.arange(start,end,step))
    # 计算现金流的现值
    present_values = pd.DataFrame(index=discount_rates, columns=['Present Value'])
    for rate in tqdm(discount_rates):
        present_value = np.sum(cash_flows['Cash Flow'] / (1 + rate) ** ((cash_flows.index - T0).days / 365))
        present_values.loc[rate] = present_value
    present_values=present_values.reset_index().rename(columns={'index':'rate'})
    dvbp=present_values.copy()
    dvbp['DVBP']=dvbp['Present Value'].diff(-1*int(0.0001/step)) #注意这里，如果步长是0.01%，那么两个相邻的数直接作差即可，如果是0.0001%（0.000001），那么应该diff(-100)才是
    dvbp=dvbp.col(['rate','Present Value','DVBP'])
    return dvbp




