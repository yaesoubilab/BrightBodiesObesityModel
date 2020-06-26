from enum import Enum
import SimPy.StatisticalClasses as Stat


class Interventions(Enum):
    """ Bright Bodies v. Clinical Care """
    CONTROL = 0
    BRIGHT_BODIES = 1


# Maintenance of Effect Levels:
class EffectMaintenance(Enum):
    NONE = 0
    DEPREC = 1
    FULL = 2


class ModelInputs:

    def __init__(self):

        # trace
        self.traceOn = False  # Set to true to trace a simulation replication
        self.deci = 5  # the decimal point to round the numbers to in the trace file

        # simulation settings
        self.simInit = 0.00001  # (years) initialization period to create the cohort
        self.simDuration = 10   # (years) simulation duration
        self.popSize = 90     # population size of each cohort
        self.nCohorts = 25      # number of cohorts

        # to discount outcomes and calculate the current value of old costs
        self.currentYear = 2020
        self.inflation = 0.02
        self.discountRate = 0.03

        # multipliers to adjust BMI trajectories
        self.dictTrajMultipliers = {
            'Control': [1.049, 0.01],
            'BB Year 1': [0.925, 0.01],
            'BB Year 2': [0.951, 0.01]
        }

        # dictionary of cost items for Bright Bodies
        # each element is a list of [mean, stDev]
        self.dictCostBB = {
            'Exercise physiologist': [9592.00, 0.1 * 9592.00],
            'Games and equipment': [1900.00, 0.1 * 1900.00],
            'Motivational tools': [240.00, 0.1 * 240.00],
            'Printed material': [25.00, 0.1 * 25.00],
            'Gym room and utilities': [0.00, 0.1 * 0.00],
            'First aid kit': [150.00, 0.1 * 150.00],
            'Registered dietitian': [6805.00, 0.1 * 6805.00],
            'Social worker': [1200.00, 0.1 * 1200.00],
            'Educational tools': [1350.00, 0.1 * 1350.00],
            'Classroom and utilities': [0.00, 0.1 * 0.00],
            'Exercise physiologist (admin)': [6990.00, 0.1 * 6990.00],
            'Registered dietitian (admin)': [16376.00, 0.1 * 16376.00],
            'Technician': [1200.00, 0.1 * 1200.00],
            'Body fat analyzer and scale': [700.00, 0.1 * 700.00],
            'Stadiometer': [100.00, 0.1 * 100.00],
            'Medical consultation': [5100.00, 0.1 * 5100.00]
        }

        # dictionary of cost items for the Control
        # each element is a list of [mean, stDev]
        self.dictCostControl = {
            'Nurse practitioner': [11686.00, 0.1 * 11686.00],
            'Registered dietitian (CC)': [6329.00, 0.1 * 6329.00],
            'Social worker (CC)': [6460.00, 0.1 * 6460.00],
            'Dept clinical secretary': [834.00, 0.1 * 834.00],
            'Clinic secretary': [1669.00, 0.1 * 1669.00],
            'Typing': [2504.00, 0.1 * 2504.00],
            'Lab technician': [1408.00, 0.1 * 1408.00],
            'Medical consultation (CC)': [10256.00, 0.1 * 10256.00],
            'Rent space, utilities': [3000.00, 0.1 * 3000.00],
            'Cleaning service': [885.00, 0.1 * 885.00],
            'Clinic equipment and supplies': [2900.00, 0.1 * 2900.00]
        }

        # calculate the standard deviation of the estimated mean
        # (note st_dev of the estimated mean = st_dev of observations / sqrt(n), which the standard error)
        sd_dev_younger18_obese = Stat.get_sterr_from_half_length(confidence_interval=[30, 450], n=2812, alpha=0.05)
        sd_dev_younger18_overweigth = Stat.get_sterr_from_half_length(confidence_interval=[30, 380], n=2832, alpha=0.05)

        self.dictHCExp = {
            '<18 years, >95th %ile': [220, sd_dev_younger18_obese],
            '<18 years, <95th %ile': [180, sd_dev_younger18_overweigth],
            '>18 years': [197, 43]
        }

        # to inflate cost estimates
        self.yearBBStudy = 2007
        self.yearHCExpStudyAdults = 2013
        self.yearHCExpStudyChildren = 2006
        self.nChildrenBB = 90

        # for Bright Bodies (8-16 y/o)
        # use to initialize cohort
        self.ageSexDist = [
            [2, 0, 0.125],  # 2, male
            [2, 1, 0.125],  # 2, female
            [3, 0, 0.125],  # 3, male
            [3, 1, 0.125],  # 3, female
            [4, 0, 0.125],  # 4, male
            [4, 1, 0.125],  # 4, female
            [5, 0, 0.125],  # 5, male
            [5, 1, 0.125],  # 5, female
        ]

        # bmi cut offs
        self.bmi95thCutOffs = [
            # age, sex, bmi_cutoff
            [2, 0, 19.3],  # 2, male
            [2, 1, 19.1],  # 2, female
            [3, 0, 18.2],  # 3, male
            [3, 1, 18.3],  # 3, female
            [4, 0, 17.8],  # 4, male
            [4, 1, 18.0],  # 4, female
            [5, 0, 17.9],  # 5, male
            [5, 1, 18.2],  # 5, female
        ]
