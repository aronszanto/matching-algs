import random


class Distribution:

    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def sample(self):
        return random.normalvariate(self.mu, self.sigma)
