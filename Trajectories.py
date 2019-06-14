from SimPy import InOutFunctions as InOutSupport
from SimPy import DataFrames as df
from SimPy import RandomVariantGenerators as RVGs


# GROWTH TRAJECTORIES

# FEMALES
# Female 13
f_13_rows = InOutSupport.read_csv_rows('female_13_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)
# to test reading rows:
# print('Testing reading by rows for female 13:')
# for row in f_13_rows:
#     print(row)

# Female 14
f_14_rows = InOutSupport.read_csv_rows('female_14_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)
# Female 15
f_15_rows = InOutSupport.read_csv_rows('female_15_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)
# Female 16
f_16_rows = InOutSupport.read_csv_rows('female_16_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)
# MALES
# Male 13
m_13_rows = InOutSupport.read_csv_rows('male_13_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)
# Male 14
m_14_rows = InOutSupport.read_csv_rows('male_14_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)
# Male 15
m_15_rows = InOutSupport.read_csv_rows('male_15_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)
# Male 16
m_16_rows = InOutSupport.read_csv_rows('male_16_obese.csv',
                                       delimiter=',',
                                       if_del_first_row=True,
                                       if_convert_float=True)

# YOUNGER - using older data for now to run model without errors
f_8_rows = InOutSupport.read_csv_rows('female_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
f_9_rows = InOutSupport.read_csv_rows('female_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
f_10_rows = InOutSupport.read_csv_rows('female_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
f_11_rows = InOutSupport.read_csv_rows('female_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
f_12_rows = InOutSupport.read_csv_rows('female_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
m_8_rows = InOutSupport.read_csv_rows('male_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
m_9_rows = InOutSupport.read_csv_rows('male_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
m_10_rows = InOutSupport.read_csv_rows('male_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
m_11_rows = InOutSupport.read_csv_rows('male_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)
m_12_rows = InOutSupport.read_csv_rows('male_13_obese.csv', delimiter=',', if_del_first_row=True, if_convert_float=True)


# class to select random row from rows (specific to age/sex)
class SetOfTrajectories:
    def __init__(self, rows):
        self.rows = rows
        self.discreteUniform = RVGs.UniformDiscrete(0, len(rows) - 1)

    def sample_traj(self, rng):
        # i = self.discreteUniform.sample(rnd)
        i = self.discreteUniform.sample(rng)
        return self.rows[i]


# ROWS
traj_13_f_rows = SetOfTrajectories(rows=f_13_rows)
traj_14_f_rows = SetOfTrajectories(rows=f_14_rows)
traj_15_f_rows = SetOfTrajectories(rows=f_15_rows)
traj_16_f_rows = SetOfTrajectories(rows=f_16_rows)
traj_13_m_rows = SetOfTrajectories(rows=m_13_rows)
traj_14_m_rows = SetOfTrajectories(rows=m_14_rows)
traj_15_m_rows = SetOfTrajectories(rows=m_15_rows)
traj_16_m_rows = SetOfTrajectories(rows=m_16_rows)
# YOUNGER - using older data for now to simulate without error
# females
traj_8_f_rows = SetOfTrajectories(rows=f_8_rows)
traj_9_f_rows = SetOfTrajectories(rows=f_9_rows)
traj_10_f_rows = SetOfTrajectories(rows=f_10_rows)
traj_11_f_rows = SetOfTrajectories(rows=f_11_rows)
traj_12_f_rows = SetOfTrajectories(rows=f_12_rows)
# males
traj_8_m_rows = SetOfTrajectories(rows=m_8_rows)
traj_9_m_rows = SetOfTrajectories(rows=m_9_rows)
traj_10_m_rows = SetOfTrajectories(rows=m_10_rows)
traj_11_m_rows = SetOfTrajectories(rows=m_11_rows)
traj_12_m_rows = SetOfTrajectories(rows=m_12_rows)


# Creating DataFrame of Trajectories for Bright Bodies Age Cohort
df_trajectories = df.DataFrameOfObjects(list_x_min=[8, 0],
                                        list_x_max=[16, 1],
                                        list_x_delta=[1, 'int'])

df_trajectories.set_obj(x_value=[13, 1], obj=traj_13_f_rows)
df_trajectories.set_obj(x_value=[14, 1], obj=traj_14_f_rows)
df_trajectories.set_obj(x_value=[15, 1], obj=traj_15_f_rows)
df_trajectories.set_obj(x_value=[16, 1], obj=traj_16_f_rows)
df_trajectories.set_obj(x_value=[13, 0], obj=traj_13_m_rows)
df_trajectories.set_obj(x_value=[14, 0], obj=traj_14_m_rows)
df_trajectories.set_obj(x_value=[15, 0], obj=traj_15_m_rows)
df_trajectories.set_obj(x_value=[16, 0], obj=traj_16_m_rows)
# YOUNGER - fix later
# females
df_trajectories.set_obj(x_value=[8, 1], obj=traj_8_f_rows)
df_trajectories.set_obj(x_value=[9, 1], obj=traj_9_f_rows)
df_trajectories.set_obj(x_value=[10, 1], obj=traj_10_f_rows)
df_trajectories.set_obj(x_value=[11, 1], obj=traj_11_f_rows)
df_trajectories.set_obj(x_value=[12, 1], obj=traj_12_f_rows)
# males
df_trajectories.set_obj(x_value=[8, 0], obj=traj_8_m_rows)
df_trajectories.set_obj(x_value=[9, 0], obj=traj_9_m_rows)
df_trajectories.set_obj(x_value=[10, 0], obj=traj_10_m_rows)
df_trajectories.set_obj(x_value=[11, 0], obj=traj_11_m_rows)
df_trajectories.set_obj(x_value=[12, 0], obj=traj_12_m_rows)

# Random Number Generator
rng = RVGs.RNG(seed=1)

# TEST: Indexing Trajectories
# person_13_f = df_trajectories.get_obj(x_value=[13, 1])
# # to print entire indexed row
# # print(person_13_f.rows[0])
# # to print random row for person of designated age/sex
# sample = person_13_f.sample_traj(rng=rng)
# print(sample)
# print(sample[2])
# # print(person_13_f.sample_traj(rng=rng))
