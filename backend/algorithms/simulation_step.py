"""
SimulationStep class for tracking DFA execution steps.

This module provides the SimulationStep class which represents a single
step in DFA simulation, tracking the current state, input position, and
the symbol being processed during each step of the simulation.
"""

from typing import Optional
from ..models.state import State
from ..models.transition import Transition


class SimulationStep:
    """
    Represents a single step in DFA simulation.
    
    Tracks the current state, input position, and the symbol being processed
    during each step of the simulation.
    """
    
    def __init__(
        self, 
        current_state: State, 
        input_position: int, 
        symbol: Optional[str] = None,
        transition_used: Optional[Transition] = None
    ):
        """
        Initialize a simulation step.
        
        Args:
            current_state: The state the automaton is in at this step
            input_position: Current position in the input string
            symbol: The symbol being processed (None for initial step)
            transition_used: The transition taken to reach this step (None for initial)
        """
        self.current_state = current_state
        self.input_position = input_position
        self.symbol = symbol
        self.transition_used = transition_used
    
    def __str__(self) -> str:
        """Return string representation of the simulation step."""
        if self.symbol is None:
            return f"Initial: {self.current_state.id}"
        return f"Step {self.input_position}: '{self.symbol}' -> {self.current_state.id}"
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"SimulationStep(state={self.current_state.id}, "
                f"position={self.input_position}, symbol={self.symbol!r})")