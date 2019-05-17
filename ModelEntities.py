import SimPy.DiscreteEventSim as SimCls
import SimPy.SimulationSupport as Sim
import SimPy.RandomVariantGenerators as RVGs
import ModelEvents as E
import InputData as D
import ModelOutputs as O
import SimPy.InOutFunctions as IO


class Individual:
    def __init__(self, id):
        """ create an individual
        :param id: (integer) patient ID
        """
        self.id = id
        self.tBirth = 0               # time of birth

    def __str__(self):
        return "Patient " + str(self.id)


class Cohort:
    def __init__(self, id, parameters):
        """ creates a cohort of individuals
        :param id: ID of this cohort
        :parameters: parameters of this cohort
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

        # find the first birth
        bith_time = self.params.timeToNextBirthDist.sample(rng=self.rng)

        # schedule the first birth
        self.simCal.add_event(
            event=E.Birth(time=bith_time, individual=Individual(id=0), cohort=self))

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
        time_death = self.simCal.time + self.params.timeToDeath.sample(rng=self.rng)

        # schedule the the death of this person
        self.simCal.add_event(
            event=E.Death(
                time=time_death,
                individual=individual,
                cohort=self
            )
        )

        # find the time of next birth
        time_next_birth = self.simCal.time + self.params.timeToNextBirthDist.sample(rng=self.rng)

        # schedule the next birth
        self.simCal.add_event(
            event=E.Birth(
                time=time_next_birth,
                individual=Individual(id=individual.id + 1),  # id of the next patient = this patient's id + 1
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

    def print_trace(self):
        """ outputs trace """

        # simulation trace
        self.trace.print_trace(filename='Trace-Replication' + str(self.id) + '.txt',
                               directory='Trace',
                               delete_existing_files=True)
