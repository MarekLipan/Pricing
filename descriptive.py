"""
DESCRIPTIVE PLOTS

"""

import matplotlib.pyplot as plt

##################################################
# 1) Time series plots of revenue/margin/quantity#
##################################################
# group the data by days
rdat_day_group = rdat[(rdat['category'] == 'EF005-Mobilní telefony') & (rdat['grp'] == 'pilot')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum()
rdat_day_group = pd.concat(
        [rdat_day_group,
         rdat[(rdat['category'] == 'EF005-Mobilní telefony') & (rdat['grp'] == 'control')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum()], axis=1
         )
rdat_day_group = pd.concat(
        [rdat_day_group,
         rdat[(rdat['category'] == 'NH018-Ohřívače vody') & (rdat['grp'] == 'pilot')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum()], axis=1
         )
rdat_day_group = pd.concat(
        [rdat_day_group,
         rdat[(rdat['category'] == 'NH018-Ohřívače vody') & (rdat['grp'] == 'control')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum()], axis=1
         )
# rename columns
day_group_cols = []
for i in ("mob", "heat"):
    for j in ("pilot", "control"):
        for k in ("grossval", "margin", "grosspcs"):
            day_group_cols += [str(i+"_"+j+"_"+k)]

rdat_day_group.columns = day_group_cols

# time series figure
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 15))

# mobile - total revenue
a = axes[0, 0]
rdat_day_group[[day_group_cols[0], day_group_cols[3]]].plot(ax=a, linewidth=1, color=["b", "g"])
a.set_title('Mobile Phones - Total Revenue (CZK)')
a.set_xlabel('Time')
a.grid(color='k', linestyle=':', linewidth=0.5)
a.axvline(x=start_pilot_old_date, color="red")
a.axvline(x=start_pilot_new_date, color="red")
a.legend(["Pilot", "Control"])
# mobile - total margin
a = axes[1, 0]
rdat_day_group[[day_group_cols[1], day_group_cols[4]]].plot(ax=a, linewidth=1, color=["b", "g"])
a.set_title('Mobile Phones - Total Margin (CZK)')
a.set_xlabel('Time')
a.grid(color='k', linestyle=':', linewidth=0.5)
a.axvline(x=start_pilot_old_date, color="red")
a.axvline(x=start_pilot_new_date, color="red")
a.legend(["Pilot", "Control"])
# mobile - quantity sold
a = axes[2, 0]
rdat_day_group[[day_group_cols[2], day_group_cols[5]]].plot(ax=a, linewidth=1, color=["b", "g"])
a.set_title('Mobile Phones - Quantity Sold (pcs.)')
a.set_xlabel('Time')
a.grid(color='k', linestyle=':', linewidth=0.5)
a.axvline(x=start_pilot_old_date, color="red")
a.axvline(x=start_pilot_new_date, color="red")
a.legend(["Pilot", "Control"])

# heaters - total revenue
a = axes[0, 1]
rdat_day_group[[day_group_cols[6], day_group_cols[9]]].plot(ax=a, linewidth=1, color=["b", "g"])
a.set_title('Water Heaters - Total Revenue (CZK)')
a.set_xlabel('Time')
a.grid(color='k', linestyle=':', linewidth=0.5)
a.axvline(x=start_pilot_old_date, color="red")
a.axvline(x=start_pilot_new_date, color="red")
a.legend(["Pilot", "Control"])
# heaters - total margin
a = axes[1, 1]
rdat_day_group[[day_group_cols[7], day_group_cols[10]]].plot(ax=a, linewidth=1, color=["b", "g"])
a.set_title('Water Heaters - Total Margin (CZK)')
a.set_xlabel('Time')
a.grid(color='k', linestyle=':', linewidth=0.5)
a.axvline(x=start_pilot_old_date, color="red")
a.axvline(x=start_pilot_new_date, color="red")
a.legend(["Pilot", "Control"])
# heaters - quantity sold
a = axes[2, 1]
rdat_day_group[[day_group_cols[8], day_group_cols[11]]].plot(ax=a, linewidth=1, color=["b", "g"])
a.set_title('Water Heaters - Quantity Sold (pcs.)')
a.set_xlabel('Time')
a.grid(color='k', linestyle=':', linewidth=0.5)
a.axvline(x=start_pilot_old_date, color="red")
a.axvline(x=start_pilot_new_date, color="red")
a.legend(["Pilot", "Control"])

# whole figure
fig.autofmt_xdate()
fig.savefig(figure_path + "time_series.pdf", bbox_inches='tight')

########################################################
# 2) Histogram of quantities sold of different products#
########################################################

# grouped by material (product number)
rdat_material = rdat.groupby('material')["grosspcs"].sum()

# histogram figure
fig, a = plt.subplots(figsize=(8, 6))
a.hist(rdat_material[rdat_material <= 250], color="b", density=False)
a.set_xlabel('Quantity (pcs.)')
a.set_ylabel('Counts')
a.set_title("Quantities of products sold")
a.grid(color='k', linestyle=':', linewidth=0.5)
fig.savefig(figure_path + "quantities_hist.pdf", bbox_inches='tight')


###############
# END OF FILE #
###############
