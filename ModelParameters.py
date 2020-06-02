import SimPy.DataFrames as df
from SimPy import InOutFunctions as InOutSupport
from SimPy import RandomVariateGenerators as RVGs
from ParamSupport import *
import InputData as D


class SetOfTrajectories:
    # class to select randomly a row from a set of rows
    def __init__(self, rows):
        self.rows = rows
        self.discreteUniform = RVGs.UniformDiscrete(0, len(rows) - 1)

    def sample_traj(self, rng):
        i = self.discreteUniform.sample(rng)
        return self.rows[i]


def get_trajectories():
    """
    :return: the list of BMI trajectories (by sex and age) from the csv files
    """

    # creating a data frame of trajectories
    trajectories = df.DataFrameOfObjects(list_x_min=[8, 0],
                                         list_x_max=[16, 1],
                                         list_x_delta=[1, 'int'])

    # populate the data frame
    for sex in ['male', 'female']:
        for age in range(8, 17, 1):
            file_name = 'csv_trajectories/{0}_{1}_o_f.csv'.format(sex, age)
            rows = InOutSupport.read_csv_rows(file_name=file_name,
                                              delimiter=',',
                                              if_ignore_first_row=True,
                                              if_convert_float=True)
            s = 0 if sex == 'male' else 1
            trajectories.set_obj(x_value=[age, s],
                                 obj=SetOfTrajectories(rows=rows))

    return trajectories


class Parameters:
    # class to contain the parameters of the model
    def __init__(self, trajectories, intervention, maintenance_scenario):
        """
        :param trajectories: (DataFrameOfObjects) of BMI trajectories (by sex and age)
        :param intervention: which intervention to model
        :param maintenance_scenario: effect maintenance scenario
        """

        self.trajectories = trajectories
        self.intervention = intervention
        self.popSize = D.POP_SIZE
        self.simInitialDuration = D.SIM_INIT

        # population distribution by age/sex for Bright Bodies (age 8 - 16)
        self.ageSexDist = df.DataFrameWithEmpiricalDist(rows=D.age_sex_dist,        # life table
                                                        list_x_min=[8, 0],          # minimum values for age/sex groups
                                                        list_x_max=[16, 1],         # maximum values for age/sex groups
                                                        list_x_delta=[1, 'int'])    # [age interval, sex categorical]

        # intervention multipliers to reduce BMI over time
        self.interventionMultipliers = []
        if intervention == D.Interventions.BRIGHT_BODIES:

            if maintenance_scenario == D.EFFECT_MAINTENANCE.FULL:
                self.interventionMultipliers = [1.0, D.multBBYear1, D.multBBYear2]
                for i in range(10):
                    self.interventionMultipliers.append(D.multBBYear2)

            elif maintenance_scenario == D.EFFECT_MAINTENANCE.NONE:
                self.interventionMultipliers = [1.0, D.multBBYear1, D.multBBYear2]
                for i in range(10):
                    self.interventionMultipliers.append(D.multCC)

            elif maintenance_scenario == D.EFFECT_MAINTENANCE.DEPREC:
                self.interventionMultipliers = [1.0, D.multBBYear1, D.multBBYear2]
                for i in range(10):
                    deprec_difference = D.multCC - D.multBBYear2
                    deprec_value = deprec_difference / 8
                    deprec_multiplier = D.multBBYear2 + (deprec_value * i)
                    self.interventionMultipliers.append(deprec_multiplier)

        else: # under control
            self.interventionMultipliers = [1]
            for i in range(10):
                self.interventionMultipliers.append(D.multCC)


