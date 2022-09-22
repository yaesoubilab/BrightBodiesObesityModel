from math import floor, pow

import deampy.discrete_event_sim as SimCls
import deampy.random_variats as RVGs
import deampy.support.simulation as Sim
from deampy.data_structure import Pyramid
from yom import ModelOutputs as O, ModelEvents as E
from yom.ModelInputs import WeightStatus


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

    def get_age_year(self, current_time):
        """
        :param current_time: current simulation time
        :return: age in year
        """
        # age of the individual at this simulation time
        return floor(self.get_age(current_time=current_time))

    def get_bmi(self, sim_year_index, intervention_multiplier):
        """
        :param sim_year_index: simulation year index 0, 1, ...
        :param intervention_multiplier: intervention effectiveness 
        :return: BMI at the given simulation year index
        """
        # note that the first element of a BMI trajectory is the id of the trajectory so we skip it
        return self.trajectory[sim_year_index + 1] * intervention_multiplier

    def get_weight_status(self, sim_year_index, intervention_multiplier, params):
        """
        :param sim_year_index: simulation year index 0, 1, ...
        :param intervention_multiplier: intervention multiplier
        :param params:  parameter object that contains overweight and obese thresholds
        :return: the weight status (normal weight, overweight, obese) of the individual given the current BMI
        """

        # age of the individual at this simulation time
        age = self.get_age_year(current_time=sim_year_index)
        bmi = self.get_bmi(sim_year_index=sim_year_index, intervention_multiplier=intervention_multiplier)

        # if the individual is above or below the BMI 95th percentile
        if bmi >= params.bmi95thCutOffs.get_value([age, self.sex]):
            return WeightStatus.Obese
        elif bmi >= params.bmi85thCutOffs.get_value([age, self.sex]):
            return WeightStatus.OverWeight
        else:
            return WeightStatus.NormalWeight


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

    def process_cohort_outcomes(self):
        """
        collect BMIs, intervention cost, and health care expenditures of the cohort at this simulation time
        """

        individual_bmis = []  # list of BMI values of all individuals at the current time
        cohort_discounted_intervention_cost = 0  # cohort intervention costs at the current time
        cohort_discounted_hc_expenditure = 0  # cohort health care expenditures at the current time

        # year index
        year_index = floor(self.simCal.time)

        # intervention multiplier
        intervention_multp_now = self.params.interventionMultipliers[year_index]
        if year_index > 0:
            intervention_multp_last_year = self.params.interventionMultipliers[year_index - 1]

        # discount factor
        discount_factor = pow(1 + self.inputs.discountRate, -year_index)

        for individual in self.individuals:
            if individual.ifAlive:

                # record BMI for this individual (baseline BMI * intervention multiplier) and add to list
                # note that the first element of a BMI trajectory is the id of the trajectory so we skip it
                individual_bmi = individual.get_bmi(sim_year_index=year_index,
                                                    intervention_multiplier=intervention_multp_now)

                individual_bmis.append(individual_bmi)

                # collect the cost of the intervention
                # for the first year we add the intervention cost
                if year_index == 1:
                    cohort_discounted_intervention_cost += self.params.annualInterventionCost * discount_factor

                # collect the health care expenditure cost (corrected for half-cycle effect)
                if year_index > 0:
                    hc_last_year = self.calculate_hc_expenditure(individual=individual,
                                                                 intervention_multiplier=intervention_multp_last_year,
                                                                 sim_year_index=year_index - 1)
                    hc_now = self.calculate_hc_expenditure(individual=individual,
                                                           intervention_multiplier=intervention_multp_now,
                                                           sim_year_index=year_index)
                    cohort_discounted_hc_expenditure += 0.5 * (hc_last_year + hc_now) * discount_factor

        # store list of individual costs and health
        if year_index > 0:
            self.simOutputs.collect_costs_of_this_period(
                intervention_cost=cohort_discounted_intervention_cost,
                hc_expenditure=cohort_discounted_hc_expenditure,
                cohort_size=self.inputs.popSize)

        # calculate and store average BMI for this year
        self.simOutputs.collect_bmi(individual_bmis)

    def calculate_hc_expenditure(self, individual, sim_year_index, intervention_multiplier):
        """
        :param individual: an individual
        :param sim_year_index: simulation year index 0, 1, ...
        :param intervention_multiplier: intervention effectiveness
        :return: the health care expenditure of an individual
        """

        bmi = individual.get_bmi(sim_year_index=sim_year_index, intervention_multiplier=intervention_multiplier)
        weight_status = individual.get_weight_status(sim_year_index=sim_year_index,
                                                     intervention_multiplier=intervention_multiplier,
                                                     params=self.params)

        if individual.get_age(current_time=self.simCal.time) < 18:
            if weight_status == WeightStatus.Obese:
                # annual HC expenditure for >95th (per individual)
                hc_exp = self.params.costAbove95thP
            elif weight_status == WeightStatus.OverWeight:
                # annual HC expenditure for 85-94th (per individual)
                hc_exp = self.params.cost85To94thP
            else:
                hc_exp = 0
        else:
            # if less than 95th (which is 30)
            if weight_status != WeightStatus.Obese:
                # no additional attributable expenditure
                hc_exp = 0
            else:
                bmi_unit_above_30 = bmi - 30
                if bmi_unit_above_30 < 0:
                    hc_exp = 0
                else:
                    hc_exp = bmi_unit_above_30 * self.params.costPerUnitBMIAdultP

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
