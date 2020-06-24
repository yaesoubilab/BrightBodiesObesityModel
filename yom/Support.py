import matplotlib.pyplot as plt
import numpy

import InputData as D
import SimPy.EconEval as Econ
import SimPy.Plots.SamplePaths as Path
import SimPy.StatisticalClasses as Stat
import yom.Data as Data
from SimPy.Plots import PopulationPyramids as Pyr


def add_yearly_change_in_bmi_to_ax(ax, sim_outcomes, intervention):
    """ add yearly change in BMI to provided axis """

    # BMI difference by year
    year_one_vs_zero = []
    year_two_vs_one = []

    for cohortID in range(D.N_COHORTS):
        bmi_values = sim_outcomes.pathsOfCohortAveBMI[cohortID].get_values()

        # year 1 minus year 0
        year_one_vs_zero.append(bmi_values[1] - bmi_values[0])
        # year 2 minus year 1
        year_two_vs_one.append(bmi_values[2] - bmi_values[1])

    if intervention == D.Interventions.BRIGHT_BODIES:
        ys = Data.YEARLY_DIFF_BMI_BB
        lbs = Data.YEARLY_DIFF_BMI_BB_LB
        ubs = Data.YEARLY_DIFF_BMI_BB_UB
        ax.set_title('\nBright Bodies')
        ax.text(-0.05, 1.025, 'B)', transform=ax.transAxes, size=11, weight='bold')
    else:
        ys = Data.YEARLY_DIFF_BMI_CONTROL
        lbs = Data.YEARLY_DIFF_BMI_CONTROL_LB
        ubs = Data.YEARLY_DIFF_BMI_CONTROL_UB
        ax.set_title('\nControl')
        ax.text(-0.05, 1.025, 'A)', transform=ax.transAxes, size=11, weight='bold')

    # adding RCT data
    ax.scatter([1, 2], ys, color='orange', label="RCT Average Difference in BMI")
    # adding error bars
    ax.errorbar([1, 2], ys, yerr=(lbs, ubs), fmt='none', capsize=4, ecolor='orange')

    # adding simulation outcomes
    for this_y in year_one_vs_zero:
        ax.scatter(1, this_y, color='blue', marker='_', s=200, alpha=0.25)
    for this_y in year_two_vs_one:
        ax.scatter(2, this_y, color='blue', marker='_', s=200, alpha=0.25)

    ax.axhline(y=0, color='k', ls='--', linewidth=0.5)

    ax.set_xlim((0.5, 2.5))
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['Year 1 to 0', 'Year 2 to 1'])
    ax.set_ylim((-3.5, 3.5))
    if intervention == D.Interventions.CONTROL:
        ax.set_ylabel('Difference in BMI (kg/m^2)')
    else:
        ax.set_ylabel(' ')

    ax.legend(['RCT', 'Model'], loc='upper right')


def plot_validation(sim_outcomes_control, sim_outcomes_bb):
    """ generates validation graphs: BMI differences by year """

    # plot
    f, axes = plt.subplots(1, 2, figsize=(7, 4), sharey=True)

    f.suptitle('Differences in Average BMI by Year')
    add_yearly_change_in_bmi_to_ax(ax=axes[0], sim_outcomes=sim_outcomes_control,
                                   intervention=D.Interventions.CONTROL)
    add_yearly_change_in_bmi_to_ax(ax=axes[1], sim_outcomes=sim_outcomes_bb,
                                   intervention=D.Interventions.BRIGHT_BODIES)

    f.subplots_adjust(hspace=2, wspace=2)
    #f.tight_layout()

    # bbox_inches set to tight: cleans up figures
    plt.savefig("figures/RCT_validation.png", dpi=300)
    plt.show()


def plot_ave_bmi_trajs(sim_outcomes_BB, sim_outcomes_CC):
    """ plot the cohort average BMI trajectories """

    # get bmi paths for both alternatives
    bmi_paths = [
        sim_outcomes_BB.pathsOfCohortAveBMI,
        sim_outcomes_CC.pathsOfCohortAveBMI
    ]

    # graph bmi paths for both alternatives (overlay)
    Path.plot_sets_of_sample_paths(
        sets_of_sample_paths=bmi_paths,
        title='Average bmis',
        x_label='Simulation time step (year)',
        y_label='average bmi',
        legends=['Bright Bodies', 'Clinical Control'],
        color_codes=['b', 'r'],
        connect='line'
    )


