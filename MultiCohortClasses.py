from ModelEntities import Cohort
import SimPy.RandomVariantGenerators as RVGs
# use Stat when extracting outcomes
import SimPy.StatisticalClasses as Stat
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
        self.pathOfBMIs.append(simulated_cohort.simOutputs.pathBMIs)

    # for CEA

        # sum annual costs and then run
        total_cost = sum(simulated_cohort.simOutputs.annualCosts)
        # store all cohort costs
        self.costs.append(total_cost)

        # store all cohort effects
        self.effects.append(simulated_cohort.simOutputs.effect)

    # NEW: for bmi diff figures
    #     self.meanBMIDiffs.append(simulated_cohort.simOutputs.pathOfBMIs.get_mean())
    #
    #     self.statMeanBMIDiff = Stat.SummaryStat(name='mean BMI diffs',
    #                                             data=self.meanBMIDiffs)

