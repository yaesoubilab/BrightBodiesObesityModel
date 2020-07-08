from math import floor, pow

import SimPy.DiscreteEventSim as SimCls
import SimPy.RandomVariateGenerators as RVGs
import SimPy.SimulationSupport as Sim
from SimPy.DataFrames import Pyramid
from yom import ModelOutputs as O, ModelEvents as E


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
    def __init__(self, id, model_inputs, parameters):
        """ creates a cohort of individuals
        :param id: ID of this cohort
        :param model_inputs: model inputs and settings
        :param parameters: parameters of this cohort
        """

        self.id = id
        self.rng = RVGs.RNG(seed=id)
        self.inputs = model_inputs
        self.params = parameters

        self.individuals = []  # list of individuals
        self.simCal = SimCls.SimulationCalendar()  # simulation calendar
        # simulation outputs
        self.simOutputs = O.SimOutputs(sim_cal=self.simCal, sim_rep=id, trace_on=model_inputs.traceOn)
        # simulation trace
        self.trace = Sim.DiscreteEventSimTrace(sim_calendar=self.simCal,
                                               if_should_trace=model_inputs.traceOn,
                                               deci=model_inputs.deci)

    def __initialize(self, sim_duration):
        """ initialize the cohort
        :param sim_duration: simulation duration
        """

        # baseline population of given population size
        for i in range(self.params.popSize):
            # find the age and sex of this individual
            age_sex = self.params.ageSexDist.sample_values(rng=self.rng)

            # time of "birth" (initialization)
            t_birth = self.params.simInitialDuration * i / self.params.popSize

            # assign randomly the BMI trajectory of this individual based on age and sex
            set_of_trajs = self.params.trajectories.get_obj(x_value=[age_sex[0], age_sex[1]])
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
            event=E.PopSurvey(time=self.params.simInitialDuration,
                              individual=self,
                              cohort=self))

        # schedule BMI survey each year
        # survey right after initialization
        self.simCal.add_event(
            event=E.BMISurvey(time=self.params.simInitialDuration,
                              individual=self,
                              cohort=self))
        # survey at years 1, 2, ...
        for t in range(1, sim_duration+1):
            self.simCal.add_event(
                event=E.BMISurvey(time=t,
                                  individual=self,
                                  cohort=self))

    def simulate(self, sim_duration):
        """ simulate the cohort
        :param sim_duration: duration of simulation (years)
        """

        # initialize the simulation
        self.__initialize(sim_duration)

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
        collect BMIs, intervention cost, and health care expenditures of the cohort at this simulation time
        """

        individual_bmis = []  # list of BMI values of all individuals at the current time
        cohort_intervention_cost = 0  # cohort intervention costs at the current time
        cohort_hc_expenditure = 0  # cohort health care expenditures at the current time

        # year index
        year_index = floor(self.simCal.time)
        # discount factor
        discount_factor = pow(1 + self.inputs.discountRate, -year_index)

        for individual in self.individuals:
            if individual.ifAlive:

                # record BMI for this individual (baseline BMI * intervention multiplier) and add to list
                # note that the first element of a BMI trajectory is the id of the trajectory so we skip it
                individual_bmi = individual.trajectory[year_index + 1] \
                                 * self.params.interventionMultipliers[year_index]
                individual_bmis.append(individual_bmi)

                # collect the cost of the intervention
                # for the first and the second years we add the intervention cost
                if year_index in (0, 1):
                    cohort_intervention_cost += self.params.annualInterventionCost * discount_factor

                # collect the health care expenditure cost
                cohort_hc_expenditure += self.calculate_hc_expenditure(individual=individual,
                                                                       bmi=individual_bmi) * discount_factor

        # store list of individual costs and health
        self.simOutputs.collect_costs_of_this_period(cohort_intervention_cost, cohort_hc_expenditure)

        # calculate and store average BMI for this year
        self.simOutputs.collect_bmi(individual_bmis)

    def calculate_hc_expenditure(self, individual, bmi):
        """
        :param individual: an individual
        :param bmi: bmi of the individual
        :return: the health care expenditure of an individual
        """

        # age of the individual at this simulation time
        age = floor(individual.get_age(current_time=self.simCal.time))

        # find the bmi 95th for this individual
        bmi_cut_off = self.params.bmi95thCutOffs.get_value([age, individual.sex])
        # if the individual is above or below the BMI 95th percentile
        if bmi < bmi_cut_off:
            individual.ifLessThan95th = True
        else:
            individual.ifLessThan95th = False

        # ATTRIBUTABLE HEALTH CARE EXPENDITURES
        bmi_unit_above_30 = bmi - 30
        if age < 18:
            if individual.ifLessThan95th is False:
                # annual HC expenditure for >95th (per individual)
                hc_exp = self.params.costAbove95thP
            else:
                # annual HC expenditure for <95th (per individual)
                hc_exp = self.params.costBelow95thP
        else:
            # if less than 95th (which is 30)
            if individual.ifLessThan95th is True:
                # no additional attributable expenditure
                hc_exp = 0
            else:
                if bmi_unit_above_30 < 0:
                    hc_exp = 0
                else:
                    hc_exp = bmi_unit_above_30 * (
                            self.params.costPerUnitBMIAdultP * ((1 + self.inputs.inflation) ** (2020 - 2017)))

        return hc_exp

    def process_pop_survey(self):
        """ processes the population distribution pyramid (age/sex) """

        # new pyramid
        min_age = self.inputs.ageSexDist[0][0]
        max_age = self.inputs.ageSexDist[-1][0]
        pyramid = Pyramid(list_x_min=[min_age, 0],
                          list_x_max=[max_age, 1],
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