def print_comparative_outcomes(sim_outcomes_BB, sim_outcomes_CC):
    """ prints comparative outcomes """

    # find difference in average BMI between interventions
    list_of_avg_BMI_diffs = []
    # find differences in average expenditure between interventions
    list_of_avg_expenditure_diffs = []
    # find differences in total expenditure between interventions
    list_of_total_expenditure_diffs = []
    # SAVINGS: find differences in individual expenditure (over 10 years) between interventions
    list_of_individual_expenditure_diffs = []

    for cohortID in range(D.N_COHORTS):
        values_cc = sim_outcomes_CC.pathsOfCohortAveBMI[cohortID].get_values()
        values_bb = sim_outcomes_BB.pathsOfCohortAveBMI[cohortID].get_values()
        diff_BMI = numpy.array(values_cc) - numpy.array(values_bb)
        list_of_avg_BMI_diffs.append(diff_BMI)

        # EXPENDITURES
        # Find Difference in Spending Per Person Per Year on Average
        expenditures_cc = sim_outcomes_CC.aveAnnualIndividualHCExpenditure[cohortID]
        expenditures_bb = sim_outcomes_BB.aveAnnualIndividualHCExpenditure[cohortID]
        diff_expenditures = numpy.array(expenditures_cc) - numpy.array(expenditures_bb)
        list_of_avg_expenditure_diffs.append(diff_expenditures)
        # Find Difference in Cohort Spending Over 10 Years
        total_exp_cc = sim_outcomes_CC.cohortHealthCareExpenditure[cohortID]
        total_exp_bb = sim_outcomes_BB.cohortHealthCareExpenditure[cohortID]
        diff_total_exp = numpy.array(total_exp_cc) - numpy.array(total_exp_bb)
        list_of_total_expenditure_diffs.append(diff_total_exp)
        # Find Differences in Spending Per Person Over 10 Years
        individual_exp_cc = sim_outcomes_CC.individualTenYearExpenditure[cohortID]
        individual_exp_bb = sim_outcomes_BB.individualTenYearExpenditure[cohortID]
        diff_individual_exp = numpy.array(individual_exp_cc) - numpy.array(individual_exp_bb)
        list_of_individual_expenditure_diffs.append(diff_individual_exp)

    # INDIVIDUAL EXPENDITURE DIFFERENCES (Total over 10 years)
    avgIndividualExpenditureDifference = Stat.SummaryStat(
        name="Average Individual Expenditure Difference over 10 Years",
        data=list_of_individual_expenditure_diffs)
    estimate_and_PI_ind_exp_diff = avgIndividualExpenditureDifference.get_formatted_mean_and_interval(interval_type='p',
                                                                                                      alpha=0.05,
                                                                                                      deci=2)
    print('Estimate/PI: Average Individual Expenditure Differences: CC-BB -->', estimate_and_PI_ind_exp_diff)

    # INDIVIDUAL EXPENDITURE DIFFERENCES (Average over 10 years)
    avgIndividualExpenditureDifferenceAnnual = Stat.SummaryStat(
        name="Average Annual Individual Expenditure Difference over 10 Years",
        data=list_of_avg_expenditure_diffs)
    estimate_and_PI_ind_exp_diff_annual = avgIndividualExpenditureDifferenceAnnual.get_formatted_mean_and_interval(
        interval_type='p',
        alpha=0.05,
        deci=2)
    print('Estimate/PI: Annual Average Individual Expenditure Differences: CC-BB -->',
          estimate_and_PI_ind_exp_diff_annual)

    # TOTAL EXPENDITURE DIFFERENCES
    avgTotalExpenditureDifference = Stat.SummaryStat(
        name="Average Total Expenditure Difference over 10 Years",
        data=list_of_total_expenditure_diffs
    )
    estimate_and_PI_total_exp_diff = avgTotalExpenditureDifference.get_formatted_mean_and_interval(
        interval_type='p',
        alpha=0.05,
        deci=2
    )
    print('Estimate/PI: Average Total Expenditure Differences: CC-BB -->',
          estimate_and_PI_total_exp_diff)

    # find average differences overall
    diff_mean_BMI_y1 = []
    diff_mean_BMI_y2 = []
    # at time 1 and time 2
    for diff_mean_BMIs in list_of_avg_BMI_diffs:
        diff_mean_BMI_y1.append(diff_mean_BMIs[1])
        diff_mean_BMI_y2.append(diff_mean_BMIs[2])


def report_CEA(sim_outcomes_BB, sim_outcomes_CC):
    """ performs cost-effectiveness analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    """

    # Define Two Strategies
    # Clinical Control
    clinical_control_strategy = Econ.Strategy(
        name='Clinical Control',
        cost_obs=sim_outcomes_CC.cohortCosts,
        effect_obs=sim_outcomes_CC.effects,
        color='orange'
    )
    # Bright Bodies
    bright_bodies_strategy = Econ.Strategy(
        name='Bright Bodies',
        cost_obs=sim_outcomes_BB.cohortCosts,
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
    CEA.plot_CE_plane(x_label='Average BMI Unit Reduction (kg/m^2) per person over 10 years',
                      y_label='Average Additional Cost per person over 10 years',
                      cost_digits=0, effect_digits=1,
                      x_range=(-0.5, 3.5)
                      )

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=0.05,
        cost_digits=2,
        effect_digits=2,
        icer_digits=2,
        file_name='analysis/CETable.csv')

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


