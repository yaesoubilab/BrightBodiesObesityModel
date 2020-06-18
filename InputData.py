from enum import Enum

# trace
TRACE_ON = False       # Set to true to trace a simulation replication
DECI = 5               # the decimal point to round the numbers to in the trace file

# simulation settings
SIM_INIT = 0.00001  # (years) initialization period to create the cohort
SIM_DURATION = 10   # (years) - changed from 10 for manuscript
POP_SIZE = 90     # population size of each cohort

# for simulation multiple cohorts
N_COHORTS = 50

# for Costs
N_CHILDREN_BB = 90
YEARS_RCT = 2

INFLATION = 0.02

# Multipliers:
# BB Year 1 reduction
multBBYear1 = 0.925
# BB Year 2 reduction
multBBYear2 = 0.951
# CC Multiplier
multCC = (1.05 + 1.048) / 2


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


