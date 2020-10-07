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
    if data['Units'] == "kg":
        return data['Quantity']*1000
    elif data['Units'] == "tonnes":
        return data['Quantity']*1000000
    else:
        return data['Quantity']


def read_df(gov_inv, subs_release, subs_dispo, subs_recycle):
    gov_inv = pd.read_csv(gov_inv, low_memory=False)
    gov_inv = gov_inv[gov_inv['STATUS'].isin(["F", "x", ".."]) == False]
    years = list(range(2006, 2017))
    subs_release = pd.read_csv(subs_release, encoding='ISO-8859-1', low_memory=False)
    subs_release = subs_release[subs_release['Reporting_Year'].isin(years)]
    subs_release['Quantity_converted'] = subs_release.apply(real_units, axis=1)
    subs_dispo = pd.read_csv(subs_dispo, encoding='ISO-8859-1', low_memory=False)
    subs_dispo = subs_dispo[subs_dispo['Reporting_Year'].isin(years)]
    subs_dispo['Quantity_converted'] = subs_dispo.apply(real_units, axis=1)
    subs_recycle = pd.read_csv(subs_recycle, encoding='ISO-8859-1', low_memory=False)
    subs_recycle = subs_recycle[subs_recycle['Reporting_Year'].isin(years)]
    subs_recycle['Quantity_converted'] = subs_recycle.apply(real_units, axis=1)
    return gov_inv, subs_release, subs_dispo, subs_recycle


a, b, c, d = path()
gov_inv, subs_release, subs_dispo, subs_recycle = read_df(a, b, c, d)
gov_inv_prov = gov_inv[gov_inv['Type of activity'] != "Total, all activities"]
gov_inv_prov = gov_inv_prov[gov_inv_prov['GEO'] != "Canada"]

print(gov_inv.info(), subs_release.info(),
    subs_dispo.info(), subs_recycle.info())
if __name__ == '__main__':
    print()
