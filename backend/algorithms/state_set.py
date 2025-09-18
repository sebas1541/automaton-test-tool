"""
StateSet class for NFA to DFA conversion.

This module provides the StateSet class which represents a set of NFA states
as a single DFA state during the subset construction algorithm.
"""

from typing import Set, FrozenSet
from ..models.state import State


class StateSet:
    """
    Represents a set of NFA states as a single DFA state.
    
    This class encapsulates a frozenset of states and provides
    utilities for generating unique identifiers and managing
    the subset construction process.
    """
    
    def __init__(self, states: Set[State]):
        """
        Initialize a state set.
        
        Args:
            states: Set of NFA states that this DFA state represents
        """
        self._states = frozenset(states)
        self._id = self._generate_id()
    
    @property
    def states(self) -> FrozenSet[State]:
        """Get the frozenset of NFA states."""
        return self._states
    
    @property
    def id(self) -> str:
        """Get the unique identifier for this state set."""
        return self._id
    
    @property
    def is_final(self) -> bool:
        """Check if this state set contains any final states."""
        return any(state.is_final for state in self._states)
    
    def _generate_id(self) -> str:
        """Generate a unique identifier based on the state IDs."""
        if not self._states:
            return "∅"
        
        state_ids = sorted(state.id for state in self._states)
        return "{" + ",".join(state_ids) + "}"
    
    def __eq__(self, other) -> bool:
        """Check equality based on the state set."""
        if not isinstance(other, StateSet):
            return False
        return self._states == other._states
    
    def __hash__(self) -> int:
        """Return hash for use in sets and dicts."""
        return hash(self._states)
    
    def __str__(self) -> str:
        """Return string representation."""
        return self._id
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return f"StateSet({self._id})"