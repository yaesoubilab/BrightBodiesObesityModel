from enum import Enum

# trace
TRACE_ON = False       # Set to true to trace a simulation replication
DECI = 5               # the decimal point to round the numbers to in the trace file

# simulation settings
SIM_INIT = 0.00001  # (years) initialization period to create the cohort
SIM_DURATION = 10   # (years) - changed from 10 for manuscript
POP_SIZE = 90     # population size (cohort at initialization)

# for MultiCohorts
N_COHORTS = 25

# for Costs
N_CHILDREN_BB = 90
YEARS_RCT = 2

# Maintenance of Effect Levels:
# TODO: I'd suggest using an Enum to represent maintenance effect.
FULL_MAINTENENCE = False
DEPREC = True


class SEX(Enum):
    MALE = 0
    FEMALE = 1


class Interventions(Enum):
    """ Bright Bodies v. Clinical Care """
    CONTROL = 0
    BRIGHT_BODIES = 1


# for Bright Bodies (8-16 y/o)
# use to initialize cohort
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
    [15, 1, 0.055305708],  # 15, female
    [16, 0, 0.057822037],  # 16, male
    [16, 1, 0.055305708]   # 16, female
]

# For later use.
bmi_status_age_sex_dist = [
    # age, sex, bmi_cutoff
    [8, 0, 20.0],   # 8, male
    [8, 1, 20.6],   # 8, female
    [9, 0, 21.1],   # 9, male
    [9, 1, 21.8],   # 9, female
    [10, 0, 22.1],  # 10, male
    [10, 1, 22.9],  # 10, female
    [11, 0, 23.2],  # 11, male
    [11, 1, 24.1],  # 11, female
    [12, 0, 24.2],  # 12, male
    [12, 1, 25.2],  # 12, female
    [13, 0, 25.2],  # 13, male
    [13, 1, 26.2],  # 13, female
    [14, 0, 26.0],  # 14, male
    [14, 1, 27.2],  # 14, female
    [15, 0, 26.8],  # 15, male
    [15, 1, 28.1],  # 15, female
    [16, 0, 27.5],  # 16, male
    [16, 1, 28.9],   # 16, female
    [17, 0, 28.2],  # 15, male
    [17, 1, 29.6],  # 15, female
    [18, 0, 30],  # 15, male
    [18, 1, 30]  # 15, female
]

