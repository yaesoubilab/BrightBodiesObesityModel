# import InputData as D
# import SimPy.Plots.SamplePaths as Path
# from SimPy.Plots import PopulationPyramids as Pyr
# import Simulate as Sim
# import numpy
#
# # SINGLE
# # sample paths for population size
# Path.graph_sample_paths(
#     sample_paths=Sim.multiCohortBB.multiSimOutputs.pathPopSizes,
#     title='Population Size',
#     y_range=[0, 1.1*D.POP_SIZE],
#     x_label='Years'
# )
#
# # COMPARATIVE
# Path.graph_sets_of_sample_paths(
#     sets_of_sample_paths=[Sim.multiCohortCC.multiSimOutputs.pathOfBMIs, Sim.multiCohortBB.multiSimOutputs.pathOfBMIs],
#     title='Average BMIs over 10 Years',
#     y_range=[0, 40],
#     x_label='Simulation Year',
#     legends=['Control', 'Bright Bodies'],
#     connect='line',
#     color_codes=['red', 'blue'],
#     transparency=0.5
# )
#
# # SINGLE
# # sample paths for average BMIs at each time step
# Path.graph_sample_paths(
#     sample_paths=Sim.multiCohortBB.multiSimOutputs.pathOfBMIs,
#     title='Average BMIs for Bright Bodies',
#     x_label='Simulation Year',
#     y_range=[0, 40],
#     connect='line'  # line graph (vs. step wise)
# )
# Path.graph_sample_paths(
#     sample_paths=Sim.multiCohortCC.multiSimOutputs.pathOfBMIs,
#     title='Average BMIs for Clinical Control',
#     x_label='Simulation Year',
#     y_range=[0, 40],
#     connect='line'  # line graph (vs. step wise)
# )
#
# # COMPARATIVE
# # to retrieve lists of average BMIs by cohort
# # and find difference in BMI between
# diffs = []
# # year 1 vs 0
# year_one_v_zero_control = []
# year_one_v_zero_bb = []
# # year 2 vs 1
# year_two_v_one_control = []
# year_two_v_one_bb = []
#
# for cohortID in range(D.N_COHORTS):
#     values_control = Sim.multiCohortCC.multiSimOutputs.pathOfBMIs[cohortID].get_values()
#     # print(values_control)
#     values_bright_bodies = Sim.multiCohortBB.multiSimOutputs.pathOfBMIs[cohortID].get_values()
#     # print(values_bright_bodies)
#     difference_bmi = numpy.array(values_control) - numpy.array(values_bright_bodies)
#     diffs.append(difference_bmi)
#
#     # year 1 minus year 0
#     year_1_v_0_control = values_control[1] - values_control[0]
#     year_one_v_zero_control.append(year_1_v_0_control)
#     year_1_v_0_bb = values_bright_bodies[1] - values_bright_bodies[0]
#     year_one_v_zero_bb.append(year_1_v_0_bb)
#
#     # year 2 minus year 1
#     year_2_v_1_control = values_control[2] - values_control[1]
#     year_two_v_one_control.append(year_2_v_1_control)
#     year_2_v_1_bb = values_bright_bodies[2] - values_bright_bodies[1]
#     year_two_v_one_bb.append(year_2_v_1_bb)
#
# print('BMI Differences: Control v BB -->', diffs)
# print('Control: BMI change y1 - y0 -->', year_one_v_zero_control)
# print('BB: BMI change y1 - y0 -->', year_one_v_zero_bb)
# print('Control: BMI change y2 - y1 -->', year_two_v_one_control)
# print('BB: BMI change y2 - y1 -->', year_two_v_one_bb)
# # find average change between year 0 and 1
# avg_control_year_0_1 = sum(year_one_v_zero_control)/len(year_one_v_zero_control)
# avg_bb_year_0_1 = sum(year_one_v_zero_bb)/len(year_one_v_zero_bb)
# print('Control: Average change in BMI between Y1 and Y0:', avg_control_year_0_1)
# print('BB: Average change in BMI between Y1 and Y0:', avg_bb_year_0_1)
# # find average change between year 1 and 2
# avg_control_year_1_2 = sum(year_two_v_one_control)/len(year_two_v_one_control)
# avg_bb_year_1_2 = sum(year_two_v_one_bb)/len(year_two_v_one_bb)
# print('Control: Average change in BMI between Y2 and Y1:', avg_control_year_1_2)
# print('BB: Average change in BMI between Y2 and Y1:', avg_bb_year_1_2)
#
# # find average differences overall
# average_diff_1 = []
# average_diff_2 = []
# # at time 1
# for diff in diffs:
#     time_1_bmi_diff = diff[1]
#     time_2_bmi_diff = diff[2]
#     average_diff_1.append(time_1_bmi_diff)
#     average_diff_2.append(time_2_bmi_diff)
# print("BB v. Control: Average BMI difference at Time 1:", sum(average_diff_1)/len(average_diff_1))
# print("BB v. Control: Average BMI difference at Time 2:", sum(average_diff_2)/len(average_diff_2))
#
#
# # PYRAMID (cohort with characteristics (age/sex) to match Bright Bodies) - at Initialization
# Pyr.plot_pyramids(observed_data=D.age_sex_dist,
#                   simulated_data=Sim.multiCohortBB.multiSimOutputs.pyramidStart,
#                   fig_size=(6, 4),
#                   x_lim=10,
#                   title="Cohort Pyramids at Initialization",
#                   colors=('blue', 'red', 'black'),
#                   y_labels=['8', '9', '10', '11', '12', '13', '14', '15', '16'],
#                   age_group_width=1,
#                   length_of_sim_bars=250,
#                   scale_of_sim_legend=0.75,
#                   transparency=0.5)
#
# # Colors: https://www.webucator.com/blog/2015/03/python-color-constants-module/
#

