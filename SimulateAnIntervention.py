import InputData as D
from source import Support as S, MultiCohortClasses as MultiCls

# SIMULATE ONE INTERVENTION UNDER A GIVEN SCENARIO OF EFFECT MAINTENANCE
INTERVENTION = D.Interventions.CONTROL
EFFECT_MAINTENANCE = D.EffectMaintenance.DEPREC

# this line is needed to avoid errors that occur on Windows computers when running the model in parallel
if __name__ == '__main__':

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

