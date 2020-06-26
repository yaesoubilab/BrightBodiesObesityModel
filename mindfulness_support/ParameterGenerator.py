import mindfulness_support.Inputs as I
import yom.ModelInputs as yomI


class ParamGenerator:
    def __init__(self, intervention, maintenance_scenario, model_inputs):
        """

        :param intervention:
        :param maintenance_scenario:
        :param model_inputs:
        """

        self.intervention = intervention
        self.maintenance_scenario = maintenance_scenario
        self.modelInputs = model_inputs

        # get BMI trajectories
        self.trajectories = yomI.get_trajectories_grouped_by_sex_age(
            csv_folder='csv_trajectories',
            age_min_max=[model_inputs.ageSexDist[0][0], model_inputs.ageSexDist[-1][0]]
        )

        # make dictionaries of RVGs for multipliers to adjust trajectories
        self.multiplierRVGs = yomI.ParamRVGs(
            dict_of_parameters=model_inputs.dictTrajMultipliers,
            dist='lognormal'
        )

        # make dictionaries of RVGs for Bright Bodies cost items
        if intervention == I.Interventions.BRIGHT_BODIES:
            self.interventionCostParamRVGs = yomI.ParamRVGs(
                dict_of_parameters=model_inputs.dictCostBB,
                dist='gamma'
            )

        # make dictionaries of RVGs for Control cost items
        elif intervention == I.Interventions.CONTROL:
            self.interventionCostParamRVGs = yomI.ParamRVGs(
                dict_of_parameters=model_inputs.dictCostControl,
                dist='gamma'
            )

        # make dictionaries of RVGs for health care expenditure cost items
        self.hcExpenditureParamRVGs = yomI.ParamRVGs(
            dict_of_parameters=model_inputs.dictHCExp,
            dist='gamma'
        )

    def get_new_parameters(self, rng):

        param = yomI.Parameters(trajectories=self.trajectories,
                                intervention=self.intervention,
                                model_inputs=self.modelInputs)

        # find multipliers to adjust trajectories
        m_bb1 = self.multiplierRVGs.get_sample(param_name='BB Year 1', rng=rng)
        m_bb2 = self.multiplierRVGs.get_sample(param_name='BB Year 2', rng=rng)
        m_control = self.multiplierRVGs.get_sample(param_name='Control', rng=rng)

        # find multipliers to adjust BMI trajectories under the Bright Bodies intervention
        if self.intervention == I.Interventions.BRIGHT_BODIES:

            param.interventionMultipliers = [1.0, m_bb1, m_bb2]

            if self.maintenance_scenario == I.EffectMaintenance.FULL:
                for i in range(int(self.modelInputs.simDuration)):
                    param.interventionMultipliers.append(m_bb2)

            elif self.maintenance_scenario == I.EffectMaintenance.NONE:
                for i in range(int(self.modelInputs.simDuration)):
                    param.interventionMultipliers.append(m_control)

            elif self.maintenance_scenario == I.EffectMaintenance.DEPREC:
                deprec_difference = m_control - m_bb2
                deprec_value = deprec_difference / 8
                for i in range(int(self.modelInputs.simDuration)):
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
        adj_factor_children = (1 + self.modelInputs.inflation) ** \
                              (self.modelInputs.currentYear - self.modelInputs.yearHCExpStudyChildren)
        adj_factor_adults = (1 + self.modelInputs.inflation) ** \
                            (self.modelInputs.currentYear - self.modelInputs.yearHCExpStudyAdults)
        param.costAbove95thP *= adj_factor_children
        param.costBelow95thP *= adj_factor_children
        param.costPerUnitBMIAdultP *= adj_factor_adults

        # sample the cost of interventions
        total_intervention_cost = self.interventionCostParamRVGs.get_total(rng)
        # adjust to inflation
        total_intervention_cost *= (1 + self.modelInputs.inflation) ** \
                                   (self.modelInputs.currentYear - self.modelInputs.yearBBStudy)
        # average cost per participants
        param.annualInterventionCost = total_intervention_cost/self.modelInputs.nChildrenBB

        return param
