"""
NFAConfiguration class for NFA simulation state tracking.

This module provides the NFAConfiguration class which represents a
configuration during NFA simulation, capturing the state of the automaton
at a specific point in the computation.
"""

from typing import List
from ..models.state import State
from ..models.transition import Transition


class NFAConfiguration:
    """
    Represents a configuration during NFA simulation.
    
    A configuration captures the state of the automaton at a specific
    point in the computation, including the current state and position
    in the input string.
    """
    
    def __init__(self, state: State, input_position: int, path: List[Transition] = None):
        """
        Initialize an NFA configuration.
        
        Args:
            state: The current state
            input_position: Current position in the input string
            path: List of transitions taken to reach this configuration
        """
        self.state = state
        self.input_position = input_position
        self.path = path if path is not None else []
    
    @property
    def is_accepting(self) -> bool:
        """Check if this configuration is in an accepting state."""
        return self.state.is_final
    
    def __str__(self) -> str:
        """Return string representation of the configuration."""
        return f"Config({self.state.id}, pos={self.input_position})"
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"NFAConfiguration(state={self.state.id}, "
                f"position={self.input_position}, path_length={len(self.path)})")
    
    def __eq__(self, other) -> bool:
        """Check equality based on state and input position."""
        if not isinstance(other, NFAConfiguration):
            return False
        return self.state == other.state and self.input_position == other.input_position
    
    def __hash__(self) -> int:
        """Return hash for use in sets and dicts."""
        return hash((self.state.id, self.input_position))