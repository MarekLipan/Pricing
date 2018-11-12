"""
TASK 2)

"""
import matplotlib.pyplot as plt
from statsmodels.genmod.generalized_estimating_equations import GEE
from statsmodels.genmod.cov_struct import (Exchangeable, Independence,
                                           Autoregressive)
from statsmodels.genmod.families import Poisson

# for each product, group by the data by weeks
t_2_rdat = rdat.loc[:, ["material", "category","grossval_adj", "cost_adj","grosspcs", "odate"]].assign(week=rdat["odate"].dt.week)
# drop the week 35 mobile phones (contains the period of outlier 1.9.-3.9.)
t_2_rdat = t_2_rdat[~((t_2_rdat["week"] == 35) & (t_2_rdat["category"] == "EF005-Mobilní telefony"))]
# grouping
t_2_rdat = t_2_rdat.groupby(["material","week"])["grossval_adj", "cost_adj", "grosspcs"].sum()

# average weekly revenue per piece of product sold
t_2_rdat["unit_grossval"] = t_2_rdat["grossval_adj"] / t_2_rdat["grosspcs"]


def price_recom(prod_number, prod_data, save_fig):
    """
    This function recommends an optimal price for a chosen product for the
    upcoming week based on the given data.

    The function firstly estimates the demand for the product using the poisson
    regression model of the following form:

            grosspcs_t = exp{theta_0 + theta_1 * grossval_adj}

    and then using the overall average cost_adj as the estimate of
    the marginal cost, it rocommends the profit maximizing price:

            price = MC - (1/theta_1)


    Note: This price recommendation model is very simple and is expected to
    work well only for products, for which there is enough price and quantity
    sold variation in the data.

    Parameters
    ----------
    prod_number : Int
        Product number of the product of our interest (material).

    prod_data : DataFrame
        DataFrame with grossval, grosspcs, cost and the unit grossval grouped
        by the weeks for different products, including the product of interest.

    save_fig : Boolean
        Indicating whether the demand estimate figure should be printed and saved.

    Returns
    -------
    price : numpy.float64
        Recommended optimal price for the product of interest.
    """

    # filter the data for the product of interest
    prod_data = prod_data[prod_data.index.get_level_values(0) == prod_number]
    prod_data.index = prod_data.index.get_level_values(1)
    prod_data["subject"] = 1

    # estimate marginal cost (simplification)
    marginal_cost = prod_data["cost_adj"].sum() / prod_data["grosspcs"].sum()

    # estimate the parameters of the poisson regression
    fam = Poisson()
    ind = Independence()
    poisson_reg_mod = GEE.from_formula("grosspcs ~ unit_grossval", "subject",
                                       prod_data, cov_struct=ind, family=fam)
    poisson_results = poisson_reg_mod.fit()
    # print(poisson_results.summary())
    theta = poisson_results.params
    # stop for the positive slope of demand curve
    if theta[1] >= 0:
        raise ValueError(
                "The 'price_recom' function cannot provide a reliable price recommendation for the selected product based on the given data."
                )
    # compute the profit maximizing price
    price = marginal_cost - (1/theta[1])

    if save_fig:
        # demand estimate figure
        q = np.arange(min(prod_data["grosspcs"]),
                      max(prod_data["grosspcs"]) + 0.1, 0.1)
        demand = (np.log(q) - theta[0])/ theta[1]
        # figure itself
        fig, a = plt.subplots(figsize=(8, 8))
        a.scatter(prod_data["grosspcs"], prod_data["unit_grossval"],
                  marker='o', color="g")
        a.plot(q, demand, color="b")
        a.scatter(np.exp(theta[0] + theta[1]*price), price, marker='o',
                  color="r")
        a.set_title('Product: '+str(prod_number) + ' demand estimate')
        a.set_xlabel('Quantity sold (pcs.)')
        a.set_ylabel('Per unit price (CZK)')
        a.grid(color='k', linestyle=':', linewidth=0.5)
        # save the figure
        fig.savefig(figure_path + "demand_" + str(prod_number) + ".pdf",
                    bbox_inches='tight')

    return price

# Example price recommendations
price = price_recom(890559, t_2_rdat, True) # Water heater (Drazice)
price = price_recom(1031616, t_2_rdat, True) # Mobile phone (Apple)
price = price_recom(905877, t_2_rdat, True) # Mobile phone (Lenovo)

###############
# END OF FILE #
###############
