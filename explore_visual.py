from data_import import gov_inv, subs_release, subs_dispo, subs_recycle
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker
import plotly.express as px
import pandas as pd
import numpy as np


def compare_graph(data_1,data_2,  x_1, y_1, hue_1, x_2, y_2, hue_2, name):
    try:
        fig, axs = plt.subplots(ncols=2)
        axs[0].ticklabel_format(useOffset=False, style="plain")
        axs[1].ticklabel_format(useOffset=False, style="plain")
        axs[0].get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        axs[1].get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        a = sns.lineplot(x=x_1, y=y_1, hue=hue_1, ci=None, ax=axs[0], data=data_1)
        g = sns.lineplot(x=x_2, y=y_2, hue=hue_2, ci=None, ax=axs[1], data=data_2)
        plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
        plt.savefig("{}.png".format(name))
        return True
    except TypeError:
        print("Missing positional arguments")


def graph(data, x, y, hue, name):
    figure, ax = plt.subplots(ncols=1)
    ax.ticklabel_format(useOffset=False, style='plain')
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    sns.lineplot(x=x, y=y, hue=hue, data=data, ci=None)
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.savefig("{}.png".format(name))
    ax.set_title(name)
    return True


def interactive_line(data, x, y, color, line_group, title):
    fig = px.line(data, x=x, y=y, title=title,
                  color=color, line_group=line_group)
    fig.write_html('{}.html'.format(title))
    return True


def recycling_dispose(data):
    # The str.contains returns a series of boolean for function choose
    data.loc[data['Group (English)'].str.contains("Recycling", regex=False, case=False),
             'general_method'] = 'recycled'
    data.loc[data['Group (English)'].str.contains("disposal", regex=False, case=False),
             "general_method"] = "disposed"
    data.loc[data['Group (English)'].str.contains('Treatment', regex=False, case=False),
             "general_method"] = "treatment"
    return data


def data_subsets_gov(data):
    year = data.groupby('REF_DATE', as_index=False).sum()
    expenditures = data.groupby(['Expenditures', 'REF_DATE'],
                                as_index=False).sum()
    location = data.groupby(['GEO', 'REF_DATE'], as_index=False).sum()
    type = data.groupby(['Type of activity', 'REF_DATE', "Expenditures"],
                        as_index=False).sum()
    return year, expenditures, location, type


def data_subs_release(data):
    data = recycling_dispose(data)
    year = data.groupby('Reporting_Year', as_index=False).sum()
    category = data.groupby(['Category (English)', 'Reporting_Year'],
                            as_index=False).sum()
    location = data.groupby(['PROVINCE', 'Reporting_Year'], as_index=False).sum()
    general_group = data.groupby(['general_method', 'Reporting_Year'],
                                 as_index=False).sum()
    detailed_group = data.groupby(['Group (English)', 'Reporting_Year'],
                                  as_index=False).sum()
    return year, category, location, general_group, detailed_group


# Data subsets
gov_inv_year, gov_inv_exp, gov_inv_loc, \
    gov_inv_activity = data_subsets_gov(gov_inv)

dispo_year, dispo_category, \
    dispo_loc, dispo_group, dispo_detailed_group = data_subs_release(subs_dispo)

recycle_year, recycle_category, \
    recycle_loc, recycle_group, \
    recycle_detailed_group = data_subs_release(subs_recycle)

print(gov_inv_activity.columns)
# Compare capital vs operating expenses
compare_graph(gov_inv, gov_inv, "REF_DATE", "VALUE", "Expenditures",
              "REF_DATE", "VALUE",
              "Type of activity", "Gov_expenditures_by_type")

gov_inv_type = gov_inv.groupby(['Expenditures', "REF_DATE"], as_index=False).sum()

interactive_line(gov_inv_type, "REF_DATE", "VALUE", "Expenditures",
                 "Expenditures",
                 "Gov_investment_compared")


# Capital expenditure analysis
cap_exp = gov_inv[gov_inv['Expenditures'] == "Capital expenditures"]
cap_exp = cap_exp.groupby(['Type of activity', "REF_DATE"], as_index=False).sum()
interactive_line(cap_exp, "REF_DATE", "VALUE", "Type of activity",
                 "Type of activity",
                 "Capital_expenditures_ana")


