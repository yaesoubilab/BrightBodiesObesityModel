import SimPy.SamplePathClasses as Path
from math import floor
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
        self.pyramids = []  # empty list to be populated with pyramids
        self.pyramidPercentage = []  # group percentages

        self.bmiTimeStep = []
        self.pathBMIs = Path.PrevalenceSamplePath(name='BMIs',
                                                  initial_size=0,
                                                  sim_rep=sim_rep,
                                                  collect_stat=False)

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

        # increment population size by 1 after a birth
        self.popSize += 1
        self.pathPopSize.record_increment(time=self.simCal.time, increment=1)

    def collect_bmi(self):
        """
        collect bmi for each individual to calculate average
        """
        index_by_time = floor(self.simCal.time)

        average_bmi = (sum(self.bmiTimeStep))/D.POP_SIZE

        self.pathBMIs.record_value(time=index_by_time, value=average_bmi)


