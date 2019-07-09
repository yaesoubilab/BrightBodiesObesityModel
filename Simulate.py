import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P


# for MultiCohort BRIGHT BODIES
multiCohortBB = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    parameters=P.Parameters(intervention=D.Interventions.BRIGHT_BODIES)
)
# simulate these cohorts (BB)
multiCohortBB.simulate()

# for MultiCohort CLINICAL CONTROL
multiCohortCC = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    parameters=P.Parameters(intervention=D.Interventions.CONTROL)
)
# simulate these cohorts (CC)
multiCohortCC.simulate()
