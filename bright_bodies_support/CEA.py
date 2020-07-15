import SimPy.EconEval as Econ

import numpy
import SimPy.StatisticalClasses as Stat
import SimPy.InOutFunctions as IO


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
    CEA.plot_CE_plane(x_label='Average BMI Unit Reduction (kg/m' + r'$^2$' + ')per Person\n(Over 10 Simulation Years)',
                      y_label='Average Additional Cost per Person ($)\n(Over 10 Simulation Years)',
                      cost_digits=0, effect_digits=1,
                      x_range=(-0.5, 3.5),
                      title='',
                      fig_size=(4.5, 4.2),
                      file_name='figures/cea.png'
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
        wtp_range=[0, 5000],
        if_paired=True,
        health_measure='d'
    )
    CBA.plot_acceptability_curves(
        x_label='Willingness-to-pay threshold\n($ per average BMI unit reduction)',
        y_range=[-0.01, 1.01],
        fig_size=(4.2, 4)
    )


def report_HC_savings(sim_outcomes_BB, sim_outcomes_CC):
    """ performs HC expenditure savings analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    """

    # INDIVIDUAL: find difference in average total and annual individual HC EXPENDITURE between interventions
    diff_ave_individual_expenditure = []
    for cohortID in range(len(sim_outcomes_CC.cohortHealthCareExpenditure)):
        hc_exp_cc = sim_outcomes_CC.cohortHealthCareExpenditure[cohortID]
        hc_exp_bb = sim_outcomes_BB.cohortHealthCareExpenditure[cohortID]
        pop_size = max(sim_outcomes_BB.pathsOfCohortPopSize[cohortID].get_values())

        # individual total:
        # divide cohort total HC expenditure (over 10 years) by pop size
        individual_hc_exp_cc = hc_exp_cc/pop_size
        individual_hc_exp_bb = hc_exp_bb/pop_size
        diff_ave_individual_expenditure.append(
            numpy.array(individual_hc_exp_cc) - numpy.array(individual_hc_exp_bb))

    statIndividualHCExpenditure = Stat.SummaryStat(
        name='Individual Total HC Expenditure',
        data=diff_ave_individual_expenditure
    )

    # generate CSV values
    hc_expenditure_savings_values = [
        ['HC Expenditure Savings over 10 years:', 'Mean (PI)'],
        ['Individual Total', statIndividualHCExpenditure.get_formatted_mean_and_interval(interval_type='p')],
    ]
    # write CSV

    IO.write_csv(rows=hc_expenditure_savings_values,
                 file_name='bright_bodies_analysis/ComparativeHCSavings.csv')


def report_incremental_effect(sim_outcomes_BB, sim_outcomes_CC):
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
        ['Difference in Average Effect (BMI Unit Reduction) per person:', 'Mean', 'PI'],
        ['BB v. CC', stat_diff_ave_effect.get_mean(), stat_diff_ave_effect.get_interval(interval_type='p')],
    ]

    # generate CSV
    IO.write_csv(rows=differences_ave_effect_values,
                 file_name='bright_bodies_analysis/ComparativeEffectOutcomes.csv')
