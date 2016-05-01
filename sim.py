import os
import random
from agent import Agent
from distribution import Distribution
import config
import numpy as np
import logging
import metrics

from algos import TTC


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

    # for TTC, every agent owns a house a priori
    for i in xrange(config.NUM_AGENTS):
        agents[i].item = i

    return agents


def main():

    logging.basicConfig(filename='matching.log', filemode='w', level=logging.DEBUG)

    # agents = assign_preferences()

    # hard-code, for debugging
    agents = [  Agent(id = 3, item = 0, ordinal_prefs = [0, 2, 3, 1]),
                Agent(id = 1, item = 1, ordinal_prefs = [0, 3, 2, 1]),
                Agent(id = 2, item = 2, ordinal_prefs = [0, 3, 1, 2]),
                Agent(id = 0, item = 3, ordinal_prefs = [0, 3, 1, 2])
             ]

    print "initial agents"
    logging.debug("INITIAL AGENTS")
    for agent in agents:
        print agent.id, agent.item, agent.ordinal_prefs
        logging.debug("agent.id, agent.item, agent.ordinal_prefs: " + str((agent.id, agent.item, agent.ordinal_prefs)))

    print "TTC agents"
    logging.debug("TTC AGENTS")
    for agent in TTC(agents):
        print agent.id, agent.item, agent.ordinal_prefs
        logging.debug("agent.id, agent.item, agent.ordinal_prefs: " + str((agent.id, agent.item, agent.ordinal_prefs)))

if __name__ == "__main__":
    main()
