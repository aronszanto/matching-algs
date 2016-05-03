import os
import pprint
import random
from agent import Agent
from distribution import Distribution
import config
import numpy as np
import logging
import sim
from fractions import Fraction
from scipy.sparse import csr_matrix

NUM_ROUNDS = 10000
LIMIT_DENOMINATOR = 100
item_morsels = [NUM_ROUNDS] * config.NUM_AGENTS

# agent_mat[i][j] is number of morsels of item j that agent i has
agent_mat = [[0 for _ in xrange(config.NUM_AGENTS)]
             for _ in xrange(config.NUM_AGENTS)]
agent_mat_fracs = [[0 for _ in xrange(config.NUM_AGENTS)]
                   for _ in xrange(config.NUM_AGENTS)]


def item_available(i):
    return item_morsels[i] > 0


def get_top_available(a):
    # print str(a) + "'s preference order is " + str(a.ordinal_prefs)
    for i in a.ordinal_prefs:
        if item_available(i):
            # print "item " + str(o) + " available"
            return i
    return -1


def bite(a, i):
    agent_mat[a.id][i] += 1
    item_morsels[i] -= 1

# PS eating algorithm on agents list, modeled with discrete time. Optional
# arguments to change default number of rounds, ouput probability
# distribution as a fractional matrix, and if so, to what extent to limit
# the denominator in the rational approximation


def prob_serial(agents, num_rounds=NUM_ROUNDS, output_fracs=False, limit_denom=LIMIT_DENOMINATOR):
    round = 0
    while round < num_rounds:
        # shuffle agents so that they all get different orders (to maximize
        # stochasticity)
        random.shuffle(agents)

        for agent in agents:
            best_item = get_top_available(agent)
            # if there is nothing left that the agent would like to eat, go on
            if best_item == -1:
                continue

            # otherwise, take a bite out of the favorite item!
            bite(agent, best_item)
        round += 1
    for i in xrange(config.NUM_AGENTS):
        for j in xrange(config.NUM_AGENTS):
            agent_mat[i][j] = float(agent_mat[i][j]) / NUM_ROUNDS
            amf = Fraction(
                agent_mat[i][j]).limit_denominator(limit_denom)
            agent_mat_fracs[i][j] = str(0) if amf.numerator == 0 else str(
                amf.numerator) + "/" + str(amf.denominator)
    return agent_mat_fracs if output_fracs else agent_mat


# print agents_list
def test_PS():
    agents_list = sim.assign_preferences()
    ps_test = prob_serial(agents_list, output_fracs=False, limit_denom=100)
    np.set_printoptions(threshold=1000, suppress=True)
    if (config.NUM_AGENTS > 10):
        print "Probability Distribution Returned: \n" + str(csr_matrix(ps_test))
    else:
        print "Probability Distribution Returned: \n" + str(ps_test)
    print "Item Morsels Remaining (should be 0): " + str(item_morsels)
    # test to ensure that columns sum to 1
    print "Column Sum (should be 1s): " + str([round(sum([row[i] for row in ps_test]), 5) for i in range(0, config.NUM_AGENTS)])
    # test to ensure that rows sum to 1
    print "Row Sum (should be 1s): " + str([round(sum(r), 5) for r in ps_test])

test_PS()
