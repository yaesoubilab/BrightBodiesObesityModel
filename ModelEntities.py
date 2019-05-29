import SimPy.DiscreteEventSim as SimCls
import SimPy.SimulationSupport as Sim
import SimPy.RandomVariantGenerators as RVGs
import ModelEvents as E
import InputData as D
import ModelOutputs as O
from SimPy.DataFrames import Pyramid
from SimPy.Plots import PopulationPyramids as Pyr

import math
import ModelParameters as P
import SimPy.InOutFunctions as IO


class Individual:
    def __init__(self, id, age_sex, sim_time):
        """ create an individual
        :param id: (integer) patient ID
        :param age_sex: [age, sex]
        :param sim_time: simulation time
        """
        self.id = id
        self.sex = age_sex[1]
        self.tBirth = sim_time - age_sex[0]    # time of birth

    def __str__(self):
        return "Individual {0}".format(self.id)

    def get_age(self, current_time):
        return current_time - self.tBirth


class Cohort:
    def __init__(self, id, parameters):
        """ creates a cohort of individuals
        :param id: ID of this cohort
        :param parameters: parameters of this cohort
        """

        self.id = id
        self.rng = RVGs.RNG(seed=id)
        self.params = parameters

        self.individuals = []       # list of individuals
        self.simCal = SimCls.SimulationCalendar()  # simulation calendar
        # simulation outputs
        self.simOutputs = O.SimOutputs(sim_cal=self.simCal, sim_rep=id, trace_on=D.TRACE_ON)
        # simulation trace
        self.trace = Sim.DiscreteEventSimTrace(sim_calendar=self.simCal,
                                               if_should_trace=D.TRACE_ON,
                                               deci=D.DECI)

    def __initialize(self):
        """ initialize the cohort """

        # age_sex = self.params.ageSexDist.sample_values(rng=self.rng)

        for i in range(D.POP_SIZE):

            # find the age and sex of this individual
            age_sex = self.params.ageSexDist.sample_values(rng=self.rng)

            # TODO: I think as you also pointed out, the issue here is that we are scheduling a lot of
            #  births right at time 0. I think you should modify the Birth event so that we can specify
            #  whether it should schedule the next birth or not.
            #  Now, if a birth is scheduled as part of the initialization, it should not schedule
            #  another birth when processed.

            # schedule the first birth
            self.simCal.add_event(
                event=E.Birth(time=0.0000001*i,
                              individual=Individual(id=i, age_sex=age_sex, sim_time=self.simCal.time),
                              cohort=self))

        # TODO: since now the Birth events we schedule above will not schedule any new births,
        #  we need to reschedule our first birth here:

        # find the time until next birth and schedule it


        # schedule population distribution test event at t=.1 and t=1
        self.simCal.add_event(
            event=E.PopSurvey(time=.1,
                              individual=self,
                              cohort=self))
        self.simCal.add_event(
            event=E.PopSurvey(time=1,
                              individual=self,
                              cohort=self))

    def simulate(self, sim_duration):
        """ simulate the cohort
        :param sim_duration: duration of simulation (years)
         """

        # initialize the simulation
        self.__initialize()

        # while there is an event scheduled in the simulation calendar
        # and the simulation time is less than the simulation duration
        while self.simCal.n_events() > 0 and self.simCal.time <= sim_duration:
            self.simCal.get_next_event().process()

        # collect the end of simulation statistics
        self.simOutputs.collect_end_of_sim_stat()

    def process_birth(self, individual):
        """
        process the birth of a new individual
        """

        # trace
        self.trace.add_message(
            'Processing the birth of ' + str(individual) + '.')

        # collect statistics on new birth
        self.simOutputs.collect_birth(individual=individual)

        # add the new person to the population
        self.individuals.append(individual)

        # find the time of death
        time_to_death = self.params.mortalityModel.sample_time_to_death(group=individual.sex,
                                                                        age=individual.get_age(self.simCal.time),
                                                                        rng=self.rng)
        time_death = self.simCal.time + time_to_death

        # schedule the the death of this person
        self.simCal.add_event(
            event=E.Death(
                time=time_death,
                individual=individual,
                cohort=self
            )
        )

        sex = D.SEX.MALE.value  # sex set to male
        # TODO: make 0.5075 a model input (add to the InputData.py)
        if self.rng.sample() < 0.5075:  # prob of being female
            sex = D.SEX.FEMALE.value

        # find the time of next birth
        time_next_birth = self.simCal.time + self.params.timeToNextBirthDist.sample(rng=self.rng)

        # schedule the next birth
        self.simCal.add_event(
            event=E.Birth(
                time=time_next_birth,
                individual=Individual(id=individual.id + 1, age_sex=[0, sex], sim_time=self.simCal.time),
                cohort=self
            )
        )

    def process_death(self, individual):
        """
        process the death of an individual
        """

        # trace
        self.trace.add_message(
            'Processing the death of ' + str(individual) + '.')

        # collect statistics on new birth
        self.simOutputs.collect_death(individual=individual)

    def process_pop_survey(self):
        """
        processes the population distribution pyramid
        """
        pyramid = Pyramid(list_x_min=[0, 0],
                          list_x_max=[100, 1],
                          list_x_delta=[5, 'int'])

        # for each individual, record age/sex and increment pyramid by 1
        for individual in self.individuals:
            pyramid.record_increment(x_values=[individual.get_age(self.simCal.time), individual.sex],
                                     increment=1)

        self.simOutputs.pyramids.append(pyramid)

        # TODO: this is great but I would create figures only after when the simulation is done.
        #  I would move these to Simulate.py or add a new Support.py file to take care of creating figures.
        #  We'll have a lot of them!

        # print time of test
        print('Population stats age/sex at time =', self.simCal.time)
        # get the total population size
        print('Population size:', pyramid.get_sum())
        # get the size of each group
        print('Population size by age, sex:', pyramid.get_values())
        # get the percentage of population in each group
        print('Population distribution by age, sex', pyramid.get_percentage())

        # plot the pyramid
        Pyr.plot_pyramids(observed_data=pyramid.get_percentage(),
                          simulated_data=None,
                          x_lim=10,
                          y_lim=100,
                          title='Population Pyramid at T = ' + str(self.simCal.time))

    # def evaluate_mortality(self, individual):
    #
    #     # trace
    #
    #     age = self.simCal.time - individual.tBirth
    #
    #     # utilize as t and add to time under schedule event mortality
    #     time_to_next_age_break = 5*math.floor(age/5) + 5 - age
    #
    #     # find time until death (time of death - current time)
    #     t = self.params.deathDist.get_dist(x_value=[age, individual.sex]).sample(rng=self.rng) - self.simCal.time
    #     # if time until death is less than time until the next age break (interval)
    #     if t <= time_to_next_age_break:
    #         # schedule death at time t
    #         self.simCal.add_event(
    #             event=E.Death(
    #                 time=self.simCal.time + t,
    #                 individual=individual,
    #                 cohort=self)
    #         )
    #     else: # else schedule Evaluate Mortality event at next age break (interval)
    #         self.simCal.add_event(
    #             event=E.EvaluateMortality(time=self.simCal.time + time_to_next_age_break,
    #                                       individual=individual,
    #                                       cohort=self)
    #         )
    def print_trace(self):
        """ outputs trace """

        # simulation trace
        self.trace.print_trace(filename='Trace-Replication' + str(self.id) + '.txt',
                               directory='Trace',
                               delete_existing_files=True)
