import SimPy.StatisticalClasses as Stat
import SimPy.Plots.SamplePaths as Path
import SimPy.EconEval as Econ
import InputData as D
import numpy
import Simulate as Sim


def print_outcomes(sim_outcomes, intervention):
    """ prints the outcomes of a simulated cohort """


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

    # find difference in BMI between interventions
    list_of_diff_mean_BMIs = []
    for cohortID in range(D.N_COHORTS):
        values_cc = sim_outcomes_CC.pathOfBMIs[cohortID].get_values()
        # effect = sum(values_cc)
        # print(values_control)
        values_bb = sim_outcomes_BB.pathOfBMIs[cohortID].get_values()
        # print(values_bright_bodies)
        diff_BMI = numpy.array(values_cc) - numpy.array(values_bb)
        list_of_diff_mean_BMIs.append(diff_BMI)
    print('BMI Differences: Clinical Control v Bright Bodies -->', list_of_diff_mean_BMIs)
    # print('effect=', effect)

    # find average differences overall
    diff_mean_BMI_y1 = []
    diff_mean_BMI_y2 = []
    # at time 1 and time 2
    for diff_mean_BMIs in list_of_diff_mean_BMIs:
        diff_mean_BMI_y1.append(diff_mean_BMIs[1])
        diff_mean_BMI_y2.append(diff_mean_BMIs[2])
    print("BB v. Control: Average BMI difference at Time 1:", sum(diff_mean_BMI_y1) / len(diff_mean_BMI_y1))
    print("BB v. Control: Average BMI difference at Time 2:", sum(diff_mean_BMI_y2) / len(diff_mean_BMI_y2))


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
        if_paired=True
    )

    # show the cost-effectiveness plane
    CEA.show_CE_plane()

    # show the cost-effectiveness plane
    # show_ce_figure(CEA=CEA)

    # # report the CE table
    # CEA.build_CE_table(
    #     interval_type='c',
    #     alpha=0.05,
    #     cost_digits=0,
    #     effect_digits=2,
    #     icer_digits=2)
