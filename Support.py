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
        # Pyr.plot_pyramids(observed_data=D.rows,
        #                   simulated_data=[pyramid.get_percentages()],
        #                   x_lim=10,
        #                   title=pyramid.name)

        Pyr.plot_pyramids(observed_data=D.age_sex_dist,
                          simulated_data=[pyramid.get_percentages()],
                          fig_size=(6, 4),
                          x_lim=10,
                          title='Population Pyramid',
                          colors=('blue', 'red', 'black'),
                          y_labels=['8', '9', '10', '11', '12', '13', '14', '15', '16'],
                          age_group_width=1,
                          length_of_sim_bars=750,
                          scale_of_sim_legend=0.5,
                          transparency=0.5
                          )


# def plot_cohort_pyramids(sim_outcomes):
#     """ plot cohort pyramids (overlay) """
#
#     Pyr.plot_pyramids(observed_data=D.rows,
#                       simulated_data=[MultiCls.MultiSimOutputs.pyramidPercentages],
#                       x_lim=10,
#                       title="Cohort Pyramids")


