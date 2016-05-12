import os
import random
from agent import Agent
from distribution import Distribution
import config
import numpy as np
import logging
import algos


def assign_preferences(n=config.NUM_AGENTS, num_items_assigned=config.NUM_AGENTS):

    # create means
    item_means = [Distribution(config.ITEM_MEAN, config.ITEM_VAR).sample()
                  for _ in xrange(n)]
    logging.debug("Item means: " + str(item_means))

    # create agents and shuffle their order
    agents = [Agent(i) for i in xrange(n)]
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

    # for TTC, every agent owns a house a priori
    for i in xrange(num_items_assigned):
        agents[i].item = i

    return agents


def main():

    logging.basicConfig(filename='matching.log',
                        filemode='w', level=logging.DEBUG)

    algos.test_TTC()
    algos.test_YRMH()


if __name__ == "__main__":
    main()

    # agents = assign_preferences(num_item_assigned=config.NUM_AGENTS/3)
    # for agent in agents:
    #     print agent.id, agent.item, agent.ordinal_prefs
