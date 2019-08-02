import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import SimPy.Plots.SamplePaths as Path
from SimPy.Plots import PopulationPyramids as Pyr
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np

# SIMULATE ONE INTERVENTION AND INDIVIDUAL OUTCOMES

# Interventions
bright_bodies = D.Interventions.BRIGHT_BODIES
clinical_control = D.Interventions.CONTROL

# for MultiCohort for specified intervention
multiCohort = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    parameters=P.Parameters(intervention=bright_bodies)
)
# Simulate cohorts
multiCohort.simulate()

# sample paths for population size
Path.graph_sample_paths(
    sample_paths=multiCohort.multiSimOutputs.pathPopSizes,
    title='Population Size',
    y_range=[0, 1.1*D.POP_SIZE],
    x_label='Years'
)

# PYRAMID (cohort with characteristics (age/sex) to match Bright Bodies) - at Initialization
Pyr.plot_pyramids(observed_data=D.age_sex_dist,
                  simulated_data=multiCohort.multiSimOutputs.pyramidStart,
                  fig_size=(6, 4),
                  x_lim=10,
                  title="Cohort Pyramids at Initialization",
                  colors=('blue', 'red', 'black'),
                  y_labels=['8', '9', '10', '11', '12', '13', '14', '15', '16'],
                  age_group_width=1,
                  length_of_sim_bars=250,
                  scale_of_sim_legend=0.75,
                  transparency=0.5)
# Colors: https://www.webucator.com/blog/2015/03/python-color-constants-module/

# sample paths for average BMIs at each time step
Path.graph_sample_paths(
    sample_paths=multiCohort.multiSimOutputs.pathOfBMIs,
    title='Average BMIs for Bright Bodies',
    x_label='Simulation Year',
    y_range=[0, 40],
    connect='line'  # line graph (vs. step wise)
)

# TO DETERMINE BMI DIFFERENCES BY YEAR
year_one_vs_zero = []
year_two_vs_one = []

for cohortID in range(D.N_COHORTS):
    bmi_values = multiCohort.multiSimOutputs.pathOfBMIs[cohortID].get_values()

    # year 1 minus year 0
    year_1_v_0 = bmi_values[1] - bmi_values[0]
    year_one_vs_zero.append(year_1_v_0)

    # year 2 minus year 1
    year_2_v_1 = bmi_values[2] - bmi_values[1]
    year_two_vs_one.append(year_2_v_1)

print('BMI change y1 - y0 -->', year_one_vs_zero)
print('BMI change y2 - y1 -->', year_two_vs_one)

# find average change between year 0 and 1
avg_year_1_v_0 = sum(year_one_vs_zero)/len(year_one_vs_zero)
# find average change between year 1 and 2
avg_year_2_v_1 = sum(year_two_vs_one)/len(year_two_vs_one)

print('Average change in BMI between Y1 and Y0:', avg_year_1_v_0)
print('Average change in BMI between Y2 and Y1:', avg_year_2_v_1)

# TO PRODUCE SCATTER: VALIDATION TO RCT
x = [0, 1, 2]
# rct data: treatment effect at year 1 and 2
model_year_diffs = [avg_year_1_v_0, avg_year_2_v_1]
rct_control_year_diffs = [1.9, 0.0]
rct_bb_year_diffs = [-1.8, 0.9]

f, ax = plt.subplots()

# adding bright bodies data
ax.scatter([1, 2], model_year_diffs, color='teal')
ax.set_title('Difference in Average BMI by Year')
plt.annotate(('Sim', model_year_diffs[0]), xy=(1, model_year_diffs[0]))
plt.annotate(('Sim', model_year_diffs[1]), xy=(2, model_year_diffs[1]))

if multiCohort.params.intervention == bright_bodies:
    ax.scatter([1, 2], rct_bb_year_diffs, color='red')
    plt.annotate(rct_bb_year_diffs[0], xy=(1, rct_bb_year_diffs[0]+.2))
    plt.annotate(rct_bb_year_diffs[1], xy=(2, rct_bb_year_diffs[1]+.2))
    rct_color = patch.Patch(color='red', label='RCT: Bright Bodies')
else:
    ax.scatter([1, 2], rct_control_year_diffs, color='blue')
    plt.annotate(rct_control_year_diffs[0], xy=(1, rct_control_year_diffs[0]+.2))
    plt.annotate(rct_control_year_diffs[1], xy=(2, rct_control_year_diffs[1]+.2))
    rct_color = patch.Patch(color='blue', label='RCT: Control')

plt.xlim((0.0, 3.0))
plt.xticks([0, 1, 2])
plt.yticks([-2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5])
plt.xlabel('Sim Years')
plt.ylabel('Difference in BMI (kg/m^2) relative to previous year')

ax.set_xticks(np.arange(len(x)))
ax.set_xticklabels(('0', 'Year 0 to 1', 'Year 1 to 2'))

# Show legend
model_data_color = patch.Patch(color='teal', label='Simulation')
plt.legend(loc='upper right', handles=[model_data_color, rct_color])
plt.show()

# TO PRODUCE BAR: VALIDATION TO RCT
if multiCohort.params.intervention == bright_bodies:
    rct_year_diffs = rct_bb_year_diffs
else:
    rct_year_diffs = rct_control_year_diffs

ind = np.arange(len(rct_year_diffs))  # the x locations for the groups
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rct_bar = ax.bar(ind - width/2,
                 rct_year_diffs,
                 width,
                 label='RCT Diffs')
sim_bar = ax.bar(ind + width/2,
                 model_year_diffs,
                 width,
                 label='Simulation Diffs')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('BMI Difference (kg/m^2)')
ax.set_xticks(ind)
ax.set_xticklabels(('Year 0 to 1', 'Year 1 to 2'))
ax.legend()
plt.yticks([-2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5])

if multiCohort.params.intervention == bright_bodies:
    ax.set_title('Bright Bodies Validation: BMI Differences by Year')
    # year 0 to 1
    plt.annotate(rct_year_diffs[0], xy=(-0.25, 0.1))
    plt.annotate(model_year_diffs[0], xy=(0.0, 0.1))
    # year 1 to 2
    plt.annotate(rct_year_diffs[1], xy=(0.75, -0.2))
    plt.annotate(model_year_diffs[1], xy=(1.0, -0.2))
else:
    ax.set_title('Control Validation: Differences by Year')
    # year 0 to 1
    plt.annotate(rct_year_diffs[0], xy=(-0.25, -0.2))
    plt.annotate(model_year_diffs[0], xy=(0.0, -0.2))
    # year 1 to 2
    plt.annotate(rct_year_diffs[1], xy=(0.75, 0.1))
    plt.annotate(model_year_diffs[1], xy=(1.0, 0.1))

plt.show()

