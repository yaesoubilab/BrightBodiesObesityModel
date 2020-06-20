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
        self.interventionMultipliers = [] # multipliers to adjust BMI trajectories


class CostParamRVGs:
    # class to contain the random variate generators of cost parameters

    def __init__(self, dict_of_cost_parameters):
        """
        :param dict_of_cost_parameters: dictionary of cost parameters
        """

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
        """
        :param cost_item_name: name of the cost item to get a sample for
        :param rng: random number generator
        :return: a sample from the distribution of the cost item specified
        """
        return self.dictOfRVGs[cost_item_name].sample(rng)

    def get_total(self, rng):
        """
        :param rng: random number generator
        :return: sum of samples from all cost items
        """
        total = 0
        for key, rvg in self.dictOfRVGs.items():
            total += rvg.sample(rng)

        return total


class MultiplierParamRVGs:
    # class to contain the random variate generators of multiplier parameters to adjust BMI trajectories

    def __init__(self, dict_of_cost_parameters):
        """
        :param dict_of_cost_parameters: dictionary of cost parameters
        """

        self.dictOfRVGs = {}
        for key, mean_stdev in dict_of_cost_parameters.items():

            # fit a log-normal distribution (only if mean > 0)
            if mean_stdev[0] > 0:
                fit_output = RVGs.LogNormal.fit_mm(mean=mean_stdev[0], st_dev=mean_stdev[1])
                # store the log-normal RVG
                self.dictOfRVGs[key] = RVGs.LogNormal(mu=fit_output["mu"],
                                                      loc=0,
                                                      sigma=fit_output["sigma"])
            else:
                # use a constant
                self.dictOfRVGs[key] = RVGs.Constant(value=0)

    def get_sample(self, multiplier_name, rng):
        """
        :param multiplier_name: name of the multiplier to get a sample for
        :param rng: random number generator
        :return: a sample from the distribution of the multiplier specified
        """
        return self.dictOfRVGs[multiplier_name].sample(rng)


class ParamGenerator:
    def __init__(self, intervention, maintenance_scenario):

        self.intervention = intervention
        self.maintenance_scenario = maintenance_scenario

        # get BMI trajectories
        self.trajectories = T.get_trajectories()

        # make dictionaries of RVGs for multipliers to adjust trajectories
        self.multiplierRVGs = MultiplierParamRVGs(
            dict_of_cost_parameters=Data.DICT_MULTIPLIERS
        )

        # make dictionaries of RVGs for Bright Bodies cost items
        if intervention == D.Interventions.BRIGHT_BODIES:
            self.interventionCostParamRVGs = CostParamRVGs(
                dict_of_cost_parameters=Data.DICT_COST_BB
            )

        # make dictionaries of RVGs for Control cost items
        elif intervention == D.Interventions.CONTROL:
            self.interventionCostParamRVGs = CostParamRVGs(
                dict_of_cost_parameters=Data.DICT_COST_CONTROL
            )

        # make dictionaries of RVGs for health care expenditure cost items
        self.hcExpenditureParamRVGs = CostParamRVGs(
            dict_of_cost_parameters=Data.DICT_HC_EXP
        )

    def get_new_parameters(self, rng):

        param = Parameters(trajectories=self.trajectories,
                           intervention=self.intervention,
                           maintenance_scenario=self.maintenance_scenario)

        # find multipliers to adjust trajectories
        m_bb1 = self.multiplierRVGs.get_sample(multiplier_name='BB Year 1', rng=rng)
        m_bb2 = self.multiplierRVGs.get_sample(multiplier_name='BB Year 2', rng=rng)
        m_control = self.multiplierRVGs.get_sample(multiplier_name='Control', rng=rng)

        # find multipliers to adjust BMI trajectories under the Bright Bodies intervention
        if self.intervention == D.Interventions.BRIGHT_BODIES:

            param.interventionMultipliers = [1.0, m_bb1, m_bb2]

            if self.maintenance_scenario == D.EffectMaintenance.FULL:
                for i in range(int(D.SIM_DURATION)):
                    param.interventionMultipliers.append(m_bb2)

            elif self.maintenance_scenario == D.EffectMaintenance.NONE:
                for i in range(int(D.SIM_DURATION)):
                    param.interventionMultipliers.append(m_control)

            elif self.maintenance_scenario == D.EffectMaintenance.DEPREC:
                deprec_difference = m_control - m_bb2
                deprec_value = deprec_difference / 8
                for i in range(int(D.SIM_DURATION)):
                    deprec_multiplier = m_bb2 + (deprec_value * i)
                    param.interventionMultipliers.append(deprec_multiplier)

        # find multipliers to adjust BMI trajectories under the Control
        else:
            param.interventionMultipliers = [1.0]
            for i in range(10):
                param.interventionMultipliers.append(m_control)

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
