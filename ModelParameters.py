import InputData as D
import SimPy.RandomVariantGenerators as RVGs
# for adding births
import SimPy.DataFrames as df


class Parameters:
    # class to contain the parameters of the model
    def __init__(self):
        self.timeToNextBirthDist = RVGs.Exponential(scale=D.INTER_BIRTH_TIME)
        self.timeToDeath = RVGs.Exponential(scale=D.LIFE_EXPECTANCY)
        self.ageSexDist = df.DataFrameWithEmpiricalDist(rows=D.rows,
                                                        list_x_min=[0, 0],
                                                        list_x_max=[85, 1],
                                                        list_x_delta=[5, 'int'])


# For Adding Births
rng = RVGs.RNG(seed=1)
probDf = df.DataFrameWithEmpiricalDist(rows=D.rows,
                                       list_x_min=[0, 0],
                                       list_x_max=[85, 1],
                                       list_x_delta=[5, 'int'])
# get a sample
print('Get a sampled index:', probDf.get_sample_indices(rng=rng))
print('Get a sampled value:', probDf.get_sample_values(rng=rng))
print('')
