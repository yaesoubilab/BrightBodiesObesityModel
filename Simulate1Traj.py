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