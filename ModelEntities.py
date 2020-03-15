import SimPy.DiscreteEventSim as SimCls
import SimPy.SimulationSupport as Sim
import SimPy.RandomVariantGenerators as RVGs
import ModelEvents as E
import InputData as D
import ModelOutputs as O
from SimPy.DataFrames import Pyramid
from math import floor
import ModelParameters as Param


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
        self.ifLessThan95th = False

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
        collect BMIs to calculate average
        """

        bmis_at_this_time = []  # list of BMI values of all individuals at the current time
        individual_costs = []   # TODO: could you add what this collects?
        health_care_expenditures = []   # TODO: could you add what this collects?

        for individual in self.individuals:
            if individual.ifAlive is True:

                # record BMI for this individual (baseline BMI * intervention multiplier) and add to list
                year_index = floor(self.simCal.time)
                bmi_individual = individual.trajectory[year_index+1]*self.params.interventionMultipliers[year_index]
                bmis_at_this_time.append(bmi_individual)

                # CHECK FOR BMI STATUS (< or >= 95th %ile by age sex)
                age = floor(individual.get_age(current_time=self.simCal.time))

                # TODO: if you put these thresholds in the same format as
                #   age_sex_dist (in the InputData.py file), we can simply this.
                #   I can help.
                # if Female
                if individual.sex == 1:
                    if age == 8:
                        if bmi_individual < 20.6:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 9:
                        if bmi_individual < 21.8:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 10:
                        if bmi_individual < 22.9:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 11:
                        if bmi_individual < 24.1:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 12:
                        if bmi_individual < 25.2:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 13:
                        if bmi_individual < 26.2:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 14:
                        if bmi_individual < 27.2:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 15:
                        if bmi_individual < 28.1:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 16:
                        if bmi_individual < 28.9:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 17:
                        if bmi_individual < 29.6:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 18:
                        if bmi_individual < 30:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    # for all older ages
                    else:
                        if bmi_individual < 30:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                # if Male
                if individual.sex == 0:
                    if age == 8:
                        if bmi_individual < 20.0:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 9:
                        if bmi_individual < 21.1:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 10:
                        if bmi_individual < 22.1:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 11:
                        if bmi_individual < 23.2:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 12:
                        if bmi_individual < 24.2:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 13:
                        if bmi_individual < 25.2:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 14:
                        if bmi_individual < 26.0:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 15:
                        if bmi_individual < 26.8:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 16:
                        if bmi_individual < 27.5:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 17:
                        if bmi_individual < 28.2:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    if age == 18:
                        if bmi_individual < 30:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False
                    # for all older ages
                    else:
                        if bmi_individual < 30:
                            individual.ifLessThan95th = True
                        else:
                            individual.ifLessThan95th = False

                # update costs of cohort
                # if year_index is 0:
                if year_index in (0, 1):
                    if self.params.intervention == D.Interventions.BRIGHT_BODIES:
                        cost_individual = self.params.annualInterventionCostBB
                    else:
                        cost_individual = self.params.annualInterventionCostCC
                else:
                    cost_individual = 0
                # individual_costs = list of individual cost at each time step
                individual_costs.append(cost_individual)

                # NEW
                # ATTRIBUTABLE HEALTH CARE EXPENDITURES
                bmi_unit_above_30 = bmi_individual - 30
                inflation_constant = 0.02
                if age < 18:
                    if individual.ifLessThan95th is False:
                        # annual HC expenditure for >95th (per individual)
                        # annual_hc_exp = 220*((1+inflation_constant)**(2020-2008 + year_index))
                        annual_hc_exp = self.params.costAbove95thP*((1+inflation_constant)**(2020-2008 + year_index))
                    else:
                        # annual HC expenditure for <95th (per individual)
                        annual_hc_exp = self.params.costBelow95thP*((1+inflation_constant)**(2020-2008 + year_index))
                else:
                    # if less than 95th (which is 30)
                    if individual.ifLessThan95th is True:
                        # no additional attributable expenditure
                        annual_hc_exp = 0
                    else:
                        if bmi_unit_above_30 < 0:
                            annual_hc_exp = 0
                        else:
                            # annual_hc_exp = bmi_unit_above_30*(197*((1+inflation_constant)**(2020-2017)))
                            annual_hc_exp = bmi_unit_above_30*(self.params.costPerUnitBMIAdultP*((1+inflation_constant)**(2020-2017)))

                health_care_expenditures.append(annual_hc_exp)

        # store list of individual costs and health
        self.simOutputs.collect_cost(individual_costs, health_care_expenditures)

        # calculate and store average BMI for this year
        self.simOutputs.collect_bmi(bmis_at_this_time)

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
