import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker
import missingno as msno
import numpy as np


def path():
    # Government investments in environment
    gov_inv_path = "3810004301_databaseLoadingData (1).csv"
    # Substance released into environment
    subs_release_path = "NPRI_subsrele_1993.csv"
    # Substance disposed off-site
    subs_dispo_path = "NPRI_SubsDisp_1993.csv"
    # Substance recycled treatment off-site
    subs_recycle_path = "NPRI_SubsDisp_Tran-Recy_1993.csv"
    return gov_inv_path, subs_release_path, subs_dispo_path, subs_recycle_path


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


def read_df(gov_inv, subs_release, subs_dispo, subs_recycle):
    gov_inv = pd.read_csv(gov_inv, low_memory=False)
    gov_inv = gov_inv[gov_inv['STATUS'].isin(["F", "x", ".."]) == False]
    subs_release = df_prep(subs_release)
    subs_recycle = df_prep(subs_recycle)
    subs_dispo = df_prep(subs_dispo)
    return gov_inv, subs_release, subs_dispo, subs_recycle


a, b, c, d = path()
gov_inv, subs_release, subs_dispo, subs_recycle = read_df(a, b, c, d)
gov_inv_prov = gov_inv[gov_inv['Type of activity'] != "Total, all activities"]
gov_inv_prov = gov_inv_prov[gov_inv_prov['GEO'] != "Canada"]

# print(gov_inv.info(), subs_release.info(),
#     subs_dispo.info(), subs_recycle.info())

if __name__ == '__main__':
    print()
