from enum import Enum


# trace
TRACE_ON = False       # Set to true to trace a simulation replication
DECI = 5               # the decimal point to round the numbers to in the trace file

# simulation settings
SIM_INIT = 0.00001  # (years) initialization period to create the cohort
SIM_DURATION = 10   # (years)
POP_SIZE = 1000     # population size (cohort at initialization)

# for MultiCohorts
N_COHORTS = 2


class SEX(Enum):
    MALE = 0
    FEMALE = 1


class Interventions(Enum):
    """ Bright Bodies v. Clinical Care """
    CONTROL = 0
    BRIGHT_BODIES = 1


# for Bright Bodies (8-16 y/o)
# use to initialize cohort
# condensed decimals for now - FIX LATER
age_sex_dist = [
    [8, 0, 0.055519863],   # 8, male
    [8, 1, 0.053217689],   # 8, female
    [9, 0, 0.055519863],   # 9, male
    [9, 1, 0.053217689],   # 9, female
    [10, 0, 0.056804797],  # 10, male
    [10, 1, 0.054449084],  # 10, female
    [11, 0, 0.056804798],  # 11, male
    [11, 1, 0.054449084],  # 11, female
    [12, 0, 0.056804797],  # 12, male
    [12, 1, 0.054449084],  # 12, female
    [13, 0, 0.056804797],  # 13, male
    [13, 1, 0.054449084],  # 13, female
    [14, 0, 0.056804797],  # 14, male
    [14, 1, 0.054449084],  # 14, female
    [15, 0, 0.057822037],  # 15, male
    [15, 1, 0.055305708],  # 15, female
    [16, 0, 0.057822037],  # 16, male
    [16, 1, 0.055305708]   # 16, female
]

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
exercise_sessions_total = exercise_physiologist +\
                          games_equipment +\
                          motivational_tools +\
                          printed_materials +\
                          gym_room_utilities +\
                          first_aid_kit
# Nutrition/Behavior Modification Sessions
registered_dietitian = 6805.00
social_worker = 1200.00
educational_tools = 1350.00
classroom_utilities = 0.00  # note: provided at no charge for BB
# Category Total
nutrition_behavior_sessions_total = registered_dietitian +\
                                    social_worker +\
                                    educational_tools +\
                                    classroom_utilities
# Parent Sessions
# includes social_worker, printed_materials, classroom_utilities
# Category Total
parent_sessions_total = social_worker +\
                        printed_materials +\
                        classroom_utilities
# Administration
exercise_physiologist_admin = 6990.00
registered_dietitian_admin = 16376.00
# Category Total
administration_bb_total = exercise_physiologist_admin +\
                       registered_dietitian_admin
# Weigh-Ins (before each session)
technician = 1200.00
body_fat_analyzer_scale = 700.00
stadiometer = 100.00
# Category Total
weigh_ins_total = technician +\
                  body_fat_analyzer_scale +\
                  stadiometer
# Medical Director
medical_consultation = 5100.00
# Category Total
medical_director_total = medical_consultation

# Total Overall for BB
total_cost_bb = exercise_sessions_total +\
             nutrition_behavior_sessions_total +\
             parent_sessions_total +\
             administration_bb_total +\
             weigh_ins_total +\
             medical_director_total
# Total per Child (based on 90 children - full BB capacity)
n_children_bb = 90
total_per_child_bb = total_cost_bb/n_children_bb


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
administration_cc_total = dept_clinical_secretary +\
                          clinical_secretary +\
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
other_costs_cc_total = rent_space_utilities +\
                    cleaning_service +\
                    clinic_equipment_supplies

# Total Overall for CC
total_cost_cc = nurse_visit_fu_total +\
                nutrition_visit_fu_total +\
                behavioral_counseling_visit_fu_total +\
                administration_cc_total +\
                weigh_ins_cc_total +\
                medical_director_cc_total +\
                other_costs_cc_total
# Total per Child (based on 90 children - full BB capacity)
total_per_child_cc = total_cost_cc/n_children_bb

# COSTS FINAL per person
cost_BB = total_per_child_bb  # should be 588
cost_CC = total_per_child_cc  # should be 533