# # TO PRODUCE BAR: VALIDATION TO RCT
# x = [0, 1, 2]
# # rct data: treatment effect at year 1 and 2
# model_year_diffs = [avg_year_1_v_0, avg_year_2_v_1]
# print(model_year_diffs)
#
# rct_control_year_diffs = [1.9, 0.0]
# rct_bb_year_diffs = [-1.8, 0.9]
#
# if multiCohort.params.intervention == bright_bodies:
#     rct_year_diffs = rct_bb_year_diffs
# else:
#     rct_year_diffs = rct_control_year_diffs
#
# ind = np.arange(len(rct_year_diffs))  # the x locations for the groups
# width = 0.25  # the width of the bars
#
# fig, ax = plt.subplots()
# rct_bar = ax.bar(ind - width/2,
#                  rct_year_diffs,
#                  width,
#                  label='RCT Diffs')
# sim_bar = ax.bar(ind + width/2,
#                  model_year_diffs,
#                  width,
#                  label='Simulation Diffs')
#
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('BMI Difference (kg/m^2)')
# ax.set_xticks(ind)
# ax.set_xticklabels(('Year 0 to 1', 'Year 1 to 2'))
# ax.legend()
# plt.yticks([-2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5])
#
# if multiCohort.params.intervention == bright_bodies:
#     ax.set_title('Bright Bodies Validation: BMI Differences by Year')
#     # year 0 to 1
#     plt.annotate(rct_year_diffs[0], xy=(-0.25, 0.1))
#     plt.annotate(model_year_diffs[0], xy=(0.0, 0.1))
#     # year 1 to 2
#     plt.annotate(rct_year_diffs[1], xy=(0.75, -0.2))
#     plt.annotate(model_year_diffs[1], xy=(1.0, -0.2))
# else:
#     ax.set_title('Control Validation: Differences by Year')
#     # year 0 to 1
#     plt.annotate(rct_year_diffs[0], xy=(-0.25, -0.2))
#     plt.annotate(model_year_diffs[0], xy=(0.0, -0.2))
#     # year 1 to 2
#     plt.annotate(rct_year_diffs[1], xy=(0.75, 0.1))
#     plt.annotate(model_year_diffs[1], xy=(1.0, 0.1))
#
# plt.show()
