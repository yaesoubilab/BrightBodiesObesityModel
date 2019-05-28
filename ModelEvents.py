from enum import Enum
import InputData as D
from SimPy.DiscreteEventSim import SimulationEvent as Event


class Priority(Enum):
    """ priority of events (low number implies higher priority)"""
    BIRTH = 1
    DEATH = 0
    TESTPOP = 2
    # EVALMORT = 2


class Birth(Event):
    def __init__(self, time, individual, cohort):
        """
        creates the birth of an individual
        """
        # initialize the master class
        Event.__init__(self, time=time, priority=Priority.BIRTH.value)

        self.individual = individual
        self.cohort = cohort

        # trace
        self.cohort.trace.add_message(
            str(individual) + ' will be born at {t:.{deci}f}.'.format(t=time, deci=D.DECI))

    def process(self):
        """ processes birth of a new individual """

        self.cohort.process_birth(individual=self.individual)


class Death(Event):
    def __init__(self, time, individual, cohort):
        """
        creates the death of an individual
        """
        # initialize the master class
        Event.__init__(self, time=time, priority=Priority.DEATH.value)

        self.individual = individual
        self.cohort = cohort

        # trace
        self.cohort.trace.add_message(
            str(individual) + ' will die at {t:.{deci}f}.'.format(t=time, deci=D.DECI))

    def process(self):
        """ processes the death of an individual """

        self.cohort.process_death(individual=self.individual)


class TestPopDistribution(Event):
    def __init__(self, time, individual, cohort):
        """
        Tests the age/sex characteristics of simulated population
        """
        # initialize master class
        Event.__init__(self, time=time, priority=Priority.TESTPOP.value)

        self.individual = individual
        self.cohort = cohort

        # trace

    def process(self):
        """ processes the population distribution test """

        self.cohort.process_testpop(individual=self.individual)

# class EvaluateMortality(Event):
#     def __init__(self, time, individual, cohort):
#         """
#         Evaluates death of individual
#         """
#         # initialize master class
#         Event.__init__(self, time=time, priority=Priority.EVALMORT.value)
#
#         self.individual = individual
#         self.cohort = cohort
#
#         # trace
#         self.cohort.trace.add_message(
#             str(individual) + ' '
#         )
#
#     def process(self):
#         """ """
#
#         self.cohort.evaluate_mortality(individual=self.individual)

