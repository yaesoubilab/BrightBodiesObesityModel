import MultiCohortClasses as MultiCls
import InputData as D
import Support
import SamplePaths as MyPath

# SIMULATE BOTH INTERVENTIONS AND PRINT COMPARATIVE OUTCOMES

# for MultiCohort BRIGHT BODIES
multiCohortBB = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    intervention=D.Interventions.BRIGHT_BODIES
)
# simulate these cohorts (BB)
multiCohortBB.simulate()

# for MultiCohort CLINICAL CONTROL
multiCohortCC = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    intervention=D.Interventions.CONTROL
)
# simulate these cohorts (CC)
multiCohortCC.simulate()

# COMPARATIVE: average BMIs over 10 years
MyPath.plot_sets_of_sample_paths(
    sets_of_sample_paths=[multiCohortCC.multiSimOutputs.pathOfBMIs, multiCohortBB.multiSimOutputs.pathOfBMIs],
    title='Cohort Average BMIs over 10 Years',
    y_range=[0, 40],
    x_label='Simulation Year',
    y_label='Average BMI (kg/m^2)',
    legends=['Clinical Control Cohorts', 'Bright Bodies Cohorts'],
    connect='line',
    color_codes=['orange', 'blue'],
    transparency=0.5,
    x_points=[0.0, 0.5, 1, 2],
    y_points_bb=[35.7, 33.6, 33.9, 34.8],
    y_points_cc=[36.2, 37.1, 38.1, 38.1],
    ci_lower_values_bb=[0, 33, 33.3, 34],
    ci_upper_values_bb=[0, 34.2, 34.6, 35.6],
    ci_lower_values_cc=[0, 36.3, 37.3, 37.1],
    ci_upper_values_cc=[0, 37.9, 39, 39.1]
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

Support.plot_bmi_figure_maintenance(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                                    sim_outcomes_CC=multiCohortCC.multiSimOutputs)

Support.plot_bmi_figure_depreciation(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                                     sim_outcomes_CC=multiCohortCC.multiSimOutputs)

