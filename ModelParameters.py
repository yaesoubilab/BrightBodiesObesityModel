import SimPy.DataFrames as df
from SimPy import InOutFunctions as InOutSupport
from SimPy import RandomVariantGenerators as RVGs
from ParamSupport import *


# class to select random row from rows (specific to age/sex)
class SetOfTrajectories:
    def __init__(self, rows):
        self.rows = rows
        self.discreteUniform = RVGs.UniformDiscrete(0, len(rows) - 1)

    def sample_traj(self, rng):
        i = self.discreteUniform.sample(rng)
        return self.rows[i]


class Parameters:
    # class to contain the parameters of the model
    def __init__(self, intervention):

        # population distribution by age/sex for Bright Bodies (age 8 - 16)
        self.ageSexDist = df.DataFrameWithEmpiricalDist(rows=D.age_sex_dist,                # life table
                                                        list_x_min=[8, 0],          # minimum values for age/sex groups
                                                        list_x_max=[16, 1],         # maximum values for age/sex groups
                                                        list_x_delta=[1, 'int'])    # [age interval, sex categorical]

        # Creating DataFrame of Trajectories for Bright Bodies Age Cohort
        self.df_trajectories = df.DataFrameOfObjects(list_x_min=[8, 0],
                                                     list_x_max=[16, 1],
                                                     list_x_delta=[1, 'int'])
        for sex in ['male', 'female']:
            for age in range(8, 17, 1):
                file_name = 'csv_trajectories/{0}_{1}_o_f.csv'.format(sex, age)
                rows = InOutSupport.read_csv_rows(file_name=file_name,
                                                  delimiter=',',
                                                  if_del_first_row=True,
                                                  if_convert_float=True)
                traj = SetOfTrajectories(rows=rows)
                s = 0 if sex == 'male' else 1
                self.df_trajectories.set_obj(x_value=[age, s],
                                             obj=traj)

        self.intervention = intervention
        self.interventionMultipliers = []  # intervention multipliers to reduce BMI over time

    # COSTS
        # BRIGHT BODIES
        # Total Overall for BB
        self.total_cost_bb = total_cost_bb
        # Total per Child (based on 90 children - full BB capacity)
        self.total_per_child_bb = total_per_child_bb

        # CLINICAL CONTROL
        # Total Overall for CC
        self.total_cost_cc = total_cost_cc
        # Total per Child (based on 90 children - full BB capacity)
        self.total_per_child_cc = total_per_child_cc

        # COSTS: ANNUAL (per person)
        self.annualInterventionCostBB = annualInterventionCostBB
        self.annualInterventionCostCC = annualInterventionCostCC

        # TODO: I would make separate parameters for the ratios in years 1 and 2
        #       so that later when you want to do uncertainty analysis or calibration, you can
        #       modify them from outside.
        if intervention == D.Interventions.BRIGHT_BODIES:
            self.interventionMultipliers \
                = [1.0, 0.925, 0.951, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        else:
            self.interventionMultipliers \
                = [1.0, 1.05, 1.048, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
