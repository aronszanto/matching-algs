import logging
import copy
from agent import Agent
import random

# helper function
# given an agent and a list of items available, find the most preferred item


def most_preferred(agent, items_remaining):
    assert len(items_remaining) > 0
    for item in agent.ordinal_prefs:
        if item in items_remaining:
            return item

# helper function
# given an item, returns an agent who owns it


def owner(item, agents):
    for agent in agents:
        if agent.item == item:
            return agent
    # can't find an agent in agents that owns item
    return None


'''
Does not alter the state of the input: agents
Return brand-new agents with same preferences but newly assigned items

'''


def TTC(agents):
    # check that all agents own items
    # this is a necessary condition
    for agent in agents:
        assert agent.item != None

    # logging.debug("All agents have an item. TTC starts.")

    # dictionary of key=agent.id, value=agent.items_assigned
    FINAL_ASSIGNMENT = dict()

    # list of items not yet traded; one traded, removed from items_remaining
    # forever
    items_remaining = [agent.item for agent in agents]
    agents_remaining = copy.deepcopy(agents)

    round_num = 0

    # agents_remaining is global: removed only once traded
    # each round has a agents_remaining round that keeps track of whether in
    # cycle or not

    # each iteration is a "round"
    while len(agents_remaining) > 0:

        # logging.debug("-----ROUND " + str(round_num) + " -------")

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

        # logging.debug("entering find-cycles loop")

        # track a cycle, starting from agent and go around the arrow until a
        # loop is found
        cycle_track = [unknown[0]]

        items_remaining = [l_agent.item for l_agent in agents_remaining]

        # logging.debug("items_remaining: " + str(items_remaining))

        # items_remaining_round = copy.deepcopy(items_remaining)

        # keep looping, putting unknown into either isCycle or isNotCycle until
        # unknown is empty
        while len(unknown) > 0:

            logging.debug("start with agent " + str(unknown[0].id))

            next_item = most_preferred(cycle_track[-1], items_remaining)
            # logging.debug("agents " + str([(agent.id, agent.item) for agent
            # in agents]))
            next_agent = owner(next_item, agents_remaining)

            # logging.debug("next_item is "+ str(next_item))
            # logging.debug("next_agent is "+ str(next_agent.id))
            # logging.debug("cycle_track is "+ str([(agent.id, agent.item) for agent in cycle_track]))

            # if next_agent appears in cycle_track, a loop is found
            # from next_agent onward is a cycle; before that agent, not a cycle
            if next_agent.id in [l_agent.id for l_agent in cycle_track]:

                start_index = [l_agent.id for l_agent in cycle_track].index(
                    next_agent.id)

                # logging.debug("before this is not a cycle")

                # for agents not in this round's cycle
                for agent in cycle_track[:start_index]:

                    isNotCycle.append(agent)
                    unknown.remove(agent)

                isCycle.append(cycle_track[start_index:])
                # remove each agent in the cycle separately from unknown

                for agent in cycle_track[start_index:]:

                    assert agent.id in [l_agent.id for l_agent in unknown]
                    unknown.remove(agent)
                    # remove from unknown *and* remove from agents_remaining
                    # (will trade) removal from agents_remaining happens later when isCycle is completed

                # reset cycle_track
                if len(unknown) > 0:
                    cycle_track = [unknown[0]]

            elif next_agent.id in [l_agent.id for l_agent in unknown]:
                cycle_track.append(next_agent)
            else:
                # not unknown, so either in cycle or not in cycle
                # in both cases, the whole thing preceding it cannot be in a cycle
                # logging.debug("hit the known, the whole thing is not in cycle")

                for agent in cycle_track:
                    isNotCycle.append(agent)
                    unknown.remove(agent)

                # reset cycle_track
                if len(unknown) > 0:
                    cycle_track = [unknown[0]]

        for cycle in isCycle:

            # logging.debug("cycle found")
            # logging.debug("cycle is "+str(cycle))
            items_to_assign = [l_agent.item for l_agent in cycle]
            # logging.debug("pre-switch items_to_assign: " + str(items_to_assign))
            # move the first element in list to last, so that when we assign agent-item
            # agent 1 get item previously own by agent 2, etc
            items_to_assign += [items_to_assign.pop(0)]
            # logging.debug("post-switch items_to_assign: " + str(items_to_assign))

            # assign items to agents
            for i in range(len(cycle)):

                cycle[i].item = items_to_assign[i]
                FINAL_ASSIGNMENT[cycle[i].id] = items_to_assign[i]
                # logging.debug("agent " + str(cycle[i].id) + " is assigned item " + str(cycle[i].item))

            # remove all agents and items just traded from agents_remaining and
            # items_remaining
            for agent in cycle:

                agents_remaining.remove(agent)
                items_remaining.remove(agent.item)

        round_num += 1

    # NOTE: during the course of the algo, the input "agents" is not touched at all intentionally
    # so it doesn't change the state of agents in the original program where TTC is called
    # we have a dictionary of FINAL_ASSIGNMENT, we can create brand new agents
    # to return

    agents_to_return = []
    for agent in agents:
        agents_to_return.append(Agent(id=agent.id,
                                      item=FINAL_ASSIGNMENT[agent.id],
                                      ordinal_prefs=agent.ordinal_prefs,
                                      cardinal_prefs=agent.cardinal_prefs)
                                )

    return agents_to_return


