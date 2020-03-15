import MultiCohortClasses as MultiCls
import InputData as D
import ModelParameters as P
import SimPy.Plots.SamplePaths as Path
from SimPy.Plots import PopulationPyramids as Pyr

# SIMULATE ONE INTERVENTION AND INDIVIDUAL OUTCOMES

# Interventions
bright_bodies = D.Interventions.BRIGHT_BODIES
clinical_control = D.Interventions.CONTROL

# for MultiCohort for specified intervention
multiCohort = MultiCls.MultiCohort(
    ids=range(D.N_COHORTS),
    intervention=bright_bodies
    # parameters=P.Parameters(intervention=bright_bodies)
)
# Simulate cohorts
multiCohort.simulate()

# sample paths for population size
Path.plot_sample_paths(
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
Path.plot_sample_paths(
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
