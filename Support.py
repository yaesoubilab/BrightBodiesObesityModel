import SimPy.StatisticalClasses as Stat
import SimPy.Plots.SamplePaths as Path


def print_outcomes(sim_outcomes, intervention):
    """ prints the outcomes of a simulated cohort """

    average_bmi = sum(sim_outcomes.bmiTimeStep)/len(sim_outcomes.bmiTimeStep)
    sim_outcomes.pathBMIs.record_value(time=int(sim_outcomes.simCal.time), value=average_bmi)

    print(intervention)
    print("average bmi for this time step/cohort:", average_bmi)


def plot_graphs(sim_outcomes_BB, sim_outcomes_CC):
    """ generates graphs """

    # get bmi paths for both alternatives
    bmi_paths = [
        sim_outcomes_BB.pathBMIs,
        sim_outcomes_CC.pathBMIs
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
        x=sim_outcomes_BB.bmiTimeStep,
        y_ref=sim_outcomes_CC.bmiTimeStep
    )

    estimate_CI = change_bmi.get_formatted_mean_and_interval(interval_type='c',
                                                             alpha=.05,
                                                             deci=2)
    print("change in BMI and CI:".format(1-0.05, prec=0), estimate_CI)









