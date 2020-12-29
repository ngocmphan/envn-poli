import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker
import missingno as msno
import numpy as np


def path():
    # Government investments in environment
    gov_inv_path = "data_sources/business_inv_env.csv"
    # Substance released into environment
    subs_release_path = "data_sources/NPRI_subsrele_1993.csv"
    # Substance disposed off-site
    subs_dispo_path = "data_sources/NPRI_SubsDisp_1993.csv"
    # Substance recycled treatment off-site
    subs_recycle_path = "data_sources/NPRI_SubsDisp_Tran-Recy_1993.csv"
    # Canadian population by province annually
    province_pop = "data_sources/canada_pop_province.csv"
    return gov_inv_path, subs_release_path, subs_dispo_path, \
        subs_recycle_path, province_pop


def real_units(data):
    if data['Units'] == 'kg':
        return data['Quantity']*0.001
    elif data['Units'] == 'tonnes':
        return data['Quantity']
    else:
        return data['Quantity']/1000000


def df_prep(data):
    years = list(range(2006, 2017))
    data_prep = pd.read_csv(data, encoding= 'ISO-8859-1', low_memory=False)
    data_prep = data_prep[data_prep['Reporting_Year'].isin(years)]
    data_prep['Quantity_converted'] = data_prep.apply(real_units, axis=1)
    return data_prep


def read_df(gov_inv, subs_release, subs_dispo, subs_recycle, can_pop):
    gov_inv = pd.read_csv(gov_inv, low_memory=False)
    gov_inv = gov_inv[gov_inv['STATUS'].isin(["F", "x", ".."]) == False]
    subs_release = df_prep(subs_release)
    subs_recycle = df_prep(subs_recycle)
    subs_dispo = df_prep(subs_dispo)
    canada_pop = pd.read_csv(can_pop, low_memory=False,
                             skiprows=lambda x: x not in list(range(5, 21)))
    canada_pop = canada_pop.iloc[1:, 2:]
    canada_pop['Reference period'] = canada_pop['Reference period'].apply(int)
    return gov_inv, subs_release, subs_dispo, subs_recycle, canada_pop


def adjusted_provinces(df):
    df_copy = df.copy()
    df_copy.loc[df_copy['PROVINCE'] == 'Alberta', 'PROVINCE_ADJUSTED'] = 'Alta.'
    df_copy.loc[df_copy['PROVINCE'] == 'British Columbia',
                'PROVINCE_ADJUSTED'] = 'B.C.'
    df_copy.loc[df_copy['PROVINCE'] == 'Manitoba',
                'PROVINCE_ADJUSTED'] = 'Man.'
    df_copy.loc[df_copy['PROVINCE'] == 'New Brunswick',
                'PROVINCE_ADJUSTED'] = 'N.B.'
    df_copy.loc[df_copy['PROVINCE'] == 'Newfoundland and Labrador',
                'PROVINCE_ADJUSTED'] = 'N.L.'
    df_copy.loc[df_copy['PROVINCE'] == 'Nova Scotia',
                'PROVINCE_ADJUSTED'] = 'N.S.'
    df_copy.loc[df_copy['PROVINCE'] == 'Northwest Territories 7',
                'PROVINCE_ADJUSTED'] = 'N.W.T.'
    df_copy.loc[df_copy['PROVINCE'] == 'Nunavut 7',
                'PROVINCE_ADJUSTED'] = 'Nvt.'
    df_copy.loc[df_copy['PROVINCE'] == 'Ontario',
                'PROVINCE_ADJUSTED'] = 'Ont.'
    df_copy.loc[df_copy['PROVINCE'] == 'Prince Edward Island',
                'PROVINCE_ADJUSTED'] = 'P.E.I.'
    df_copy.loc[df_copy['PROVINCE'] == 'Quebec',
                'PROVINCE_ADJUSTED'] = 'Que.'
    df_copy.loc[df_copy['PROVINCE'] == 'Saskatchewan',
                'PROVINCE_ADJUSTED'] = 'Sask.'
    df_copy.loc[df_copy['PROVINCE'] == 'Yukon',
                'PROVINCE_ADJUSTED'] = 'Y.T.'
    df_copy = df_copy[['Reference period', 'PROVINCE_ADJUSTED', 'population']]
    return df_copy


a, b, c, d, e = path()
gov_inv, subs_release, subs_dispo, subs_recycle, canada_population = read_df(a, b, c, d, e)
gov_inv_prov = gov_inv[gov_inv['Type of activity'] != "Total, all activities"]
gov_inv_prov = gov_inv_prov[gov_inv_prov['GEO'] != "Canada"]
canada_pop = canada_population.melt(id_vars=['Reference period'],
                                    var_name='PROVINCE',
                                    value_name='population')
canada_pop = adjusted_provinces(canada_pop)
if __name__ == '__main__':
    print()
