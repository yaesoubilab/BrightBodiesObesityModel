from enum import Enum


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
        self.nCohorts = 16      # number of cohorts

        # to discount outcomes and calculate the current value of old costs
        self.currentYear = 2020
        self.discountRate = 0.03

        # multipliers to adjust BMI trajectories
        self.dictAdjFactorCC = {
            'Control': [1.049, 0.01],  # all years
        }
        # effectiveness of bright bodies (BMI under BB = effectiveness * BMI under control)
        self.dictEffBB = {
            'BB Year 1': [0.88, 0.01],
            'BB Year 2': [0.9, 0.01]
        }

        # fringe
        fringe_rate = 0.4575

        # dictionary of cost items for Bright Bodies
        # each element is a list of [mean, stDev]
        self.dictCostBB = {
            'Exercise Physiologist A': [5595.00 * (1 + fringe_rate), 0.1 * 5595.00 * (1 + fringe_rate)],
            'Exercise Physiologist B': [6993.75 * (1 + fringe_rate), 0.1 * 6993.75 * (1 + fringe_rate)],
            'Games and Equipment:': [2521.25, 0.1 * 2521.25],
            'Motivational Tools:': [318.47, 0.1 * 318.47],
            'Printed Materials (Exercise Session)': [33.17, 0.1 * 33.17],
            'Gym Room and Utilities': [10400.00, 0.1 * 10400.00],
            'First Aid Kit': [199.05, 0.1 * 199.05],
            'Registered Dietitian A': [1592.73 * (1 + fringe_rate), 0.1 * 1592.73 * (1 + fringe_rate)],
            'Registered Dietitian B': [4778.18 * (1 + fringe_rate), 0.1 * 4778.18 * (1 + fringe_rate)],
            'Social Worker (Nutrition Session)': [1287.68 * (1 + fringe_rate), 0.1 * 1287.68 * (1 + fringe_rate)],
            'Educational Tools ': [1791.41, 0.1 * 1791.41],
            'Classroom and Utilities (Nutrition Session)': [2600.00, 0.1 * 2600.00],
            'Social Worker (Parent Session)': [1287.68 * (1 + fringe_rate), 0.1 * 1287.68 * (1 + fringe_rate)],
            'Printed Materials (Parent Session)': [33.17, 0.1 * 33.17],
            'Classroom and Utilities (Parent Session)': [2600.00, 0.1 * 2600.00],
            'Program Coordinator (exercise physiologist)(admin)': [6993.75 * (1 + fringe_rate),
                                                                   0.1 * 6993.75 * (1 + fringe_rate)],
            'Program Director (registered dietitian)(admin)': [12741.81 * (1 + fringe_rate),
                                                               0.1 * 12741.81 * (1 + fringe_rate)],
            'Department Clinical Secretary': [561.38 * (1 + fringe_rate), 0.1 * 561.38 * (1 + fringe_rate)],
            'Technician': [1447.77 * (1 + fringe_rate), 0.1 * 1447.77 * (1 + fringe_rate)],
            'Equipment (Weight): ': [928.88, 0.1 * 928.88],
            'Equipment (Height):': [79.62, 0.1 * 79.62],
            'Medical Director': [5448.85 * (1 + fringe_rate), 0.1 * 5448.85 * (1 + fringe_rate)],
            'Space:': [3980.91, 0.1 * 3980.91],
            'Cleaning Service': [1174.37, 0.1 * 1174.37],
            'Clinic Equipment and Supplies ': [3848.22, 0.1 * 3848.22]
        }

        # dictionary of cost items for the Control
        # each element is a list of [mean, stDev]
        self.dictCostControl = {
            'Nurse Practitioner': [14837.29 * (1 + fringe_rate), 0.1 * 14837.29 * (1 + fringe_rate)],
            'Registered Dietitian': [5743.00 * (1 + fringe_rate), 0.1 * 5743.00 * (1 + fringe_rate)],
            'Social Worker (Behavioral visit)': [4457.35 * (1 + fringe_rate), 0.1 * 4457.35 * (1 + fringe_rate)],
            'Department Clinical Secretary': [2245.54 * (1 + fringe_rate), 0.1 * 2245.54 * (1 + fringe_rate)],
            'Technician': [1447.77 * (1 + fringe_rate), 0.1 * 1447.77 * (1 + fringe_rate)],
            'Medical Director': [12574.28 * (1 + fringe_rate), 0.1 * 12574.28 * (1 + fringe_rate)],
            'Space:': [3980.91, 0.1 * 3980.91],
            'Cleaning Service': [1174.37, 0.1 * 1174.37],
            'Clinic Equipment and Supplies ': [3848.22, 0.1 * 3848.22]
        }

        # calculate the standard deviation of the estimated mean
        # sd_dev_younger18_obese = Stat.get_sterr_from_half_length(
        #     confidence_interval=[30, 450], n=2812, alpha=0.05)
        # sd_dev_younger18_overweigth = Stat.get_sterr_from_half_length(
        #     confidence_interval=[30, 380], n=2832, alpha=0.05)
        #
        # self.dictHCExp = {
        #     '<18 years, >95th %ile': [220, sd_dev_younger18_obese],
        #     '<18 years, <95th %ile': [180, sd_dev_younger18_overweigth],
        #     '>18 years': [197, 43]
        # }

        self.dictHCExp = {
            '<18 years, >95th %ile': [133, 62],
            '<18 years, <95th %ile': [180, 89],
            '>18 years': [223, 44]
        }

        # to inflate cost estimates
        self.inflation = 0.022
        self.yearInterventionCosts = 2019
        self.yearHCExpStudyAdults = 2013
        self.yearHCExpStudyChildren = 2006
        self.nChildrenBB = 90

        # for Bright Bodies (8-16 y/o)
        # use to initialize cohort
        self.ageSexDist = [
            [8, 0, 0.055519863],  # 8, male
            [8, 1, 0.053217689],  # 8, female
            [9, 0, 0.055519863],  # 9, male
            [9, 1, 0.053217689],  # 9, female
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
            [16, 1, 0.055305708]  # 16, female
        ]

        # bmi cutoffs
        # 85th bmi cutoffs
        self.bmi85thCutOffs = [
            # age, sex, bmi_cutoff
            [2, 0, 18.2],  # 2, male
            [2, 1, 18.0],  # 2, female
            [3, 0, 17.4],  # 3, male
            [3, 1, 17.2],  # 3, female
            [4, 0, 16.9],  # 4, male
            [4, 1, 16.8],  # 4, female
            [5, 0, 16.8],  # 5, male
            [5, 1, 16.8],  # 5, female
            [6, 0, 17.0],  # 6, male
            [6, 1, 17.1],  # 6, female
            [7, 0, 17.4],  # 7, male
            [7, 1, 17.6],  # 7, female
            [8, 0, 17.9],  # 8, male
            [8, 1, 18.3],  # 8, female
            [9, 0, 18.6],  # 9, male
            [9, 1, 19.1],  # 9, female
            [10, 0, 19.4],  # 10, male
            [10, 1, 19.9],  # 10, female
            [11, 0, 20.2],  # 11, male
            [11, 1, 20.8],  # 11, female
            [12, 0, 21.0],  # 12, male
            [12, 1, 21.7],  # 12, female
            [13, 0, 21.8],  # 13, male
            [13, 1, 22.6],  # 13, female
            [14, 0, 22.6],  # 14, male
            [14, 1, 23.3],  # 14, female
            [15, 0, 23.4],  # 15, male
            [15, 1, 24.0],  # 15, female
        ]
        # 95th bmi cutoffs
        self.bmi95thCutOffs = [
            # age, sex, bmi_cutoff
            [8, 0, 20.0],  # 8, male
            [8, 1, 20.6],  # 8, female
            [9, 0, 21.1],  # 9, male
            [9, 1, 21.8],  # 9, female
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
            [16, 1, 28.9],  # 16, female
            [17, 0, 28.2],  # 15, male
            [17, 1, 29.6],  # 15, female
            [18, 0, 30],  # 15, male
            [18, 1, 30]  # 15, female
        ]
