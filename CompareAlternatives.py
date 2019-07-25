import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import Support
import SimPy.Plots.SamplePaths as Path
import numpy

# SIMULATE BOTH INTERVENTIONS AND PRINT COMPARATIVE OUTCOMES

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

# find difference in BMI between interventions
diffs = []
for cohortID in range(D.N_COHORTS):
    values_cc = multiCohortCC.multiSimOutputs.pathOfBMIs[cohortID].get_values()
    # effect = sum(values_cc)
    # print(values_control)
    values_bb = multiCohortBB.multiSimOutputs.pathOfBMIs[cohortID].get_values()
    # print(values_bright_bodies)
    difference_bmi = numpy.array(values_cc) - numpy.array(values_bb)
    diffs.append(difference_bmi)
print('BMI Differences: Clinical Control v Bright Bodies -->', diffs)
# print('effect=', effect)

# find average differences overall
average_diff_1 = []
average_diff_2 = []
# at time 1 and time 2
for diff in diffs:
    time_1_bmi_diff = diff[1]
    time_2_bmi_diff = diff[2]
    average_diff_1.append(time_1_bmi_diff)
    average_diff_2.append(time_2_bmi_diff)
print("BB v. Control: Average BMI difference at Time 1:", sum(average_diff_1)/len(average_diff_1))
print("BB v. Control: Average BMI difference at Time 2:", sum(average_diff_2)/len(average_diff_2))


# print outcomes
# Support.print_outcomes(sim_outcomes=multiCohortBB.multiSimOutputs, intervention=D.Interventions.BRIGHT_BODIES)
# Support.print_outcomes(sim_outcomes=multiCohortCC.multiSimOutputs, intervention=D.Interventions.CONTROL)
#
# # print comparative outcomes
# # Support.print_comparative_outcomes(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
# #                                    sim_outcomes_CC=multiCohortCC.multiSimOutputs)
#
# # plot graphs
# Support.plot_graphs(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
#                     sim_outcomes_CC=multiCohortCC.multiSimOutputs)

# report cost-effectiveness analysis
Support.report_CEA(sim_outcomes_BB=multiCohortBB.multiSimOutputs,
                   sim_outcomes_CC=multiCohortCC.multiSimOutputs)
