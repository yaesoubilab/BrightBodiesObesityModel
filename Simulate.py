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


# TODO: you can choose colors from here: https://www.webucator.com/blog/2015/03/python-color-constants-module/
Pyr.plot_pyramids(observed_data=D.rows,
                  simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesStart,
                  x_lim=10,
                  title="   Cohort Pyramids at the Initialization",
                  colors=('blue', 'red', 'black'),
                  length_of_sim_bars=100,
                  scale_of_sim_legend=1,
                  transparency=0.5)
Pyr.plot_pyramids(observed_data=D.rows,
                  simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesEnd,
                  x_lim=10,
                  title="   Cohort Pyramids at Year {}".format(D.SIM_DURATION),
                  colors=('blue', 'red', 'black'),
                  length_of_sim_bars=100,
                  scale_of_sim_legend=1,
                  transparency=0.5)
