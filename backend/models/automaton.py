"""
Automaton class for representing Deterministic Finite Automata (DFA).

This module provides the Automaton class which represents Deterministic 
Finite Automata. It manages states, transitions, and provides core
functionality for DFA operations.
"""

from typing import Set, List, Optional, Dict, Iterator
from .state import State
from .transition import Transition


class Automaton:
    """
    Represents a Deterministic Finite Automaton (DFA).
    
    A DFA consists of states, transitions, an initial state,
    final states, and an alphabet. This class provides methods for
    managing these components and performing basic DFA operations.
    """
    
    def __init__(
        self,
        states: Optional[Set[State]] = None,
        transitions: Optional[Set[Transition]] = None,
        initial_state: Optional[State] = None,
        final_states: Optional[Set[State]] = None,
        alphabet: Optional[Set[str]] = None
    ):
        """
        Initialize a new DFA.
        
        Args:
            states: Set of states in the DFA (default: empty set)
            transitions: Set of transitions in the DFA (default: empty set)
            initial_state: The initial state (default: None)
            final_states: Set of final/accepting states (default: empty set)
            alphabet: Set of symbols in the alphabet (default: empty set)
        """
        self._states = states if states is not None else set()
        self._transitions = transitions if transitions is not None else set()
        self._initial_state = initial_state
        self._final_states = final_states if final_states is not None else set()
        self._alphabet = alphabet if alphabet is not None else set()
        
        # Validate that all referenced states exist and DFA properties
        self._validate_consistency()
    
    def _validate_consistency(self) -> None:
        """Validate that the automaton is internally consistent and deterministic."""
        # Check that initial state is in states set
        if self._initial_state is not None and self._initial_state not in self._states:
            raise ValueError("Initial state must be in the states set")
        
        # Check that final states are in states set
        for final_state in self._final_states:
            if final_state not in self._states:
                raise ValueError("All final states must be in the states set")
        
        # Check that transition states are in states set
        for transition in self._transitions:
            if transition.from_state not in self._states:
                raise ValueError("All transition source states must be in the states set")
            if transition.to_state not in self._states:
                raise ValueError("All transition destination states must be in the states set")
        
        # Validate DFA determinism: no multiple transitions from same state on same symbol
        state_symbol_pairs = set()
        for transition in self._transitions:
            pair = (transition.from_state, transition.symbol)
            if pair in state_symbol_pairs:
                raise ValueError(f"Multiple transitions from state {transition.from_state.id} on symbol '{transition.symbol}' - not a valid DFA")
            state_symbol_pairs.add(pair)
    
    @property
    def states(self) -> Set[State]:
        """Get all states in the DFA."""
        return self._states.copy()
    
    @property
    def transitions(self) -> Set[Transition]:
        """Get all transitions in the DFA."""
        return self._transitions.copy()
    
    @property
    def initial_state(self) -> Optional[State]:
        """Get the initial state."""
        return self._initial_state
    
    @initial_state.setter
    def initial_state(self, state: Optional[State]) -> None:
        """Set the initial state."""
        if state is not None and state not in self._states:
            raise ValueError("Initial state must be in the states set")
        self._initial_state = state
    
    @property
    def final_states(self) -> Set[State]:
        """Get all final states."""
        return self._final_states.copy()
    
    @property
    def alphabet(self) -> Set[str]:
        """Get the alphabet."""
        return self._alphabet.copy()
    
    def add_state(self, state: State) -> None:
        """
        Add a state to the DFA.
        
        Args:
            state: The state to add
            
        Raises:
            ValueError: If a state with the same ID already exists
        """
        if any(s.id == state.id for s in self._states):
            raise ValueError(f"State with ID '{state.id}' already exists")
        self._states.add(state)
    
    def remove_state(self, state: State) -> None:
        """
        Remove a state from the DFA.
        
        Also removes all transitions involving this state and updates
        initial/final state references.
        
        Args:
            state: The state to remove
            
        Raises:
            ValueError: If the state is not in the DFA
        """
        if state not in self._states:
            raise ValueError("State not found in DFA")
        
        # Remove all transitions involving this state
        self._transitions = {t for t in self._transitions 
                           if t.from_state != state and t.to_state != state}
        
        # Update initial state if necessary
        if self._initial_state == state:
            self._initial_state = None
        
        # Remove from final states if necessary
        self._final_states.discard(state)
        
        # Remove the state
        self._states.remove(state)
    
    def add_transition(self, transition: Transition) -> None:
        """
        Add a transition to the DFA.
        
        Args:
            transition: The transition to add
            
        Raises:
            ValueError: If the transition already exists, references unknown states,
                       or violates DFA determinism
        """
        if transition.from_state not in self._states:
            raise ValueError("Transition source state not in DFA")
        if transition.to_state not in self._states:
            raise ValueError("Transition destination state not in DFA")
        
        # Check for determinism: no multiple transitions from same state on same symbol
        for existing_transition in self._transitions:
            if (existing_transition.from_state == transition.from_state and
                existing_transition.symbol == transition.symbol):
                raise ValueError(f"DFA already has transition from {transition.from_state.id} on symbol '{transition.symbol}'")
        
        if transition in self._transitions:
            raise ValueError("Transition already exists")
        
        self._transitions.add(transition)
        
        # Add symbol to alphabet
        self._alphabet.add(transition.symbol)
    
    def remove_transition(self, transition: Transition) -> None:
        """
        Remove a transition from the DFA.
        
        Args:
            transition: The transition to remove
            
        Raises:
            ValueError: If the transition is not in the DFA
        """
        if transition not in self._transitions:
            raise ValueError("Transition not found in DFA")
        
        self._transitions.remove(transition)
    
    def add_final_state(self, state: State) -> None:
        """
        Mark a state as final.
        
        Args:
            state: The state to mark as final
            
        Raises:
            ValueError: If the state is not in the DFA
        """
        if state not in self._states:
            raise ValueError("State not found in DFA")
        
        self._final_states.add(state)
        state.is_final = True
    
    def remove_final_state(self, state: State) -> None:
        """
        Unmark a state as final.
        
        Args:
            state: The state to unmark as final
        """
        self._final_states.discard(state)
        state.is_final = False
    
    def get_state_by_id(self, state_id: str) -> Optional[State]:
        """
        Get a state by its ID.
        
        Args:
            state_id: The ID of the state to find
            
        Returns:
            The state with the given ID, or None if not found
        """
        for state in self._states:
            if state.id == state_id:
                return state
        return None
    
    def get_transitions_from_state(self, state: State) -> List[Transition]:
        """
        Get all transitions originating from a specific state.
        
        Args:
            state: The source state
            
        Returns:
            List of transitions from the given state
        """
        return [t for t in self._transitions if t.from_state == state]
    
    def get_transitions_to_state(self, state: State) -> List[Transition]:
        """
        Get all transitions leading to a specific state.
        
        Args:
            state: The destination state
            
        Returns:
            List of transitions to the given state
        """
        return [t for t in self._transitions if t.to_state == state]
    
    def get_transitions_on_symbol(self, symbol: str) -> List[Transition]:
        """
        Get all transitions triggered by a specific symbol.
        
        Args:
            symbol: The input symbol
            
        Returns:
            List of transitions triggered by the given symbol
        """
        return [t for t in self._transitions if t.symbol == symbol]
    
    def get_transition_from_state_on_symbol(self, state: State, symbol: str) -> Optional[Transition]:
        """
        Get the transition from a specific state on a specific symbol.
        
        Since this is a DFA, there can be at most one such transition.
        
        Args:
            state: The source state
            symbol: The input symbol
            
        Returns:
            The transition, or None if no such transition exists
        """
        for transition in self._transitions:
            if transition.from_state == state and transition.symbol == symbol:
                return transition
        return None
    
    def __str__(self) -> str:
        """Return string representation of the DFA."""
        return (f"DFA(states={len(self._states)}, "
                f"transitions={len(self._transitions)}, "
                f"alphabet={sorted(self._alphabet)})")
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"Automaton(states={self._states!r}, "
                f"transitions={self._transitions!r}, "
                f"initial_state={self._initial_state!r}, "
                f"final_states={self._final_states!r}, "
                f"alphabet={self._alphabet!r})")
    
    def to_dict(self) -> dict:
        """
        Convert DFA to dictionary representation.
        
        Returns:
            Dictionary with DFA properties for serialization
        """
        return {
            'states': [state.to_dict() for state in self._states],
            'transitions': [transition.to_dict() for transition in self._transitions],
            'initial_state_id': self._initial_state.id if self._initial_state else None,
            'final_state_ids': [state.id for state in self._final_states],
            'alphabet': list(self._alphabet)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Automaton':
        """
        Create DFA from dictionary representation.
        
        Args:
            data: Dictionary containing DFA properties
            
        Returns:
            Automaton object created from dictionary data
            
        Raises:
            KeyError: If required keys are missing
            ValueError: If data is inconsistent or not a valid DFA
        """
        # Create states
        states = set()
        state_lookup = {}
        for state_data in data.get('states', []):
            state = State.from_dict(state_data)
            states.add(state)
            state_lookup[state.id] = state
        
        # Create transitions
        transitions = set()
        for transition_data in data.get('transitions', []):
            transition = Transition.from_dict(transition_data, state_lookup)
            transitions.add(transition)
        
        # Get initial state
        initial_state_id = data.get('initial_state_id')
        initial_state = state_lookup.get(initial_state_id) if initial_state_id else None
        
        # Get final states
        final_state_ids = data.get('final_state_ids', [])
        final_states = {state_lookup[state_id] for state_id in final_state_ids}
        
        # Mark final states
        for state in final_states:
            state.is_final = True
        
        # Get alphabet
        alphabet = set(data.get('alphabet', []))
        
        return cls(states, transitions, initial_state, final_states, alphabet)