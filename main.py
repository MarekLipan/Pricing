"""
MAIN SCRIPT

"""

import pandas as pd
import numpy as np


# paths
data_path = "/Users/marek/Desktop/Work/Mall/"
figure_path = data_path + "Latex/Figures/"
table_path = data_path + "Latex/Tables/"
# set the seed for replicability of results
np.random.seed(444)

##########################
# LOAD AND CLEAN THE DATA#
##########################
data = pd.read_csv(data_path + "DataScientist__Data.csv", delimiter=";")

# reduced dataset including only "important" columns
rdat = data[["material", "odate", "category", "brand", "grossval_adj",
             "grosspcs", "cost_adj", "vendor_bonus_adj", "period",
             "treatment_change", "grp"]]

# replace strings with floats
for c in ['grossval_adj', "cost_adj", "vendor_bonus_adj"]:
    rdat[c] = pd.to_numeric(rdat[c].str.replace(',', '', regex=True))

# zero bonus
rdat["vendor_bonus_adj"].fillna(0, inplace=True)

# rename values of treatment variable (handy for sorting)
rdat["treatment_change"].fillna("a_base_period", inplace=True)
rdat["treatment_change"] = rdat["treatment_change"].str.replace(
        'old', 'b_old', regex=True)
rdat["treatment_change"] = rdat["treatment_change"].str.replace(
        'new', 'c_new', regex=True)

# compute margin = grossval − cost + bonus
rdat["margin"] = rdat["grossval_adj"] - rdat["cost_adj"] + rdat["vendor_bonus_adj"]
rdat["unit_margin"] = rdat["margin"] / rdat["grosspcs"]

# dates:
start_date = pd.to_datetime("20170501", format='%Y%m%d')
start_pilot_old_date = pd.to_datetime("20170816", format='%Y%m%d')
start_pilot_new_date = pd.to_datetime("20171012", format='%Y%m%d')
end_date = pd.to_datetime("20171101", format='%Y%m%d') # at 00:00

# data for the last day is not complete
rdat = rdat.iloc[:-1, :]

# lengths of periods
base_period_len = (start_pilot_old_date - start_date).days
pilot_old_len = (start_pilot_new_date - start_pilot_old_date).days
pilot_new_len = (end_date - start_pilot_new_date).days
total_len = (end_date - start_date).days
period_len_vec = np.array([base_period_len, pilot_old_len, pilot_new_len, total_len])[:, np.newaxis]

# date in proper format
rdat["odate"] = pd.to_datetime(rdat["odate"], format='%Y%m%d')

# len(pd.unique(rdat.loc[:, "material"]))
# 228 unique products

# len(pd.unique(rdat.loc[:, "category"]))
# 2 unique categories: ['NH018-Ohřívače vody', 'EF005-Mobilní telefony']
rdat_heat = rdat.loc[rdat.loc[:,'category'] == 'NH018-Ohřívače vody']
rdat_mob = rdat.loc[rdat.loc[:,'category'] == 'EF005-Mobilní telefony']

# len(pd.unique(rdat_heat.loc[:, "brand"]))
# len(pd.unique(rdat_heat.loc[:, "material"]))
# 8 unique categories for water heaters
# 117 unique products for water heaters

# len(pd.unique(rdat_mob.loc[:, "brand"]))
# len(pd.unique(rdat_mob.loc[:, "material"]))
# 21 unique categories for mobile phones
# 111 unique products for mobile phones

###########################
# CREATE DESCRIPTIVE PLOTS#
###########################
#runfile(data_path + 'Pricing/descriptive.py')

##################
# TASK 1 ANALYSIS#
##################
#runfile(data_path + 'Pricing/task_1.py')

##################
# TASK 2 ANALYSIS#
##################
#runfile(data_path + 'Pricing/task_2.py')

###############
# END OF FILE #
###############
