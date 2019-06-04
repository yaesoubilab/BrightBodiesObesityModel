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
        self.pyramids = []  # empty list to be populated with pyramids
        self.pyramidPercentage = []  # group percentages

    def collect_end_of_sim_stat(self):
        """
        collects the performance statistics at the end of this replication
        """

        # update sample paths
        self.pathPopSize.record_increment(time=self.simCal.time, increment=0)

    def collect_birth(self, individual):
        """
        collect statistics on the birth of this individual
        """
        # record time of birth
        # individual.tBirth = self.simCal.time

        # increment population size by 1 after a birth
        self.popSize += 1
        self.pathPopSize.record_increment(time=self.simCal.time, increment=1)

    def collect_death(self, individual):
        """
        collect statistics on the death of this individual
        """

        individual.ifAlive = False

        # decrement population size by 1 after a death
        self.popSize -= 1
        self.pathPopSize.record_increment(time=self.simCal.time, increment=-1)



