import os
import InputData as D
from source import Support as S, MultiCohortClasses as MultiCls

# SIMULATE ONE INTERVENTION UNDER A GIVEN SCENARIO OF EFFECT MAINTENANCE
INTERVENTION = D.Interventions.BRIGHT_BODIES
EFFECT_MAINTENANCE = D.EffectMaintenance.NONE

# this line is needed to avoid errors that occur on Windows computers when running the model in parallel
if __name__ == '__main__':

    # change the working directory to the root directory
    os.chdir('../')

    # create a multi-cohort for the specified intervention and maintenance effect
    multiCohort = MultiCls.MultiCohort(
        ids=range(D.N_COHORTS),
        intervention=INTERVENTION,
        maintenance_scenario=EFFECT_MAINTENANCE
    )
    # simulate cohorts
    multiCohort.simulate(sim_duration=D.SIM_DURATION,
                         if_run_in_parallel=False)

    # produce simulation outputs
    S.generate_simulation_outputs(simulated_multi_cohort=multiCohort)

