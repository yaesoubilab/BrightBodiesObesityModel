import SimPy.EconEval as Econ

import numpy
import SimPy.StatisticalClasses as Stat


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
    """ performs cost-effectiveness bright_bodies_analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    """

    # COHORT: find difference in yearly average cohort HC EXPENDITURE between interventions
    diff_yearly_ave_expenditure = []
    for cohortID in range(len(sim_outcomes_CC.cohortHealthCareExpenditure)):
        hc_exp_cc = sim_outcomes_CC.cohortHealthCareExpenditure[cohortID]
        # print(hc_exp_cc)
        hc_exp_bb = sim_outcomes_BB.cohortHealthCareExpenditure[cohortID]
        # print(hc_exp_bb)
        diff_yearly_ave_expenditure.append(numpy.array(hc_exp_cc) - numpy.array(hc_exp_bb))

    statCohortHCExpenditure = Stat.SummaryStat(
        name='Cohort HC Expenditure',
        data=diff_yearly_ave_expenditure
    )

    print('cohort HC exp: mean, PI',
          statCohortHCExpenditure.get_formatted_mean_and_interval(interval_type='p'))

    # INDIVIDUAL: find difference in yearly average individual HC expenditure btw int.
    diff_yearly_ave_individual_expenditure = []
    for cohortID in range(len(sim_outcomes_CC.cohortHealthCareExpenditure)):
        hc_exp_cc = sim_outcomes_CC.aveIndividualHCExpenditure[cohortID]
        hc_exp_bb = sim_outcomes_BB.aveIndividualHCExpenditure[cohortID]
        diff_yearly_ave_individual_expenditure.append(numpy.array(hc_exp_cc) - numpy.array(hc_exp_bb))

    statIndividualHCExpenditure = Stat.SummaryStat(
        name='Individual HC Expenditure',
        data=diff_yearly_ave_individual_expenditure
    )

    print('individual HC exp: mean, PI',
          statIndividualHCExpenditure.get_formatted_mean_and_interval(interval_type='p'))