def YRMH_IGYT(agents, items):

    # helper function, check if request_loop is a loop
    def IsRequestLoop(request_loop):
        assert len(request_loop) > 0
        last_requestee = request_loop[-1][1]
        # if last_requestee appears earlier as requester, loop is found, return the reappearing requester index
        # otherwise return -1
        try:
            loop_start_index = [requester for (
                requester, requestee) in request_loop].index(last_requestee)
            return loop_start_index
        # if not in list, ValueError
        except ValueError:
            return -1

    # priority order will also function as agent_remaining: remove once
    # assigned
    priority_order = copy.deepcopy(agents)
    random.shuffle(priority_order)

    # this is to track whether a request loop occurs.
    # A request loop is, e.g. A4 requests A5's item and A5 requests A4's item.
    # request_loop is then [(A4, A5), (A5, A4)]
    request_loop = []

    FINAL_ASSIGNMENT = dict()

    logging.debug("agents: " + str(agents))
    logging.debug("starting priority_order: " + str(priority_order))

    items_remaining = items

    logging.debug("beginning items_remaining: " + str(items_remaining))

    while len(priority_order) > 0:
        curr_agent = priority_order[0]
        requested_item = most_preferred(curr_agent, items_remaining)
        requested_item_owner = owner(requested_item, priority_order)

        logging.debug("curr_agent: " + str(curr_agent))
        logging.debug("requested_item: " + str(requested_item))
        logging.debug("requested_item_owner: " + str(requested_item_owner))

        # if the requested item has no owner, assign it permanently and take
        # the agent and item off the list
        if requested_item_owner is None:

            logging.debug("requested_item_owner is None")
            logging.debug("FINAL ASSIGN AGENT " +
                          str(curr_agent.id) + " TO ITEM " + str(requested_item))

            # curr_agent gives up its current item to get the requested one; assignment finalized
            # curr_agent.item = requested_item -- actually this is not necessary
            # because curr_agent is taken off priority list anyway
            FINAL_ASSIGNMENT[curr_agent.id] = requested_item
            priority_order.remove(curr_agent)
            items_remaining.remove(requested_item)

            # reset request_loop
            request_loop = []

        # someone owns the requested house
        # that owner gets his turn (move to top of priority order) and record the request in request_loop
        # check if loop occurs, if YES, trade and remove
        else:

            logging.debug("requested_item_owner is not None")

            logging.debug("Before request_loop append and priority reorder")
            logging.debug("request_loop: " + str(request_loop))
            logging.debug("priority_order: " + str(priority_order))

            request_loop.append((curr_agent, requested_item_owner))
            # remove owner from list and insert at index 0
            priority_order.remove(requested_item_owner)
            priority_order.insert(0, requested_item_owner)

            logging.debug("After request_loop append and priority reorder")
            logging.debug("request_loop: " + str(request_loop))
            logging.debug("priority_order: " + str(priority_order))

            loop_start_index = IsRequestLoop(request_loop)

            # if loop yes, trade and remove
            if loop_start_index != -1:
                logging.debug("IsRequestLoop True")

                # only from index loop_start_index onward in request_loop that
                # is actually a loop
                request_loop = request_loop[loop_start_index:]

                logging.debug("truncated request_loop: " + str(request_loop))

                # assign the requested items
                # and remove requester (aka all agents involved) off priority
                # list
                for (requester, requestee) in request_loop:
                    FINAL_ASSIGNMENT[requester.id] = requestee.item
                    priority_order.remove(requester)
                    items_remaining.remove(requestee.item)

                # done with request_loop, back to empty
                request_loop = []

            else:
                logging.debug("IsRequestLoop False")
                pass

    agents_to_return = []
    for agent in agents:
        agents_to_return.append(Agent(id=agent.id,
                                      item=FINAL_ASSIGNMENT[agent.id],
                                      ordinal_prefs=agent.ordinal_prefs,
                                      cardinal_prefs=agent.cardinal_prefs)
                                )

    return agents_to_return
