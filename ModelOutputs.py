import SimPy.SamplePathClasses as Path
import InputData as D


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

        # totalCosts: list that holds the cost of all of the cohorts
        self.totalCosts = []
        # effects_cohort: list of average BMI over simulation for given cohort
        self.effects_cohort = []

    def collect_end_of_sim_stat(self):
        """
        collects the performance statistics at the end of this replication
        """

        # update sample paths
        self.pathPopSize.record_increment(time=self.simCal.time, increment=0)

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

        # effect_values: list of average BMI for cohort at each time step
        effect_values = self.pathAveBMIs.get_values()
        # print("effect values", effect_values)
        # print(len(effect_values))

        # Calculate Effect: Average BMI over Simulation Time Horizon for given cohort

        # effect: average BMI for cohort over entire sim duration
        # effect = (sum(effect_values))/D.SIM_DURATION
        effect = sum(effect_values)
        # print('Sum of avg. BMIs over sim:', effect)

        # effects: list of average BMI for each cohort
        self.effects_cohort.append(effect)

    def collect_cost(self, costs):
        """
        :param costs: (list) of costs of each individual per year of sim time
        ex. [532, 588, 588, ...]
        """

        # cohort_cost_total: sum of each person's cost in a given cohort (by year)
        cohort_cost_total = sum(costs)
        print('cost total', cohort_cost_total)
        cost_per_person = cohort_cost_total/D.N_CHILDREN_BB
        print('cost pp', cost_per_person)

        # COST: list of cohort cost per year (to get total cost)
        # self.totalCosts.append(cost_per_person)
        self.totalCosts.append(cohort_cost_total)


