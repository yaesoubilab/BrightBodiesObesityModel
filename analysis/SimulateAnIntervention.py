import os
from support.ParameterGenerator import ParamGenerator
import support.Inputs as I
import yom.ModelInputs as yomI
import yom.MultiCohortClasses as MultiCls
import yom.OutputAnalysis as yomS

# SIMULATE ONE INTERVENTION UNDER A GIVEN SCENARIO OF EFFECT MAINTENANCE
INTERVENTION = I.Interventions.BRIGHT_BODIES
EFFECT_MAINTENANCE = I.EffectMaintenance.NONE

# this line is needed to avoid errors that occur on Windows computers when running the model in parallel
if __name__ == '__main__':

    # change the working directory to the root directory
    os.chdir('../')

    # create an instance of the model inputs
    inputs = I.ModelInputs()

    # create a multi-cohort for the specified intervention and maintenance effect
    multiCohort = MultiCls.MultiCohort(
        ids=range(inputs.nCohorts),
        parameter_generator=ParamGenerator(
            intervention=INTERVENTION,
            maintenance_scenario=EFFECT_MAINTENANCE.NONE,
            model_inputs=inputs)
    )
    # simulate cohorts
    multiCohort.simulate(sim_duration=inputs.simDuration,
                         if_run_in_parallel=False)

    # produce simulation outputs
    yomS.generate_simulation_outputs(simulated_multi_cohort=multiCohort,
                                     age_sex_dist=inputs.ageSexDist)

