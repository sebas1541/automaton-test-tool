"""
NFA to DFA Converter implementing the subset construction algorithm.

This module provides the NFAToDFAConverter class which converts any
nondeterministic finite automaton (NFA) into an equivalent deterministic
finite automaton (DFA) using the subset construction algorithm.
"""

from typing import Set, Dict, List, Tuple, Optional, FrozenSet
from collections import deque
from ..models.automaton import Automaton
from ..models.state import State
from ..models.transition import Transition
from .nfa_simulator import EpsilonClosureCalculator


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


class NFAToDFAConverter:
    """
    Converts NFAs to equivalent DFAs using subset construction.
    
    This converter implements the standard subset construction algorithm,
    handling epsilon transitions and creating an equivalent DFA that
    accepts the same language as the input NFA.
    """
    
    def __init__(self):
        """Initialize the NFA to DFA converter."""
        self._closure_calculator = EpsilonClosureCalculator()
    
    def convert(self, nfa: Automaton) -> Tuple[Automaton, List[ConversionStep]]:
        """
        Convert an NFA to an equivalent DFA.
        
        Args:
            nfa: The NFA to convert
            
        Returns:
            Tuple of (dfa, conversion_steps)
            - dfa: The equivalent DFA
            - conversion_steps: List of steps taken during conversion
            
        Raises:
            ValueError: If the NFA has no initial state
        """
        if nfa.initial_state is None:
            raise ValueError("NFA must have an initial state")
        
        # Initialize conversion tracking
        conversion_steps = []
        step_counter = 0
        
        # Create initial DFA state from epsilon closure of NFA initial state
        initial_nfa_closure = self._closure_calculator.compute_closure_single(
            nfa.initial_state, nfa
        )
        initial_state_set = StateSet(initial_nfa_closure)
        
        # Maps StateSet to corresponding DFA State
        state_set_to_dfa_state: Dict[StateSet, State] = {}
        
        # Create initial DFA state
        initial_dfa_state = State(
            state_id=f"q{len(state_set_to_dfa_state)}",
            position=(100, 100),  # Default position
            is_final=initial_state_set.is_final,
            label=initial_state_set.id
        )
        state_set_to_dfa_state[initial_state_set] = initial_dfa_state
        
        # Initialize DFA
        dfa_states = {initial_dfa_state}
        dfa_transitions = set()
        dfa_final_states = set()
        if initial_state_set.is_final:
            dfa_final_states.add(initial_dfa_state)
        
        # Queue for processing unprocessed state sets
        unprocessed_queue = deque([initial_state_set])
        processed_state_sets = set()
        
        # Process each state set
        while unprocessed_queue:
            current_state_set = unprocessed_queue.popleft()
            if current_state_set in processed_state_sets:
                continue
            
            processed_state_sets.add(current_state_set)
            current_dfa_state = state_set_to_dfa_state[current_state_set]
            
            # For each symbol in the alphabet
            for symbol in nfa.alphabet:
                # Compute the set of states reachable on this symbol
                target_nfa_states = self._compute_transition_target(
                    current_state_set.states, symbol, nfa
                )
                
                if target_nfa_states:
                    target_state_set = StateSet(target_nfa_states)
                    
                    # Check if this is a new state set
                    is_new_state = target_state_set not in state_set_to_dfa_state
                    
                    # Create DFA state if it doesn't exist
                    if is_new_state:
                        target_dfa_state = State(
                            state_id=f"q{len(state_set_to_dfa_state)}",
                            position=(100 + len(state_set_to_dfa_state) * 150, 100),
                            is_final=target_state_set.is_final,
                            label=target_state_set.id
                        )
                        state_set_to_dfa_state[target_state_set] = target_dfa_state
                        dfa_states.add(target_dfa_state)
                        
                        if target_state_set.is_final:
                            dfa_final_states.add(target_dfa_state)
                        
                        # Add to processing queue
                        unprocessed_queue.append(target_state_set)
                    else:
                        target_dfa_state = state_set_to_dfa_state[target_state_set]
                    
                    # Create DFA transition
                    dfa_transition = Transition(current_dfa_state, target_dfa_state, symbol)
                    dfa_transitions.add(dfa_transition)
                    
                    # Record conversion step
                    step_counter += 1
                    conversion_steps.append(ConversionStep(
                        step_counter,
                        current_state_set,
                        symbol,
                        target_state_set,
                        is_new_state
                    ))
        
        # Create the resulting DFA
        dfa = Automaton(
            states=dfa_states,
            transitions=dfa_transitions,
            initial_state=initial_dfa_state,
            final_states=dfa_final_states,
            alphabet=nfa.alphabet.copy()
        )
        
        return dfa, conversion_steps
    
    def convert_with_state_mapping(self, nfa: Automaton) -> Tuple[Automaton, Dict[str, StateSet]]:
        """
        Convert NFA to DFA and return state mapping.
        
        Args:
            nfa: The NFA to convert
            
        Returns:
            Tuple of (dfa, state_mapping)
            - dfa: The equivalent DFA
            - state_mapping: Maps DFA state IDs to corresponding NFA state sets
        """
        dfa, _ = self.convert(nfa)
        
        # Extract state mapping from DFA state labels
        state_mapping = {}
        for state in dfa.states:
            if state.label:
                # Parse the label to reconstruct the state set
                if state.label == "∅":
                    nfa_state_ids = set()
                else:
                    # Remove braces and split by comma
                    label_content = state.label.strip("{}")
                    if label_content:
                        nfa_state_ids = set(label_content.split(","))
                    else:
                        nfa_state_ids = set()
                
                # Find corresponding NFA states
                nfa_states = set()
                for nfa_state in nfa.states:
                    if nfa_state.id in nfa_state_ids:
                        nfa_states.add(nfa_state)
                
                state_mapping[state.id] = StateSet(nfa_states)
        
        return dfa, state_mapping
    
    def _compute_transition_target(
        self, 
        source_states: FrozenSet[State], 
        symbol: str, 
        nfa: Automaton
    ) -> Set[State]:
        """
        Compute the set of states reachable from source states on a symbol.
        
        Args:
            source_states: Set of source states
            symbol: Input symbol
            nfa: The NFA
            
        Returns:
            Set of states reachable via the symbol (including epsilon closure)
        """
        intermediate_states = set()
        
        # Find all states reachable via the symbol
        for state in source_states:
            transitions = nfa.get_transitions_from_state(state)
            for transition in transitions:
                if transition.matches_symbol(symbol):
                    intermediate_states.add(transition.to_state)
        
        # Compute epsilon closure of the intermediate states
        if intermediate_states:
            return self._closure_calculator.compute_closure(intermediate_states, nfa)
        else:
            return set()
    
    def analyze_conversion(self, nfa: Automaton) -> Dict:
        """
        Analyze the conversion process and return detailed information.
        
        Args:
            nfa: The NFA to analyze
            
        Returns:
            Dictionary with conversion analysis information
        """
        dfa, conversion_steps = self.convert(nfa)
        
        # Count various metrics
        nfa_state_count = len(nfa.states)
        dfa_state_count = len(dfa.states)
        nfa_transition_count = len(nfa.transitions)
        dfa_transition_count = len(dfa.transitions)
        
        # Analyze epsilon transitions in NFA
        epsilon_transitions = [t for t in nfa.transitions if t.is_epsilon]
        
        # Calculate state explosion ratio
        explosion_ratio = dfa_state_count / nfa_state_count if nfa_state_count > 0 else 0
        
        return {
            'nfa_stats': {
                'states': nfa_state_count,
                'transitions': nfa_transition_count,
                'epsilon_transitions': len(epsilon_transitions),
                'alphabet_size': len(nfa.alphabet),
                'is_deterministic': nfa.is_deterministic()
            },
            'dfa_stats': {
                'states': dfa_state_count,
                'transitions': dfa_transition_count,
                'alphabet_size': len(dfa.alphabet),
                'is_deterministic': dfa.is_deterministic()
            },
            'conversion_metrics': {
                'steps_taken': len(conversion_steps),
                'state_explosion_ratio': explosion_ratio,
                'new_states_created': dfa_state_count - 1,  # Excluding initial state
                'equivalent_languages': True  # By definition of the algorithm
            },
            'conversion_steps': conversion_steps
        }
    
    def verify_equivalence(self, nfa: Automaton, dfa: Automaton, test_strings: List[str]) -> bool:
        """
        Verify that the NFA and DFA accept the same strings.
        
        Args:
            nfa: The original NFA
            dfa: The converted DFA
            test_strings: List of strings to test
            
        Returns:
            True if both automata agree on all test strings, False otherwise
        """
        from .nfa_simulator import NFASimulator
        from .dfa_simulator import DFASimulator
        
        nfa_sim = NFASimulator(nfa)
        dfa_sim = DFASimulator(dfa)
        
        for test_string in test_strings:
            try:
                nfa_result = nfa_sim.is_accepted(test_string)
                dfa_result = dfa_sim.is_accepted(test_string)
                
                if nfa_result != dfa_result:
                    return False
            except ValueError:
                # If either simulator rejects due to alphabet issues,
                # both should reject for the same reason
                try:
                    nfa_sim.is_accepted(test_string)
                    return False  # NFA accepted but DFA had alphabet issue
                except ValueError:
                    try:
                        dfa_sim.is_accepted(test_string)
                        return False  # DFA accepted but NFA had alphabet issue
                    except ValueError:
                        continue  # Both rejected for alphabet reasons
        
        return True