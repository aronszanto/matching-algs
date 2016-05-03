import os
import random
from agent import Agent
from distribution import Distribution
import config
import numpy as np
import logging
import sim

NUM_ROUNDS = 10000
item_morsels = [NUM_ROUNDS] * config.NUM_AGENTS

# agent_mat[i][j] is number of morsels of item j that agent i has
agent_mat = [[0 for _ in xrange(config.NUM_AGENTS)]
             for _ in xrange(config.NUM_AGENTS)]


def item_available(i):
    return item_morsels[i] > 0


def get_top_available(a):
    # print str(a) + "'s preference order is " + str(a.ordinal_prefs)
    for i, o in enumerate(a.ordinal_prefs):
        if item_available(o):
            # print "item " + str(o) + " available"
            return i
    return -1


def bite(a, i):
    agent_mat[a.id][i] += 1
    item_morsels[i] -= 1


def prob_serial(agents):
    round = 0
    while round < NUM_ROUNDS:
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
            agent_mat[i][j] = float(agent_mat[i][j]) / \
                (NUM_ROUNDS * config.NUM_AGENTS)

agents_list = sim.assign_preferences()
for a in agents_list:
    a.ordinal_prefs = [0, 1, 2, 3, 4]
agents_list[0].ordinal_prefs = [4, 3, 2, 1, 0]
agents_list[1].ordinal_prefs = [4, 3, 2, 1, 0]
# print agents_list

prob_serial(agents_list)
print agent_mat
print sum([a[4] for a in agent_mat])
