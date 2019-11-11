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
        self.costs = []
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
        total_cost = sum(simulated_cohort.simOutputs.totalCosts)
        print('NEW TOTAL COST', total_cost)

        # store all cohort costs
        self.costs.append(total_cost)

        # store all cohort effects
        self.effects.append(simulated_cohort.simOutputs.effect)

