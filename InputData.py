from enum import Enum

# simulation settings
SIM_INIT = 0.00001  # (years) initialization period to create the cohort
SIM_DURATION = 10   # (years) simulation duration
POP_SIZE = 90     # population size of each cohort
N_COHORTS = 50      # number of cohorts

# for Costs
N_CHILDREN_BB = 90
YEARS_RCT = 2

# to discount outcomes and calculate the current value of old costs
CURRENT_YEAR = 2020
INFLATION = 0.02
DISCOUNT = 0.03

# Multipliers:
# BB Year 1 reduction
multBBYear1 = 0.925
# BB Year 2 reduction
multBBYear2 = 0.951
# CC Multiplier
multCC = (1.05 + 1.048) / 2


# trace
TRACE_ON = False       # Set to true to trace a simulation replication
DECI = 5               # the decimal point to round the numbers to in the trace file

# Maintenance of Effect Levels:
class EffectMaintenance(Enum):
    NONE = 0
    DEPREC = 1
    FULL = 2


class Sex(Enum):
    MALE = 0
    FEMALE = 1


class Interventions(Enum):
    """ Bright Bodies v. Clinical Care """
    CONTROL = 0
    BRIGHT_BODIES = 1


