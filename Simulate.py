import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import SimPy.Plots.SamplePaths as Path
from SimPy.Plots import PopulationPyramids as Pyr

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
    x_label='Simulation Year',
    connect='line'  # line graph (vs. step wise)
)

# PYRAMID (cohort with characteristics (age/sex) to match Bright Bodies) - at Initialization
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

# Colors: https://www.webucator.com/blog/2015/03/python-color-constants-module/

# Example: Pyramid Plot (for other sim years)
# Pyr.plot_pyramids(observed_data=D.rows,
#                   simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesStart,
#                   x_lim=10,
#                   title="   Cohort Pyramids at Year {}".format(D.SIM_DURATION),
#                   colors=('blue', 'red', 'black'),
#                   length_of_sim_bars=100,
#                   scale_of_sim_legend=1,
#                   transparency=0.5)







