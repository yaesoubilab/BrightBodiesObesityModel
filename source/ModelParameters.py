import SimPy.DataFrames as df
from SimPy import RandomVariateGenerators as RVGs
import source.ParamSupport as P
import InputData as D
import source.SupportData as Data
import source.ModelTrajectory as T


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

        self.annualInterventionCost = 0
        self.costAbove95thP = 0
        self.costBelow95thP = 0
        self.costPerUnitBMIAdultP = 0

        # population distribution by age/sex for Bright Bodies (age 8 - 16)
        self.ageSexDist = df.DataFrameWithEmpiricalDist(rows=Data.age_sex_dist,        # life table
                                                        list_x_min=[8, 0],          # minimum values for age/sex groups
                                                        list_x_max=[16, 1],         # maximum values for age/sex groups
                                                        list_x_delta=[1, 'int'])    # [age interval, sex categorical]

        # BMI 95th cut offs
        self.bmi95thCutOffs = df.DataFrame(rows=Data.bmi_95th_cut_offs,
                                           list_x_min=[8, 0],  # minimum values for age/sex groups
                                           list_x_max=[18, 1],  # maximum values for age/sex groups
                                           list_x_delta=[1, 'int'])  # [age interval, sex categorical]

        # intervention multipliers to reduce BMI over time
        self.interventionMultipliers = []
        if intervention == D.Interventions.BRIGHT_BODIES:

            if maintenance_scenario == D.EffectMaintenance.FULL:
                self.interventionMultipliers = [1.0, D.multBBYear1, D.multBBYear2]
                for i in range(10):
                    self.interventionMultipliers.append(D.multBBYear2)

            elif maintenance_scenario == D.EffectMaintenance.NONE:
                self.interventionMultipliers = [1.0, D.multBBYear1, D.multBBYear2]
                for i in range(10):
                    self.interventionMultipliers.append(D.multCC)

            elif maintenance_scenario == D.EffectMaintenance.DEPREC:
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


class CostParamRVGs:
    def __init__(self, dict_of_cost_parameters):

        self.dictOfRVGs = {}
        for key, mean_stdev in dict_of_cost_parameters.items():

            # fit a gamma distribution
            fit_output = RVGs.Gamma.fit_mm(mean=mean_stdev[0],
                                           st_dev=mean_stdev[1])
            # store the gamma RVG
            self.dictOfRVGs[key] = RVGs.Gamma(a=fit_output["a"],
                                              loc=0,
                                              scale=fit_output["scale"])


class ParamGenerator:
    def __init__(self, intervention, maintenance_scenario):

        self.intervention = intervention
        self.maintenance_scenario = maintenance_scenario

        # get BMI trajectories
        self.trajectories = T.get_trajectories()

        # make dictionaries of RVGs for Bright Bodies cost items
        if intervention == D.Interventions.BRIGHT_BODIES:
            self.interventionCostParamRVGs = CostParamRVGs(dict_of_cost_parameters=P.DICT_COST_BB)

        # make dictionaries of RVGs for Control cost items
        elif intervention == D.Interventions.CONTROL:
            self.interventionCostParamRVGs = CostParamRVGs(dict_of_cost_parameters=P.DICT_COST_CONTROL)

        # make dictionaries of RVGs for health care expenditure cost items
        self.hcExpenditureParamRVGs = CostParamRVGs(dict_of_cost_parameters=P.DICT_HC_EXP)


    def get_new_parameters(self, rng):

        param = Parameters(trajectories=self.trajectories,
                           intervention=self.intervention,
                           maintenance_scenario=self.maintenance_scenario)

        # sample from distributions
        # BRIGHT BODIES

        # exercise sessions
        if self.intervention is D.Interventions.BRIGHT_BODIES:
            exercise_physiologist = self.exPhysRVG.sample(rng)
            games_equipment = self.gamesRVG.sample(rng)
            motivational_tools = self.motivToolsRVG.sample(rng)
            printed_materials = self.printedMaterialRVG.sample(rng)
            first_aid_kit = self.firstAidRVG.sample(rng)
            # nutrition behavior modification
            registered_dietitian = self.regDietRVG.sample(rng)
            social_worker = self.socialWorkerRVG.sample(rng)
            educational_tools = self.eduToolsRVG.sample(rng)
            # parent sessions
            social_worker_2 = self.socialWorkerRVG.sample(rng)
            printed_materials_2 = self.printedMaterialRVG.sample(rng)
            # administration
            exercise_physiologist_admin = self.exPhysCoordRVG.sample(rng)
            registered_dietitian_admin = self.regDietCoordRVG.sample(rng)
            # weigh ins
            technician = self.technicianRVG.sample(rng)
            body_fat_analyzer_scale = self.bfAnalyserRVG.sample(rng)
            stadiometer = self.stadiometerRVG.sample(rng)
            # medical director
            medical_consultation = self.medConsultRVG.sample(rng)

            # calculate category totals: BRIGHT BODIES
            total_exercise_sessions = (
                exercise_physiologist + games_equipment + motivational_tools
                + printed_materials + first_aid_kit)
            total_nutrition_behavior_sessions = (registered_dietitian + social_worker + educational_tools)
            total_parent_sessions = (social_worker_2 + printed_materials_2)
            total_administration = (exercise_physiologist_admin + registered_dietitian_admin)
            total_weigh_ins = (technician + body_fat_analyzer_scale + stadiometer)
            total_medical_director = medical_consultation

            # OVERALL cost: BB
            param.total_cost_bb = total_exercise_sessions + total_nutrition_behavior_sessions + \
                total_parent_sessions + total_administration + total_weigh_ins + \
                total_medical_director
            # adjusting for inflation (2007 dollar --> current dollar)
            param.total_cost_bb = param.total_cost_bb*((1+D.INFLATION)**(D.CURRENT_YEAR - 2007))

            # INDIVIDUAL cost: BB
            param.annualInterventionCost = param.total_cost_bb / D.N_CHILDREN_BB

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
            nurse_practitioner = self.nursePractitionerRVG.sample(rng)
            # nutrition visit and follow up
            registered_dietitian_cc = self.regDietControlRVG.sample(rng)
            # behavioral counseling visit and follow up
            social_worker_cc = self.socialWorkerControlRVG.sample(rng)
            # administration
            dept_clinical_secretary = self.deptClinicSecretaryRVG.sample(rng)
            clinical_secretary = self.clinicSecretaryRVG.sample(rng)
            typing = self.typingRVG.sample(rng)
            # weigh ins and labs
            lab_technician = self.labTechRVG.sample(rng)
            # medical director visit and follow up
            medical_consultation_cc = self.medConsultControlRVG.sample(rng)
            # rent space/utilities and cleaning service
            rent_space_utilities = self.rentSpaceRVG.sample(rng)
            cleaning_service = self.cleaningRVG.sample(rng)
            clinic_equipment_supplies = self.clinicEquipRVG.sample(rng)

            # calculate category totals: CONTROL
            total_nurse_visit = nurse_practitioner
            total_nutrition_visit = registered_dietitian_cc
            total_behavior_counseling = social_worker_cc
            total_administration_control = (dept_clinical_secretary + clinical_secretary + typing)
            total_weigh_ins_control = lab_technician
            total_medical_director_control = medical_consultation_cc
            total_rent_utilities = (rent_space_utilities + cleaning_service +
                                    clinic_equipment_supplies)

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
