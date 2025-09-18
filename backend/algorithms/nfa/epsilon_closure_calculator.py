"""
EpsilonClosureCalculator for computing epsilon closures of states.

This module provides the EpsilonClosureCalculator class which computes
the epsilon closure of states in finite automata. The epsilon closure
of a state is the set of all states reachable from that state using
only epsilon (empty string) transitions.
"""

from typing import Set
from ...models.automaton import Automaton
from ...models.state import State


class EpsilonClosureCalculator:
    """
    Utility class for computing epsilon closures of states.
    
    The epsilon closure of a state is the set of all states reachable
    from that state using only epsilon (empty string) transitions.
    """
    
    @staticmethod
    def compute_closure(states: Set[State], automaton: Automaton) -> Set[State]:
        """
        Compute the epsilon closure of a set of states.
        
        Args:
            states: Set of states to compute closure for
            automaton: The automaton containing the states
            
        Returns:
            Set of states reachable via epsilon transitions
        """
        closure = set(states)
        stack = list(states)
        
        while stack:
            current_state = stack.pop()
            
            # Find all epsilon transitions from current state
            transitions = automaton.get_transitions_from_state(current_state)
            for transition in transitions:
                if transition.is_epsilon and transition.to_state not in closure:
                    closure.add(transition.to_state)
                    stack.append(transition.to_state)
        
        return closure
    
    @staticmethod
    def compute_closure_single(state: State, automaton: Automaton) -> Set[State]:
        """
        Compute the epsilon closure of a single state.
        
        Args:
            state: State to compute closure for
            automaton: The automaton containing the state
            
        Returns:
            Set of states reachable via epsilon transitions
        """
        return EpsilonClosureCalculator.compute_closure({state}, automaton)