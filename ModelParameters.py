import SimPy.DataFrames as df
from SimPy import InOutFunctions as InOutSupport
from SimPy import RandomVariantGenerators as RVGs
import SimPy.FittingProbDist_MM as MM
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
        self.annualInterventionCost = []
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


class ParamGenerator:
    def __init__(self, intervention):
        self.intervention = intervention

    # create variable for each cost item

        # create gamma dist for exercise physiologist cost (BRIGHT BODIES)
        fit_output = MM.get_gamma_params(mean=exercise_physiologist,
                                         st_dev=0)
        self.exphysRVG = RVGs.Gamma(a=fit_output["a"],
                                    loc=0,
                                    scale=fit_output["scale"])

    # CONSTANTS
        # BRIGHT BODIES
        # exercise sessions
        self.gamesRVG = RVGs.Constant(value=games_equipment)
        self.motivtoolsRVG = RVGs.Constant(value=motivational_tools)
        self.printedmaterialRVG = RVGs.Constant(value=printed_materials)
        self.gymroomRVG = RVGs.Constant(value=gym_room_utilities)
        self.firstaidRVG = RVGs.Constant(value=first_aid_kit)
        # nutrition behavior modification sessions
        self.regdietRVG = RVGs.Constant(value=registered_dietitian)
        self.socialworkerRVG = RVGs.Constant(value=social_worker)
        self.edutoolsRVG = RVGs.Constant(value=educational_tools)
        self.classroomRVG = RVGs.Constant(value=classroom_utilities)
        # parent sessions (all included in previous sections)
        self.socialworkerRVG = RVGs.Constant(value=social_worker)
        self.printedmaterialRVG = RVGs.Constant(value=printed_materials)
        self.classroomRVG = RVGs.Constant(value=classroom_utilities)
        # administration
        self.exphysCoorRVG = RVGs.Constant(value=exercise_physiologist_admin)
        self.regdietCoorRVG = RVGs.Constant(value=registered_dietitian_admin)
        # weigh ins
        self.technicianRVG = RVGs.Constant(value=technician)
        self.bfanalyserRVG = RVGs.Constant(value=body_fat_analyzer_scale)
        self.stadiometerRVG = RVGs.Constant(value=stadiometer)
        # medical director
        self.medconsultRVG = RVGs.Constant(value=medical_consultation)

        # CONTROL
        # Nurse Visit and Follow Up
        self.nursepractitionerRVG = RVGs.Constant(value=nurse_practitioner)
        # Nutrition Visit and Follow Up
        self.regdiet_controlRVG = RVGs.Constant(value=registered_dietitian_cc)
        # Behavioral Counseling Visit and Follow Up
        self.socialworker_controlRVG = RVGs.Constant(value=social_worker_cc)
        # Administration
        self.deptclinsecretaryRVG = RVGs.Constant(value=dept_clinical_secretary)
        self.clinsecretaryRVG = RVGs.Constant(value=clinical_secretary)
        self.typingRVG = RVGs.Constant(value=typing)
        # Weigh Ins + Labs
        self.labtechRVG = RVGs.Constant(value=lab_technician)
        # Medical Director Visit and Follow Up
        self.medconsult_controlRVG = RVGs.Constant(value=medical_consultation_cc)
        # Rent Space/Utilities + Cleaning Service + Clinic Equipment/Supplies
        self.rentspaceRVG = RVGs.Constant(value=rent_space_utilities)
        self.cleaningRVG = RVGs.Constant(value=cleaning_service)
        self.clinicequipRVG = RVGs.Constant(value=clinic_equipment_supplies)

    def get_new_parameters(self, rng):
        param = Parameters(intervention=self.intervention)

    # sample from distributions
        # BRIGHT BODIES
        # exercise sessions
        param_exercise_physiologist = self.exphysRVG.sample(rng)
        param_games_equipment = self.gamesRVG.sample(rng)
        param_motivational_tools = self.motivtoolsRVG.sample(rng)
        param_printed_materials = self.printedmaterialRVG.sample(rng)
        param_gym_room_utilities = self.gymroomRVG.sample(rng)
        param_first_aid_kit = self.firstaidRVG.sample(rng)
        # nutrition behavior modification
        param_registered_dietitian = self.regdietRVG.sample(rng)
        param_social_worker = self.socialworkerRVG.sample(rng)
        param_educational_tools = self.edutoolsRVG.sample(rng)
        param_classroom_utilities = self.classroomRVG.sample(rng)
        # parent sessions
        param_social_worker_2 = self.socialworkerRVG.sample(rng)
        param_printed_materials_2 = self.printedmaterialRVG.sample(rng)
        param_classroom_utilities_2 = self.classroomRVG.sample(rng)
        # administration
        param_exercise_physiologist_admin = self.exphysCoorRVG.sample(rng)
        param_registered_dietitian_admin = self.regdietCoorRVG.sample(rng)
        # weigh ins
        param_technician = self.technicianRVG.sample(rng)
        param_body_fat_analyzer_scale = self.bfanalyserRVG.sample(rng)
        param_stadiometer = self.stadiometerRVG.sample(rng)
        # medical director
        param_medical_consultation = self.medconsultRVG.sample(rng)

        # CONTROL
        # nurse visit and follow up
        param_nurse_practitioner = self.nursepractitionerRVG.sample(rng)
        # nutrition visit and follow up
        param_registered_dietitian_cc = self.regdiet_controlRVG.sample(rng)
        # behavioral counseling visit and follow up
        param_social_worker_cc = self.socialworker_controlRVG.sample(rng)
        # administration
        param_dept_clinical_secretary = self.deptclinsecretaryRVG.sample(rng)
        param_clinical_secretary = self.clinsecretaryRVG.sample(rng)
        param_typing = self.typingRVG.sample(rng)
        # weigh ins and labs
        param_lab_technician = self.labtechRVG.sample(rng)
        # medical director visit and follow up
        param_medical_consultation_cc = self.medconsult_controlRVG.sample(rng)
        # rent space/utilities and cleaning service
        param_rent_space_utilities = self.rentspaceRVG.sample(rng)
        param_cleaning_service = self.cleaningRVG.sample(rng)
        param_clinic_equipment_supplies = self.clinicequipRVG.sample(rng)

        # calculate category totals: BRIGHT BODIES
        total_exercise_sessions = sum(param_exercise_physiologist + param_games_equipment + param_motivational_tools +
                                      param_printed_materials + param_gym_room_utilities + param_first_aid_kit)
        total_nutrition_behavior_sessions = sum(param_registered_dietitian + param_social_worker +
                                                param_educational_tools + param_classroom_utilities)
        total_parent_sessions = sum(param_social_worker_2 + param_printed_materials_2 + param_classroom_utilities_2)
        total_administration = sum(param_exercise_physiologist_admin + param_registered_dietitian_admin)
        total_weigh_ins = sum(param_technician + param_body_fat_analyzer_scale + param_stadiometer)
        total_medical_director = param_medical_consultation

        # calculate category totals: CONTROL
        total_nurse_visit = param_nurse_practitioner
        total_nutrition_visit = param_registered_dietitian_cc
        total_behavior_counseling = param_social_worker_cc
        total_administration_control = sum(param_dept_clinical_secretary + param_clinical_secretary + param_typing)
        total_weigh_ins_control = param_lab_technician
        total_medical_director_control = param_medical_consultation_cc
        total_rent_utilities = sum(param_rent_space_utilities + param_cleaning_service +
                                   param_clinic_equipment_supplies)

        # OVERALL cost: BB
        overall_total_bright_bodies = total_exercise_sessions + total_nutrition_behavior_sessions + \
            total_parent_sessions + total_administration + total_weigh_ins + total_medical_director

        # OVERALL cost: Control
        overall_total_control = total_nurse_visit + total_nutrition_visit + total_behavior_counseling + \
            total_administration_control + total_weigh_ins_control + total_medical_director_control + \
            total_rent_utilities

        return param, overall_total_bright_bodies, overall_total_control

