import os
import random
from agent import Agent
from distribution import Distribution
import config
import numpy as np
import logging


def assign_preferences():

    # create means
    item_means = [Distribution(config.ITEM_MEAN, config.ITEM_VAR).sample()
                  for _ in xrange(config.NUM_AGENTS)]
    logging.debug("Item means: " + str(item_means))

    # create agents and shuffle their order
    agents = [Agent(i) for i in xrange(config.NUM_AGENTS)]
    random.shuffle(agents)

    # assign agents preferences

    for agent in agents:
        agent.cardinal_prefs = [Distribution(
            item_mean, config.PREFERENCE_VAR).sample() for item_mean in item_means]

    logging.debug("Cardinal Prefs: " + str(agents[0].cardinal_prefs))

    logging.debug("correlation between means and preferences is " +
                  str(np.corrcoef(item_means, agents[0].cardinal_prefs)[0, 1]))

    # sort agents' preferences
    for agent in agents:
        agent.ordinal_prefs = [sorted(agent.cardinal_prefs).index(x)
                               for x in agent.cardinal_prefs]

    logging.debug(agents[0].cardinal_prefs)
    logging.debug(agents[0].ordinal_prefs)
