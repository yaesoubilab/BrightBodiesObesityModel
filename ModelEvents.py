from enum import Enum
import InputData as D
from SimPy.DiscreteEventSim import SimulationEvent as Event


class Priority(Enum):
    """ priority of events (low number implies higher priority)"""
    BIRTH = 0
    POP_SURVEY = 1
    BMI_SURVEY = 2


class Birth(Event):
    def __init__(self, time, individual, cohort):
        """
        creates the birth of an individual
        :param time: sim time
        :param individual: individual
        :param cohort: cohort
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


class BMISurvey(Event):
    def __init__(self, time, individual, cohort):
        """
        Tests the age/sex characteristics of simulated population (pyramid)
        """
        # initialize master class
        Event.__init__(self, time=time, priority=Priority.BMI_SURVEY.value)

        self.individual = individual
        self.cohort = cohort

        # trace
        self.cohort.trace.add_message(
            'Average BMI of ' + str(cohort) + ' was assessed at {t:.{deci}f}.'.format(t=time, deci=D.DECI))

    def process(self):
        """ processes the population distribution test """

        self.cohort.process_bmi()


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
        """ processes the population distribution test at initialization """

        self.cohort.process_pop_survey()
