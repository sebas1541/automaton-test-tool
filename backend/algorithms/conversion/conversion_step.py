"""
ConversionStep class for tracking NFA to DFA conversion steps.

This module provides the ConversionStep class which represents a step
in the NFA to DFA conversion process, tracking the creation of new DFA
states and transitions during the subset construction algorithm.
"""

from .state_set import StateSet


class ConversionStep:
    """
    Represents a step in the NFA to DFA conversion process.
    
    Tracks the creation of new DFA states and transitions during
    the subset construction algorithm for debugging and visualization.
    """
    
    def __init__(
        self,
        step_number: int,
        source_state_set: StateSet,
        symbol: str,
        target_state_set: StateSet,
        is_new_state: bool = False
    ):
        """
        Initialize a conversion step.
        
        Args:
            step_number: The step number in the conversion process
            source_state_set: The source DFA state (set of NFA states)
            symbol: The symbol triggering the transition
            target_state_set: The target DFA state (set of NFA states)
            is_new_state: Whether the target state was newly created
        """
        self.step_number = step_number
        self.source_state_set = source_state_set
        self.symbol = symbol
        self.target_state_set = target_state_set
        self.is_new_state = is_new_state
    
    def __str__(self) -> str:
        """Return string representation of the conversion step."""
        new_marker = " (NEW)" if self.is_new_state else ""
        return (f"Step {self.step_number}: {self.source_state_set} "
                f"--{self.symbol}--> {self.target_state_set}{new_marker}")