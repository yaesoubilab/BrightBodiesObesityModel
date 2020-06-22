import SimPy.DataFrames as df
from SimPy import InOutFunctions as InOutSupport
from SimPy import RandomVariateGenerators as RVGs


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

