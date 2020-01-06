from ModelEntities import Cohort
import SimPy.RandomVariantGenerators as RVGs
import InputData as D
from ModelParameters import ParamGenerator


class MultiCohort:
    """ simulates multiple cohorts """

    #def __init__(self, ids, parameters):
    def __init__(self, ids, intervention):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param parameters: cohort parameters
        """

        self.ids = ids
        self.rng = RVGs.RNG(seed=ids)
        #self.params = parameters

        self.cohorts = []       # list of cohorts
        self.param_sets = []  # list of parameter sets (for each cohort)

        # for cohort outcomes
        self.multiSimOutputs = MultiSimOutputs()

        # create parameter sets
        self.__populate_parameter_sets(intervention=intervention)

    def simulate(self):
        """ simulates all cohorts """

        for i in range(len(self.ids)):

            # create cohort
            # cohort = Cohort(id=self.ids[i], parameters=self.params)
            cohort = Cohort(id=self.ids[i], parameters=self.param_sets[i])

            # simulate the cohort
            cohort.simulate(sim_duration=D.SIM_DURATION)

            # outcomes from simulating all cohorts
            self.multiSimOutputs.extract_outcomes(simulated_cohort=cohort)

    def __populate_parameter_sets(self, intervention):

        param_generator = ParamGenerator(intervention=intervention)

        # create as many sets of parameters as the number of cohorts
        for i in range(len(self.ids)):
            # create new rng for each parameter set
            rng = RVGs.RNG(seed=i)
            # get and store new set of parameters
            self.param_sets.append(param_generator.get_new_parameters(rng=rng))


class MultiSimOutputs:

    def __init__(self):

        self.pathPopSizes = []  # empty list to be populated with population sizes
        self.pyramidStart = []

        self.pathOfBMIs = []

        # for CEA
        # costs = list of total cost for all participants over entire sim duration, per cohort
        self.costs = []
        # effects = list of the average effect over entire sim duration, per cohort
        self.effects = []

        # NEW: for bmi diff figures
        self.meanBMIDiffs = []
        self.statMeanBMIDiff = None

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort """

        # store all cohort population size paths
        self.pathPopSizes.append(simulated_cohort.simOutputs.pathPopSize)

        # store all cohort pyramid percentages
        self.pyramidStart.append(simulated_cohort.simOutputs.pyramids[0])

        # store all cohort average BMI paths
        self.pathOfBMIs.append(simulated_cohort.simOutputs.pathAveBMIs)

    # for CEA

        # NEW
        # sum cost per year for all participants to get total cohort cost
        # over sim duration
        print(simulated_cohort.simOutputs.totalCosts)
        total_cost = sum(simulated_cohort.simOutputs.totalCosts)
        print('NEW TOTAL COST', total_cost)
        # ~ 298,000 ( ~ 266 * 100 p = 26600 per year * 10 years = 298,491)

        average_cost = total_cost/D.POP_SIZE

        # store costs for use in CEA
        self.costs.append(average_cost)

        # NEW
        print(simulated_cohort.simOutputs.pathAveBMIs.get_values())
        effect_values = simulated_cohort.simOutputs.pathAveBMIs.get_values()
        # total_effect: sum of average BMIs (by year) for sim duration
        # total_effect = sum(simulated_cohort.simOutputs.pathAveBMIs.get_values())
        total_effect = effect_values[1] + effect_values[2]

        # do NOT need to divide by pop size because values are already an average over the cohort
        average_effect = total_effect/D.YEARS_RCT

        # print("AVERAGE EFFECT:", average_effect)
        print("TOTAL EFFECT", total_effect)

        # store all cohort effects for use in CEA
        # use TOTAL EFFECT because the values are already an average
        self.effects.append(average_effect)

