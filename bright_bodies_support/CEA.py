import SimPy.EconEval as Econ

import numpy as np
import SimPy.StatisticalClasses as Stat
import SimPy.InOutFunctions as IO
import numpy


def report_CEA(sim_outcomes_BB, sim_outcomes_CC, color_bb, color_cc):
    """ performs cost-effectiveness bright_bodies_analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    :param color_bb: color code for Bright Bodies
    :param color_cc: color code for Clinical Control
    """

    # Define Two Strategies
    # Clinical Control
    clinical_control_strategy = Econ.Strategy(
        name='Clinical Control',
        cost_obs=sim_outcomes_CC.aveIndividualCosts,
        effect_obs=sim_outcomes_CC.effects,
        color=color_cc
    )
    # Bright Bodies
    bright_bodies_strategy = Econ.Strategy(
        name='Bright Bodies',
        cost_obs=sim_outcomes_BB.aveIndividualCosts,
        effect_obs=sim_outcomes_BB.effects,
        color=color_bb
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
                      file_name='figures/CEA.png'
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
    if_cba = False
    if if_cba:
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


def report_time_to_cost_savings(sim_outcomes_BB, sim_outcomes_CC):
    """ reports incremental effect
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    """

    list_of_lists_of_diff_avg_cum_cost = []
    for cohort in range(len(sim_outcomes_BB.cumAveIndividualCosts)):
        cumulative_cost_bb = numpy.array(sim_outcomes_BB.cumAveIndividualCosts[cohort])
        cumulative_cost_cc = numpy.array(sim_outcomes_CC.cumAveIndividualCosts[cohort])
        diff_avg_cum_cost = cumulative_cost_bb - cumulative_cost_cc
        list_of_lists_of_diff_avg_cum_cost.append(diff_avg_cum_cost)

    # algorithm for exact time to cost-savings
    list_of_time_of_cost_savings = []
    for list in list_of_lists_of_diff_avg_cum_cost:
        diff_avg_cum_cost_values = list
        # x-axis
        x_axis = numpy.arange(0, 11)
        # year during which cost savings occurs
        year_before_cost_savings = numpy.argwhere(numpy.diff(numpy.sign(diff_avg_cum_cost_values - x_axis))).flatten()
        # year following cost savings
        year_after_cost_savings = year_before_cost_savings+1
        # find exact time during year of cost savings
        C1 = int(year_before_cost_savings[0])
        C2 = int(year_after_cost_savings[0])

        x = list[C1]
        y = list[C2]

        time_of_cost_savings = C1 + (x/(x-y))
        list_of_time_of_cost_savings.append(time_of_cost_savings)

    # find mean and UI of time to cost-saving
    stat_time_to_cost_savings = Stat.SummaryStat(
        data=list_of_time_of_cost_savings,
        name='Time to Cost Savings'
    )

    avg_time_to_cost_savings = [
        ['Time to Cost Savings', 'Mean (PI)'],
        ['BB v. CC', stat_time_to_cost_savings.get_formatted_mean_and_interval(interval_type='p', deci=2)],
    ]
    # generate CSV
    IO.write_csv(rows=avg_time_to_cost_savings,
                 file_name='bright_bodies_analysis/TimeToCostSavings.csv')
