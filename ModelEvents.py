from enum import Enum
import InputData as D
from SimPy.DiscreteEventSim import SimulationEvent as Event


class Priority(Enum):
    """ priority of events (low number implies higher priority)"""
    BIRTH = 1
    DEATH = 0
    POP_SURVEY = 2
    # EVALMORT = 2


class Birth(Event):
    def __init__(self, time, individual, cohort, if_schedule_birth):
        """
        creates the birth of an individual
        :param time: sim time
        :param individual: individual
        :param cohort: cohort
        :param if_schedule_birth: schedule next births (T/F)
        """
        # initialize the master class
        Event.__init__(self, time=time, priority=Priority.BIRTH.value)

        self.individual = individual
        self.cohort = cohort
        self.ifScheduleBirth = if_schedule_birth

        # trace
        self.cohort.trace.add_message(
            str(individual) + ' will be born at {t:.{deci}f}.'.format(t=time, deci=D.DECI))

    def process(self):
        """ processes birth of a new individual """

        self.cohort.process_birth(individual=self.individual,
                                  if_schedule_birth=self.ifScheduleBirth)


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


class PopSurvey(Event):
    def __init__(self, time, individual, cohort):
        """
        Tests the age/sex characteristics of simulated population (pyramid)
        """
        # initialize master class
        Event.__init__(self, time=time, priority=Priority.POP_SURVEY.value)

        self.individual = individual
        self.cohort = cohort

    def process(self):
        """ processes the population distribution test """

        self.cohort.process_pop_survey()


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

