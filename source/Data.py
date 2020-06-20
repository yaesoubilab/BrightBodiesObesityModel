
YEAR_BB_STUDY = 2007
YEAR_HCEXP_STUDY = 2010

# dictionary of cost items for Bright Bodies
# each element is a list of [mean, stDev]
DICT_COST_BB = {
    'Exercise physiologist': [9592.00, 0.1*9592.00, 2007],
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

DICT_HC_EXP = {
    '<18 years, >95th %ile': [220, 0.1*220],
    '<18 years, <95th %ile': [180, 0.1*180],
    '>18 years': [197, 197*0.1]
}


# for Bright Bodies (8-16 y/o)
# use to initialize cohort
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

# bmi cut offs
bmi_95th_cut_offs = [
    # age, sex, bmi_cutoff
    [8, 0, 20.0],   # 8, male
    [8, 1, 20.6],   # 8, female
    [9, 0, 21.1],   # 9, male
    [9, 1, 21.8],   # 9, female
    [10, 0, 22.1],  # 10, male
    [10, 1, 22.9],  # 10, female
    [11, 0, 23.2],  # 11, male
    [11, 1, 24.1],  # 11, female
    [12, 0, 24.2],  # 12, male
    [12, 1, 25.2],  # 12, female
    [13, 0, 25.2],  # 13, male
    [13, 1, 26.2],  # 13, female
    [14, 0, 26.0],  # 14, male
    [14, 1, 27.2],  # 14, female
    [15, 0, 26.8],  # 15, male
    [15, 1, 28.1],  # 15, female
    [16, 0, 27.5],  # 16, male
    [16, 1, 28.9],   # 16, female
    [17, 0, 28.2],  # 15, male
    [17, 1, 29.6],  # 15, female
    [18, 0, 30],  # 15, male
    [18, 1, 30]  # 15, female
]