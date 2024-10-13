
from logic import *

# Mapping from actions and initial and goal states to a formula

# Turn variable name 'x' to an atomic formula 'x@t'.

def timedVar(varname,time):
    return ATOM(varname + "@" + str(time))

# Turn action name 'x' to an atomic formula 'x@t'.

def timedAction(varname,time):
    return ATOM("ACTION" + varname + "@" + str(time))

# Two actions cannot be taken at the same time?

def exclusive(c1,pe1,ne1,c2,pe2,ne2):
    return (bool(set(c1) & set(ne2))) or (bool(set(ne1) & set(c2)))

# DO NOT MODIFY ANY DEFINITION ABOVE THIS LINE

# Map a reachability problem to a propositional formula

def reachability2fma(init,goal,actions,T):
    initvars = { v for v in init }
    goalvars = { v for v in goal }
    actioncvars = { v for n,c,pe,ne in actions for v in c }
    actionpvars = { v for n,c,pe,ne in actions for v in pe }
    actionnvars = { v for n,c,pe,ne in actions for v in ne }
    varsets = [initvars,goalvars,actioncvars,actionpvars,actionnvars]
    allStateVars = set().union(*varsets)

    initformulas = [ timedVar(v,0) for v in initvars ] + [ NOT(timedVar(v,0)) for v in allStateVars if v not in initvars ]

    goalformulas = [ timedVar(v,T) for v in goalvars ]

    # For representing the formulas we have for all t in 0..T-1
    # the following formulas.
    #
    #   a@t -> x@t if x belongs to 'condition' for action 'a'
    #   a@t -> x@(t+1) if x belongs to 'posEffects' for action 'a'
    #   a@t -> not x@(t+1) if x belongs to 'negEffects' for action 'a'
    preconditions = [ IMPL(timedAction(n,t),timedVar(x,t)) for n,c,pe,ne in actions for t in range(0,T) for x in c ]

    # IMPLEMENT THE FORMULA FOR POSITIVE EFFECTS
    posEffects = [ IMPL(timedAction(n,t), timedVar(x,t+1)) for n,c,pe,ne in actions for t in range(0,T) for x in pe]
    # IMPLEMENT THE FORMULA FOR NEGATIVE EFFECTS
    negEffects = [ IMPL(timedAction(n,t), NOT(timedVar(x,t+1))) for n,c,pe,ne in actions for t in range(0,T) for x in ne]

    # Finally, we require that for every change for a state
    # variable there must be an action that makes that change.
    # In other words, there cannot be change without a cause.
    # For each state variable x and time point t we have the formula
    #
    #   (x@t & not x@(t+1)) -> a1@t V a2@t V ... V an@t
    #
    # for all t in 0..T-1, where a1,a2,...,an are all actions
    # with x in negEffects. Similarly we have
    #
    #   (not x@t & x@(t+1)) -> a1@t V a2@t V ... V an@t
    #
    # where a1,a2,...,an are all actions with x in posEffects.
    # The formulas are called 'frame axioms' for historical
    # reasons.

    # IMPLEMENT THE POSITIVE FRAME AXIOMS
    posFrameAxioms = [IMPL(AND([timedVar(x,t), NOT(timedVar(x,t+1))]), OR([timedAction(n,t) for n,c,pe,ne in actions if x in ne])) for t in range(0,T) for x in allStateVars]
    # IMPLEMENT THE NEGATIVE FRAME AXIOMS
    negFrameAxioms = [IMPL(AND([timedVar(x,t+1), NOT(timedVar(x,t))]), OR([timedAction(n,t) for n,c,pe,ne in actions if x in pe])) for t in range(0,T) for x in allStateVars]

    # So far none of the formulas directly forbid taking
    # any two or more actions at the same time point.
    # We allow to action a1 and a2 at the same time point
    # if we can execute them in either order a1,a2 or a2,a1.
    # If this is not possible, we prohibit their simultaneous
    # execution by the formula
    #
    #   not(a1@t & a2@t)
    #
    # for all t in 0..T-1. Two actions a1 and a2 can be executed
    # in both ordering a1,a2 and a2,a1 if
    # - the conditions of both are true (no need to test this!),
    # - condition of a1 does not intersect negEffects of a2
    # - condition of a2 does not intersect negEffects of a1.
    # If we have non-empty intersection in one of those two
    # cases, then we need that formula not(a1@t & a2@t).
    # If these formulas are omitted, then we will be getting
    # plans that are impossible to execute, like going from
    # location A simultaneously to both locations B and C.
    # WARNING: Make sure yo do not use this formula if a1=a2.
    # IMPLEMENT THE ACTION EXCLUSION CONSTRAINTS
    def all_pairs(elements):
        """
        Helper function, giving all pairs of a list of elements

        Parameter
        --------
        elements: List[Any]
            list of elements

        Returns
        -------
        List[Tuple[Any, Any]]
           Unique pairings of the elements in the given list.
        """
        return [(elements[i], elements[j]) for i in range(0, len(elements)) for j in range(i + 1, len(elements))]

    actionMutexes = [NOT(AND([timedAction(a1, t), timedAction(a2, t)])) for t in range(0,T) for ((a1,c1,pe1,ne1), (a2,c2,pe2,ne2)) in all_pairs(actions) if set(c1)&set(ne2) or set(c2)&set(ne1)]

    return AND(initformulas + goalformulas + preconditions + posEffects + negEffects + posFrameAxioms + negFrameAxioms + actionMutexes)