class ParamGenerator:
    def __init__(self, intervention, maintenance_scenario):

        self.intervention = intervention
        self.maintenance_scenario = maintenance_scenario

        # get BMI trajectories
        self.trajectories = get_trajectories()

    # create variable for each cost item

        # BRIGHT BODIES

        # create gamma dist for exercise physiologist cost (BRIGHT BODIES)        
        fit_output = RVGs.Gamma.fit_mm(mean=exercise_physiologist,
                                       st_dev=0.1*exercise_physiologist)
        self.exPhysRVG = RVGs.Gamma(a=fit_output["a"],
                                    loc=0,
                                    scale=fit_output["scale"])
        # create gamma dist for games_equipment
        fit_output = RVGs.Gamma.fit_mm(mean=games_equipment,
                                       st_dev=0.1*games_equipment)
        self.gamesRVG = RVGs.Gamma(a=fit_output["a"],
                                   loc=0,
                                   scale=fit_output["scale"])
        # create gamma dist for motivational_tools
        fit_output = RVGs.Gamma.fit_mm(mean=motivational_tools,
                                       st_dev=0.1*motivational_tools)
        self.motivToolsRVG = RVGs.Gamma(a=fit_output["a"],
                                        loc=0,
                                        scale=fit_output["scale"])
        # create gamma dist for printed_materials
        fit_output = RVGs.Gamma.fit_mm(mean=printed_materials,
                                       st_dev=0.1*printed_materials)
        self.printedMaterialRVG = RVGs.Gamma(a=fit_output["a"],
                                             loc=0,
                                             scale=fit_output["scale"])
        # create gamma dist for first_aid_kit
        fit_output = RVGs.Gamma.fit_mm(mean=first_aid_kit,
                                       st_dev=0.1*first_aid_kit)
        self.firstAidRVG = RVGs.Gamma(a=fit_output["a"],
                                      loc=0,
                                      scale=fit_output["scale"])
        # create gamma dist for registered_dietitian
        fit_output = RVGs.Gamma.fit_mm(mean=registered_dietitian,
                                       st_dev=0.1*registered_dietitian)
        self.regDietRVG = RVGs.Gamma(a=fit_output["a"],
                                     loc=0,
                                     scale=fit_output["scale"])
        # create gamma dist for social_worker
        fit_output = RVGs.Gamma.fit_mm(mean=social_worker,
                                       st_dev=0.1*social_worker)
        self.socialWorkerRVG = RVGs.Gamma(a=fit_output["a"],
                                          loc=0,
                                          scale=fit_output["scale"])
        # create gamma dist for educational_tools
        fit_output = RVGs.Gamma.fit_mm(mean=educational_tools,
                                       st_dev=0.1*educational_tools)
        self.eduToolsRVG = RVGs.Gamma(a=fit_output["a"],
                                      loc=0,
                                      scale=fit_output["scale"])
        # create gamma dist for exercise_physiologist_admin
        fit_output = RVGs.Gamma.fit_mm(mean=exercise_physiologist_admin,
                                       st_dev=0.1*exercise_physiologist_admin)
        self.exPhysCoordRVG = RVGs.Gamma(a=fit_output["a"],
                                         loc=0,
                                         scale=fit_output["scale"])
        # create gamma dist for registered_dietitian_admin
        fit_output = RVGs.Gamma.fit_mm(mean=registered_dietitian_admin,
                                       st_dev=0.1*registered_dietitian_admin)
        self.regDietCoordRVG = RVGs.Gamma(a=fit_output["a"],
                                          loc=0,
                                          scale=fit_output["scale"])
        # create gamma dist for technician
        fit_output = RVGs.Gamma.fit_mm(mean=technician,
                                       st_dev=0.1*technician)
        self.technicianRVG = RVGs.Gamma(a=fit_output["a"],
                                        loc=0,
                                        scale=fit_output["scale"])
        # create gamma dist for body_fat_analyzer_scale
        fit_output = RVGs.Gamma.fit_mm(mean=body_fat_analyzer_scale,
                                       st_dev=0.1*body_fat_analyzer_scale)
        self.bfAnalyserRVG = RVGs.Gamma(a=fit_output["a"],
                                        loc=0,
                                        scale=fit_output["scale"])
        # create gamma dist for stadiometer
        fit_output = RVGs.Gamma.fit_mm(mean=stadiometer,
                                       st_dev=0.1*stadiometer)
        self.stadiometerRVG = RVGs.Gamma(a=fit_output["a"],
                                         loc=0,
                                         scale=fit_output["scale"])
        # create gamma dist for medical_consultation
        fit_output = RVGs.Gamma.fit_mm(mean=medical_consultation,
                                       st_dev=0.1*medical_consultation)
        self.medConsultRVG = RVGs.Gamma(a=fit_output["a"],
                                        loc=0,
                                        scale=fit_output["scale"])
        # ***gym room utilities and classroom utilities costs are 0

        # CLINICAL CONTROL

        # create gamma dist for nurse_practitioner
        fit_output = RVGs.Gamma.fit_mm(mean=nurse_practitioner,
                                       st_dev=0.1*nurse_practitioner)
        self.nursePractitionerRVG = RVGs.Gamma(a=fit_output["a"],
                                               loc=0,
                                               scale=fit_output["scale"])
        # create gamma dist for registered_dietitian_cc
        fit_output = RVGs.Gamma.fit_mm(mean=registered_dietitian_cc,
                                       st_dev=0.1*registered_dietitian_cc)
        self.regDietControlRVG = RVGs.Gamma(a=fit_output["a"],
                                            loc=0,
                                            scale=fit_output["scale"])
        # create gamma dist for social_worker_cc
        fit_output = RVGs.Gamma.fit_mm(mean=social_worker_cc,
                                       st_dev=0.1*social_worker_cc)
        self.socialWorkerControlRVG = RVGs.Gamma(a=fit_output["a"],
                                                 loc=0,
                                                 scale=fit_output["scale"])
        # create gamma dist for dept_clinical_secretary
        fit_output = RVGs.Gamma.fit_mm(mean=dept_clinical_secretary,
                                       st_dev=0.1*dept_clinical_secretary)
        self.deptClinicSecretaryRVG = RVGs.Gamma(a=fit_output["a"],
                                                 loc=0,
                                               scale=fit_output["scale"])
        # create gamma dist for clinical_secretary
        fit_output = RVGs.Gamma.fit_mm(mean=clinical_secretary,
                                       st_dev=0.1*clinical_secretary)
        self.clinicSecretaryRVG = RVGs.Gamma(a=fit_output["a"],
                                             loc=0,
                                             scale=fit_output["scale"])
        # create gamma dist for typing
        fit_output = RVGs.Gamma.fit_mm(mean=typing,
                                       st_dev=0.1*typing)
        self.typingRVG = RVGs.Gamma(a=fit_output["a"],
                                    loc=0,
                                    scale=fit_output["scale"])
        # create gamma dist for lab_technician
        fit_output = RVGs.Gamma.fit_mm(mean=lab_technician,
                                       st_dev=0.1*lab_technician)
        self.labTechRVG = RVGs.Gamma(a=fit_output["a"],
                                     loc=0,
                                     scale=fit_output["scale"])
        # create gamma dist for medical_consultation_cc
        fit_output = RVGs.Gamma.fit_mm(mean=medical_consultation_cc,
                                       st_dev=0.1*medical_consultation_cc)
        self.medConsultControlRVG = RVGs.Gamma(a=fit_output["a"],
                                               loc=0,
                                               scale=fit_output["scale"])
        # create gamma dist for rent_space_utilities
        fit_output = RVGs.Gamma.fit_mm(mean=rent_space_utilities,
                                       st_dev=0.1*rent_space_utilities)
        self.rentSpaceRVG = RVGs.Gamma(a=fit_output["a"],
                                       loc=0,
                                       scale=fit_output["scale"])
        # create gamma dist for cleaning_service
        fit_output = RVGs.Gamma.fit_mm(mean=cleaning_service,
                                       st_dev=0.1*cleaning_service)
        self.cleaningRVG = RVGs.Gamma(a=fit_output["a"],
                                      loc=0,
                                      scale=fit_output["scale"])
        # create gamma dist for clinic_equipment_supplies
        fit_output = RVGs.Gamma.fit_mm(mean=clinic_equipment_supplies,
                                       st_dev=0.1*clinic_equipment_supplies)
        self.clinicEquipRVG = RVGs.Gamma(a=fit_output["a"],
                                         loc=0,
                                         scale=fit_output["scale"])

        # CONSTANTS
        self.costAbove95th = RVGs.Constant(value=cost_above_95th)
        self.costBelow95th = RVGs.Constant(value=cost_below_95th)
        self.costPerUnitBMI_Adult = RVGs.Constant(value=cost_per_unit_bmi_above_95th_adult)

    def get_new_parameters(self, rng):

        param = Parameters(trajectories=self.trajectories,
                           intervention=self.intervention,
                           maintenance_scenario=self.maintenance_scenario)

        # sample from distributions

        # TODO: if there are parameters that are common between the two
        #   interventions and are sampled from the same distribution,
        #   would you please move them here before the if statement.
        #   That is less error prone than having them twice under the
        #   if statement.

        # BRIGHT BODIES

        # exercise sessions
        if self.intervention is D.Interventions.BRIGHT_BODIES:
            # TODO: I'd suggest removing 'param_' from the beginning of these
            #   variables to simplify the variable names.
            param_exercise_physiologist = self.exPhysRVG.sample(rng)
            param_games_equipment = self.gamesRVG.sample(rng)
            param_motivational_tools = self.motivToolsRVG.sample(rng)
            param_printed_materials = self.printedMaterialRVG.sample(rng)
            param_first_aid_kit = self.firstAidRVG.sample(rng)
            # nutrition behavior modification
            param_registered_dietitian = self.regDietRVG.sample(rng)
            param_social_worker = self.socialWorkerRVG.sample(rng)
            param_educational_tools = self.eduToolsRVG.sample(rng)
            # parent sessions
            param_social_worker_2 = self.socialWorkerRVG.sample(rng)
            param_printed_materials_2 = self.printedMaterialRVG.sample(rng)
            # administration
            param_exercise_physiologist_admin = self.exPhysCoordRVG.sample(rng)
            param_registered_dietitian_admin = self.regDietCoordRVG.sample(rng)
            # weigh ins
            param_technician = self.technicianRVG.sample(rng)
            param_body_fat_analyzer_scale = self.bfAnalyserRVG.sample(rng)
            param_stadiometer = self.stadiometerRVG.sample(rng)
            # medical director
            param_medical_consultation = self.medConsultRVG.sample(rng)

            # calculate category totals: BRIGHT BODIES
            total_exercise_sessions = (
                param_exercise_physiologist + param_games_equipment + param_motivational_tools
                + param_printed_materials + param_first_aid_kit)
            total_nutrition_behavior_sessions = (param_registered_dietitian + param_social_worker + param_educational_tools)
            total_parent_sessions = (param_social_worker_2 + param_printed_materials_2)
            total_administration = (param_exercise_physiologist_admin + param_registered_dietitian_admin)
            total_weigh_ins = (param_technician + param_body_fat_analyzer_scale + param_stadiometer)
            total_medical_director = param_medical_consultation

            # OVERALL cost: BB
            param.total_cost_bb = total_exercise_sessions + total_nutrition_behavior_sessions + \
                total_parent_sessions + total_administration + total_weigh_ins + \
                total_medical_director
            # adjusting for inflation (2007 dollar --> 2020 dollar)
            param.total_cost_bb = param.total_cost_bb*((1+D.INFLATION)**(2020-2007))

            # INDIVIDUAL cost: BB
            param.annualInterventionCost = param.total_cost_bb / D.N_CHILDREN_BB
            # param.annualInterventionCostBB = param.total_cost_bb / D.N_CHILDREN_BB

            # HC EXPENDITURE (constants)
            cost_above_95 = self.costAbove95th.sample(rng)
            param.costAbove95thP = cost_above_95
            cost_below_95 = self.costBelow95th.sample(rng)
            param.costBelow95thP = cost_below_95
            cost_per_unit_bmi = self.costPerUnitBMI_Adult.sample(rng)
            param.costPerUnitBMIAdultP = cost_per_unit_bmi

        # CONTROL
        if self.intervention is D.Interventions.CONTROL:
            # nurse visit and follow up
            param_nurse_practitioner = self.nursePractitionerRVG.sample(rng)
            # nutrition visit and follow up
            param_registered_dietitian_cc = self.regDietControlRVG.sample(rng)
            # behavioral counseling visit and follow up
            param_social_worker_cc = self.socialWorkerControlRVG.sample(rng)
            # administration
            param_dept_clinical_secretary = self.deptClinicSecretaryRVG.sample(rng)
            param_clinical_secretary = self.clinicSecretaryRVG.sample(rng)
            param_typing = self.typingRVG.sample(rng)
            # weigh ins and labs
            param_lab_technician = self.labTechRVG.sample(rng)
            # medical director visit and follow up
            param_medical_consultation_cc = self.medConsultControlRVG.sample(rng)
            # rent space/utilities and cleaning service
            param_rent_space_utilities = self.rentSpaceRVG.sample(rng)
            param_cleaning_service = self.cleaningRVG.sample(rng)
            param_clinic_equipment_supplies = self.clinicEquipRVG.sample(rng)

            # calculate category totals: CONTROL
            total_nurse_visit = param_nurse_practitioner
            total_nutrition_visit = param_registered_dietitian_cc
            total_behavior_counseling = param_social_worker_cc
            total_administration_control = (param_dept_clinical_secretary + param_clinical_secretary + param_typing)
            total_weigh_ins_control = param_lab_technician
            total_medical_director_control = param_medical_consultation_cc
            total_rent_utilities = (param_rent_space_utilities + param_cleaning_service +
                                    param_clinic_equipment_supplies)

            # OVERALL cost: CC
            param.total_cost_cc = total_nurse_visit + total_nutrition_visit + total_behavior_counseling + \
                total_administration_control + total_weigh_ins_control + total_medical_director_control + \
                total_rent_utilities
            # adjusting for inflation (2007 dollar --> 2020 dollar)
            param.total_cost_cc = param.total_cost_cc*((1+D.INFLATION)**(2020-2007))

            # INDIVIDUAL cost: CC
            param.annualInterventionCost = param.total_cost_cc/D.N_CHILDREN_BB
            # param.annualInterventionCostCC = param.total_cost_cc/D.N_CHILDREN_BB

            # attributable hc expenditure
            cost_above_95 = self.costAbove95th.sample(rng)
            param.costAbove95thP = cost_above_95
            cost_below_95 = self.costBelow95th.sample(rng)
            param.costBelow95thP = cost_below_95
            cost_per_unit_bmi = self.costPerUnitBMI_Adult.sample(rng)
            param.costPerUnitBMIAdultP = cost_per_unit_bmi

        # return the parameter set
        return param
