from typing import List
from modules.lr0_items import State

class DFA:
    def __init__(self, states: List[State]):
        self.states = states
        self.transitions = []
        
        for state in self.states:
            for symbol, next_state in state.transitions.items():
                self.transitions.append({
                    'from': state.state_id,
                    'to': next_state,
                    'symbol': symbol
                })