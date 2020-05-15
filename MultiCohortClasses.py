from ModelEntities import Cohort
import SimPy.RandomVariantGenerators as RVGs
import InputData as D
from ModelParameters import ParamGenerator
import multiprocessing as mp


class MultiCohort:
    """ simulates multiple cohorts """

    def __init__(self, ids, intervention, maintenance_scenario):
        """
        :param ids: (list) of ids for cohorts to simulate
        """

        self.ids = ids
        self.param_sets = []  # list of parameter sets (for each cohort)

        # for cohort outcomes
        self.multiSimOutputs = MultiSimOutputs()

        # create parameter sets
        self.__populate_parameter_sets(intervention=intervention,
                                       maintenance_scenario=maintenance_scenario)

    def simulate(self, sim_duration, if_run_in_parallel=False):
        """ simulates all cohorts """

        if not if_run_in_parallel:
            for i in range(len(self.ids)):

                # create cohort
                cohort = Cohort(id=self.ids[i], parameters=self.param_sets[i])

                # simulate the cohort
                cohort.simulate(sim_duration=sim_duration)

                # outcomes from simulating all cohorts
                self.multiSimOutputs.extract_outcomes(simulated_cohort=cohort)
        else:
            # create cohorts
            cohorts = []
            for i in range(len(self.ids)):
                cohorts.append(Cohort(id=self.ids[i],
                                      parameters=self.param_sets[i]))

            # create a list of arguments for simulating the cohorts in parallel
            args = [(cohort, sim_duration) for cohort in cohorts]

            # simulate all cohorts in parallel
            n_processes = mp.cpu_count()  # maximum number of processors
            with mp.Pool(n_processes) as pl:
                simulated_cohorts = pl.starmap(simulate_this_cohort, args)

            # outcomes from simulating all cohorts
            for cohort in simulated_cohorts:
                self.multiSimOutputs.extract_outcomes(simulated_cohort=cohort)

    def __populate_parameter_sets(self, intervention, maintenance_scenario):

        param_generator = ParamGenerator(intervention=intervention,
                                         maintenance_scenario=maintenance_scenario)

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

        # expenditures = list of average expenditures per year per person over entire sim duration, per cohort
        self.expenditures = []
        # totalExpenditures = list of total expenditures for all people over 10 years, per cohort
        self.totalExpenditures = []
        # individualTotalExpenditure = list of individual expenditures over 10 years
        self.individualTotalExpenditure = []

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

        # sum cost per year for all participants to get total cohort cost
        # over sim duration
        total_cost = sum(simulated_cohort.simOutputs.totalCosts)

        average_cost = total_cost/D.POP_SIZE

        # store costs for use in CEA
        self.costs.append(average_cost)

        # average BMI by year
        effect_values = simulated_cohort.simOutputs.pathAveBMIs.get_values()

        # represent RCT effect (skip index 0 because that's baseline)
        rct_effect = effect_values[1] + effect_values[2]
        # represent 10 year effect
        ten_year_effect = (effect_values[1] + effect_values[2] +
                           effect_values[3] + effect_values[4] +
                           effect_values[5] + effect_values[6] +
                           effect_values[7] + effect_values[8] +
                           effect_values[9] + effect_values[10])

        # do NOT need to divide by pop size because values are already an average over the cohort
        # average_rct_effect = rct_effect/D.YEARS_RCT
        average_effect_ten_years = ten_year_effect/D.SIM_DURATION

        # print("AVERAGE 10 year EFFECT:", average_effect_ten_years)
        # print("TOTAL RCT EFFECT (sum of year 1 and 2 avg. bmi)", rct_effect)

        # store all cohort effects for use in CEA
        # EFFECT FOR 2 YEARS RCT
        # self.effects.append(average_rct_effect)
        # EFFECT FOR 10 YEARS SIM
        self.effects.append(average_effect_ten_years)

        # EXPENDITURES
        # total expenditures over 10 years (for cohort)
        total_expenditures = sum(simulated_cohort.simOutputs.totalExpenditures)
        # average expenditure per year (over 10 years)
        annual_avg_expenditure = total_expenditures/D.SIM_DURATION
        # total expenditure per person over 10 years
        individual_total_expenditure = total_expenditures/D.N_CHILDREN_BB
        # average expenditure per year PER PERSON (over 10 years)
        individual_annual_expenditure = annual_avg_expenditure/D.N_CHILDREN_BB
        # store average expenditures
        self.expenditures.append(individual_annual_expenditure)
        # store total expenditures
        self.totalExpenditures.append(total_expenditures)
        # store individual expenditure over 10 years
        self.individualTotalExpenditure.append(individual_total_expenditure)


def simulate_this_cohort(cohort, sim_duration):
    """
    :param cohort: a cohort of patients
    :param sim_duration: simulation length
    :return: cohort after being simulated
    """

    # simulate and return the cohort
    cohort.simulate(sim_duration)
    return cohort



