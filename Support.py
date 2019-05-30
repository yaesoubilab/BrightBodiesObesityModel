from SimPy.Plots import PopulationPyramids as Pyr
import InputData as D
import ModelOutputs as O
import MultiCohortClasses as MultiCls


def plot_pyramids(sim_outcomes):
    """
    plot pyramid: population distribution by age/sex
    :param sim_outcomes: outcomes of simulated cohort
    """

    for pyramid in sim_outcomes.pyramids:

        # print time of test
        print(pyramid.name)
        # get the total population size
        print('Population size:', pyramid.get_sum())
        # get the size of each group
        print('Population size by age, sex:', pyramid.get_values())
        # get the percentage of population in each group
        print('Population distribution by age, sex', pyramid.get_percentages())

        # plot the pyramid
        Pyr.plot_pyramids(observed_data=D.rows,
                          simulated_data=[pyramid.get_percentages()],
                          x_lim=10,
                          title=pyramid.name)


# def plot_cohort_pyramids(sim_outcomes):
#     """ plot cohort pyramids (overlay) """
#
#     Pyr.plot_pyramids(observed_data=D.rows,
#                       simulated_data=[MultiCls.MultiSimOutputs.pyramidPercentages],
#                       x_lim=10,
#                       title="Cohort Pyramids")


