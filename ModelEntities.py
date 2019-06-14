import SimPy.DiscreteEventSim as SimCls
import SimPy.SimulationSupport as Sim
import SimPy.RandomVariantGenerators as RVGs
import ModelEvents as E
import InputData as D
import ModelOutputs as O
from SimPy.DataFrames import Pyramid
import Trajectories as T
from math import floor


class Individual:
    def __init__(self, id, age_sex, bmi_trajectory):
        """ create an individual
        :param id: (integer) patient ID
        :param age_sex: [age, sex]
        :param bmi_trajectory: bmi trajectory for individual (based on age/sex)
        """
        self.id = id
        self.sex = age_sex[1]
        self.initialAge = age_sex[0]
        self.ifAlive = True
        self.trajectory = bmi_trajectory

    def __str__(self):
        return "Individual {0}".format(self.id)

    def get_age(self, current_time):
        """
        :param current_time: current simulation time
        :return: age (current time - age at initialization)
        """
        return current_time + self.initialAge


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

        # baseline population of given population size
        for i in range(D.POP_SIZE):

            # find the age and sex of this individual
            age_sex = self.params.ageSexDist.sample_values(rng=self.rng)

            # time of "birth" (initialization)
            t_birth = D.SIM_INIT * i / D.POP_SIZE

            # find the BMI trajectory
            rows = T.df_trajectories.get_obj(x_value=[age_sex[0], age_sex[1]])
            bmi_trajectory = rows.sample_traj(rng=self.rng)

            # schedule the first "birth" at approximately time 0
            self.simCal.add_event(
                event=E.Birth(time=t_birth,
                              individual=Individual(id=i,
                                                    age_sex=age_sex,
                                                    bmi_trajectory=bmi_trajectory),
                              cohort=self)
            )

        # schedule population distribution survey event right after initialization period
        self.simCal.add_event(
            event=E.PopSurvey(time=D.SIM_INIT,
                              individual=self,
                              cohort=self))
        # schedule at time 1
        self.simCal.add_event(
            event=E.PopSurvey(time=1,
                              individual=self,
                              cohort=self))
        # schedule at time 2
        self.simCal.add_event(
            event=E.PopSurvey(time=2,
                              individual=self,
                              cohort=self))
        # schedule at time 3
        self.simCal.add_event(
            event=E.PopSurvey(time=3,
                              individual=self,
                              cohort=self))
        # schedule at time 4
        self.simCal.add_event(
            event=E.PopSurvey(time=4,
                              individual=self,
                              cohort=self))
        # schedule at time 5
        self.simCal.add_event(
            event=E.PopSurvey(time=5,
                              individual=self,
                              cohort=self))
        # schedule at time 6
        self.simCal.add_event(
            event=E.PopSurvey(time=6,
                              individual=self,
                              cohort=self))
        # schedule at time 7
        self.simCal.add_event(
            event=E.PopSurvey(time=7,
                              individual=self,
                              cohort=self))
        # schedule at time 8
        self.simCal.add_event(
            event=E.PopSurvey(time=8,
                              individual=self,
                              cohort=self))
        # schedule at time 9
        self.simCal.add_event(
            event=E.PopSurvey(time=9,
                              individual=self,
                              cohort=self))
        # schedule population distribution survey event at the end of simulation (time 10)
        self.simCal.add_event(
            event=E.PopSurvey(time=D.SIM_DURATION,
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
        # get next event and process it
        while self.simCal.n_events() > 0 and self.simCal.time <= sim_duration:
            self.simCal.get_next_event().process()

        # collect the end of simulation statistics
        self.simOutputs.collect_end_of_sim_stat()

    def process_birth(self, individual):
        """
        process the birth of a new individual
        :param individual: individual
        """

        # trace
        self.trace.add_message(
            'Processing the birth of ' + str(individual) + '.')

        # collect statistics on new birth
        self.simOutputs.collect_birth()

        # add the new individual to the population (list of individuals)
        self.individuals.append(individual)

    def process_pop_survey(self):
        """
        processes the population distribution pyramid (age/sex)
        """

        # new pyramid
        pyramid = Pyramid(list_x_min=[8, 0],
                          list_x_max=[16, 1],
                          list_x_delta=[1, 'int'],
                          name='Population Pyramid at Time ' + str(self.simCal.time))

        # for each individual, record age/sex and increment pyramid by 1
        # x values: [age, sex]
        self.simOutputs.bmiTimeStep = []
        for individual in self.individuals:
            if individual.ifAlive is True:
                pyramid.record_increment(x_values=[individual.get_age(self.simCal.time), individual.sex],
                                         increment=1)

            # record BMI for each individual and add to list
            index_by_time = floor(self.simCal.time) + 1
            self.simOutputs.bmiTimeStep.append(individual.trajectory[index_by_time])

            # if want to print details of individual bmi at each time step
            # print(int(individual.get_age(current_time=self.simCal.time)),
            #       "year old at time step:",
            #       index_by_time - 1,
            #       '=',
            #       individual.trajectory[index_by_time])

        # calculate average BMI at each time step
        self.simOutputs.collect_bmi()

        self.simOutputs.pyramidPercentage.append(pyramid.get_percentages())

        # record each pyramid in list in simulation outputs
        self.simOutputs.pyramids.append(pyramid)

    def print_trace(self):
        """ outputs trace """

        # simulation trace
        self.trace.print_trace(filename='Trace-Replication' + str(self.id) + '.txt',
                               directory='Trace',
                               delete_existing_files=True)
