import InputData as D
from source import ModelParameters as P, ModelEntities as Cls
import SimPy.Plots.SamplePaths as Path

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
