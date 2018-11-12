"""
TASK 1)

"""
from pylatex import Table, Tabular, MultiColumn, MultiRow, Tabu
from pylatex.utils import NoEscape

# prepare table for outputs
output_table = pd.DataFrame(
        data=np.full((3, 8), 0, dtype=float),
        columns=["Coeff.", "p-val"]*4,
        index=["Revenue", "Margin", "Quantity"]
        )

################
# Mobile Phones#
################

mob_prod = pd.unique(rdat_mob.loc[:, "material"])
# len(pd.unique(rdat_mob.loc[:, "material"]))
# sum(rdat_heat.groupby(['material', "grp"])[
#        "grossval_adj"].sum().index.get_level_values(1) == "pilot")
# 111 products - 58 pilot, 53 control
# remove 1.9. - 3.9. as an outlier from the testing
t_1_mob = rdat_mob.loc[~rdat_mob["odate"].isin(pd.to_datetime(
        ["20170901", "20170902", "20170903"], format='%Y%m%d')), :]
t_1_mob_days = len(pd.unique(t_1_mob["odate"]))
# group by date for running difference-in-differences
t_1_mob_did_original = pd.concat([
        t_1_mob[(t_1_mob['grp'] == 'pilot')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=1), #, time = range(1, t_1_mob_days+1)
        t_1_mob[(t_1_mob['grp'] == 'control')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=0) #, time = range(1, t_1_mob_days+1)
        ])
# add dummies for interaction (pilot periods x pilot group)
t_1_mob_did_original = t_1_mob_did_original.assign(pilot_period_1=t_1_mob_did_original["pilot"]*((t_1_mob_did_original.index>=start_pilot_old_date) & (t_1_mob_did_original.index<start_pilot_new_date)),
                                                   pilot_period_2=t_1_mob_did_original["pilot"]*(t_1_mob_did_original.index>=start_pilot_new_date))
