import SimPy.Plots.SamplePaths as Path
import SimPy.EconEval as Econ
import InputData as D
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import SimPy.StatisticalClasses as Stat


# TODO: it seems you are not using this method. If so, please delete.
def print_outcomes(sim_outcomes, intervention):
    """ prints the outcomes of a simulated cohort """

    # year 1 vs 0
    year_one_v_zero = []
    # year 2 vs 1
    year_two_v_one = []

    # CONTROL VALIDATION
    for cohortID in range(D.N_COHORTS):
        values = sim_outcomes.pathsOfBMIs[cohortID].get_values()
        # FOR YEAR SPECIFIC COMPARISONS
        # year 1 minus year 0
        year_1_v_0 = values[1] - values[0]
        year_one_v_zero.append(year_1_v_0)
        # year 2 minus year 1
        year_2_v_1 = values[2] - values[1]
        year_two_v_one.append(year_2_v_1)

    # print(intervention, 'BMI change y1 - y0 -->', year_one_v_zero)
    # print(intervention, 'BMI change y2 - y1 -->', year_two_v_one)


def plot_validation(sim_outcomes, intervention):
    """ generates validation graphs: BMI differences by year """

    # BMI difference by year
    year_one_vs_zero = []
    year_two_vs_one = []

    for cohortID in range(D.N_COHORTS):
        bmi_values = sim_outcomes.pathsOfBMIs[cohortID].get_values()

        # year 1 minus year 0
        year_one_vs_zero.append(bmi_values[1] - bmi_values[0])
        # year 2 minus year 1
        year_two_vs_one.append(bmi_values[2] - bmi_values[1])

    # find average change between year 0 and 1
    year1v0SummStat = Stat.SummaryStat(name="Average change in BMI between year 0 and 1",
                                          data=year_one_vs_zero)
    aveYear1vs0 = year1v0SummStat.get_mean()

    # find average change between year 1 and 2
    tear2v1SummStat = Stat.SummaryStat(name="Average change in BMI between year 0 and 1",
                                          data=year_two_vs_one)
    aveYear2vs1 = tear2v1SummStat.get_mean()

    # estimates from Bright Bodies RCT for the control
    rct_control_year_diffs = [1.9, 0.0]
    rct_control_year_diffs_lb = [.7, .8]
    rct_control_year_diffs_ub = [.6, .8]
    # estimates from Bright Bodies RCT for Bright Bodies
    rct_bb_year_diffs = [-1.8, 0.9]
    rct_bb_year_diffs_lb = [.8, 1.0]
    rct_bb_year_diffs_ub = [.9, 1.0]

    # plot
    f, ax = plt.subplots(figsize=(5, 5))

    if intervention == D.Interventions.BRIGHT_BODIES:
        ys = rct_bb_year_diffs
        lbs = rct_bb_year_diffs_lb
        ubs = rct_bb_year_diffs_ub
        ax.set_title('Differences in Average BMI by Year\nunder Bright Bodies')
    else:
        ys = rct_control_year_diffs
        lbs = rct_control_year_diffs_lb
        ubs = rct_control_year_diffs_ub
        ax.set_title('Differences in Average BMI by Year\nunder Control')

    # adding RCT data
    ax.scatter([1, 2], ys, color='black', label="RCT Average Difference in BMI")
    # adding error bars
    ax.errorbar([1, 2], ys, yerr=(lbs, ubs), fmt='none', capsize=4, ecolor='black')

    # adding simulation outcomes
    for this_y in year_one_vs_zero:
        ax.scatter(1, this_y, color='blue', marker='_', s=200, alpha=0.25)
    for this_y in year_two_vs_one:
        ax.scatter(2, this_y, color='blue', marker='_', s=200, alpha=0.25)

    plt.xlim((0.5, 2.5))
    ticks = [1, 2]
    plt.xticks(ticks, labels=['Year 0 to 1', 'Year 1 to 2'])
    plt.yticks([-3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    plt.xlabel('Sim Years')
    plt.ylabel('Difference in BMI (kg/m^2)')

    plt.legend(['Bright Bodies RCT', 'Model'], loc='upper right')
    # to save plotted figures
    # bbox_inches set to tight: cleans up figures
    plt.savefig("Figures/RCT_validation.png", dpi=300)


def plot_graphs(sim_outcomes_BB, sim_outcomes_CC):
    """ generates graphs """

    # get bmi paths for both alternatives
    bmi_paths = [
        sim_outcomes_BB.pathsOfBMIs,
        sim_outcomes_CC.pathsOfBMIs
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

    # find difference in BMI between interventions
    list_of_diff_mean_BMIs = []
    # find differences in expenditures between interventions
    list_of_diff_mean_expenditures = []
    # find differences in total expenditure between interventions
    list_of_diff_total_expenditures = []
    # SAVINGS: find differences in individual expenditure (over 10 years) between interventions
    list_of_diff_individual_expenditure = []

    for cohortID in range(D.N_COHORTS):
        values_cc = sim_outcomes_CC.pathsOfBMIs[cohortID].get_values()
        values_bb = sim_outcomes_BB.pathsOfBMIs[cohortID].get_values()
        diff_BMI = numpy.array(values_cc) - numpy.array(values_bb)
        list_of_diff_mean_BMIs.append(diff_BMI)

        # EXPENDITURES
        # Find Difference in Spending Per Person Per Year on Average
        expenditures_cc = sim_outcomes_CC.expenditures[cohortID]
        expenditures_bb = sim_outcomes_BB.expenditures[cohortID]
        diff_expenditures = numpy.array(expenditures_cc) - numpy.array(expenditures_bb)
        list_of_diff_mean_expenditures.append(diff_expenditures)
        # Find Difference in Total Spending Over 10 Years
        total_exp_cc = sim_outcomes_CC.totalExpenditures[cohortID]
        total_exp_bb = sim_outcomes_BB.totalExpenditures[cohortID]
        diff_total_exp = numpy.array(total_exp_cc) - numpy.array(total_exp_bb)
        list_of_diff_total_expenditures.append(diff_total_exp)
        # Find Differences in Spending Per Person Over 10 Years
        individual_exp_cc = sim_outcomes_CC.individualTotalExpenditure[cohortID]
        individual_exp_bb = sim_outcomes_BB.individualTotalExpenditure[cohortID]
        diff_individual_exp = numpy.array(individual_exp_cc) - numpy.array(individual_exp_bb)
        list_of_diff_individual_expenditure.append(diff_individual_exp)

    # print('BMI Differences: Clinical Control v Bright Bodies -->', list_of_diff_mean_BMIs)
    # print('Average Expenditure Differences: Clinical Control - Bright Bodies -->', list_of_diff_mean_expenditures)
    # print('Total Expenditure Differences: CC - BB -->', list_of_diff_total_expenditures)
    # print('Individual Expenditure Differences over 10year: CC - BB -->', list_of_diff_individual_expenditure)

    # AVERAGE FOR ALL SIMULATIONS:
    # print('SIM: Average Expenditure Difference: CC - BB -->', (sum(list_of_diff_mean_expenditures)/D.N_COHORTS))
    # print('SIM: Total Expenditure Differences: CC - BB -->', (sum(list_of_diff_total_expenditures)/D.N_COHORTS))
    # print('SIM: Individual Expenditure Differences: CC - BB -->', (sum(list_of_diff_individual_expenditure)/D.N_COHORTS))

    # INDIVIDUAL EXPENDITURE DIFFERENCES (Total over 10 years)
    avgIndividualExpenditureDifference = Stat.SummaryStat(
        name="Average Individual Expenditure Difference over 10 Years",
        data=list_of_diff_individual_expenditure)
    estimate_and_PI_ind_exp_diff = avgIndividualExpenditureDifference.get_formatted_mean_and_interval(interval_type='p',
                                                                                                      alpha=0.05,
                                                                                                      deci=2)
    print('Estimate/PI: Average Individual Expenditure Differences: CC-BB -->', estimate_and_PI_ind_exp_diff)

    # INDIVIDUAL EXPENDITURE DIFFERENCES (Average over 10 years)
    avgIndividualExpenditureDifferenceAnnual = Stat.SummaryStat(
        name="Average Annual Individual Expenditure Difference over 10 Years",
        data=list_of_diff_mean_expenditures)
    estimate_and_PI_ind_exp_diff_annual = avgIndividualExpenditureDifferenceAnnual.get_formatted_mean_and_interval(
        interval_type='p',
        alpha=0.05,
        deci=2)
    print('Estimate/PI: Annual Average Individual Expenditure Differences: CC-BB -->',
          estimate_and_PI_ind_exp_diff_annual)

    # TOTAL EXPENDITURE DIFFERENCES
    avgTotalExpenditureDifference = Stat.SummaryStat(
        name="Average Total Expenditure Difference over 10 Years",
        data=list_of_diff_total_expenditures
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
    for diff_mean_BMIs in list_of_diff_mean_BMIs:
        diff_mean_BMI_y1.append(diff_mean_BMIs[1])
        diff_mean_BMI_y2.append(diff_mean_BMIs[2])
    # print("BB v. Control: Average BMI difference at Time 1:", sum(diff_mean_BMI_y1) / len(diff_mean_BMI_y1))
    # print("BB v. Control: Average BMI difference at Time 2:", sum(diff_mean_BMI_y2) / len(diff_mean_BMI_y2))


def report_CEA(sim_outcomes_BB, sim_outcomes_CC):
    """ performs cost-effectiveness analysis
    :param sim_outcomes_BB: outcomes of a cohort simulated under Bright Bodies
    :param sim_outcomes_CC: outcomes of a cohort simulated under Clinical Control
    """

    # Define Two Strategies
    # Clinical Control
    clinical_control_strategy = Econ.Strategy(
        name='Clinical Control',
        cost_obs=sim_outcomes_CC.costs,
        effect_obs=sim_outcomes_CC.effects,
        color='orange'
    )
    # Bright Bodies
    bright_bodies_strategy = Econ.Strategy(
        name='Bright Bodies',
        cost_obs=sim_outcomes_BB.costs,
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
        icer_digits=2)

    # do CBA
    CBA = Econ.CBA(
        strategies=[clinical_control_strategy, bright_bodies_strategy],
        wtp_range=[0, 1000],
        if_paired=True,
        health_measure='d'
    )
    CBA.plot_acceptability_curves(
        x_label='Willingness-to-pay threshold\n($ per BMI averted)',
        y_range=[-0.01, 1.01],
        fig_size=(4.2, 4)
    )


def plot_bmi_figure(sim_outcomes_BB, sim_outcomes_CC):
    """ plot differences in BMI by intervention
    and compare to RCT data """

    # find difference in BMI between interventions
    list_of_diff_mean_BMIs = []
    for cohortID in range(D.N_COHORTS):
        values_cc = sim_outcomes_CC.pathsOfBMIs[cohortID].get_values()
        values_bb = sim_outcomes_BB.pathsOfBMIs[cohortID].get_values()
        diff_BMI = numpy.array(values_cc) - numpy.array(values_bb)
        list_of_diff_mean_BMIs.append(diff_BMI)
    # print('BMI Differences: Clinical Control v Bright Bodies -->', list_of_diff_mean_BMIs)

    # to produce figure
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sim_ys = list_of_diff_mean_BMIs
    # rct data: treatment effect at 6 mo, year 1, and 2
    bb_ys = [3.0, 3.7, 2.8]
    lower_bounds = [1, 1.1, 1.2]
    upper_bounds = [1, 1.1, 1.2]

    f, ax = plt.subplots()

    for sim_y in sim_ys:
        ax.plot(x, sim_y, color='blue')

    # adding bright bodies data
    ax.scatter([.5, 1, 2], bb_ys, color='black')
    ax.errorbar([.5, 1, 2], bb_ys, yerr=[lower_bounds, upper_bounds], fmt='none', capsize=4, ecolor='black', elinewidth=2)

    ax.set_title('Difference in Average BMI by Intervention: No Effect Maintenance')
    plt.xlim((0.0, 10.5))
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    plt.xlabel('Simulation Time (Years)')
    plt.ylabel('Difference in BMI (kg/m^2)')
    # Show legend
    model_data_color = patch.Patch(color='blue', label='Simulation BMI Differences')
    rct_data_color = patch.Patch(color='black', label='RCT: BMI Differences')
    plt.legend(loc='upper right', handles=[model_data_color, rct_data_color])
    plt.savefig("Figures/Avg_BMI_No_Maintenance.png", dpi=300)
    plt.show()


def plot_bmi_figure_maintenance(sim_outcomes_BB, sim_outcomes_CC):
    """ plot differences in BMI by intervention
    and compare to RCT data """

    # find difference in BMI between interventions
    list_of_diff_mean_BMIs = []
    for cohortID in range(D.N_COHORTS):
        values_cc = sim_outcomes_CC.pathsOfBMIs[cohortID].get_values()
        values_bb = sim_outcomes_BB.pathsOfBMIs[cohortID].get_values()
        diff_BMI = numpy.array(values_cc) - numpy.array(values_bb)
        diff_BMI_2years = []
        diff_BMI_2years.append(diff_BMI[0])
        diff_BMI_2years.append(diff_BMI[1])
        diff_BMI_2years.append(diff_BMI[2])
        for i in range(8):
            diff_BMI_2years.append(diff_BMI[2])

        list_of_diff_mean_BMIs.append(diff_BMI_2years)
    # print('BMI Differences: Clinical Control v Bright Bodies -->', list_of_diff_mean_BMIs)

    # to produce figure
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sim_ys = list_of_diff_mean_BMIs
    # rct data: treatment effect at year 1 and 2
    bb_ys = [3.0, 3.7, 2.8]
    lower_bounds = [1, 1.1, 1.2]
    upper_bounds = [1, 1.1, 1.2]

    f, ax = plt.subplots()

    for sim_y in sim_ys:
        ax.plot(x, sim_y, color='blue')

    # adding bright bodies data
    ax.scatter([0.5, 1, 2], bb_ys, color='black', s=80)
    ax.errorbar([0.5, 1, 2], bb_ys, yerr=[lower_bounds, upper_bounds], fmt='none', capsize=4, ecolor='black', elinewidth=2)

    ax.set_title('Difference in Average BMI by Intervention: Full Maintenance of Effect ')
    plt.xlim((0.0, 10.5))
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    plt.xlabel('Simulation Time (Years)')
    plt.ylabel('Difference in BMI (kg/m^2)')
    # Show legend
    model_data_color = patch.Patch(color='blue', label='Simulation BMI Differences')
    rct_data_color = patch.Patch(color='black', label='RCT: BMI Differences')
    plt.legend(loc='upper right', handles=[model_data_color, rct_data_color])
    plt.savefig("Figures/Avg_BMI_Full_Maintenance.png", dpi=300)
    plt.show()


def plot_bmi_figure_depreciation(sim_outcomes_BB, sim_outcomes_CC):
    """ plot differences in BMI by intervention
    and compare to RCT data """

    # find difference in BMI between interventions
    list_of_diff_mean_BMIs = []
    for cohortID in range(D.N_COHORTS):
        values_cc = sim_outcomes_CC.pathsOfBMIs[cohortID].get_values()
        values_bb = sim_outcomes_BB.pathsOfBMIs[cohortID].get_values()
        diff_BMI = numpy.array(values_cc) - numpy.array(values_bb)
        diff_BMI_2years = []
        diff_BMI_2years.append(diff_BMI[0])
        diff_BMI_2years.append(diff_BMI[1])
        diff_BMI_2years.append(diff_BMI[2])
        for i in range(8):
            deprec_value = diff_BMI[2]/(10-2)
            deprec_next_value = diff_BMI[2]-(deprec_value*(i+1))
            diff_BMI_2years.append(deprec_next_value)

        list_of_diff_mean_BMIs.append(diff_BMI_2years)
    # print('BMI Differences: Clinical Control v Bright Bodies -->', list_of_diff_mean_BMIs)

    # to produce figure
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sim_ys = list_of_diff_mean_BMIs
    # rct data: treatment effect at year 1 and 2
    bb_ys = [3.0, 3.7, 2.8]
    lower_bounds = [1, 1.1, 1.2]
    upper_bounds = [1, 1.1, 1.2]

    f, ax = plt.subplots()

    for sim_y in sim_ys:
        ax.plot(x, sim_y, color='blue')

    # adding bright bodies data
    ax.scatter([0.5, 1, 2], bb_ys, color='black', s=80)
    ax.errorbar([0.5, 1, 2], bb_ys, yerr=[lower_bounds, upper_bounds], fmt='none', capsize=4, ecolor='black', elinewidth=2)

    ax.set_title('Difference in Average BMI by Intervention: Depreciation of Effect ')
    plt.xlim((0.0, 10.5))
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    plt.xlabel('Simulation Time (Years)')
    plt.ylabel('Difference in BMI (kg/m^2)')
    # Show legend
    model_data_color = patch.Patch(color='blue', label='Simulation BMI Differences')
    rct_data_color = patch.Patch(color='black', label='RCT: BMI Differences')
    plt.legend(loc='upper right', handles=[model_data_color, rct_data_color])
    plt.savefig("Figures/Avg_BMI_Deprec_Maintenance.png", dpi=300)
    plt.show()


