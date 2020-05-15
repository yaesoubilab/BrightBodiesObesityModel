import ModelEntities as Cls
import InputData as D
import ModelParameters as P

# Cohort
cohortBrightBodies = Cls.Cohort(id=1,
                                parameters=P.Parameters(intervention=D.Interventions.BRIGHT_BODIES))
cohortClinicalControl = Cls.Cohort(id=2,
                                   parameters=P.Parameters(intervention=D.Interventions.CONTROL))
cohortBrightBodies.simulate(sim_duration=D.SIM_DURATION)
cohortClinicalControl.simulate(sim_duration=D.SIM_DURATION)