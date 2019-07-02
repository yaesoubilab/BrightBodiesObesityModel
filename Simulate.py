import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import SimPy.Plots.SamplePaths as Path
from SimPy.Plots import PopulationPyramids as Pyr
import ModelEntities as Cls
import SimPy.Plots.FigSupport as Fig

# NEW
intervention_BB = D.Interventions.BRIGHT_BODIES
intervention_CC = D.Interventions.CLINICAL_CONTROL

# Cohort
cohortBrightBodies = Cls.Cohort(id=1,
                                parameters=P.Parameters(intervention=intervention_BB))
cohortClinicalControl = Cls.Cohort(id=2,
                                   parameters=P.Parameters(intervention=intervention_CC))
cohortBrightBodies.simulate(sim_duration=D.SIM_DURATION)
cohortClinicalControl.simulate(sim_duration=D.SIM_DURATION)


# for MultiCohort BRIGHT BODIES
multiCohortBB = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    parameters=P.Parameters(intervention=intervention_BB)
)
# simulate these cohorts (BB)
multiCohortBB.simulate()

# for MultiCohort CLINICAL CONTROL
multiCohortCC = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    parameters=P.Parameters(intervention=intervention_CC)
)
# simulate these cohorts (CC)
multiCohortCC.simulate()

# sample paths for population size
Path.graph_sample_paths(
    sample_paths=multiCohortBB.multiSimOutputs.pathPopSizes,
    title='Population Size',
    y_range=[0, 1.1*D.POP_SIZE],
    x_label='Years'
)

# sample paths for average BMIs at each time step
Path.graph_sample_paths(
    sample_paths=multiCohortBB.multiSimOutputs.pathOfBMIs,
    title='Average BMIs for Bright Bodies',
    x_label='Simulation Year',
    y_range=[0, 40],
    connect='line'  # line graph (vs. step wise)
)
Path.graph_sample_paths(
    sample_paths=multiCohortCC.multiSimOutputs.pathOfBMIs,
    title='Average BMIs for Clinical Control',
    x_label='Simulation Year',
    y_range=[0, 40],
    connect='line'  # line graph (vs. step wise)
)


# PYRAMID (cohort with characteristics (age/sex) to match Bright Bodies) - at Initialization
Pyr.plot_pyramids(observed_data=D.age_sex_dist,
                  simulated_data=multiCohortBB.multiSimOutputs.pyramidPercentagesStart,
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

