import ModelEntities as Cls
import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import SimPy.Plots.SamplePaths as Path
import SimPy.Plots.FigSupport as Fig
from SimPy.Plots import PopulationPyramids as Pyr
import Support as Support


# create a cohort with parameters
myCohort = Cls.Cohort(id=1, parameters=P.Parameters())

# simulate the cohort for given simulation duration
myCohort.simulate(sim_duration=D.SIM_DURATION)

# sample path for population size
Path.graph_sample_path(
    sample_path=myCohort.simOutputs.pathPopSize,
    title='Population size',
    x_label='Years',
)

# print trace
myCohort.print_trace()

# print pyramids
Support.plot_pyramids(sim_outcomes=myCohort.simOutputs)

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
    title='Population sizes',
    x_label='Years'
)

# # plot pyramids from all cohorts
# for pyramids in multiCohort.multiSimOutputs.pyramids:
#     Support.plot_pyramids(sim_outcomes=myCohort.simOutputs)
#

# Support.plot_cohort_pyramids(sim_outcomes=multiCohort.multiSimOutputs)
Pyr.plot_pyramids(observed_data=D.rows,
                  simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesStart,
                  x_lim=10,
                  title="Cohort Pyramids at time 0.1")
Pyr.plot_pyramids(observed_data=D.rows,
                  simulated_data=multiCohort.multiSimOutputs.pyramidPercentagesEnd,
                  x_lim=10,
                  title="Cohort Pyramids at time 1")
