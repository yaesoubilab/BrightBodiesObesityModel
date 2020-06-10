from ModelEntities import Cohort
import SimPy.RandomVariateGenerators as RVGs
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

        self.pathsOfPopSize = []
        self.pathsOfBMIs = []
        self.popPyramidAtStart = []

        # for CEA
        # list of total intervention costs for all participants over entire sim duration, per cohort
        # TODO: I think this is the variable you are using in CEA so
        #  it should include both intervention cost and obesity-related HC costs. Is that right?
        self.costs = []
        # list of the average effect (BMI) over entire sim duration, per cohort
        self.effects = []

        # list of average HC expenditures per year per person over entire sim duration, per cohort
        # Annual Average Individual Expenditure
        self.expenditures = []

        # list of total expenditures for all people over 10 years, per cohort
        # Average Total Expenditure
        self.totalExpenditures = []

        # list of individual expenditures over 10 years
        # Average Individual Expenditure
        self.individualTotalExpenditure = []

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort """

        # store sample path of cohort population size
        self.pathsOfPopSize.append(simulated_cohort.simOutputs.pathPopSize)
        # store sample path of cohort average BMI
        self.pathsOfBMIs.append(simulated_cohort.simOutputs.pathAveBMIs)
        # store sample path of cohort population pyramid at time 0
        self.popPyramidAtStart.append(simulated_cohort.simOutputs.pyramids[0])

    # for CEA

        # COST (Intervention Costs)

        # sum cost per year for all participants to get total cohort cost over sim duration
        total_cost = sum(simulated_cohort.simOutputs.annualTotalInterventionCosts)
        # average cost per person (of intervention/control)
        average_cost = total_cost/D.POP_SIZE

        # store costs for use in CEA
        self.costs.append(average_cost)

        # EFFECT (BMI unit change)

        # average BMI by year (list of 10 BMI values)
        effect_values = simulated_cohort.simOutputs.pathAveBMIs.get_values()

        # represent 10 year effect (sum of 10 avg BMI values)
        ten_year_effect_total = (effect_values[1] + effect_values[2] +
                           effect_values[3] + effect_values[4] +
                           effect_values[5] + effect_values[6] +
                           effect_values[7] + effect_values[8] +
                           effect_values[9] + effect_values[10])

        # average effect of the cohort over 10 years (average BMI)
        average_effect_ten_years = ten_year_effect_total/D.SIM_DURATION

        # Store cohort effect: average BMI for 10 YEAR SIM
        self.effects.append(average_effect_ten_years)

        # EXPENDITURE
        # TODO: There is still something confusing about the name of these variables
        #   Maybe we should use 'cohort' instead of 'total' whenever we are referring to
        #   the cost or expenditure of the cohort.
        #   for example, 'annualCohortHCExpenditures' instead of 'annualTotalHCExpenditures'
        #   And reserve 'total' for when we sum over the entire simulation horizon        #
        #   And maybe whenever we average over individuals, we add 'ave' to the variable name
        #   for example, 'aveIndividualTotalExpenditure' instead of 'individualTotalExpenditure'

        # total expenditures over 10 years (for cohort) ~700,000
        total_expenditures = sum(simulated_cohort.simOutputs.annualTotalHCExpenditures)
        # average expenditure per year (over 10 years) ~70,000
        annual_avg_expenditure = total_expenditures/D.SIM_DURATION
        # total expenditure per person over 10 years ~7700
        individual_total_expenditure = total_expenditures/D.N_CHILDREN_BB
        # average expenditure per year PER PERSON (over 10 years) ~770
        individual_annual_expenditure = annual_avg_expenditure/D.N_CHILDREN_BB
        # store annual average individual expenditure
        self.expenditures.append(individual_annual_expenditure)
        # store total expenditure
        self.totalExpenditures.append(total_expenditures)
        # store individual total expenditure over 10 years
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



