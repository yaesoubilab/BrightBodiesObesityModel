from enum import Enum

from deampy.discrete_event_sim import SimulationEvent as Event


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

    def process(self, rng=None):
        """ processes birth of a new individual """

        self.cohort.process_birth(individual=self.individual)


class BMISurvey(Event):
    def __init__(self, time, individual, cohort):
        """
        tests the age/sex characteristics of simulated population (pyramid)
        """
        # initialize master class
        Event.__init__(self, time=time, priority=Priority.BMI_SURVEY.value)

        self.individual = individual
        self.cohort = cohort

    def process(self, rng=None):
        """ processes the population distribution test """

        self.cohort.process_cohort_outcomes()


class PopSurvey(Event):
    def __init__(self, time, individual, cohort):
        """
        tests the age/sex characteristics of simulated population (pyramid)
        """
        # initialize master class
        Event.__init__(self, time=time, priority=Priority.POP_SURVEY.value)

        self.individual = individual
        self.cohort = cohort

    def process(self, rng=None):
        """ processes the population distribution test at initialization """

        self.cohort.process_pop_survey()
