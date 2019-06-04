import InputData as D
import SimPy.RandomVariantGenerators as RVGs
# for adding births/deaths
import SimPy.DataFrames as df
from SimPy.Models import MortalityModel


class Parameters:
    # class to contain the parameters of the model
    def __init__(self):
        # exponential distribution of time to next birth
        self.timeToNextBirthDist = RVGs.Exponential(scale=D.INTER_BIRTH_TIME)
        # exponential distribution of time to death
       # self.timeToDeath = RVGs.Exponential(scale=D.LIFE_EXPECTANCY)
        # population distribution by age/sex
        self.ageSexDist = df.DataFrameWithEmpiricalDist(rows=D.rows,                # life table
                                                        list_x_min=[0, 0],          # minimum values for age/sex groups
                                                        list_x_max=[85, 1],         # maximum values for age/sex groups
                                                        list_x_delta=[5, 'int'])    # [age interval, sex categorical]
        # population mortality rates by age/sex
        self.mortalityModel = MortalityModel(rows=D.death_test,           # life table
                                             group_mins=0,        # minimum value of sex group
                                             group_maxs=1,        # maximum value of sex group
                                             group_delta='int',   # sex group is a category
                                             age_min=0,           # minimum age in this life table
                                             age_delta=5)         # age interval


# # For Adding Births
# rng = RVGs.RNG(seed=1)
# probDf = df.DataFrameWithEmpiricalDist(rows=D.rows,
#                                        list_x_min=[0, 0],
#                                        list_x_max=[85, 1],
#                                        list_x_delta=[5, 'int'])
# # get a sample
# print('Get a sampled index:', probDf.sample_indices(rng=rng))
# print('Get a sampled value:', probDf.sample_values(rng=rng))
# print('')


# # For Adding Deaths
# df2 = df.DataFrameWithExpDist(rows=D.death,
#                               list_x_min=[0, 0],
#                               list_x_max=[85, 1],
#                               list_x_delta=[5, 'int'])
#
# # get a sample
# rng = RVGs.RNG(seed=1)
# print('Sample 1: ', df2.get_dist(x_value=[0, 0]).sample(rng))
# print('Sample 2', df2.get_dist(x_value=[1, 0]).sample(rng))
# print('Sample 3', df2.get_dist(x_value=[2, 1]).sample(rng))
# print('Sample 4', df2.get_dist(x_value=[5, 0]).sample(rng))

# Mortality Model Samples

# mortalityModel = MortalityModel(rows=D.death,        # life table
#                                 group_mins=0,        # minimum value of sex group
#                                 group_maxs=1,        # maximum value of sex group
#                                 group_delta='int',   # sex group is a category
#                                 age_min=0,           # minimum age in this life table
#                                 age_delta=5)         # age interval
# # get sample for time until death
# print(mortalityModel.sample_time_to_death(group=0, age=8.9, rng=rng))
# print(mortalityModel.sample_time_to_death(group=0, age=0, rng=rng))
# print(mortalityModel.sample_time_to_death(group=0, age=32, rng=rng))


