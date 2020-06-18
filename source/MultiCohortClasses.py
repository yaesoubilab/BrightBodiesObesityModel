from source.ModelEntities import Cohort
import SimPy.RandomVariateGenerators as RVGs
import InputData as D
from source.ModelParameters import ParamGenerator
import multiprocessing as mp
import SimPy.StatisticalClasses as Stat


class MultiCohort:
    """ simulates multiple cohorts """

    def __init__(self, ids, intervention, maintenance_scenario):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param intervention: intervention to simulate
        :param maintenance_scenario: maintenance scenario to simulate
        """

        self.ids = ids
        self.param_sets = []  # list of parameter sets (for each cohort)

        # cohort outcomes
        self.multiSimOutputs = MultiSimOutputs()

        # create parameter sets
        self.__populate_parameter_sets(intervention=intervention,
                                       maintenance_scenario=maintenance_scenario)

    def simulate(self, sim_duration, if_run_in_parallel=False):
        """ simulates all cohorts
        :param sim_duration: simulation duration
        :param if_run_in_parallel: set to True to run the cohorts in parallel
        """

        if not if_run_in_parallel:
            for i in range(len(self.ids)):

                # create cohort
                cohort = Cohort(id=self.ids[i], parameters=self.param_sets[i])

                # simulate the cohort
                cohort.simulate(sim_duration=sim_duration)

                # outcomes from simulating all cohorts
                self.multiSimOutputs.extract_outcomes(simulated_cohort=cohort)

        else:  # if run cohorts in parallel
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

        # create a parameter generator
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

        self.pathsOfCohortPopSize = []  # (list of list) sample paths of cohort population size
        self.pathsOfCohortAveBMI = []   # (list of list) sample paths of cohort BMI
        self.popPyramidAtStart = []     # (list of pyramids) population pyramid of cohorts at initialization
        self.changeInBMIByYear = []     # (list of list) change in cohort BMI by year with respect to the baseline

        # for CEA
        # effect: average cohort BMI over the entire sim duration
        self.effects = []   # (list) of effect from each simulated cohort

        # cost: total cost (including the intervention costs and HC expenditures) for all participants
        #       over the entire simulation duration.
        self.costs = []     # (list) of costs from each simulated cohort

        # list of intervention costs for all participants over entire sim duration, per cohort
        self.cohortInterventionCosts = []

        # list of average HC expenditures per year per person over entire sim duration, per cohort
        # Annual Average Individual Expenditure
        self.individualAvgExpenditure = []

        # list of total expenditures for all people over 10 years, per cohort
        # Total Expenditure
        self.cohortTenYearExpenditure = []

        # list of individual expenditures over 10 years
        # Average Individual Expenditure
        self.individualTenYearExpenditure = []

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort """

        # store sample path of cohort population size
        self.pathsOfCohortPopSize.append(simulated_cohort.simOutputs.pathPopSize)
        # store sample path of cohort average BMI
        self.pathsOfCohortAveBMI.append(simulated_cohort.simOutputs.pathAveBMIs)
        # store sample path of cohort population pyramid at time 0
        self.popPyramidAtStart.append(simulated_cohort.simOutputs.pyramids[0])
        # store the change in BMI by year
        d_bmi = []
        bmi0 = simulated_cohort.simOutputs.pathAveBMIs.get_values()[0]
        for bmi in simulated_cohort.simOutputs.pathAveBMIs.get_values():
            d_bmi.append(bmi - bmi0)
        self.changeInBMIByYear.append(d_bmi)

    # for CEA

        # COSTS: Intervention Costs + HC Expenditure
        # store costs for use in CEA

        # sum cost per year for all participants to get total cohort cost over sim duration
        cohort_intervention_cost = sum(simulated_cohort.simOutputs.annualCohortInterventionCosts)
        cohort_expenditure = sum(simulated_cohort.simOutputs.annualCohortHCExpenditures)
        # average cost per person (of intervention/control)
        average_intervention_cost_per_person = cohort_intervention_cost/D.POP_SIZE
        average_expenditure_per_person = cohort_expenditure/D.POP_SIZE

        # sum average IC per person and average HC per person
        total_cost = average_intervention_cost_per_person + average_expenditure_per_person
        # self.costs.append(average_intervention_cost_per_person)
        self.costs.append(total_cost)

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

        # INTERVENTION COSTS:
        self.cohortInterventionCosts.append(average_intervention_cost_per_person)

        # EXPENDITURE

        # total expenditure over 10 years (for cohort) ~700,000
        cohort_10yr_expenditure = sum(simulated_cohort.simOutputs.annualCohortHCExpenditures)
        # average expenditure per year (over 10 years) ~70,000
        cohort_avg_expenditure = cohort_10yr_expenditure/D.SIM_DURATION
        # total expenditure per person over 10 years ~7700
        individual_10yr_expenditure = cohort_10yr_expenditure/D.N_CHILDREN_BB
        # average expenditure per year PER PERSON (over 10 years) ~770
        individual_avg_expenditure = cohort_avg_expenditure/D.N_CHILDREN_BB
        # store annual average individual expenditure
        self.individualAvgExpenditure.append(individual_avg_expenditure)
        # store total expenditure of cohort for 10 years
        self.cohortTenYearExpenditure.append(cohort_10yr_expenditure)
        # store individual expenditure over 10 years
        self.individualTenYearExpenditure.append(individual_10yr_expenditure)

    def get_mean_interval_change_in_bmi(self, year, deci=None):

        data = []
        for bmi_change_by_year in self.changeInBMIByYear:
            data.append(bmi_change_by_year[year])

        stat = Stat.SummaryStat(
            name='Change in BMI with respect to the baseline',
            data=data
        )

        if deci is None:
            return stat.get_mean(), stat.get_PI(alpha=0.05)
        else:
            return stat.get_formatted_mean_and_interval(interval_type='p', deci=deci)


def simulate_this_cohort(cohort, sim_duration):
    """
    :param cohort: a cohort of patients
    :param sim_duration: simulation length
    :return: cohort after being simulated
    """

    # simulate and return the cohort
    cohort.simulate(sim_duration)
    return cohort