def plot_diff_in_mean_bmi(sim_outcomes_BB, sim_outcomes_CC, maintenance_effect):
    """ plot differences in BMI by intervention
    and compare to RCT data """

    # find difference in yearly average BMI between interventions
    diff_yearly_ave_bmis = []
    for cohortID in range(D.N_COHORTS):
        bmis_cc = sim_outcomes_CC.pathsOfCohortAveBMI[cohortID].get_values()
        bmis_bb = sim_outcomes_BB.pathsOfCohortAveBMI[cohortID].get_values()
        diff_yearly_ave_bmis.append(numpy.array(bmis_cc) - numpy.array(bmis_bb))

    # to produce figure
    # rct data: treatment effect at 6 mo, year 1, and 2
    bb_ys = [3.0, 3.7, 2.8]
    lower_bounds = [1, 1.1, 1.2]
    upper_bounds = [1, 1.1, 1.2]

    f, ax = plt.subplots()

    # simulates trajectories
    for ys in diff_yearly_ave_bmis:
        ax.plot(range(D.SIM_DURATION+1), ys, color='blue', alpha=0.2, label='Model')

    # bright bodies data
    ax.scatter([.5, 1, 2], bb_ys, color='orange', label='Bright Bodies RCT')
    ax.errorbar([.5, 1, 2], bb_ys, yerr=[lower_bounds, upper_bounds],
                fmt='none', capsize=4, ecolor='orange', elinewidth=2)

    ax.set_title('Treatment Effect: Difference in Average BMI')
    ax.set_xlim((0.0, 10.5))
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    ax.set_xlabel('Simulation Time (Years)')
    ax.set_ylabel('Difference in BMI (kg/m^2)')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1][:2], labels[::-1][:2], loc='upper right')

    if maintenance_effect == D.EffectMaintenance.FULL:
        plt.savefig("figures/Avg_BMI_Full_Maintenance.png", dpi=300)
    elif maintenance_effect == D.EffectMaintenance.DEPREC:
        plt.savefig("figures/Avg_BMI_Deprec_Maintenance.png", dpi=300)
    elif maintenance_effect == D.EffectMaintenance.NONE:
        plt.savefig("figures/Avg_BMI_No_Maintenance.png", dpi=300)
    plt.show()


def generate_simulation_outputs(simulated_multi_cohort):

    # sample paths for population size
    Path.plot_sample_paths(
        sample_paths=simulated_multi_cohort.multiSimOutputs.pathsOfCohortPopSize,
        title='Population Size',
        y_range=[0, 1.1 * D.POP_SIZE],
        x_label='Years'
    )

    # population pyramid at initialization
    Pyr.plot_pyramids(observed_data=Data.age_sex_dist,
                      simulated_data=simulated_multi_cohort.multiSimOutputs.popPyramidAtStart,
                      fig_size=(6, 4),
                      x_lim=10,
                      title="Cohort Pyramids at Initialization",
                      colors=('blue', 'red', 'black'),
                      y_labels=['8', '9', '10', '11', '12', '13', '14', '15', '16'],
                      age_group_width=1,
                      length_of_sim_bars=250,
                      scale_of_sim_legend=0.75,
                      transparency=0.5)
    # colors: https://www.webucator.com/blog/2015/03/python-color-constants-module/

    # sample paths for average BMIs at each time step
    Path.plot_sample_paths(
        sample_paths=simulated_multi_cohort.multiSimOutputs.pathsOfCohortAveBMI,
        title='Average BMIs for Bright Bodies',
        x_label='Simulation Year',
        y_range=[0, 40],
        connect='line'  # line graph (vs. step wise)
    )

    output = simulated_multi_cohort.multiSimOutputs
    print('Average BMI over the simulation period:',
          output.statEffect.get_formatted_mean_and_interval(interval_type='p', deci=2))
    print()
    print('Total cohort cost:',
          output.statCohortCost.get_formatted_mean_and_interval(interval_type='p', deci=1, form=','))
    print('Total cohort intervention cost:',
          output.statCohortInterventionCost.get_formatted_mean_and_interval(interval_type='p', deci=1, form=','))
    print('Total cohort health care expenditure:',
          output.statCohortHCExpenditure.get_formatted_mean_and_interval(interval_type='p', deci=1, form=','))

    # average chance in BMI with respect to the baseline (time 0)
    print()
    print('Average change in BMI at year 1 with respect to the baseline (and 95% uncertainty interval)',
          simulated_multi_cohort.multiSimOutputs.get_mean_interval_change_in_bmi(year=1, deci=1))
    print('Average change in BMI at year 2 with respect to the baseline (and 95% uncertainty interval)',
          simulated_multi_cohort.multiSimOutputs.get_mean_interval_change_in_bmi(year=2, deci=1))
