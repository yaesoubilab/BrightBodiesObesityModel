import InputData as D
from yom import ModelParameters as P, ModelEntities as Cls

# Cohort
cohortBrightBodies = Cls.Cohort(id=1,
                                parameters=P.Parameters(intervention=D.Interventions.BRIGHT_BODIES))
cohortClinicalControl = Cls.Cohort(id=2,
                                   parameters=P.Parameters(intervention=D.Interventions.CONTROL))
cohortBrightBodies.simulate(sim_duration=D.SIM_DURATION)
cohortClinicalControl.simulate(sim_duration=D.SIM_DURATION)
