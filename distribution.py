import random

class Distribution:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def sample(self):
        print random.normalvariate(self.mu,self.sigma)

d = Distribution(0,1)
print d.sample()
