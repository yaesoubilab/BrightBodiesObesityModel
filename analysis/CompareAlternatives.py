import os

import InputData as D
from source import Support, MultiCohortClasses as MultiCls, SamplePaths as MyPath

# SIMULATE BOTH INTERVENTIONS AND PRINT COMPARATIVE OUTCOMES

# *** Alter maintenance scenarios via MAINTENANCE_EFFECT.
MAINTENANCE_EFFECT = D.EffectMaintenance.DEPREC

# change the working directory to the root directory
os.chdir('../')

# for MultiCohort BRIGHT BODIES
multiCohortBB = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    intervention=D.Interventions.BRIGHT_BODIES,
    maintenance_scenario=MAINTENANCE_EFFECT
)
# simulate these cohorts (BB)
multiCohortBB.simulate(D.SIM_DURATION)

# for MultiCohort CLINICAL CONTROL
multiCohortCC = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    intervention=D.Interventions.CONTROL,
    maintenance_scenario=MAINTENANCE_EFFECT
)
# simulate these cohorts (CC)
multiCohortCC.simulate(D.SIM_DURATION)

# COMPARATIVE: average BMIs over 10 years
MyPath.plot_sets_of_sample_paths(
    sets_of_sample_paths=[multiCohortCC.multiSimOutputs.pathsOfCohortAveBMI,
                          multiCohortBB.multiSimOutputs.pathsOfCohortAveBMI],
    title='Cohort Average BMIs over 10 Years',
    y_range=[0, 40],
    x_label='Simulation Year',
    y_label='Average BMI (kg/m^2)',
    legends=['Model: Clinical Control', 'Model: Bright Bodies'],
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


# plot RCT validation: BMI differences (year 0/1 and 1/2)
Support.plot_validation(sim_outcomes_control=multiCohortCC.multiSimOutputs,
                        sim_outcomes_bb=multiCohortBB.multiSimOutputs)

# report cost-effectiveness analysis
Support.report_CEA(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                   sim_outcomes_CC=multiCohortCC.multiSimOutputs)

Support.plot_diff_in_mean_bmi(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                              sim_outcomes_CC=multiCohortCC.multiSimOutputs,
                              maintenance_effect=MAINTENANCE_EFFECT)

