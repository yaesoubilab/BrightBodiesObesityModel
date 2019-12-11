from ModelEntities import Cohort
import SimPy.RandomVariantGenerators as RVGs
import InputData as D


class MultiCohort:
    """ simulates multiple cohorts """

    def __init__(self, ids, parameters):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param parameters: cohort parameters
        """

        self.ids = ids
        self.rng = RVGs.RNG(seed=ids)
        self.params = parameters

        self.cohorts = []       # list of cohorts

        # for cohort outcomes
        self.multiSimOutputs = MultiSimOutputs()

    def simulate(self):
        """ simulates all cohorts """

        for i in range(len(self.ids)):

            # create cohort
            cohort = Cohort(id=self.ids[i], parameters=self.params)

            # simulate the cohort
            cohort.simulate(sim_duration=D.SIM_DURATION)

            # outcomes from simulating all cohorts
            self.multiSimOutputs.extract_outcomes(simulated_cohort=cohort)


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
        total_cost = sum(simulated_cohort.simOutputs.totalCosts)
        print('NEW TOTAL COST', total_cost)
        # ~ 298,000 ( ~ 266 * 100 p = 26600 per year * 10 years = 298,491)

        average_cost = total_cost/D.POP_SIZE

        # store costs for use in CEA
        self.costs.append(average_cost)

        # NEW
        # total_effect: sum of average BMIs (by year) for sim duration
        total_effect = sum(simulated_cohort.simOutputs.pathAveBMIs.get_values())

        average_effect = total_effect/D.POP_SIZE
        # average_effect = total_effect/D.SIM_DURATION

        print("AVERAGE EFFECT:", average_effect)
        # print("TOTAL EFFECT", total_effect)

        # store all cohort effects for use in CEA
        self.effects.append(average_effect)

