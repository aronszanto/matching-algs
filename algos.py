import logging
import copy


def TTC(agents):
    # check that all agents own items
    # this is a necessary condition
    for agent in agents:
        assert agent.item != None

    logging.debug("All agents have an item. TTC starts.")

    # list of items not yet traded; one traded, removed from items_remaining
    # forever
    items_remaining = [agent.item for agent in agents]
    agents_remaining = copy.deepcopy(agents)

    # helper function
    # given an agent and a list of items available, find the most preferred
    # item
    def most_preferred(agent, items_remaining):
        assert len(items_remaining) > 0
        logging.debug("Items remaining: " + str(items_remaining))
        for item in agent.ordinal_prefs:
            logging.debug("Agent " + str(agent.id) +
                          "'s ordinal prefs: + " + str(agent.ordinal_prefs))
            if item in items_remaining:
                logging.debug("Returning item " + str(item))
                return item

    # helper function
    # given an item, returns an agent who owns it
    def owner(item, agents):
        for agent in agents:
            if agent.item == item:
                return agent

    round_num = 0

    # agents_remaining is global: removed only once traded
    # each round has a agents_remaining round that keeps track of whether in
    # cycle or not

    # each iteration is a "round"
    while len(agents_remaining) > 0:

        logging.debug("-----ROUND " + str(round_num) + " -------")

        # Note: isCycle, isNotCycle and unknown tracks what cycles are formed in this particular round
        # so it is different from round to round

        # agents_remaining_round = copy.deepcopy(agents_remaining)

        # a list of known cycles of agents like [[1,2],[4,5,6]]
        isCycle = []
        # a list of agents known not to be in a cycle in this round
        isNotCycle = []
        # a list of items not yet known for sure to be in a cycle or not
        # everything in items_remaining that is not in isCycle or isNotCycle
        unknown = copy.deepcopy(agents_remaining)

        logging.debug("entering find-cycles loop")

        # track a cycle, starting from agent and go around the arrow until a
        # loop is found
        cycle_track = [unknown[0]]

        items_remaining = [agent.item for agent in agents_remaining]

        logging.debug("items_remaining: " + str(items_remaining))

        # items_remaining_round = copy.deepcopy(items_remaining)

        # keep looping, putting unknown into either isCycle or isNotCycle until
        # unknown is empty
        while len(unknown) > 0:

            logging.debug("BEGIN CATEGORIZING LOOP")

            logging.debug(
                "isCycle: " + str([[(agent.id, agent.item) for agent in cycle] for cycle in isCycle]))
            logging.debug(
                "isNotCycle " + str([(agent.id, agent.item) for agent in isNotCycle]))
            logging.debug(
                "unknown " + str([(agent.id, agent.item) for agent in unknown]))

            logging.debug("start with agent " + str(unknown[0].id))

            next_item = most_preferred(cycle_track[-1], items_remaining)
            # logging.debug("agents " + str([(agent.id, agent.item) for agent
            # in agents]))
            next_agent = owner(next_item, agents_remaining)

            logging.debug("next_item is " + str(next_item))
            logging.debug("next_agent is " + str(next_agent.id))
            logging.debug("cycle_track is " +
                          str([(agent.id, agent.item) for agent in cycle_track]))

            # if next_agent appears in cycle_track, a loop is found
            # from next_agent onward is a cycle; before that agent, not a cycle
            if next_agent.id in [agent.id for agent in cycle_track]:

                # start_index = cycle_track.index(next_agent)

                start_index = [agent.id for agent in cycle_track].index(
                    next_agent.id)

                logging.debug(
                    "next_agent in cycle_track, index " + str(start_index))

                logging.debug("current unknown: " +
                              str([(agent.id, agent.item) for agent in unknown]))

                logging.debug("before this is not a cycle")

                # for agents not in this round's cycle
                for agent in cycle_track[:start_index]:
                    logging.debug(
                        "agent " + str(agent.id) + " appended to isNotCycle and removed from unknown")
                    isNotCycle.append(agent)
                    # items_remaining_round.remove(agent.item)

                    logging.debug("PRE-REMOVAL ASSERT")
                    logging.debug("agent: " + str((agent.id, agent.item)))
                    logging.debug(
                        "current unknown: " + str([(agent.id, agent.item) for agent in unknown]))
                    assert agent.id in [agent.id for agent in unknown]
                    unknown = [
                        new_agent for new_agent in unknown if new_agent.id != agent.id]
                    logging.debug("POST-REMOVAL")
                    logging.debug(
                        "unknown: " + str([(agent.id, agent.item) for agent in unknown]))
                    # unknown.remove(agent)

                logging.debug("after this is a cycle")
                # for agents in this round's cycle
                # append the whole cycle to isCycle, not each agent separately
                isCycle.append(cycle_track[start_index:])
                # remove each agent in the cycle separately from unknown

                # unknown = [agent for agent in unknown if agent.id not in
                # [agent.id for agent in cycle_track[start_index:]]]
                for agent in cycle_track[start_index:]:
                    logging.debug("PRE-REMOVAL ASSERT")
                    logging.debug("agent: " + str((agent.id, agent.item)))
                    logging.debug(
                        "current unknown: " + str([(agent.id, agent.item) for agent in unknown]))

                    # items_remaining_round.remove(agent.item)

                    assert agent.id in [agent.id for agent in unknown]
                    # unknown = [new_agent for new_agent in unknown if
                    # new_agent.id != agent.id]
                    logging.debug("TEMP CHANGE TO DEBUG")
                    unknown.remove(agent)
                    logging.debug("POST-REMOVAL")
                    logging.debug(
                        "unknown: " + str([(agent.id, agent.item) for agent in unknown]))
                    # unknown.remove(agent)
                    # remove from unknown *and* remove from agents_remaining
                    # (will trade)

                # reset cycle_track
                if len(unknown) > 0:
                    cycle_track = [unknown[0]]
                    logging.debug("reset cycle_track, now: " +
                                  str([(agent.id, agent.item) for agent in cycle_track]))

            elif next_agent.id in [agent.id for agent in unknown]:
                logging.debug("cycle_track append agent " + str(next_agent.id))
                cycle_track.append(next_agent)
                logging.debug("current cycle_track: " +
                              str([(agent.id, agent.item) for agent in cycle_track]))
            else:
                # not unknown, so either in cycle or not in cycle
                # in both cases, the whole thing preceding it cannot be in a
                # cycle
                logging.debug("hit the known, the whole thing is not in cycle")
                logging.debug("TO CHECK BUG")
                logging.debug("next_agent.id " + str(next_agent.id))
                logging.debug("current unknown: " +
                              str([(agent.id, agent.item) for agent in unknown]))
                for agent in cycle_track:
                    logging.debug(
                        "BEFORE isNotCycle append and unknown remove")
                    logging.debug(
                        "current unknown: " + str([(agent.id, agent.item) for agent in unknown]))
                    logging.debug("agent: " + str((agent.id, agent.item)))

                    isNotCycle.append(agent)
                    # items_remaining_round.remove(agent.item)
                    logging.debug("PRE-REMOVAL ASSERT")
                    logging.debug("agent: " + str((agent.id, agent.item)))
                    logging.debug(
                        "current unknown: " + str([(agent.id, agent.item) for agent in unknown]))
                    assert agent.id in [agent.id for agent in unknown]
                    logging.debug("UNKNOWN REMOVAL")
                    logging.debug("PRE-REMOVAL")
                    logging.debug("agent " + str((agent.id, agent.item)))
                    logging.debug(
                        "unknown: " + str([(agent.id, agent.item) for agent in unknown]))
                    unknown = [
                        new_agent for new_agent in unknown if new_agent.id != agent.id]
                    logging.debug("POST-REMOVAL")
                    logging.debug(
                        "unknown: " + str([(agent.id, agent.item) for agent in unknown]))
                    # unknown.remove(agent)

                logging.debug("POST REMOVAL")
                logging.debug("agent " + str(agent.id) +
                              " appended to isNotCycle and removed from unknown")
                logging.debug(
                    "current isNotCycle: " + str([(agent.id, agent.item) for agent in isNotCycle]))
                logging.debug(
                    "current isCycle: " + str([[(agent.id, agent.item) for agent in cycle] for cycle in isCycle]))
                logging.debug("current agents_remaining: " +
                              str([(agent.id, agent.item) for agent in agents_remaining]))
                logging.debug("current unknown: " +
                              str([(agent.id, agent.item) for agent in unknown]))

                # reset cycle_track
                if len(unknown) > 0:
                    cycle_track = [unknown[0]]
                    logging.debug("reset cycle_track, now: " +
                                  str([(agent.id, agent.item) for agent in cycle_track]))

        # finish categorizing isCycle or isNotCycle, unknown should be empty
        # now
        logging.debug("round " + str(round_num) + " categorization completed")
        logging.debug("current isNotCycle: " +
                      str([(agent.id, agent.item) for agent in isNotCycle]))
        logging.debug("current isCycle: " +
                      str([[(agent.id, agent.item) for agent in cycle] for cycle in isCycle]))

        for cycle in isCycle:
            items_to_assign = [agent.item for agent in cycle]
            # move the first element in list to last, so that when we assign agent-item
            # agent 1 get item previously own by agent 2, etc
            items_to_assign += [items_to_assign.pop(0)]

            logging.debug("cycle found")

            # assign items to agents
            for i in range(len(cycle)):
                agents[i].item = items_to_assign[i]
                logging.debug("agent " + str(i) +
                              " is assigned item " + str(agents[i].item))

            # remove all agents and items just traded from agents_remaining and
            # items_remaining
            for agent in cycle:
                logging.debug("remove agents in cycle")
                logging.debug("pre-removal")
                logging.debug(
                    "current isNotCycle: " + str([(agent.id, agent.item) for agent in isNotCycle]))
                logging.debug(
                    "current isCycle: " + str([[(agent.id, agent.item) for agent in cycle] for cycle in isCycle]))
                logging.debug("current agents_remaining: " +
                              str([(agent.id, agent.item) for agent in agents_remaining]))
                agents_remaining.remove(agent)
                items_remaining.remove(agent.item)

        round_num += 1

        logging.debug("------- END OF ROUND --------")
        logging.debug("current agents_remaining: " +
                      str([(agent.id, agent.item) for agent in agents_remaining]))

    return agents
