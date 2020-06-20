import SimPy.DataFrames as df
from SimPy import RandomVariateGenerators as RVGs
import InputData as D
import source.Data as Data
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

        # cost parameters are determined later by a sample from specified probability distributions
        self.annualInterventionCost = 0
        self.costAbove95thP = 0
        self.costBelow95thP = 0
        self.costPerUnitBMIAdultP = 0

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

            # fit a gamma distribution (only if mean > 0)
            if mean_stdev[0] > 0:
                fit_output = RVGs.Gamma.fit_mm(mean=mean_stdev[0], st_dev=mean_stdev[1])
                # store the gamma RVG
                self.dictOfRVGs[key] = RVGs.Gamma(a=fit_output["a"],
                                                  loc=0,
                                                  scale=fit_output["scale"])
            else:
                # use a constant
                self.dictOfRVGs[key] = RVGs.Constant(value=0)

    def get_sample(self, cost_item_name, rng):

        return self.dictOfRVGs[cost_item_name].sample(rng)

    def get_total(self, rng):

        total = 0
        for key, rvg in self.dictOfRVGs.items():
            total += rvg.sample(rng)

        return total


class ParamGenerator:
    def __init__(self, intervention, maintenance_scenario):

        self.intervention = intervention
        self.maintenance_scenario = maintenance_scenario

        # get BMI trajectories
        self.trajectories = T.get_trajectories()

        # make dictionaries of RVGs for Bright Bodies cost items
        if intervention == D.Interventions.BRIGHT_BODIES:
            self.interventionCostParamRVGs = CostParamRVGs(
                dict_of_cost_parameters=Data.DICT_COST_BB)

        # make dictionaries of RVGs for Control cost items
        elif intervention == D.Interventions.CONTROL:
            self.interventionCostParamRVGs = CostParamRVGs(
                dict_of_cost_parameters=Data.DICT_COST_CONTROL)

        # make dictionaries of RVGs for health care expenditure cost items
        self.hcExpenditureParamRVGs = CostParamRVGs(
            dict_of_cost_parameters=Data.DICT_HC_EXP)

    def get_new_parameters(self, rng):

        param = Parameters(trajectories=self.trajectories,
                           intervention=self.intervention,
                           maintenance_scenario=self.maintenance_scenario)

        # sample health care expenditure items
        param.costAbove95thP = self.hcExpenditureParamRVGs.get_sample(
            cost_item_name='<18 years, >95th %ile', rng=rng)
        param.costBelow95thP = self.hcExpenditureParamRVGs.get_sample(
            cost_item_name='<18 years, <95th %ile', rng=rng)
        param.costPerUnitBMIAdultP = self.hcExpenditureParamRVGs.get_sample(
            cost_item_name='>18 years', rng=rng)
        # adjust for inflation
        adj_factor = (1+D.INFLATION)**(D.CURRENT_YEAR - Data.YEAR_BB_STUDY)
        param.costAbove95thP *= adj_factor
        param.costBelow95thP *= adj_factor
        param.costPerUnitBMIAdultP *= adj_factor

        # sample the cost of interventions
        total_intervention_cost = self.interventionCostParamRVGs.get_total(rng)
        # adjust to inflation
        total_intervention_cost *= (1+D.INFLATION)**(D.CURRENT_YEAR - Data.YEAR_HCEXP_STUDY)
        # average cost per participants
        param.annualInterventionCost = total_intervention_cost/D.N_CHILDREN_BB

        return param
