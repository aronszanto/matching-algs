import logging
import copy


'''
envyfree checks whether the given assignment is envy-free or not
agent_pairs is a list of (agent, [list of probabilities sorted by item.id])
for example, agent_pairs = [(A1,[0.3,0.2]),(A2,[0.8,0.1])] means agent 1 is assigned house 1 with
Access to agent.id and agent.ordinal_prefs necessary for stochastic dominance envy-free (type=sd)
Access to agent.id and agent.cardinal_prefs necessary for cardinal envy-free (type=cardinal)
'''


def envyfree(agent_pairs, type='sd'):
    assert type == 'sd' or type == 'cardinal'
    if type == 'sd':
        return envyfree_sd(agent_pairs)
    if type == 'cardinal':
        return envyfree_card(agent_pairs)

'''
Helper function sort_pref:
The probabilities given are sorted by item.id, but we want it sorted by preference so we can
test stochastic dominance.
Input: 	probs must be a list of n probabilities of items numbered 0,1,...,n-1
		prefs must be a
Example:
sort_pref(probs = [a,b,c,d], prefs = [2,0,3,1]) -> return [c,a,d,b]
'''


def sort_pref(probs, prefs):
    return [probs[i] for i in prefs]

'''
Helper function list_sd:
Check whether list1 weakly stochastically dominates list2.
If list1 = [a0,...,ak] and list2 = [b0,...,bk] then list1 stochastically dominates list 2
iff a0+...+ai >= b0+...+bi for all 0<=i<=k
'''


def list_sd(list1, list2):
    assert len(list1) == len(list2)
    for i in xrange(len(list1)):
        if sum(list1[0:i]) < sum(list2[0:i]):
            return False
    return True

'''
Helper function utility:
Compute the utility an agent has given a probability list
If agent's cardinal preference/utility is [u0,...,uk] and it is assigned [p0,...,pk]
then the agent's utility is u0*p0+...+uk*pk
'''


def utility(agent, probs):
    assert len(agent.cardinal_prefs) == len(probs)
    return sum([agent.cardinal_prefs[i] * probs[i] for i in xrange(len(probs))])


def envyfree_sd(agent_pairs):
    for (curr_agent, curr_probs) in agent_pairs:
        for (other_agent, other_probs) in agent_pairs:
            # you don't envy yourself, so checking like this is fine
            if not list_sd(sort_pref(curr_probs, curr_agent.ordinal_prefs), sort_pref(other_probs, curr_agent.ordinal_prefs)):
                return False
    return True


def envyfree_card(agent_pairs):
    for (curr_agent, curr_probs) in agent_pairs:
        for (other_agent, other_probs) in agent_pairs:
            # you don't envy yourself, so checking like this is fine
            if utility(curr_agent, curr_probs) < utility(curr_agent, other_probs):
                return False
    return True
