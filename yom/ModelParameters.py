import InputData as D
import SimPy.DataFrames as df
import yom.Data as Data
import yom.ModelTrajectory as T
from SimPy import RandomVariateGenerators as RVGs


class Parameters:
    # class to contain the parameters of the model
    def __init__(self, trajectories, intervention):
        """
        :param trajectories: (DataFrameOfObjects) of BMI trajectories (by sex and age)
        :param intervention: which intervention to model
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
        self.interventionMultipliers = []  # multipliers to adjust BMI trajectories


class ParamRVGs:
    # class to contain the random variate generators for parameters

    def __init__(self, dict_of_parameters, dist):
        """
        :param dict_of_parameters: dictionary of parameters
        :param dist: (string) distribution assumed for all parameters ('gamma' or 'lognormal')
        """

        self.dictOfRVGs = {}
        for key, mean_stdev in dict_of_parameters.items():

            # fit a distribution (only if st_dev > 0)
            if mean_stdev[1] > 0:
                if dist == 'gamma':
                    fit_output = RVGs.Gamma.fit_mm(mean=mean_stdev[0], st_dev=mean_stdev[1])
                    # store the gamma RVG
                    self.dictOfRVGs[key] = RVGs.Gamma(a=fit_output["a"],
                                                      loc=0,
                                                      scale=fit_output["scale"])
                elif dist == 'lognormal':
                    fit_output = RVGs.LogNormal.fit_mm(mean=mean_stdev[0], st_dev=mean_stdev[1])
                    # store the log-normal RVG
                    self.dictOfRVGs[key] = RVGs.LogNormal(mu=fit_output["mu"],
                                                          loc=0,
                                                          sigma=fit_output["sigma"])
            else:
                # use a constant distribution
                self.dictOfRVGs[key] = RVGs.Constant(value=mean_stdev[0])

    def get_sample(self, param_name, rng):
        """
        :param param_name: name of the parameter to get a sample for
        :param rng: random number generator
        :return: a sample from the distribution of the assumed distribution
        """
        return self.dictOfRVGs[param_name].sample(rng)

    def get_total(self, rng):
        """
        :param rng: random number generator
        :return: sum of samples from all parameters
        """
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

        # make dictionaries of RVGs for multipliers to adjust trajectories
        self.multiplierRVGs = ParamRVGs(
            dict_of_parameters=Data.DICT_MULTIPLIERS,
            dist='lognormal'
        )

        # make dictionaries of RVGs for Bright Bodies cost items
        if intervention == D.Interventions.BRIGHT_BODIES:
            self.interventionCostParamRVGs = ParamRVGs(
                dict_of_parameters=Data.DICT_COST_BB,
                dist='gamma'
            )

        # make dictionaries of RVGs for Control cost items
        elif intervention == D.Interventions.CONTROL:
            self.interventionCostParamRVGs = ParamRVGs(
                dict_of_parameters=Data.DICT_COST_CONTROL,
                dist='gamma'
            )

        # make dictionaries of RVGs for health care expenditure cost items
        self.hcExpenditureParamRVGs = ParamRVGs(
            dict_of_parameters=Data.DICT_HC_EXP,
            dist='gamma'
        )

    def get_new_parameters(self, rng):

        param = Parameters(trajectories=self.trajectories,
                           intervention=self.intervention)

        # find multipliers to adjust trajectories
        m_bb1 = self.multiplierRVGs.get_sample(param_name='BB Year 1', rng=rng)
        m_bb2 = self.multiplierRVGs.get_sample(param_name='BB Year 2', rng=rng)
        m_control = self.multiplierRVGs.get_sample(param_name='Control', rng=rng)

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
                    deprec_multiplier = m_bb2 + (deprec_value * (i+1))
                    param.interventionMultipliers.append(deprec_multiplier)

        # find multipliers to adjust BMI trajectories under the Control
        else:
            param.interventionMultipliers = [1.0]
            for i in range(10):
                param.interventionMultipliers.append(m_control)

        # sample health care expenditure items
        param.costAbove95thP = self.hcExpenditureParamRVGs.get_sample(
            param_name='<18 years, >95th %ile', rng=rng)
        param.costBelow95thP = self.hcExpenditureParamRVGs.get_sample(
            param_name='<18 years, <95th %ile', rng=rng)
        param.costPerUnitBMIAdultP = self.hcExpenditureParamRVGs.get_sample(
            param_name='>18 years', rng=rng)
        # adjust for inflation
        adj_factor_children = (1+D.INFLATION)**(D.CURRENT_YEAR - Data.YEAR_HCEXP_STUDY_CHILDREN)
        adj_factor_adults = (1+D.INFLATION)**(D.CURRENT_YEAR - Data.YEAR_HCEXP_STUDY_ADULTS)
        param.costAbove95thP *= adj_factor_children
        param.costBelow95thP *= adj_factor_children
        param.costPerUnitBMIAdultP *= adj_factor_adults

        # sample the cost of interventions
        total_intervention_cost = self.interventionCostParamRVGs.get_total(rng)
        # adjust to inflation
        total_intervention_cost *= (1+D.INFLATION)**(D.CURRENT_YEAR - Data.YEAR_BB_STUDY)
        # average cost per participants
        param.annualInterventionCost = total_intervention_cost/D.N_CHILDREN_BB

        return param
