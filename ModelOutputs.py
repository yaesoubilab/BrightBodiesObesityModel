import SimPy.SamplePathClasses as Path


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
                                                     collect_stat=False)

        # TODO: Will the first two variables hold
        #  the intervention cost and HC expenditure
        #  of the cohort during years of the simulation?
        # totalCosts: list that holds the cost of all of the cohorts
        self.totalCosts = []
        # totalExpenditures: list that holds the expenditures
        self.totalExpenditures = []
        # effects_cohort: list of average BMI over simulation for given cohort
        self.effects_cohort = []

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

        # average BMI
        average_bmi = sum(BMIs)/len(BMIs)

        self.pathAveBMIs.record_value(time=int(self.simCal.time), value=average_bmi)

        # EFFECT for CEA: Average BMI over Simulation Horizon

        # TODO: I am a little confused about how effect is being calculate,
        #   let's talk about it.

        # effect_values: list of average BMI for cohort at each time step
        effect_values = self.pathAveBMIs.get_values()

        # effect: average BMI for cohort over entire sim duration
        effect = sum(effect_values)

        # effects: list of average BMI for each cohort
        self.effects_cohort.append(effect)

    def collect_cost(self, costs, expenditures):
        """
        :param costs: (list) of costs of each individual per year of sim time
        :param expenditures: (list) of annual health care expenditures for each individual
        """

        # cohort_cost_total: sum of each person's cost in a given cohort (by year)
        cohort_cost_total = sum(costs)
        print('cost total', cohort_cost_total)

        # totalCosts: list of cohort cost per year (to get total cost)
        self.totalCosts.append(cohort_cost_total)

        # EXPENDITURES
        cohort_expenditure_total = sum(expenditures)
        print('expenditure total', cohort_expenditure_total)

        # totalExpenditures: list of cohort expenditure totals per year (to get total expenditure)
        self.totalExpenditures.append(cohort_expenditure_total)


