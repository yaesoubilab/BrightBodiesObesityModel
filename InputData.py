from enum import Enum
from SimPy import InOutFunctions as InOutSupport
import pandas as pd

# trace
TRACE_ON = False        # Set to true to trace a simulation replication
DECI = 5               # the decimal point to round the numbers to in the trace file

# simulation settings
SIM_INIT = 0.00001  # (years) initialization period to create the cohort
SIM_DURATION = 10   # (years)

POP_SIZE = 100             # population size (at initialization)

# mean time (years) between births
# source: from here https://www.cdc.gov/nchs/nvss/births.htm, we know
# that Birth rate= 12.4 per 1,000 population
INTER_BIRTH_TIME = (1/12.4) * (1000/POP_SIZE)

PROB_FEMALE = 0.5075    # probability of being female

# for MultiCohorts
N_COHORTS = 2


class SEX(Enum):
    MALE = 0
    FEMALE = 1


# for Bright Bodies (8-16 y/o)
# use to initialize cohort
# condensed decimals for now - FIX LATER
age_sex_dist = [
    [8, 0, 0.055519863],   # 8, male
    [8, 1, 0.053217689],   # 8, female
    [9, 0, 0.055519863],   # 9, male
    [9, 1, 0.053217689],   # 9, female
    [10, 0, 0.056804797],  # 10, male
    [10, 1, 0.054449084],  # 10, female
    [11, 0, 0.056804798],  # 11, male
    [11, 1, 0.054449084],  # 11, female
    [12, 0, 0.056804797],  # 12, male
    [12, 1, 0.054449084],  # 12, female
    [13, 0, 0.056804797],  # 13, male
    [13, 1, 0.054449084],  # 13, female
    [14, 0, 0.056804797],  # 14, male
    [14, 1, 0.054449084],  # 14, female
    [15, 0, 0.057822037],  # 15, male
    [15, 1, 0.055305708],   # 15, female
    [16, 0, 0.057822037],  # 16, male
    [16, 1, 0.055305708]    # 16, female
]

#
# # for Adding Births: US population distribution by age/sex (as of 7/1/17)
# # limited percentages to 3 decimal places for now (had to adjust to = 1)
# rows = [
#     [0, 0, 0.03],    # < 5, male
#     [0, 1, 0.030],    # < 5, female
#     [5, 0, 0.031],    # 5-9, male
#     [5, 1, 0.031],    # 5-9, female
#     [10, 0, 0.033],   # 10-14, male
#     [10, 1, 0.031],   # 10-14, female
#     [15, 0, 0.033],   # 15-19, male
#     [15, 1, 0.031],   # 15-19, female
#     [20, 0, 0.035],   # 20-24, male
#     [20, 1, 0.033],   # 20-24, female
#     [25, 0, 0.037],   # 25-29, male
#     [25, 1, 0.035],   # 25-29, female
#     [30, 0, 0.034],   # 30-34, male
#     [30, 1, 0.033],   # 30-34, female
#     [35, 0, 0.033],   # 35-39, male
#     [35, 1, 0.031],   # 35-39, female
#     [40, 0, 0.030],   # 40-44, male
#     [40, 1, 0.030],   # 40-44, female
#     [45, 0, 0.032],   # 45-49, male
#     [45, 1, 0.033],   # 45-49, female
#     [50, 0, 0.032],   # 50-54, male
#     [50, 1, 0.033],   # 50-54, female
#     [55, 0, 0.032],   # 55-59, male
#     [55, 1, 0.035],   # 55-59, female
#     [60, 0, 0.029],   # 60-64, male
#     [60, 1, 0.031],   # 60-64, female
#     [65, 0, 0.024],   # 65-69, male
#     [65, 1, 0.027],   # 65-69, female
#     [70, 0, 0.018],   # 70-74, male
#     [70, 1, 0.027],   # 70-74, female
#     [75, 0, 0.012],   # 75-79, male
#     [75, 1, 0.015],   # 75-79, female
#     [80, 0, 0.008],   # 80-84, male
#     [80, 1, 0.011],   # 80-84, female
#     [85, 0, 0.007],   # >= 85, male
#     [85, 1, 0.013]    # >= 85, female
# ]
#
#
# # for Adding Deaths: US mortality distribution by age/sex
# # limited rates to 4 decimal places for now
# # last column = mortality rate
# death = [
#     [0, 0, 0.0015],    # < 5, male
#     [0, 1, 0.0013],    # < 5, female
#     [5, 0, 0.0001],    # 5-9, male
#     [5, 1, 0.0001],    # 5-9, female
#     [10, 0, 0.0002],   # 10-14, male
#     [10, 1, 0.0001],   # 10-14, female
#     [15, 0, 0.0007],   # 15-19, male
#     [15, 1, 0.0003],   # 15-19, female
#     [20, 0, 0.0013],   # 20-24, male
#     [20, 1, 0.0005],   # 20-24, female
#     [25, 0, 0.0015],   # 25-29, male
#     [25, 1, 0.0006],   # 25-29, female
#     [30, 0, 0.0017],   # 30-34, male
#     [30, 1, 0.0008],   # 30-34, female
#     [35, 0, 0.0020],   # 35-39, male
#     [35, 1, 0.0011],   # 35-39, female
#     [40, 0, 0.0025],   # 40-44, male
#     [40, 1, 0.0016],   # 40-44, female
#     [45, 0, 0.0037],   # 45-49, male
#     [45, 1, 0.0024],   # 45-49, female
#     [50, 0, 0.0061],   # 50-54, male
#     [50, 1, 0.0038],   # 50-54, female
#     [55, 0, 0.0092],   # 55-59, male
#     [55, 1, 0.0056],   # 55-59, female
#     [60, 0, 0.0133],   # 60-64, male
#     [60, 1, 0.0078],   # 60-64, female
#     [65, 0, 0.0183],   # 65-69, male
#     [65, 1, 0.0117],   # 65-69, female
#     [70, 0, 0.0279],   # 70-74, male
#     [70, 1, 0.0189],   # 70-74, female
#     [75, 0, 0.0441],   # 75-79, male
#     [75, 1, 0.0313],   # 75-79, female
#     [80, 0, 0.0743],   # 80-84, male
#     [80, 1, 0.0550],   # 80-84, female
#     [85, 0, 0.2376],   # >= 85, male
#     [85, 1, 0.1926]    # >= 85, female
# ]
