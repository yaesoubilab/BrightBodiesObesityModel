import SimPy.SamplePathClasses as Path
import InputData as D
import ModelParameters as P


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
        #
        self.annualBMIs = []
        self.pathBMIs = Path.PrevalenceSamplePath(name='BMIs',
                                                  initial_size=0,
                                                  sim_rep=sim_rep,
                                                  collect_stat=False)
        self.annualCosts = []
        self.cost = []
        self.effect = []

    def collect_end_of_sim_stat(self):
        """
        collects the performance statistics at the end of this replication
        """

        # update sample paths
        self.pathPopSize.record_increment(time=self.simCal.time, increment=0)

    # # COST for CEA
    #     # if the intervention is BB...
    #     if D.Interventions.BRIGHT_BODIES:
    #         # cost = cost of BB per person * number of individuals in cohort
    #         cost = D.cost_BB * D.POP_SIZE
    #     # if the intervention is CC...
    #     else:
    #         cost = D.cost_CC * D.POP_SIZE
    #     # store cost of this cohort
    #     self.cost.append(cost)
    #     print('Total cost:', cost)
    # EFFECT for CEA
        effect_values = self.pathBMIs.get_values()
        effect = sum(effect_values)
        self.effect.append(effect)
        print('Total effect (sum of BMIs):', effect)

    def collect_birth(self):
        """
        collect statistics on the birth of this individual
        """

        # increment population size by 1 after a birth
        self.popSize += 1
        self.pathPopSize.record_increment(time=self.simCal.time, increment=1)

    def collect_bmi(self, BMIs):
        """
        calculate average bmi of cohort at each time step
        """

        # average BMI
        average_bmi = sum(BMIs)/len(BMIs)

        self.pathBMIs.record_value(time=int(self.simCal.time), value=average_bmi)

    def collect_cost(self, costs):
        cohort_cost_total = sum(costs)
        self.annualCosts.append(cohort_cost_total)


