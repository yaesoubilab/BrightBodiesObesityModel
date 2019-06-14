import ModelEntities as Cls
import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import SimPy.Plots.SamplePaths as Path
import SimPy.Plots.FigSupport as Fig
from SimPy.Plots import PopulationPyramids as Pyr
import Support as Support

# for MultiCohort
multiCohort = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    parameters=P.Parameters()
)

# simulate all cohorts
multiCohort.simulate()

# sample paths for population size
Path.graph_sample_paths(
    sample_paths=multiCohort.multiSimOutputs.pathPopSizes,
    title='Population Size',
    x_label='Years'
)

# sample paths for average BMIs at each time step
Path.graph_sample_paths(
    sample_paths=multiCohort.multiSimOutputs.pathOfBMIs,
    title='Average BMIs',
    x_label='Sim Year',
    connect='line'
)


# # colors can be chosen from here:
# # https://www.webucator.com/blog/2015/03/python-color-constants-module/
# Pyr.plot_pyramids(observed_data=D.rows,
#                   simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesStart,
#                   x_lim=10,
#                   title="   Cohort Pyramids at the Initialization",
#                   colors=('blue', 'red', 'black'),
#                   length_of_sim_bars=100,
#                   scale_of_sim_legend=1,
#                   transparency=0.5)
# Pyr.plot_pyramids(observed_data=D.rows,
#                   simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesEnd,
#                   x_lim=10,
#                   title="   Cohort Pyramids at Year {}".format(D.SIM_DURATION),
#                   colors=('blue', 'red', 'black'),
#                   length_of_sim_bars=100,
#                   scale_of_sim_legend=1,
#                   transparency=0.5)

# NEW PYRAMIDS FOR BRIGHT BODIES AGES ONLY
# colors can be chosen from here:
# https://www.webucator.com/blog/2015/03/python-color-constants-module/
# Pyr.plot_pyramids(observed_data=D.age_sex_dist,
#                   simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesStart,
#                   x_lim=10,
#                   title="   Cohort Pyramids at the Initialization",
#                   colors=('blue', 'red', 'black'),
#                   length_of_sim_bars=100,
#                   scale_of_sim_legend=1,
#                   transparency=0.5)
# Pyr.plot_pyramids(observed_data=D.age_sex_dist,
#                   simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesEnd,
#                   x_lim=10,
#                   title="   Cohort Pyramids at Year {}".format(D.SIM_DURATION),
#                   colors=('blue', 'red', 'black'),
#                   length_of_sim_bars=100,
#                   scale_of_sim_legend=1,
#                   transparency=0.5)
# NEW PYRAMID CHARACTERISTICS TO MATCH BB
# at initialization
Pyr.plot_pyramids(observed_data=D.age_sex_dist,
                  simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesStart,
                  fig_size=(6, 4),
                  x_lim=10,
                  title="Cohort Pyramids at Initialization",
                  colors=('blue', 'red', 'black'),
                  y_labels=['8', '9', '10', '11', '12', '13', '14', '15', '16'],
                  age_group_width=1,
                  length_of_sim_bars=250,
                  scale_of_sim_legend=0.75,
                  transparency=0.5)






