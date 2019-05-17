import InputData as D
import SimPy.RandomVariantGenerators as RVGs


class Parameters:
    # class to contain the parameters of the model
    def __init__(self):
        self.timeToNextBirthDist = RVGs.Exponential(scale=D.INTER_BIRTH_TIME)
        self.timeToDeath = RVGs.Exponential(scale=D.LIFE_EXPECTANCY)