# Operating expenditures analysis
non_cap_exp = gov_inv[gov_inv['Expenditures'] == "Capital expenditures"]
non_cap_exp = non_cap_exp.groupby(['Type of activity', "REF_DATE"],
                                  as_index=False).sum()
interactive_line(non_cap_exp, "REF_DATE", "VALUE", "Type of activity",
                 "Type of activity",
                 "Operating_expenditures_ana")


# Quantity and method used: substance disposed vs substance recycle
subs_dispo_type = subs_dispo.groupby(['Category (English)', "Reporting_Year"],
                                     as_index=False).sum()
interactive_line(subs_dispo_type, "Reporting_Year", "Quantity_converted",
                 "Category (English)", "Category (English)", "Disposal_method")


# Merge recycling and disposing data set
frames = [subs_recycle, subs_dispo]
merged_recycle_dispo = pd.concat(frames)
merged_recycle_dispo = merged_recycle_dispo.sort_values(by=['Reporting_Year'],
                                                        ascending=True)
merged_recycle_dispo = recycling_dispose(merged_recycle_dispo)
merged_recycle_dispo_year = merged_recycle_dispo.groupby(["PROVINCE",
                                                          "Reporting_Year"],
                                                         as_index=False).sum()
merged_recycle_dispo_method = merged_recycle_dispo.groupby(["Reporting_Year",
                                                           "general_method"],
                                                           as_index=False).sum()
merged_recycle_dispo_group = merged_recycle_dispo.groupby(['Group (English)',
                                                           "Reporting_Year"],
                                                          as_index=False).sum()


# Recycling/Disposal method and amount of waste evaluation
graph(merged_recycle_dispo, "Reporting_Year", "Quantity_converted",
      "Group (English)", "waste_disposed_recycled")
plt.close()
graph(merged_recycle_dispo, "Reporting_Year", "Quantity_converted",
      "general_method", "methods_summary")
plt.close()


# Amount of waste by province
interactive_line(merged_recycle_dispo_year, "Reporting_Year", "Quantity_converted",
                "PROVINCE", "PROVINCE", "waste_by_provinces")
interactive_line(merged_recycle_dispo_method, "Reporting_Year",
                 "Quantity_converted", "general_method",
                 "general_method", "methods_summary")
interactive_line(merged_recycle_dispo_group, "Reporting_Year",
                 "Quantity_converted", "Group (English)",
                 "Group (English)", "waste_disposed_recycled")


# Correlation coefficient between Waste and investment: -0.89785
aggregate_waste_by_year = merged_recycle_dispo.groupby('Reporting_Year',
                                                       as_index=False).sum()
interactive_line(aggregate_waste_by_year, 'Reporting_Year', "Quantity_converted",
                 None, None, "Waste_by_year")

aggregate_gov = gov_inv.groupby(['REF_DATE']).sum()
aggregate_waste_inv = pd.merge(aggregate_waste_by_year, aggregate_gov,
                               how='right', right_on=aggregate_gov.index,
                               left_on=aggregate_waste_by_year.index)

corr_waste_inv = np.corrcoef(aggregate_waste_inv['Quantity'],
                             aggregate_waste_inv['VALUE'])


# Correlation coefficient between waste recycled and investment related:
recycle_data = merged_recycle_dispo[merged_recycle_dispo
                                    ['general_method'] == 'recycled']
aggregate_recycle_by_year = recycle_data.groupby('Reporting_Year').sum()
aggregate_recycle_inv = pd.merge(aggregate_recycle_by_year, aggregate_gov,
                                 how='right', right_on=aggregate_gov.index,
                                 left_on=aggregate_recycle_by_year.index)

corr_recycle_inv = np.corrcoef(aggregate_recycle_inv['Quantity'],
                               aggregate_recycle_inv['VALUE'])


# Correlation coefficient between waste disposed and investment related:
dispose_data = merged_recycle_dispo[merged_recycle_dispo
                                    ['general_method'] == 'disposed']
aggregate_dispose_by_year = dispose_data.groupby('Reporting_Year').sum()
aggregate_dispose_inv = pd.merge(aggregate_dispose_by_year, aggregate_gov,
                                 how='right', right_on=aggregate_gov.index,
                                 left_on=aggregate_dispose_by_year.index)

corr_dispose_inv = np.corrcoef(aggregate_dispose_inv['Quantity'],
                               aggregate_dispose_inv['VALUE'])

if __name__ == '__main__':
    print()

