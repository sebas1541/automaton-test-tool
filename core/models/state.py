"""
State class for representing automaton states.

This module provides the State class which represents individual states
in finite automata. Each state has an identifier, position coordinates
for visualization, and properties indicating whether it's a final state.
"""

from typing import Optional, Tuple


class State:
    """
    Represents a state in a finite automaton.
    
    A state is a fundamental component of automata with properties including
    a unique identifier, position for visualization, final state status,
    and an optional human-readable label.
    """
    
    def __init__(
        self, 
        state_id: str, 
        position: Tuple[float, float] = (0.0, 0.0), 
        is_final: bool = False,
        label: Optional[str] = None
    ):
        """
        Initialize a new State.
        
        Args:
            state_id: Unique identifier for the state
            position: (x, y) coordinates for visualization (default: (0.0, 0.0))
            is_final: Whether this is a final/accepting state (default: False)
            label: Optional human-readable label (default: None)
        
        Raises:
            ValueError: If state_id is empty or None
        """
        if not state_id:
            raise ValueError("State ID cannot be empty or None")
        
        self._id = state_id
        self._position = position
        self._is_final = is_final
        self._label = label
    
    @property
    def id(self) -> str:
        """Get the state identifier."""
        return self._id
    
    @property
    def position(self) -> Tuple[float, float]:
        """Get the state position as (x, y) coordinates."""
        return self._position
    
    @position.setter
    def position(self, value: Tuple[float, float]) -> None:
        """Set the state position."""
        self._position = value
    
    @property
    def is_final(self) -> bool:
        """Check if this is a final/accepting state."""
        return self._is_final
    
    @is_final.setter
    def is_final(self, value: bool) -> None:
        """Set the final state status."""
        self._is_final = value
    
    @property
    def label(self) -> Optional[str]:
        """Get the state label."""
        return self._label
    
    @label.setter
    def label(self, value: Optional[str]) -> None:
        """Set the state label."""
        self._label = value
    
    def __str__(self) -> str:
        """Return string representation of the state."""
        final_marker = " (final)" if self._is_final else ""
        label_info = f" '{self._label}'" if self._label else ""
        return f"State({self._id}{label_info}{final_marker})"
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"State(state_id='{self._id}', position={self._position}, "
                f"is_final={self._is_final}, label={self._label!r})")
    
    def __eq__(self, other) -> bool:
        """Check equality based on state ID."""
        if not isinstance(other, State):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Return hash based on state ID for use in sets and dicts."""
        return hash(self._id)
    
    def to_dict(self) -> dict:
        """
        Convert state to dictionary representation.
        
        Returns:
            Dictionary with state properties for serialization
        """
        return {
            'id': self._id,
            'position': self._position,
            'is_final': self._is_final,
            'label': self._label
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'State':
        """
        Create state from dictionary representation.
        
        Args:
            data: Dictionary containing state properties
            
        Returns:
            State object created from dictionary data
            
        Raises:
            KeyError: If required 'id' key is missing
            ValueError: If state_id is invalid
        """
        return cls(
            state_id=data['id'],
            position=data.get('position', (0.0, 0.0)),
            is_final=data.get('is_final', False),
            label=data.get('label')
        )