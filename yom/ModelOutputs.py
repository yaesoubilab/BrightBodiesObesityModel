import deampy.sample_path as Path


class SimOutputs:
    # to collect the outputs of a simulation run

    def __init__(self, sim_cal, sim_rep, trace_on=False):
        """
        :param sim_cal: simulation calendar
        :param sim_rep: simulation replication
        :param trace_on: set to True to report patient summary
        """

        self.simCal = sim_cal       # simulation calendar
        self.traceOn = trace_on     # if should prepare patient summary report

        self.popSize = 0    # current population size
        self.pathPopSize = Path.PrevalenceSamplePath(name='Population size',
                                                     initial_size=0,
                                                     sim_rep=sim_rep,
                                                     collect_stat=False)

        self.pyramids = []  # population pyramids over time (% of population in each age-sex group)

        # sample path: average BMI of population over time
        self.pathAveBMIs = Path.PrevalenceSamplePath(name='BMIs',
                                                     initial_size=0,
                                                     sim_rep=sim_rep,
                                                     collect_stat=True,
                                                     ave_method='linear')

        # cohort intervention cost by year
        self.annualCohortInterventionCosts = []
        # cohort health care expenditure costs by year
        self.annualCohortHCExpenditures = []
        # cohort total cumulative cost by each year
        self.cumulativeCohortCost = []
        # average individual health care expenditure costs by year
        self.annualIndividualHCExpenditures = []
        # cohort total cost
        self.totalCost = 0

        # half cycle correction
        self.listAnnualCostValues = []
        self.hccCostValues = []

    def collect_end_of_sim_stat(self):
        """
        collects the performance statistics at the end of this replication
        """

        # close sample paths
        self.pathPopSize.close(time=self.simCal.time)

    def collect_birth(self):
        """
        collect statistics on the birth of this individual
        """

        # increment population size by 1 after a birth
        self.popSize += 1
        self.pathPopSize.record_increment(time=self.simCal.time, increment=1)

    def collect_bmi(self, BMIs):
        """
        calculate average bmi of cohort at this time step
        :param BMIs: (list) of the population's BMIs at the current time step
        """

        # average BMI of cohort
        average_bmi = sum(BMIs)/len(BMIs)

        self.pathAveBMIs.record_value(time=int(self.simCal.time), value=average_bmi)

    def collect_costs_of_this_period(self, intervention_cost, hc_expenditure, cohort_size):
        """
        :param intervention_cost: cohort intervention cost in this year
        :param hc_expenditure: cohort health care expenditures at this year
        :param cohort_size: size of this cohort
        """

        # list of cohort cost per year (to get total cost)
        self.annualCohortInterventionCosts.append(intervention_cost)

        # list of cohort expenditure totals per year (to get total expenditure)
        self.annualCohortHCExpenditures.append(hc_expenditure)

        # list of cohort total cumulative cost by this year
        cum = 0
        if len(self.cumulativeCohortCost) > 0:
            cum = self.cumulativeCohortCost[-1]
        self.cumulativeCohortCost.append(intervention_cost + hc_expenditure + cum)

        # list of individual expenditure totals per year (to get total expenditure per individual)
        self.annualIndividualHCExpenditures.append(hc_expenditure / cohort_size)

        # update total cohort cost
        self.totalCost += intervention_cost + hc_expenditure
