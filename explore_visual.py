from data_import import gov_inv, subs_release, subs_dispo, subs_recycle
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker
import plotly.express as px
import pandas as pd


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


def interactive_line(data, x, y, title, color, line_group):
    fig = px.line(data, x=x, y=y, title=title, color=color, line_group=line_group)
    fig.write_html('{}.html'.format(title))
    fig.show()
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


# Compare capital vs operating expenses
compare_graph(gov_inv, gov_inv, "REF_DATE", "VALUE", "Expenditures",
              "REF_DATE", "VALUE",
              "Type of activity", "Gov_expenditures_by_type")
plt.close()
graph(gov_inv, "REF_DATE", "VALUE",
      "Expenditures", "Government_investment_compared")
plt.close()

# Capital expenditure analysis
cap_exp = gov_inv[gov_inv['Expenditures'] == "Capital expenditures"]
graph(cap_exp, "REF_DATE", "VALUE", "Type of activity", "Capital_expenditure_ana")
plt.close()
# Operating expenditures analysis
non_cap_exp = gov_inv[gov_inv['Expenditures'] == "Capital expenditures"]
graph(non_cap_exp, "REF_DATE", "VALUE", "Type of activity", "Operating_expenditures_ana")
plt.close()
# Quantity and method used: substance disposed vs substance recycle
graph(subs_dispo, "Reporting_Year", "Quantity_converted",
      "Category (English)", "Disposal_method")
plt.close()
# Merge recycling and disposing data set
frames = [subs_recycle, subs_dispo]
merged_recycle_dispo = pd.concat(frames)
merged_recycle_dispo = merged_recycle_dispo.sort_values(by=['Reporting_Year'],
                                                        ascending=True)
merged_recycle_dispo = recycling_dispose(merged_recycle_dispo)
merged_recycle_dispo_year = merged_recycle_dispo.groupby(["PROVINCE", "Reporting_Year"], as_index=False).sum()

# Recycling/Disposal method and amount of waste evaluation
graph(merged_recycle_dispo, "Reporting_Year", "Quantity_converted",
      "Group (English)", "waste_disposed_recycled")
plt.close()
graph(merged_recycle_dispo, "Reporting_Year", "Quantity_converted",
      "general_method", "methods_summary")
plt.close()

# Amount of waste by province
graph(merged_recycle_dispo, "Reporting_Year", "Quantity_converted",
      "PROVINCE", "waste_by_provinces")
plt.close()
interactive_line(merged_recycle_dispo_year, "Reporting_Year", "Quantity_converted",
                 "waste_by_province", "PROVINCE", "PROVINCE")

if __name__ == '__main__':
    print()

