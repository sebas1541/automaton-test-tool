"""
Transition class for representing automaton transitions.

This module provides the Transition class which represents transitions (edges)
between states in finite automata. Each transition connects two states and
is triggered by a specific symbol from the alphabet.
"""

from typing import Optional
from .state import State


class Transition:
    """
    Represents a transition between two states in a finite automaton.
    
    A transition defines how an automaton moves from one state to another
    when processing a specific input symbol. It includes support for
    epsilon (lambda) transitions using None or empty string as the symbol.
    """
    
    # Constants for special transition types
    EPSILON = ""  # Empty string represents epsilon/lambda transitions
    
    def __init__(
        self, 
        from_state: State, 
        to_state: State, 
        symbol: Optional[str] = None
    ):
        """
        Initialize a new Transition.
        
        Args:
            from_state: The source state of the transition
            to_state: The destination state of the transition
            symbol: The input symbol that triggers this transition.
                   None or empty string represents epsilon transition.
        
        Raises:
            TypeError: If from_state or to_state are not State instances
        """
        if not isinstance(from_state, State):
            raise TypeError("from_state must be a State instance")
        if not isinstance(to_state, State):
            raise TypeError("to_state must be a State instance")
        
        self._from_state = from_state
        self._to_state = to_state
        self._symbol = symbol if symbol is not None else self.EPSILON
    
    @property
    def from_state(self) -> State:
        """Get the source state of the transition."""
        return self._from_state
    
    @property
    def to_state(self) -> State:
        """Get the destination state of the transition."""
        return self._to_state
    
    @property
    def symbol(self) -> str:
        """Get the symbol that triggers this transition."""
        return self._symbol
    
    @symbol.setter
    def symbol(self, value: Optional[str]) -> None:
        """Set the transition symbol."""
        self._symbol = value if value is not None else self.EPSILON
    
    @property
    def is_epsilon(self) -> bool:
        """Check if this is an epsilon (lambda) transition."""
        return self._symbol == self.EPSILON
    
    def matches_symbol(self, input_symbol: str) -> bool:
        """
        Check if this transition can be triggered by the given input symbol.
        
        Args:
            input_symbol: The input symbol to check
            
        Returns:
            True if the transition can be triggered, False otherwise
        """
        return self._symbol == input_symbol
    
    def __str__(self) -> str:
        """Return string representation of the transition."""
        symbol_display = "ε" if self.is_epsilon else self._symbol
        return f"{self._from_state.id} --{symbol_display}--> {self._to_state.id}"
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"Transition(from_state={self._from_state!r}, "
                f"to_state={self._to_state!r}, symbol={self._symbol!r})")
    
    def __eq__(self, other) -> bool:
        """Check equality based on from_state, to_state, and symbol."""
        if not isinstance(other, Transition):
            return False
        return (self._from_state == other._from_state and 
                self._to_state == other._to_state and 
                self._symbol == other._symbol)
    
    def __hash__(self) -> int:
        """Return hash for use in sets and dicts."""
        return hash((self._from_state.id, self._to_state.id, self._symbol))
    
    def to_dict(self) -> dict:
        """
        Convert transition to dictionary representation.
        
        Returns:
            Dictionary with transition properties for serialization
        """
        return {
            'from_state_id': self._from_state.id,
            'to_state_id': self._to_state.id,
            'symbol': self._symbol
        }
    
    @classmethod
    def from_dict(cls, data: dict, state_lookup: dict[str, State]) -> 'Transition':
        """
        Create transition from dictionary representation.
        
        Args:
            data: Dictionary containing transition properties
            state_lookup: Dictionary mapping state IDs to State objects
            
        Returns:
            Transition object created from dictionary data
            
        Raises:
            KeyError: If required keys are missing or state IDs not found
            ValueError: If state lookup fails
        """
        from_state_id = data['from_state_id']
        to_state_id = data['to_state_id']
        
        if from_state_id not in state_lookup:
            raise ValueError(f"State with ID '{from_state_id}' not found")
        if to_state_id not in state_lookup:
            raise ValueError(f"State with ID '{to_state_id}' not found")
        
        return cls(
            from_state=state_lookup[from_state_id],
            to_state=state_lookup[to_state_id],
            symbol=data.get('symbol')
        )
    
    def copy_with_states(self, from_state: State, to_state: State) -> 'Transition':
        """
        Create a copy of this transition with different states.
        
        Useful for automaton transformations like NFA to DFA conversion.
        
        Args:
            from_state: New source state
            to_state: New destination state
            
        Returns:
            New Transition with same symbol but different states
        """
        return Transition(from_state, to_state, self._symbol)