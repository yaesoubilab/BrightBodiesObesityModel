import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import Support
import SimPy.Plots.SamplePaths as Path

# SIMULATE BOTH INTERVENTIONS AND PRINT COMPARATIVE OUTCOMES

# for MultiCohort BRIGHT BODIES
multiCohortBB = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    intervention=D.Interventions.BRIGHT_BODIES
    #parameters=P.Parameters(intervention=D.Interventions.BRIGHT_BODIES)
)
# simulate these cohorts (BB)
multiCohortBB.simulate()

# for MultiCohort CLINICAL CONTROL
multiCohortCC = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    intervention=D.Interventions.CONTROL
    #parameters=P.Parameters(intervention=D.Interventions.CONTROL)
)
# simulate these cohorts (CC)
multiCohortCC.simulate()

# COMPARATIVE: average BMIs over 10 years
Path.graph_sets_of_sample_paths(
    sets_of_sample_paths=[multiCohortCC.multiSimOutputs.pathOfBMIs, multiCohortBB.multiSimOutputs.pathOfBMIs],
    title='Average BMIs over 10 Years',
    y_range=[0, 40],
    x_label='Simulation Year',
    legends=['Control', 'Bright Bodies'],
    connect='line',
    color_codes=['red', 'blue'],
    transparency=0.5
)

Support.print_comparative_outcomes(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                                   sim_outcomes_CC=multiCohortCC.multiSimOutputs)

# plot RCT validation: BMI differences (year 0/1 and 1/2)
Support.plot_rct_validation(sim_outcomes=multiCohortBB.multiSimOutputs, intervention=D.Interventions.BRIGHT_BODIES)
Support.plot_rct_validation(sim_outcomes=multiCohortCC.multiSimOutputs, intervention=D.Interventions.CONTROL)

# report cost-effectiveness analysis
Support.report_CEA(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                   sim_outcomes_CC=multiCohortCC.multiSimOutputs)

Support.plot_bmi_figure(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                        sim_outcomes_CC=multiCohortCC.multiSimOutputs)