## estimate DiD (OLS)
beta_original = np.full((1, 6), 0, dtype=float)
# revenue
y = t_1_mob_did_original.loc[:, "grossval_adj"].values
X = t_1_mob_did_original.iloc[:, 3:].values
beta_original[0, 0:2] = np.linalg.multi_dot(
        [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
        )[-2:]
# margin
y = t_1_mob_did_original.loc[:, "margin"].values
X = t_1_mob_did_original.iloc[:, 3:].values
beta_original[0, 2:4] = np.linalg.multi_dot(
        [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
        )[-2:]
# quantity sold
y = t_1_mob_did_original.loc[:, "grosspcs"].values
X = t_1_mob_did_original.iloc[:, 3:].values
beta_original[0, 4:6] = np.linalg.multi_dot(
        [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
        )[-2:]

## Randomization inference
np.random.seed(444)
beta_dist = np.full((1000, 6), 0, dtype=float)
for r in range(1000):
    # select randomly the products for the pilot group
    random_pilot_group = np.random.choice(mob_prod, size=58, replace=False)
    t_1_mob_random = t_1_mob
    # replace the assignment to pilot/control groups, 1=pilot, 0=control
    t_1_mob_random.loc[:, "grp"] = 1*t_1_mob_random["material"].isin(random_pilot_group)
    # group by date for running difference-in-differences
    t_1_mob_did_random = pd.concat([
            t_1_mob[(t_1_mob_random['grp'] == 1)].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=1),
            t_1_mob[(t_1_mob_random['grp'] == 0)].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=0)
            ])
    # add dummies for interaction (pilot periods x pilot group)
    t_1_mob_did_random = t_1_mob_did_random.assign(pilot_period_1=t_1_mob_did_random["pilot"]*((t_1_mob_did_random.index>=start_pilot_old_date) & (t_1_mob_did_random.index<start_pilot_new_date)),
                                                       pilot_period_2=t_1_mob_did_random["pilot"]*(t_1_mob_did_random.index>=start_pilot_new_date))
    ## estimate DiD (OLS)
    # revenue
    y = t_1_mob_did_random.loc[:, "grossval_adj"].values
    X = t_1_mob_did_random.iloc[:, 3:].values
    beta_dist[r, 0:2] = np.linalg.multi_dot(
            [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
            )[-2:]
    # margin
    y = t_1_mob_did_random.loc[:, "margin"].values
    X = t_1_mob_did_random.iloc[:, 3:].values
    beta_dist[r, 2:4] = np.linalg.multi_dot(
            [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
            )[-2:]
    # quantity sold
    y = t_1_mob_did_random.loc[:, "grosspcs"].values
    X = t_1_mob_did_random.iloc[:, 3:].values
    beta_dist[r, 4:6] = np.linalg.multi_dot(
            [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
            )[-2:]

# randomization inference p-values
p = np.mean(abs(beta_original) <= abs(beta_dist), axis=0)

# fill the output table
output_table.iloc[:, [0, 2]] = beta_original.reshape((3, 2))
output_table.iloc[:, [1, 3]] = p.reshape((3, 2))

################
# Water Heaters#
################

heat_prod = pd.unique(rdat_heat.loc[:, "material"])
# len(pd.unique(rdat_heat.loc[:, "material"]))
# sum(rdat_heat.groupby(['material', "grp"])[
#        "grossval_adj"].sum().index.get_level_values(1) == "pilot")
# 117 products - 58 pilot, 59 control
t_1_heat = rdat_heat
t_1_heat_days = len(pd.unique(t_1_heat["odate"]))
# group by date for running difference-in-differences
t_1_heat_did_original = pd.concat([
        t_1_heat[(t_1_heat['grp'] == 'pilot')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=1), #, time = range(1, t_1_heat_days+1)
        t_1_heat[(t_1_heat['grp'] == 'control')].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=0) #, time = range(1, t_1_heat_days+1)
        ])
# add dummies for interaction (pilot periods x pilot group)
t_1_heat_did_original = t_1_heat_did_original.assign(pilot_period_1=t_1_heat_did_original["pilot"]*((t_1_heat_did_original.index>=start_pilot_old_date) & (t_1_heat_did_original.index<start_pilot_new_date)),
                                                   pilot_period_2=t_1_heat_did_original["pilot"]*(t_1_heat_did_original.index>=start_pilot_new_date))
## estimate DiD (OLS)
beta_original = np.full((1, 6), 0, dtype=float)
# revenue
y = t_1_heat_did_original.loc[:, "grossval_adj"].values
X = t_1_heat_did_original.iloc[:, 3:].values
beta_original[0, 0:2] = np.linalg.multi_dot(
        [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
        )[-2:]
# margin
y = t_1_heat_did_original.loc[:, "margin"].values
X = t_1_heat_did_original.iloc[:, 3:].values
beta_original[0, 2:4] = np.linalg.multi_dot(
        [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
        )[-2:]
# quantity sold
y = t_1_heat_did_original.loc[:, "grosspcs"].values
X = t_1_heat_did_original.iloc[:, 3:].values
beta_original[0, 4:6] = np.linalg.multi_dot(
        [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
        )[-2:]

## Randomization inference
np.random.seed(555)
beta_dist = np.full((1000, 6), 0, dtype=float)
for r in range(1000):
    # select randomly the products for the pilot group
    random_pilot_group = np.random.choice(heat_prod, size=58, replace=False)
    t_1_heat_random = t_1_heat
    # replace the assignment to pilot/control groups, 1=pilot, 0=control
    t_1_heat_random.loc[:, "grp"] = 1*t_1_heat_random["material"].isin(random_pilot_group)
    # group by date for running difference-in-differences
    t_1_heat_did_random = pd.concat([
            t_1_heat[(t_1_heat_random['grp'] == 1)].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=1),
            t_1_heat[(t_1_heat_random['grp'] == 0)].groupby(['odate'])["grossval_adj", "margin", "grosspcs"].sum().assign(intercept = 1, pilot=0)
            ])
    # add dummies for interaction (pilot periods x pilot group)
    t_1_heat_did_random = t_1_heat_did_random.assign(pilot_period_1=t_1_heat_did_random["pilot"]*((t_1_heat_did_random.index>=start_pilot_old_date) & (t_1_heat_did_random.index<start_pilot_new_date)),
                                                       pilot_period_2=t_1_heat_did_random["pilot"]*(t_1_heat_did_random.index>=start_pilot_new_date))
    ## estimate DiD (OLS)
    # revenue
    y = t_1_heat_did_random.loc[:, "grossval_adj"].values
    X = t_1_heat_did_random.iloc[:, 3:].values
    beta_dist[r, 0:2] = np.linalg.multi_dot(
            [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
            )[-2:]
    # margin
    y = t_1_heat_did_random.loc[:, "margin"].values
    X = t_1_heat_did_random.iloc[:, 3:].values
    beta_dist[r, 2:4] = np.linalg.multi_dot(
            [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
            )[-2:]
    # quantity sold
    y = t_1_heat_did_random.loc[:, "grosspcs"].values
    X = t_1_heat_did_random.iloc[:, 3:].values
    beta_dist[r, 4:6] = np.linalg.multi_dot(
            [np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X), y]
            )[-2:]

# randomization inference p-values
p = np.mean(abs(beta_original) <= abs(beta_dist), axis=0)

# fill the output table
output_table.iloc[:, [4, 6]] = beta_original.reshape((3, 2))
output_table.iloc[:, [5, 7]] = p.reshape((3, 2))

########################
# Printing output table#
########################
# create tabule object
tabl = Table()
tabl.add_caption("Estimates of the effects of changing price rules on differents variables for both categories along with the p-values from the randomization inference.")
tabl.append(NoEscape("\label{tab: output_table}"))

# create tabular object
tabr = Tabular(table_spec="l|cc|cc|cc|cc")
tabr.add_hline()
tabr.add_hline()

# header row
tabr.add_row((MultiRow(3, data="Dependent Variable"),
              MultiColumn(4, align='|c|', data="Mobile Phones"),
              MultiColumn(4, align='|c', data="Water Heaters")))
tabr.add_hline(start=2, end=9, cmidruleoption="lr")
tabr.add_row(("",
              MultiColumn(2, align='|c|', data="Pilot 1"),
              MultiColumn(2, align='|c|', data="Pilot 2"),
              MultiColumn(2, align='|c|', data="Pilot 1"),
              MultiColumn(2, align='|c', data="Pilot 2")))
tabr.add_hline(start=2, end=9, cmidruleoption="lr")
tabr.add_row([""] + 4*["Coeff.", "p-val."])
tabr.add_hline()

# specify format
fmt = "{:.3f}"

# fill in the rows for each combination method (-3 for individuals)
for i in range(3):
    tabr.add_row([output_table.index[i]] + [
            fmt.format(item) for item in output_table.iloc[i, :]])


# end of table
tabr.add_hline()
tabr.add_hline()

# add tabular to table
tabl.append(tabr)

# export the table
tabl.generate_tex(table_path + "output_table")


###############
# END OF FILE #
###############
