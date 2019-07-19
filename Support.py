import SimPy.StatisticalClasses as Stat
import SimPy.Plots.SamplePaths as Path
import SimPy.EconEval as Econ
import InputData as D
import numpy
import Simulate as Sim


def print_outcomes(sim_outcomes, intervention):
    """ prints the outcomes of a simulated cohort """

    # to retrieve lists of average BMIs by cohort
    # and find difference in BMI between
    diffs = []
    # year 1 vs 0
    year_one_v_zero_control = []
    year_one_v_zero_bb = []
    # year 2 vs 1
    year_two_v_one_control = []
    year_two_v_one_bb = []

    for cohortID in range(D.N_COHORTS):
        values_control = Sim.multiCohortCC.multiSimOutputs.pathOfBMIs[cohortID].get_values()
        # print(values_control)
        values_bright_bodies = Sim.multiCohortBB.multiSimOutputs.pathOfBMIs[cohortID].get_values()
        # print(values_bright_bodies)
        difference_bmi = numpy.array(values_control) - numpy.array(values_bright_bodies)
        diffs.append(difference_bmi)

        # year 1 minus year 0
        year_1_v_0_control = values_control[1] - values_control[0]
        year_one_v_zero_control.append(year_1_v_0_control)
        year_1_v_0_bb = values_bright_bodies[1] - values_bright_bodies[0]
        year_one_v_zero_bb.append(year_1_v_0_bb)

        # year 2 minus year 1
        year_2_v_1_control = values_control[2] - values_control[1]
        year_two_v_one_control.append(year_2_v_1_control)
        year_2_v_1_bb = values_bright_bodies[2] - values_bright_bodies[1]
        year_two_v_one_bb.append(year_2_v_1_bb)

    print('BMI Differences: Control v BB -->', diffs)
    print('Control: BMI change y1 - y0 -->', year_one_v_zero_control)
    print('BB: BMI change y1 - y0 -->', year_one_v_zero_bb)
    print('Control: BMI change y2 - y1 -->', year_two_v_one_control)
    print('BB: BMI change y2 - y1 -->', year_two_v_one_bb)
    # find average change between year 0 and 1
    avg_control_year_0_1 = sum(year_one_v_zero_control)/len(year_one_v_zero_control)
    avg_bb_year_0_1 = sum(year_one_v_zero_bb)/len(year_one_v_zero_bb)
    print('Control: Average change in BMI between Y1 and Y0:', avg_control_year_0_1)
    print('BB: Average change in BMI between Y1 and Y0:', avg_bb_year_0_1)
    # find average change between year 1 and 2
    avg_control_year_1_2 = sum(year_two_v_one_control)/len(year_two_v_one_control)
    avg_bb_year_1_2 = sum(year_two_v_one_bb)/len(year_two_v_one_bb)
    print('Control: Average change in BMI between Y2 and Y1:', avg_control_year_1_2)
    print('BB: Average change in BMI between Y2 and Y1:', avg_bb_year_1_2)

    # find average differences overall
    average_diff_1 = []
    average_diff_2 = []
    # at time 1
    for diff in diffs:
        time_1_bmi_diff = diff[1]
        time_2_bmi_diff = diff[2]
        average_diff_1.append(time_1_bmi_diff)
        average_diff_2.append(time_2_bmi_diff)
    print("BB v. Control: Average BMI difference at Time 1:", sum(average_diff_1)/len(average_diff_1))
    print("BB v. Control: Average BMI difference at Time 2:", sum(average_diff_2)/len(average_diff_2))


def plot_graphs(sim_outcomes_BB, sim_outcomes_CC):
    """ generates graphs """

    # get bmi paths for both alternatives
    bmi_paths = [
        sim_outcomes_BB.pathOfBMIs,
        sim_outcomes_CC.pathOfBMIs
    ]

    # graph bmi paths for both alternatives (overlay)
    Path.graph_sets_of_sample_paths(
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

    change_bmi = Stat.DifferenceStatIndp(
        name='Change in average BMI',
        x=sim_outcomes_BB.pathOfBMIs,
        y_ref=sim_outcomes_CC.pathOfBMIs
    )
    print(change_bmi)


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
        color='green'
    )
    # Bright Bodies
    bright_bodies_strategy = Econ.Strategy(
        name='Bright Bodies',
        cost_obs=sim_outcomes_BB.costs,
        effect_obs=sim_outcomes_BB.effects,
        color='red'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[clinical_control_strategy, bright_bodies_strategy],
        if_paired=False
    )

    # # show the cost-effectiveness plane
    # show_ce_figure(CEA=CEA)
    #
    # # report the CE table
    # CEA.build_CE_table(
    #     interval_type='c',
    #     alpha=0.05,
    #     cost_digits=0,
    #     effect_digits=2,
    #     icer_digits=2)
