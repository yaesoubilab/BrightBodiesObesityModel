import SimPy.SamplePathClasses as Path
import InputData as D
import SimPy.StatisticalClasses as Stat


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
        # TODO: I found what is happening in this class a little confusing and maybe could be
        #       simplified a little.

        # TODO: I am not sure what we need this.
        #       You are updating it from outside but I am not sure if we ever use it,
        self.annualBMIs = []

        # TODO: maybe this should be renamed to self.pathAveBMIs to make it explicit that
        #       the sample path here is the average BMI of the population over time
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

        # effect for CEA
        effect_values = self.pathBMIs.get_values()
        # TODO: isn't the effect the average BMI over the simulation horizon?
        effect = sum(effect_values)
        self.effect.append(effect)
        # print('Total effect (sum of BMIs):', effect)

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
        :param BMIs: (list) of the population's BMIs
        """

        # average BMI
        average_bmi = sum(BMIs)/len(BMIs)

        self.pathBMIs.record_value(time=int(self.simCal.time), value=average_bmi)

    def collect_cost(self, costs):
        cohort_cost_total = sum(costs)
        # print('cost total', cohort_cost_total)
        cost_per_person = cohort_cost_total/D.POP_SIZE
        # print('cost pp', cost_per_person)
        self.annualCosts.append(cost_per_person)


