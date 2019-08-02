import InputData as D
# for age/sex distribution
import SimPy.DataFrames as df
from SimPy import InOutFunctions as InOutSupport
from SimPy import RandomVariantGenerators as RVGs


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

        # INTERVENTION COSTS of BRIGHT BODIES (detailed)
        # Exercise Sessions
        exercise_physiologist = 9592.00
        games_equipment = 1900.00
        motivational_tools = 240.00
        printed_materials = 25.00
        gym_room_utilities = 0.00  # note: provided at no charge for BB
        first_aid_kit = 150.00
        # Category Total
        exercise_sessions_total = exercise_physiologist + \
            games_equipment + \
            motivational_tools + \
            printed_materials + \
            gym_room_utilities + \
            first_aid_kit
        # Nutrition/Behavior Modification Sessions
        registered_dietitian = 6805.00
        social_worker = 1200.00
        educational_tools = 1350.00
        classroom_utilities = 0.00  # note: provided at no charge for BB
        # Category Total
        nutrition_behavior_sessions_total = registered_dietitian + \
            social_worker + \
            educational_tools + \
            classroom_utilities
        # Parent Sessions
        # includes social_worker, printed_materials, classroom_utilities
        # Category Total
        parent_sessions_total = social_worker + \
            printed_materials + \
            classroom_utilities
        # Administration
        exercise_physiologist_admin = 6990.00
        registered_dietitian_admin = 16376.00
        # Category Total
        administration_bb_total = exercise_physiologist_admin + \
            registered_dietitian_admin
        # Weigh-Ins (before each session)
        technician = 1200.00
        body_fat_analyzer_scale = 700.00
        stadiometer = 100.00
        # Category Total
        weigh_ins_total = technician + \
            body_fat_analyzer_scale + \
            stadiometer
        # Medical Director
        medical_consultation = 5100.00
        # Category Total
        medical_director_total = medical_consultation

        # Total Overall for BB
        total_cost_bb = exercise_sessions_total + \
            nutrition_behavior_sessions_total + \
            parent_sessions_total + \
            administration_bb_total + \
            weigh_ins_total + \
            medical_director_total
        # Total per Child (based on 90 children - full BB capacity)
        total_per_child_bb = total_cost_bb / D.N_CHILDREN_BB

        # INTERVENTIONS COSTS of CLINICAL CONTROL
        # Nurse Visit and Follow Up
        nurse_practitioner = 11686.00
        # Category Total
        nurse_visit_fu_total = nurse_practitioner
        # Nutrition Visit and Follow Up
        registered_dietitian_cc = 6329.00
        # Category Total
        nutrition_visit_fu_total = registered_dietitian_cc
        # Behavioral Counseling Visit and Follow Up
        social_worker_cc = 6460.00
        # Category Total
        behavioral_counseling_visit_fu_total = social_worker_cc
        # Administration
        dept_clinical_secretary = 834.00
        clinical_secretary = 1669.00
        typing = 2504.00
        # Category Total
        administration_cc_total = dept_clinical_secretary + \
            clinical_secretary + \
            typing
        # Weigh Ins + Labs
        lab_technician = 1408.00
        # Category Total
        weigh_ins_cc_total = lab_technician
        # Medical Director Visit and Follow Up
        medical_consultation_cc = 10256.00
        # Category Total
        medical_director_cc_total = medical_consultation_cc
        # Rent Space/Utilities + Cleaning Service + Clinic Equipment/Supplies
        rent_space_utilities = 3000.00
        cleaning_service = 885.00
        clinic_equipment_supplies = 2900.00
        # Category Total
        other_costs_cc_total = rent_space_utilities + \
            cleaning_service + \
            clinic_equipment_supplies

        # Total Overall for CC
        total_cost_cc = nurse_visit_fu_total + nutrition_visit_fu_total + \
            behavioral_counseling_visit_fu_total + \
            administration_cc_total + \
            weigh_ins_cc_total + \
            medical_director_cc_total + \
            other_costs_cc_total

        # Total per Child (based on 90 children - full BB capacity)
        total_per_child_cc = total_cost_cc / D.N_CHILDREN_BB

        # COSTS: ANNUAL (per person)
        self.annualInterventionCostBB = total_per_child_bb / D.YEARS_RCT  # should be 588
        self.annualInterventionCostCC = total_per_child_cc / D.YEARS_RCT  # should be 533

        if intervention == D.Interventions.BRIGHT_BODIES:
            self.interventionMultipliers \
                = [1.0, 0.925, 0.951, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        else:
            self.interventionMultipliers \
                = [1.0, 1.05, 1.048, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
