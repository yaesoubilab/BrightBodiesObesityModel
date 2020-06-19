# COSTING OF BB/CONTROL: Original Data

# TODO: Sydney would you please complete these two dictionaries?

# dictionary of cost items for Bright Bodies
# each element is a list of [mean, stDev]
DICT_COST_BB = {
    'Exercise physiologist': [9592.00, 0.1*9592.00],
    'Games and equipment': [1900.00, 0.1*1900.00],
    'Motivational tools': [240.00, 0.1 * 240.00],
    'Printed material': [25.00, 0.1 * 25.00],
    'Gym room and utilities': [0.00, 0.1 * 0.00],
    'First aid kit': [150.00, 0.1 * 150.00],
    'Registered dietitian': [6805.00, 0.1 * 6805.00],
    'Social worker': [1200.00, 0.1 * 1200.00],
    'Educational tools': [1350.00, 0.1 * 1350.00],
    'Classroom and utilities': [0.00, 0.1 * 0.00],
    'Exercise physiologist (admin)': [6990.00, 0.1 * 6990.00],
    'Registered dietitian (admin)': [16376.00, 0.1 * 16376.00],
    'Technician': [1200.00, 0.1 * 1200.00],
    'Body fat analyzer and scale': [700.00, 0.1 * 700.00],
    'Stadiometer': [100.00, 0.1 * 100.00],
    'Medical consultation': [5100.00, 0.1 * 5100.00]
}

# dictionary of cost items for the Control
# each element is a list of [mean, stDev]
DICT_COST_CONTROL = {
    'Nurse practitioner': [11686.00, 0.1*11686.00],
    'Registered dietitian (CC)': [6329.00, 0.1*6329.00],
    'Social worker (CC)': [6460.00, 0.1*6460.00],
    'Dept clinical secretary': [834.00, 0.1*834.00],
    'Clinic secretary': [1669.00, 0.1*1669.00],
    'Typing': [2504.00, 0.1*2504.00],
    'Lab technician': [1408.00, 0.1*1408.00],
    'Medical consultation (CC)': [10256.00, 0.1*10256.00],
    'Rent space, utilities': [3000.00, 0.1*3000.00],
    'Cleaning service': [885.00, 0.1*885.00],
    'Clinic equipment and supplies': [2900.00, 0.1*2900.00]
}


# INTERVENTION COSTS of BRIGHT BODIES (detailed)

# Exercise Sessions
exercise_physiologist = 9592.00
games_equipment = 1900.00
motivational_tools = 240.00
printed_materials = 25.00
gym_room_utilities = 0.00  # note: provided at no charge for BB
first_aid_kit = 150.00

# Nutrition/Behavior Modification Sessions
registered_dietitian = 6805.00
social_worker = 1200.00
educational_tools = 1350.00
classroom_utilities = 0.00  # note: provided at no charge for BB

# Administration
exercise_physiologist_admin = 6990.00
registered_dietitian_admin = 16376.00

# Weigh-Ins (before each session)
technician = 1200.00
body_fat_analyzer_scale = 700.00
stadiometer = 100.00

# Medical Director
medical_consultation = 5100.00


# INTERVENTIONS COSTS of CLINICAL CONTROL

# Nurse Visit and Follow Up
nurse_practitioner = 11686.00

# Nutrition Visit and Follow Up
registered_dietitian_cc = 6329.00

# Behavioral Counseling Visit and Follow Up
social_worker_cc = 6460.00

# Administration
dept_clinical_secretary = 834.00
clinic_secretary = 1669.00
typing = 2504.00

# Weigh Ins + Labs
lab_technician = 1408.00

# Medical Director Visit and Follow Up
medical_consultation_cc = 10256.00

# Rent Space/Utilities + Cleaning Service + Clinic Equipment/Supplies
rent_space_utilities = 3000.00
cleaning_service = 885.00
clinic_equipment_supplies = 2900.00


# ATTRIBUTABLE HC EXPENDITURE: generate distributions

# <18 years, >95th %ile
cost_above_95th = 220
# <18 years, <95th %ile
cost_below_95th = 180
# >18 years
cost_per_unit_bmi_above_95th_adult = 197
