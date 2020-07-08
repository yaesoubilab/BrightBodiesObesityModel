import SimPy.Plots.SamplePaths as Path
from SimPy.Plots import PopulationPyramids as Pyr


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


def generate_simulation_outputs(simulated_multi_cohort, age_sex_dist, pyramid_x_max=10):

    # sample paths for population size
    Path.plot_sample_paths(
        sample_paths=simulated_multi_cohort.multiSimOutputs.pathsOfCohortPopSize,
        title='Population Size',
        #y_range=[0, 1.1 * len(D.],
        x_label='Years'
    )

    # find lables of age groups
    age_labels = []
    for i in range(0, len(age_sex_dist), 2):
        age_labels.append(age_sex_dist[i][0])

    # population pyramid at initialization
    Pyr.plot_pyramids(observed_data=age_sex_dist,
                      simulated_data=simulated_multi_cohort.multiSimOutputs.popPyramidAtStart,
                      fig_size=(6, 4),
                      x_lim=pyramid_x_max,
                      title="Cohort Pyramids at Initialization",
                      colors=('blue', 'red', 'black'),
                      y_labels=age_labels,
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
