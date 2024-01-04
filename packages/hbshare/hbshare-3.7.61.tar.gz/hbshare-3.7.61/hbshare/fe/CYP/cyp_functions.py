#%% 库

import pandas as pd
import hbshare as hbs
hbs.set_token("qwertyuisdfghjkxcvbn1000")

#%% 取数据

def get_df(sql, db, page_size=2000):
    data = hbs.db_data_query(db, sql, page_size=page_size, timeout=120)
    pages = data['pages']
    data = pd.DataFrame(data['data'])
    if pages > 1:
        for page in range(2, pages + 1):
            temp_data = hbs.db_data_query(db, sql, page_size=page_size, page_num=page, timeout=120)
            data = pd.concat([data, pd.DataFrame(temp_data['data'])], axis=0)
    return data


def msci_without_881001(end_date):
    # msci
    sql_msci = "select zqdm 证券代码, jyrq 交易日期, hbdr 日回报\
                from st_market.t_st_zs_rhb\
                where zqdm = '892400' and jyrq>={0} and jyrq <={1}".format('20120731',end_date)

    msci = get_df(sql_msci, db='alluser')
    msci = msci.pivot_table(values='日回报', index='交易日期', columns='证券代码')
    msci = msci.iloc[1:, :]

    # 881001
    sql_881001 = "select zqdm 证券代码, jyrq 交易日期, hbdr 日回报\
                from st_market.t_st_zs_rhb\
                where zqdm = '881001' and jyrq>={0} and jyrq <={1}".format('20120731',end_date)

    wind_881001 = get_df(sql_881001, db='alluser')
    wind_881001 = wind_881001.pivot_table(values='日回报', index='交易日期', columns='证券代码')
    wind_881001 = wind_881001.iloc[1:, :]

    # 合并
    msci_final = pd.merge(msci, wind_881001, on='交易日期', how='left')

    """
    万得全A 比重: 0.05
    MSCI 剔除中国部分影响 比重: 0.95
    """
    wind_weight = 0.05
    msci_weight = 0.95

    msci_final['MSCI%'] = (msci_final['892400'] - (wind_weight * msci_final['881001'])) / msci_weight

    MSCI_without_881001 = msci_final[['MSCI%']]

    return MSCI_without_881001

#%% End