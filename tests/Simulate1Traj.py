from analysis import InputData as D
import SimPy.Plots.SamplePaths as Path
from yom import ModelInputs as P, ModelEntities as Cls

# create a cohort with parameters
myCohort = Cls.Cohort(id=1, parameters=P.Parameters())

# simulate the cohort for given simulation duration
myCohort.simulate(sim_duration=D.simDuration)

# sample path for population size
Path.graph_sample_path(
    sample_path=myCohort.simOutputs.pathPopSize,
    title='Population size',
    x_label='Years',
)

# print trace
myCohort.print_trace()
