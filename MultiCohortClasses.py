from ModelEntities import Cohort
import SimPy.DiscreteEventSim as SimCls
import SimPy.SimulationSupport as Sim
import ModelOutputs as O
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

        # calculate summary statistics from all cohorts


class MultiSimOutputs:

    def __init__(self):

        self.pathPopSizes = []  # empty list to be populated with population sizes
        self.pyramidPercentagesStart = []
        self.pyramidPercentagesEnd = []

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort """

        # store all cohort population size paths
        self.pathPopSizes.append(simulated_cohort.simOutputs.pathPopSize)

        # store all cohort pyramid percentages
        self.pyramidPercentagesStart.append(simulated_cohort.simOutputs.pyramidPercentage[0])
        self.pyramidPercentagesEnd.append(simulated_cohort.simOutputs.pyramidPercentage[1])
