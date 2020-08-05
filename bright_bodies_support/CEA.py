import SimPy.EconEval as Econ

import numpy as np
import SimPy.StatisticalClasses as Stat
import SimPy.InOutFunctions as IO
import matplotlib.pyplot as plt

def report_CEA(sim_outcomes_BB, sim_outcomes_CC):
    """ performs cost-effectiveness bright_bodies_analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    """

    # Define Two Strategies
    # Clinical Control
    clinical_control_strategy = Econ.Strategy(
        name='Clinical Control',
        cost_obs=sim_outcomes_CC.aveIndividualCosts,
        effect_obs=sim_outcomes_CC.effects,
        color='darkorange'
    )
    # Bright Bodies
    bright_bodies_strategy = Econ.Strategy(
        name='Bright Bodies',
        cost_obs=sim_outcomes_BB.aveIndividualCosts,
        effect_obs=sim_outcomes_BB.effects,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[clinical_control_strategy, bright_bodies_strategy],
        if_paired=True,
        health_measure='d'
    )

    # show the cost-effectiveness plane
    CEA.plot_CE_plane(x_label='Average BMI Unit Reduction (kg/m' + r'$^2$' + ') per Person-Year'
                                                                             '\n(Over 10 Simulation Years)',
                      y_label='Average Additional Cost per Person ($)\n(Over 10 Simulation Years)',
                      cost_digits=0, effect_digits=1,
                      x_range=(-0.5, 3.5),
                      title='Cost-Effectiveness Plane',
                      fig_size=(4.6, 4),
                      file_name='figures/cea.png'
                      )
    CEA.plot_CE_plane(x_label='Average BMI Unit Reduction (kg/m' + r'$^2$' + ') per Person-Year'
                                                                             '\n(Over 10 Simulation Years)',
                      y_label='Average Additional Cost per Person ($)\n(Over 10 Simulation Years)',
                      cost_digits=0, effect_digits=1,
                      x_range=(-0.5, 3.5),
                      title='Cost-Effectiveness Plane',
                      fig_size=(4.6, 4),
                      )

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=0.05,
        cost_digits=2,
        effect_digits=2,
        icer_digits=2,
        file_name='bright_bodies_analysis/CETable.csv')

    # do CBA
    CBA = Econ.CBA(
        strategies=[clinical_control_strategy, bright_bodies_strategy],
        wtp_range=[0, 50000],
        if_paired=True,
        health_measure='d'
    )
    CBA.plot_acceptability_curves(
        x_label='Willingness-to-pay threshold\n($ per average BMI unit reduction)',
        y_range=[-0.01, 1.01],
        fig_size=(4.2, 4)
    )


def report_HC_savings(sim_outcomes_BB, sim_outcomes_CC, pop_size):
    """ performs HC expenditure savings analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    :param pop_size: population size
    """

    stat_diff_ind_hc_exp = Stat.DifferenceStatPaired(
        name='Individual Total HC Expenditure',
        x=np.array(sim_outcomes_CC.cohortHealthCareExpenditure)/pop_size,
        y_ref=np.array(sim_outcomes_BB.cohortHealthCareExpenditure)/pop_size
    )

    # generate CSV values
    hc_expenditure_savings_values = [
        ['HC Expenditure Savings over 10 years:', 'Mean (PI)'],
        ['Individual Total', stat_diff_ind_hc_exp.get_formatted_mean_and_interval(interval_type='p')],
    ]

    # write CSV
    IO.write_csv(rows=hc_expenditure_savings_values,
                 file_name='bright_bodies_analysis/ComparativeHCSavings.csv')


def report_incremental_cost_effect_savings(sim_outcomes_BB, sim_outcomes_CC):
    """ reports incremental effect
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    """

    # find difference in yearly average BMI between interventions
    stat_diff_ave_effect = Stat.DifferenceStatPaired(
        name='Difference in effect',
        x=sim_outcomes_CC.effects,
        y_ref=sim_outcomes_BB.effects)

    # create list of lists:
    differences_ave_effect_values = [
        ['Difference in Average Effect (BMI Unit Reduction) per person:', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_effect.get_formatted_mean_and_interval(interval_type='p', deci=2)],
    ]

    # generate CSV
    IO.write_csv(rows=differences_ave_effect_values,
                 file_name='bright_bodies_analysis/ComparativeEffectOutcomes.csv')

    # INCREMENTAL COST

    # TOTAL COST
    # find difference in yearly average BMI between interventions
    stat_diff_ave_cost = Stat.DifferenceStatPaired(
        name='Difference in cost',
        x=sim_outcomes_CC.aveIndividualCosts,
        y_ref=sim_outcomes_BB.aveIndividualCosts)

    # create list of lists:
    differences_ave_cost_values = [
        ['Difference in Average Cost per person:', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_cost.get_formatted_mean_and_interval(interval_type='p', deci=2)],
    ]
    print(differences_ave_cost_values)

    # INTERVENTION COST
    # find difference in yearly average intervention costs between interventions (individual)
    stat_diff_ave_int_cost = Stat.DifferenceStatPaired(
        name='Difference in cost',
        x=sim_outcomes_CC.aveIndividualInterventionCosts,
        y_ref=sim_outcomes_BB.aveIndividualInterventionCosts)

    # create list of lists:
    differences_ave_int_cost_values = [
        ['Difference in Average Intervention Cost per person:', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_int_cost.get_formatted_mean_and_interval(interval_type='p', deci=2)],
    ]

    # HC EXPENDITURE COST
    # find difference in yearly average BMI between interventions
    stat_diff_ave_hc_cost = Stat.DifferenceStatPaired(
        name='Difference in cost',
        x=sim_outcomes_CC.aveIndividualHCExpenditure,
        y_ref=sim_outcomes_BB.aveIndividualHCExpenditure)

    # create list of lists:
    differences_ave_hc_cost_values = [
        ['Difference in Average HC Cost per person:', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_hc_cost.get_formatted_mean_and_interval(interval_type='p', deci=2)],
    ]
    # generate CSV
    IO.write_csv(rows=(differences_ave_cost_values, differences_ave_int_cost_values, differences_ave_hc_cost_values),
                 file_name='bright_bodies_analysis/ComparativeCostOutcomes.csv')

    # TODO: Sydney, would you please make a new function for this
    #   in bright_bodies_support/Plots.py
    # FOR COST-SAVINGS

    # list (array) of cost of BB each year for each cohort
    total_cost_by_year_bb = np.array(sim_outcomes_BB.costSavings)
    # average of each element over all the lists (ex. average first element of all lists, add to new list)
    average_cost_by_year_bb = (total_cost_by_year_bb.mean(axis=0))
    print(average_cost_by_year_bb)

    # list (array) of cost of BB each year for each cohort
    total_cost_by_year_cc = np.array(sim_outcomes_CC.costSavings)
    # average of each element over all the lists (ex. average first element of all lists, add to new list)
    average_cost_by_year_cc = (total_cost_by_year_cc.mean(axis=0))
    print(average_cost_by_year_cc)

    difference_average_cost_by_year = average_cost_by_year_bb - average_cost_by_year_cc
    print(difference_average_cost_by_year)

    # FIGURE: Years until BB Cost-Saving
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = difference_average_cost_by_year

    f, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Average Time to Cost-Savings of BB Cohorts relative to CC Cohorts: \n'
                 'Difference in Total Cost by Simulation Year')
    ax.set_xlabel('Simulation Years')
    ax.set_ylabel('Difference in Total Discounted Cost by Year ($)')

    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.axhline(color='black')
    plt.show()

    plt.savefig("figures/TimeToCostSavings.png", dpi=300)

