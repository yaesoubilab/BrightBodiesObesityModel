from enum import Enum

import SimPy.DataFrames as df
import SimPy.InOutFunctions as IO
from SimPy import RandomVariateGenerators as RVGs


class Sex(Enum):
    MALE = 0
    FEMALE = 1


class SetOfTrajectories:
    # class to select randomly a row from a set of rows
    def __init__(self, rows):
        self.rows = rows
        self.discreteUniform = RVGs.UniformDiscrete(0, len(rows) - 1)

    def sample_traj(self, rng):
        i = self.discreteUniform.sample(rng)
        return self.rows[i]


def get_trajectories_grouped_by_sex_age(csv_folder, age_min_max):
    """
    :param csv_folder: folder (relative to the root) where csv files are located
    :param age_min_max: (list) [min age, max age]
    :return: the list of BMI trajectories (grouped by sex and age) from the csv files
    """

    # creating a data frame of trajectories
    trajectories = df.DataFrameOfObjects(list_x_min=[age_min_max[0], 0],
                                         list_x_max=[age_min_max[1], 1],
                                         list_x_delta=[1, 'int'])

    # populate the data frame
    for sex in ['male', 'female']:
        for age in range(age_min_max[0], age_min_max[1]+1, 1):
            file_name = csv_folder + '/{0}_{1}.csv'.format(sex, age)
            rows = IO.read_csv_rows(file_name=file_name,
                                    delimiter=',',
                                    if_ignore_first_row=True,
                                    if_convert_float=True)
            s = 0 if sex == 'male' else 1
            trajectories.set_obj(x_value=[age, s],
                                 obj=SetOfTrajectories(rows=rows))

    return trajectories


class Parameters:
    # class to contain the parameters of the model
    def __init__(self, trajectories, intervention, model_inputs):
        """
        :param trajectories: (DataFrameOfObjects) of BMI trajectories (by sex and age)
        :param intervention: which intervention to model
        :param model_inputs: model inputs
        """

        self.trajectories = trajectories
        self.intervention = intervention
        self.popSize = model_inputs.popSize
        self.simInitialDuration = model_inputs.simInit

        # population distribution by age/sex for Bright Bodies (age 8 - 16)
        min_age = model_inputs.ageSexDist[0][0]
        max_age = model_inputs.ageSexDist[-1][0]
        self.ageSexDist = df.DataFrameWithEmpiricalDist(rows=model_inputs.ageSexDist,  # life table
                                                        list_x_min=[min_age, 0],  # minimum values for age/sex groups
                                                        list_x_max=[max_age, 1],  # maximum values for age/sex groups
                                                        list_x_delta=[1, 'int'])    # [age interval, sex categorical]

        # BMI 95th cut offs
        min_age = model_inputs.bmi95thCutOffs[0][0]
        max_age = model_inputs.bmi95thCutOffs[-1][0]
        self.bmi95thCutOffs = df.DataFrame(rows=model_inputs.bmi95thCutOffs,
                                           list_x_min=[min_age, 0],  # minimum values for age/sex groups
                                           list_x_max=[max_age, 1],  # maximum values for age/sex groups
                                           list_x_delta=[1, 'int'])  # [age interval, sex categorical]
        self.bmi85thCutOffs = df.DataFrame(rows=model_inputs.bmi85thCutOffs,
                                           list_x_min=[min_age, 0],  # minimum values for age/sex groups
                                           list_x_max=[max_age, 1],  # maximum values for age/sex groups
                                           list_x_delta=[1, 'int'])  # [age interval, sex categorical]

        # cost parameters are determined later by a sample from specified probability distributions
        self.annualInterventionCost = 0
        self.costAbove95thP = 0
        self.cost85_94thP = 0
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



