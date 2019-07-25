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

    # change_bmi = Stat.DifferenceStatIndp(
    #     name='Change in average BMI',
    #     x=sim_outcomes_BB.pathOfBMIs,
    #     y_ref=sim_outcomes_CC.pathOfBMIs
    # )
    # print(change_bmi)


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
