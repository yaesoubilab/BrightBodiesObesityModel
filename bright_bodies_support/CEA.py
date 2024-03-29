import numpy
import numpy as np

import deampy.econ_eval as Econ
import deampy.in_out_functions as IO
import deampy.statistics as Stat


def report_CEA(sim_outcomes_BB, sim_outcomes_CC, maintenance_effect, color_bb, color_cc, fig_size=(4.6, 4)):
    """ performs cost-effectiveness bright_bodies_analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    :param maintenance_effect: scenario for the maintenance effect
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
                      x_range=(-0.5, 4), y_range=(-4000, 500),
                      title='Cost-Effectiveness Plane',
                      fig_size=fig_size,
                      file_name='outputs/figs/CEA-{}.png'.format(maintenance_effect),
                      add_clouds=True)

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=0.05,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='outputs/csv/CEA-{}.csv'.format(maintenance_effect))

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


def report_HC_savings(sim_outcomes_BB, sim_outcomes_CC, pop_size, maintenance_effect):
    """ performs HC expenditure savings analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    :param pop_size: population size
    :param maintenance_effect: scenario for maintenance effect
    """

    stat_diff_ind_hc_exp = Stat.DifferenceStatPaired(
        name='Individual Total HC Expenditure',
        x=np.array(sim_outcomes_CC.cohortHealthCareExpenditure)/pop_size,
        y_ref=np.array(sim_outcomes_BB.cohortHealthCareExpenditure)/pop_size
    )

    # generate CSV values
    hc_expenditure_savings_values = [
        ['HC Expenditure Savings over 10 years:', 'Mean (PI)'],
        ['Individual Total', stat_diff_ind_hc_exp.get_formatted_mean_and_interval(interval_type='p', deci=0)],
    ]

    # write CSV
    IO.write_csv(rows=hc_expenditure_savings_values,
                 file_name='outputs/csv/ComparativeHCSavings-{}.csv'.format(maintenance_effect))


def report_incremental_cost_effect_savings(sim_outcomes_BB, sim_outcomes_CC, maintenance_effect):
    """ reports incremental effect
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    :param maintenance_effect: scenario for maintenance effect
    """

    # find difference in yearly average BMI between interventions
    stat_diff_ave_effect = Stat.DifferenceStatPaired(
        name='Difference in effect',
        x=sim_outcomes_CC.effects,
        y_ref=sim_outcomes_BB.effects)

    # create list of lists:
    diff_ave_effect_values = [
        ['BMI Unit Reduction (per person):', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_effect.get_formatted_mean_and_interval(interval_type='p', deci=2)],
    ]

    # generate CSV
    IO.write_csv(rows=diff_ave_effect_values,
                 file_name='outputs/csv/ComparativeEffectOutcomes-{}.csv'.format(maintenance_effect))

    # INCREMENTAL COST

    # TOTAL COST
    # find difference in yearly average BMI between interventions
    stat_diff_ave_cost = Stat.DifferenceStatPaired(
        name='Difference in cost',
        x=sim_outcomes_BB.aveIndividualCosts,
        y_ref=sim_outcomes_CC.aveIndividualCosts)

    # create list of lists:
    differences_ave_cost_values = [
        ['Increase in Average Cost (per person):', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_cost.get_formatted_mean_and_interval(interval_type='p', deci=0)],
    ]

    # INTERVENTION COST
    # find difference in yearly average intervention costs between interventions (individual)
    stat_diff_ave_int_cost = Stat.DifferenceStatPaired(
        name='Difference in cost',
        x=sim_outcomes_BB.aveIndividualInterventionCosts,
        y_ref=sim_outcomes_CC.aveIndividualInterventionCosts)

    # create list of lists:
    differences_ave_int_cost_values = [
        ['Increase in Average Intervention Cost per person:', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_int_cost.get_formatted_mean_and_interval(interval_type='p', deci=0)],
    ]

    # HC EXPENDITURE COST
    # find difference in yearly average BMI between interventions
    stat_diff_ave_hc_cost = Stat.DifferenceStatPaired(
        name='Difference in cost',
        x=sim_outcomes_BB.aveIndividualHCExpenditure,
        y_ref=sim_outcomes_CC.aveIndividualHCExpenditure)

    # create list of lists:
    differences_ave_hc_cost_values = [
        ['Increase in Average HC Cost per person:', 'Mean (PI)'],
        ['BB v. CC', stat_diff_ave_hc_cost.get_formatted_mean_and_interval(interval_type='p', deci=0)],
    ]
    # generate CSV
    IO.write_csv(rows=(differences_ave_cost_values, differences_ave_int_cost_values, differences_ave_hc_cost_values),
                 file_name='outputs/csv/ComparativeCostOutcomes-{}.csv'.format(maintenance_effect))


def get_list_of_diff_ave_cum_costs(multisim_outcomes_BB, multisim_outcomes_CC):
    """ reports difference in cumulative average cost (over individuals) by cohort
    :param multisim_outcomes_BB: outcomes of multiple cohorts simulated under Bright Bodies
    :param multisim_outcomes_CC: outcomes of multiple cohorts simulated under Clinical Control
    """
    list_of_lists_of_diff_avg_cum_cost = []
    for cohort in range(len(multisim_outcomes_BB.cumAveIndividualCosts)):
        cumulative_cost_bb = numpy.array(multisim_outcomes_BB.cumAveIndividualCosts[cohort])
        cumulative_cost_cc = numpy.array(multisim_outcomes_CC.cumAveIndividualCosts[cohort])
        diff_avg_cum_cost = cumulative_cost_bb - cumulative_cost_cc
        list_of_lists_of_diff_avg_cum_cost.append(diff_avg_cum_cost)
        # return diff_avg_cum_cost, list_of_lists_of_diff_avg_cum_cost
    return list_of_lists_of_diff_avg_cum_cost


def get_estimated_time_of_cost_saving(incremental_costs):
    """
    :param incremental_costs: (list) of non-increasing incremental cost values
    :return: estimated time where cost-saving occurs
    """

    # find year index when cost-saving occurs
    cost_saving_occurred = False
    for year_index, incre_cost in enumerate(incremental_costs):
        if incre_cost < 0:
            cost_saving_occurred = True
            break

    # estimate the time until cost saving
    if cost_saving_occurred:
        cost_last_positive = incremental_costs[year_index - 1]
        cost_first_negative = incremental_costs[year_index]
        time_of_cost_saving = year_index + (cost_last_positive / (cost_last_positive - cost_first_negative))
    else:
        time_of_cost_saving = np.inf

    return time_of_cost_saving


def report_time_to_cost_savings(sim_outcomes_BB, sim_outcomes_CC, maintenance_effect):
    """ reports incremental effect
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    :param maintenance_effect: scenario for maintenance effect
    """

    incremental_cum_costs = get_list_of_diff_ave_cum_costs(multisim_outcomes_BB=sim_outcomes_BB,
                                                           multisim_outcomes_CC=sim_outcomes_CC)

    diff_cum_ave_cost = numpy.array(incremental_cum_costs).mean(axis=0)

    expected_time_until_cost_saving = get_estimated_time_of_cost_saving(diff_cum_ave_cost)

    # algorithm for exact time to cost-savings
    list_of_time_of_cost_savings = []
    for incremental_costs in incremental_cum_costs:

        # find year index when cost-saving occurs
        time_of_cost_saving = get_estimated_time_of_cost_saving(incremental_costs)
        list_of_time_of_cost_savings.append(time_of_cost_saving)

    # find mean and UI of time to cost-saving
    stat_time_to_cost_savings = Stat.SummaryStat(
        data=list_of_time_of_cost_savings,
        name='Time to Cost Savings'
    )

    avg_time_to_cost_savings = [
        ['Time to Cost Savings', 'Mean', 'PI'],
        ['BB v. CC',
         '{:.{prec}f}'.format(expected_time_until_cost_saving, prec=2),
         stat_time_to_cost_savings.get_formatted_interval(interval_type='p', deci=2)],
    ]
    # generate CSV
    IO.write_csv(rows=avg_time_to_cost_savings,
                 file_name='outputs/csv/TimeToCostSavings-{}.csv'.format(maintenance_effect))
