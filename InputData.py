from enum import Enum


# trace
TRACE_ON = False       # Set to true to trace a simulation replication
DECI = 5               # the decimal point to round the numbers to in the trace file

# simulation settings
SIM_INIT = 0.00001  # (years) initialization period to create the cohort
SIM_DURATION = 10   # (years)
POP_SIZE = 1000     # population size (cohort at initialization)

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

