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
        # population distribution by age/sex
        self.ageSexDist = df.DataFrameWithEmpiricalDist(rows=D.rows,                # life table
                                                        list_x_min=[0, 0],          # minimum values for age/sex groups
                                                        list_x_max=[85, 1],         # maximum values for age/sex groups
                                                        list_x_delta=[5, 'int'])    # [age interval, sex categorical]
        # population mortality rates by age/sex
        self.mortalityModel = MortalityModel(rows=D.death,        # life table
                                             group_mins=0,        # minimum value of sex group
                                             group_maxs=1,        # maximum value of sex group
                                             group_delta='int',   # sex group is a category
                                             age_min=0,           # minimum age in this life table
                                             age_delta=5)         # age interval


