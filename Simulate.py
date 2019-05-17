import ModelEntities as Cls
import InputData as D
import ModelParameters as P
import SimPy.SamplePathClasses as Path
import SimPy.FigureSupport as Fig

# create a cohort
myCohort = Cls.Cohort(id=1, parameters=P.Parameters())

# simulate the cohort
myCohort.simulate(sim_duration=D.SIM_DURATION)

# sample path for patients waiting
Path.graph_sample_path(
    sample_path=myCohort.simOutputs.pathPopSize,
    title='Population size',
    x_label='Years',
)

# print trace
myCohort.print_trace()
