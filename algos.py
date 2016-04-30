
def TTC(agents):
    # check that all agents own items
    # this is a necessary condition
    for agent in agents:
        assert agent.item != None

    logging.debug("All agents have an item. TTC starts.")

    # list of items not yet traded; one traded, removed from items_remaining forever
    items_remaining = [agent.item for agent in agents] 
    agents_remaining = agents 

    # helper function
    # given an agent and a list of items available, find the most preferred item
    def most_preferred(agent, items_remaining):
        assert len(items_remaining) > 0
        for item in agent.ordinal_prefs:
            if item in items_remaining:
                return item
    
    # helper function
    # given an item, returns an agent who owns it
    def owner(item):
        for agent in agents:
            if agent.item == item:
                return agent

    round_num = 0

    # each iteration is a "round"
    while len(agents_remaining) > 0:

        logging.debug("round %d", round_num)
        
        # Note: isCycle, isNotCycle and unknown tracks what cycles are formed in this particular round
        # so it is different from round to round

        # a list of known cycles of agents like [[1,2],[4,5,6]]
        isCycle = []
        # a list of agents known not to be in a cycle in this round
        isNotCycle = []
        # a list of items not yet known for sure to be in a cycle or not
        # everything in items_remaining that is not in isCycle or isNotCycle
        unknown = agents_remaining

        logging.debug("entering find-cycles loop")

        # keep looping, putting unknown into either isCycle or isNotCycle until unknown is empty
        while len(unknown) > 0:

            logging.debug("isCycle " + str(isCycle))
            logging.debug("isNotCycle " + str(isNotCycle))
            logging.debug("unknown " + str(unknown))


            print "start with agent ", agents_remaining[0].id 

            # track a cycle, starting from agent and go around the arrow until a loop is found
            cycle_track = [agents_remaining[0]]

            next_item = most_preferred(cycle_track[-1], items_remaining)
            next_agent = owner(next_item)

            print "next_item is ", next_item
            print "next_agent is ", next_agent.id

            # if next_agent appears in cycle_track, a loop is found
            # from next_agent onward is a cycle; before that agent, not a cycle
            if next_agent in cycle_track:
                start_index = cycle_track.index(next_agent)

                print "next_agent in cycle_track, index ", start_index

                # for agents not in this round's cycle
                for agent in cycle_track[:start_index]:
                    print "agent " + str(agent.id) + " appended to isNotCycle and removed from unknown"
                    isNotCycle.append(agent)
                    unknown.remove(agent)


                # for agents in this round's cycle
                # append the whole cycle to isCycle, not each agent separately
                isCycle.append(cycle_track[start_index:]) 
                # remove each agent in the cycle separately from unknown
                for agent in cycle_track[start_index:]:
                    unknown.remove(agent)

            if next_agent in unknown:
                cycle_track.append(next_agent)
            else:
                # not unknown, so either in cycle or not in cycle
                # in both cases, the whole thing preceding it cannot be in a cycle
                for agent in cycle_track:
                    isNotCycle.append(agent)
                    unknown.remove(agent)

        # finish categorizing isCycle or isNotCycle, unknown should be empty now
        for cycle in isCycle:
            items_to_assign = [agent.item for agent in cycle]
            # move the first element in list to last, so that when we assign agent-item
            # agent 1 get item previously own by agent 2, etc
            items_to_assign += [items_to_assign.pop(0)]

            # assign items to agents
            for i in range(cycle):
                agents[i].item = items_to_assign[i]

            # remove all agents and items just traded from agents_remaining and items_remaining
            for agent in isCycle:
                agents_remaining.remove(agent)
                items_remaining.remove(agent.item)

        round_num += 1

    return agents