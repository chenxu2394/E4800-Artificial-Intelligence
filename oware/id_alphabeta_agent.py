from iterative_deepening import IterativeDeepening
from agent import Agent


class IDAlphaBetaAgent(IterativeDeepening):
    def __init__(self):
        super().__init__(AgentClass=Agent)
