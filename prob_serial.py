import os
import random
from agent import Agent
from distribution import Distribution
import config
import numpy as np
import logging

NUM_ROUNDS = 10000
item_morsels = [NUM_ROUNDS] * config.NUM_AGENTS

# agent_mat[i][j] is number of morsels of item j that agent i has
agent_mat = [[0 for _ in xrange(config.NUM_AGENTS)]
             for _ in xrange(config.NUM_AGENTS)]


def item_available(i):
    return item_morsels[i] > 0


def get_top_available(a):
    for i, o in enumerate(item_morsels):
        if item_available(o):
            return i


def bite(a, i):
    agent_mat[a.id][i] += 1
    item_morsels[i] -= 1


def prob_serial(agents):
    round = 0
    while round < NUM_ROUNDS:
        shuffled_agents = random.shuffle([])

print agent_mat
