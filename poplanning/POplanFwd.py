
from plans import PlanNode, PlanEmpty

#
# Find a plan that solves a partially observable planning problem
#

# Identify all actions applicable in a belief state (set of states).
# This is the intersection of the sets of actions for each state.

def Bapplicable(bstate):
    # print(type(bstate))
    bstate_copy = set()
    for s in bstate:
        bstate_copy.add(s.clonestate())
    try:
        intersection = set(bstate_copy.pop().applActions())
    except KeyError:
        return []
    while bstate_copy:
        intersection &= set(bstate_copy.pop().applActions())
    # print('interaction', type(intersection))
    # print(intersection.__len__())
    return list(intersection)
### YOUR CODE HERE
### YOUR CODE HERE
### YOUR CODE HERE
### YOUR CODE HERE
### YOUR CODE HERE

# Compute the successor state set w.r.t. a given action.

def Bsucc(bstate,action):
    result = set()
    for s in bstate:
        result.update(s.succs(action))
    return result

# Return the subset of states compatible with the observation.

def Bobserve(bstate,observation):
    return { s for s in bstate if s.compatible(observation) }

# Uncomment the print if you want to see the info about the computation

def DEBUG(s):
    # print(s)
    pass

# And-Or tree search
# Check that a belief state or its super-set does not appear earlier
# in the current path.

import random

def constructPlan(bstate,path,goalstates):
    # Return the empty plan if belief state is goal states only.
    if bstate.issubset(goalstates):
        DEBUG("Goals reached")
        return PlanEmpty()
    # Cut the branch if the belief state has been encountered before.
    for bstate0 in path:
        if bstate0.issubset(bstate):
            DEBUG("Cycle cut at depth " + str(len(path)))
            return None
    # Use a depth cut-off, just in case.
    if len(path) > 30:
        return None

    actions = Bapplicable(bstate)
    random.shuffle(actions)

    DEBUG(str(len(actions)) + " applicable actions")
    for a in actions:
        DEBUG(str(a))
    DEBUG("in belief state:")
    for s in bstate:
        DEBUG("  " + str(s))

    # Try to find a plan
    for act in actions: # Iterate over actions (OR)
        DEBUG("Trying action " + str(act))

### WHAT IS THE IMPACT OF TAKING THE ACTION
### INSERT YOUR CODE HERE!
        success = True
        subplans = []
        # if act not in Bapplicable(bstate):
        #     print(act, 'not in')
        # else:
        #     print(act, 'in')
        # for s in Bsucc(bstate, act):
        #     print('successor state', s)
        succ_bstate = Bsucc(bstate, act)
        for obs in act.observations(): # Iterate over observations (AND)
            DEBUG("Considering observation " + str(obs))
            # print(len(Bsucc(bstate, act) & Bobserve(bstate, obs)))
            # for s in Bobserve(bstate, obs):
            #     print('observed state', s)
            obser_bstate = Bobserve(succ_bstate, obs)
            # for s in obser_bstate:
            #     print('observed state', s)
            subplan = constructPlan(obser_bstate, path + [bstate], goalstates)
            if subplan is None:
                success = False
                break
            subplans += [(obs, subplan)]
        if success:
            return PlanNode(act, subplans)

    # return None
### HOW DOES THE BELIEF STATE CHANGE UPON MAKING THIS OBSERVATION?
### (IF THE OBSERVATION IS NOT POSSIBLE, DO NOT CONSIDER THIS CASE FURTHER!)
### RECURSIVELY SEARCH FOR A PLAN FOR THE RESULTING BELIEF STATE
### INSERT YOUR CODE HERE!
### INSERT YOUR CODE HERE!
### INSERT YOUR CODE HERE!
### IF A SUBPLAN WAS FOUND FOR EVERY OBSERVATION, RETURN A PLAN
### CONSISTING OF THE CURRENT ACTION AND THE SUBPLANS.

    # IF no plan was found with any action, so return None
    DEBUG("No plan")
    return None

# Construct a branching plan for a problem instance with partial observability.

def POsolver(instance):
    initialStates, goalStates, allActions = instance
    return constructPlan(initialStates,[],goalStates)
