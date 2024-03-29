import multiprocessing as mp

import deampy.random_variats as RVGs
import deampy.statistics as Stat
from yom.ModelEntities import Cohort


class MultiCohort:
    """ simulates multiple cohorts """

    def __init__(self, ids, parameter_generator):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param parameter_generator: an instance of ParamGenerator
        """

        self.ids = ids
        self.inputs = parameter_generator.modelInputs
        self.param_sets = []  # list of parameter sets (for each cohort)

        # cohort outcomes
        self.multiSimOutputs = MultiSimOutputs()

        # create parameter sets
        self.__populate_parameter_sets(parameter_generator=parameter_generator)

    def simulate(self, sim_duration, if_run_in_parallel=False):
        """ simulates all cohorts
        :param sim_duration: simulation duration
        :param if_run_in_parallel: set to True to run the cohorts in parallel
        """

        if not if_run_in_parallel:
            for i in range(len(self.ids)):

                # create cohort
                cohort = Cohort(id=self.ids[i], model_inputs=self.inputs, parameters=self.param_sets[i])

                # simulate the cohort
                cohort.simulate(sim_duration=sim_duration)

                # outcomes from simulating all cohorts
                self.multiSimOutputs.extract_outcomes(simulated_cohort=cohort)

        else:  # if run cohorts in parallel
            # create cohorts
            cohorts = []
            for i in range(len(self.ids)):
                cohorts.append(Cohort(id=self.ids[i],
                                      model_inputs=self.inputs,
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

        # calculate summary statistics
        self.multiSimOutputs.calculate_summary_stats()

    def __populate_parameter_sets(self, parameter_generator):
        """
        populates parameters for the specified intervention and effect maintenance assumption
        """

        # create as many sets of parameters as the number of cohorts
        for i in range(len(self.ids)):
            # create new rng for each parameter set
            rng = RVGs.RNG(seed=i)
            # get and store new set of parameters
            self.param_sets.append(parameter_generator.get_new_parameters(rng=rng))


class MultiSimOutputs:

    def __init__(self):

        self.statEffect = None          # cohort average BMI over the simulation period
        self.statCohortCost = None      # cohort total cost over the simulation period
        self.statCohortInterventionCost = None  # cohort intervention cost over the simulation period
        self.statCohortHCExpenditure = None     # cohort health care expenditure over the simulation period

        self.pathsOfCohortPopSize = []  # (list of list) sample paths of cohort population size
        self.pathsOfCohortAveBMI = []   # (list of list) sample paths of cohort BMI
        self.popPyramidAtStart = []     # (list of pyramids) population pyramid of cohorts at initialization
        # (list of list) change in cohort average BMI by year with respect to the baseline
        self.changeInCohortAveBMIByYear = []

        # for CEA
        # effect: average cohort BMI over the entire sim duration
        self.effects = []   # (list) of effect from each simulated cohort

        # cost: total cost (including the intervention costs and HC expenditures) for all participants
        #       over the entire simulation duration.
        self.cohortCosts = []     # (list) of costs from each simulated cohort
        self.aveIndividualCosts = []  # (list) of average individual cost in each simulated cohort

        # intervention costs for all participants over entire simulation duration
        self.cohortInterventionCosts = []
        self.aveIndividualInterventionCosts = []

        # list of total health care expenditures for all people over the simulation
        self.cohortHealthCareExpenditure = []
        self.aveIndividualHCExpenditure = []

        # list of lists of cumulative average individual costs in all cohorts
        self.cumAveIndividualCosts = []

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort """

        pop_size = simulated_cohort.simOutputs.popSize

        # store sample path of cohort population size
        self.pathsOfCohortPopSize.append(simulated_cohort.simOutputs.pathPopSize)
        # store sample path of cohort average BMI
        self.pathsOfCohortAveBMI.append(simulated_cohort.simOutputs.pathAveBMIs)
        # store sample path of cohort population pyramid at time 0
        self.popPyramidAtStart.append(simulated_cohort.simOutputs.pyramids[0])

        # store the change in cohort average BMI by year
        d_bmi = []  # changes in average BMI of this cohort (year 0 to 0, year 1 to 0, year 2 to 0, etc.)
        bmi0 = simulated_cohort.simOutputs.pathAveBMIs.get_values()[0]  # average BMI at time 0
        for bmi in simulated_cohort.simOutputs.pathAveBMIs.get_values():
            d_bmi.append(bmi - bmi0)
        self.changeInCohortAveBMIByYear.append(d_bmi)

        # for CEA
        # EFFECT (BMI unit change)
        # average cohort BMI over the simulation period
        self.effects.append(simulated_cohort.simOutputs.pathAveBMIs.stat.get_mean())

        # COSTS: Intervention Costs + HC Expenditure
        self.cohortCosts.append(simulated_cohort.simOutputs.totalCost)
        self.aveIndividualCosts.append(simulated_cohort.simOutputs.totalCost / pop_size)

        # cohort intervention costs
        cohort_intervention_cost = sum(simulated_cohort.simOutputs.annualCohortInterventionCosts)
        self.cohortInterventionCosts.append(cohort_intervention_cost)
        self.aveIndividualInterventionCosts.append(cohort_intervention_cost / pop_size)
        # cohort health care expenditure
        cohort_hc_expenditure = sum(simulated_cohort.simOutputs.annualCohortHCExpenditures)
        self.cohortHealthCareExpenditure.append(cohort_hc_expenditure)
        self.aveIndividualHCExpenditure.append(cohort_hc_expenditure / pop_size)

        # list of lists of cost by year

        cum_ave_individual_cost = [c/pop_size for c in simulated_cohort.simOutputs.cumulativeCohortCost]
        self.cumAveIndividualCosts.append(cum_ave_individual_cost)

    def calculate_summary_stats(self):

        self.statEffect = Stat.SummaryStat(name='Effect', data=self.effects)
        self.statCohortCost = Stat.SummaryStat(name='Cohort cost', data=self.cohortCosts)
        self.statCohortInterventionCost = Stat.SummaryStat(
            name='Cohort intervention cost', data=self.cohortInterventionCosts)
        self.statCohortHCExpenditure = Stat.SummaryStat(
            name='Cohort health care expenditure', data=self.cohortHealthCareExpenditure)

    def get_mean_interval_change_in_bmi(self, year, deci=None):
        """
        :param year: (int) year at which the changes should be calculated with respect to the baseline
        :param deci: (float) the decimal number to round the numbers to
        :return: (mean, 95% uncertainty interval) of change in BMI with respect to the baseline
        """

        data = []
        for bmi_change_by_year in self.changeInCohortAveBMIByYear:
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



