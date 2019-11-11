import SimPy.DiscreteEventSim as SimCls
import SimPy.SimulationSupport as Sim
import SimPy.RandomVariantGenerators as RVGs
import ModelEvents as E
import InputData as D
import ModelOutputs as O
from SimPy.DataFrames import Pyramid
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
        :return: age (current time + age at initialization)
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

            # assign randomly the BMI trajectory of this individual based on age and sex
            set_of_trajs = self.params.df_trajectories.get_obj(x_value=[age_sex[0], age_sex[1]])
            bmi_trajectory = set_of_trajs.sample_traj(rng=self.rng)

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

        # schedule BMI survey at times 0, 1, 2, ..., 10
        self.simCal.add_event(
            event=E.BMISurvey(time=D.SIM_INIT,
                              individual=self,
                              cohort=self))
        for t in range(1, D.SIM_DURATION + 1, 1):
            self.simCal.add_event(
                event=E.BMISurvey(time=t,
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

    def process_obesity_outcomes(self):
        """
        processes the population distribution pyramid (age/sex)
        collect BMIs to calculate average
        """

        bmi_time_step = []
        individual_costs = []

        for individual in self.individuals:
            if individual.ifAlive is True:

                # record BMI for this individual (baseline BMI * intervention multiplier) and add to list
                year_index = floor(self.simCal.time)
                bmi_time_step.append(
                    individual.trajectory[year_index+1]  # note the first element of individual.trajectory is
                                                         # the individual ID so we need to skip it.
                    * self.params.interventionMultipliers[year_index])

                # update costs of cohort
                if year_index == 1 or 2:
                    if self.params.intervention == D.Interventions.BRIGHT_BODIES:
                        cost_individual = self.params.annualInterventionCostBB
                    else:
                        cost_individual = self.params.annualInterventionCostCC
                else:
                    cost_individual = self.params.annualInterventionCostCC
                individual_costs.append(cost_individual)

        # store list of individual costs
        self.simOutputs.collect_cost(individual_costs)

        # calculate and store average BMI for this year
        self.simOutputs.collect_bmi(bmi_time_step)

    def process_pop_survey(self):
        """ processes the population distribution pyramid (age/sex) """

        # new pyramid
        pyramid = Pyramid(list_x_min=[8, 0],
                          list_x_max=[16, 1],
                          list_x_delta=[1, 'int'],
                          name='Population Pyramid at Time ' + str(self.simCal.time))

        # for each individual, record age/sex and increment pyramid by 1
        for individual in self.individuals:
            if individual.ifAlive is True:
                # update population pyramid
                # x values: [age, sex]
                pyramid.record_increment(x_values=[individual.get_age(self.simCal.time), individual.sex],
                                         increment=1)

        self.simOutputs.pyramids.append(pyramid.get_percentages())

    def print_trace(self):
        """ outputs trace """

        # simulation trace
        self.trace.print_trace(filename='Trace-Replication' + str(self.id) + '.txt',
                               directory='Trace',
                               delete_existing_files=True)
