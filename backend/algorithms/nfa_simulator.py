"""
NFA Simulator for nondeterministic finite automaton execution.

This module provides the NFASimulator class which simulates the execution
of nondeterministic finite automata on input strings. It handles epsilon
transitions, multiple computation paths, and implements the standard
NFA simulation algorithm with epsilon closure computation.
"""

from typing import Set, List, Dict, Tuple, Optional
from collections import deque
from ..models.automaton import Automaton
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


class NFASimulator:
    """
    Simulates execution of nondeterministic finite automata.
    
    This simulator handles multiple computation paths simultaneously,
    epsilon transitions, and implements the standard NFA simulation
    algorithm using configuration sets.
    """
    
    def __init__(self, automaton: Automaton):
        """
        Initialize the NFA simulator.
        
        Args:
            automaton: The automaton to simulate
            
        Raises:
            ValueError: If the automaton has no initial state
        """
        if automaton.initial_state is None:
            raise ValueError("Automaton must have an initial state")
        
        self._automaton = automaton
        self._closure_calculator = EpsilonClosureCalculator()
    
    @property
    def automaton(self) -> Automaton:
        """Get the automaton being simulated."""
        return self._automaton
    
    def simulate(self, input_string: str) -> Tuple[bool, List[Set[NFAConfiguration]]]:
        """
        Simulate the NFA on an input string.
        
        Args:
            input_string: The string to process
            
        Returns:
            Tuple of (is_accepted, configuration_sets)
            - is_accepted: True if the string is accepted, False otherwise
            - configuration_sets: List of configuration sets for each step
            
        Raises:
            ValueError: If input contains symbols not in the alphabet
        """
        # Validate input string
        self._validate_input(input_string)
        
        # Initialize with epsilon closure of initial state
        initial_config = NFAConfiguration(self._automaton.initial_state, 0)
        initial_closure = self._closure_calculator.compute_closure_single(
            self._automaton.initial_state, self._automaton
        )
        
        current_configs = {NFAConfiguration(state, 0) for state in initial_closure}
        all_configuration_sets = [current_configs.copy()]
        
        # Process each symbol in the input
        for i, symbol in enumerate(input_string):
            next_configs = set()
            
            # For each current configuration
            for config in current_configs:
                # Find all transitions on this symbol
                transitions = self._automaton.get_transitions_from_state(config.state)
                for transition in transitions:
                    if transition.matches_symbol(symbol):
                        # Create new configuration after taking transition
                        new_path = config.path + [transition]
                        new_config = NFAConfiguration(
                            transition.to_state, 
                            i + 1, 
                            new_path
                        )
                        next_configs.add(new_config)
            
            # Compute epsilon closure of all reached states
            if next_configs:
                reached_states = {config.state for config in next_configs}
                closure_states = self._closure_calculator.compute_closure(
                    reached_states, self._automaton
                )
                
                # Create configurations for all states in closure
                current_configs = set()
                for config in next_configs:
                    # Add the direct configuration
                    current_configs.add(config)
                    
                    # Add configurations for epsilon-reachable states
                    epsilon_reachable = self._closure_calculator.compute_closure_single(
                        config.state, self._automaton
                    )
                    for state in epsilon_reachable:
                        if state != config.state:  # Don't duplicate the original
                            current_configs.add(NFAConfiguration(state, i + 1, config.path))
            else:
                current_configs = set()
            
            all_configuration_sets.append(current_configs.copy())
        
        # Check if any final configuration is accepting
        is_accepted = any(config.is_accepting for config in current_configs)
        return is_accepted, all_configuration_sets
    
    def is_accepted(self, input_string: str) -> bool:
        """
        Check if an input string is accepted by the NFA.
        
        Args:
            input_string: The string to test
            
        Returns:
            True if the string is accepted, False otherwise
        """
        accepted, _ = self.simulate(input_string)
        return accepted
    
    def get_accepting_paths(self, input_string: str) -> List[List[Transition]]:
        """
        Get all accepting computation paths for an input string.
        
        Args:
            input_string: The string to analyze
            
        Returns:
            List of accepting paths (each path is a list of transitions)
        """
        accepted, config_sets = self.simulate(input_string)
        
        if not accepted or not config_sets:
            return []
        
        # Get accepting configurations from final step
        final_configs = config_sets[-1]
        accepting_configs = [config for config in final_configs if config.is_accepting]
        
        return [config.path for config in accepting_configs]
    
    def simulate_with_details(self, input_string: str) -> Dict:
        """
        Simulate with detailed information for debugging/visualization.
        
        Args:
            input_string: The string to simulate
            
        Returns:
            Dictionary with detailed simulation information
        """
        is_accepted, config_sets = self.simulate(input_string)
        accepting_paths = self.get_accepting_paths(input_string) if is_accepted else []
        
        # Count configurations at each step
        config_counts = [len(configs) for configs in config_sets]
        
        # Get states active at each step
        states_by_step = []
        for configs in config_sets:
            states = {config.state.id for config in configs}
            states_by_step.append(sorted(states))
        
        return {
            'accepted': is_accepted,
            'total_steps': len(input_string),
            'configuration_counts': config_counts,
            'states_by_step': states_by_step,
            'accepting_paths_count': len(accepting_paths),
            'accepting_paths': accepting_paths,
            'is_deterministic': self._automaton.is_deterministic()
        }
    
    def _validate_input(self, input_string: str) -> None:
        """
        Validate that the input string uses only alphabet symbols.
        
        Args:
            input_string: The string to validate
            
        Raises:
            ValueError: If input contains invalid symbols
        """
        alphabet = self._automaton.alphabet
        for i, symbol in enumerate(input_string):
            if symbol not in alphabet:
                raise ValueError(
                    f"Symbol '{symbol}' at position {i} is not in the alphabet {sorted(alphabet)}"
                )


class NFAStepByStepSimulator:
    """
    Interactive step-by-step NFA simulation.
    
    Allows stepping through an NFA simulation one symbol at a time,
    showing the evolution of configuration sets and epsilon closures.
    """
    
    def __init__(self, simulator: NFASimulator, input_string: str):
        """
        Initialize step-by-step NFA simulation.
        
        Args:
            simulator: The NFA simulator to use
            input_string: The string to simulate
        """
        self._simulator = simulator
        self._input_string = input_string
        self._current_position = 0
        self._configuration_sets = []
        self._finished = False
        
        # Validate input and initialize
        self._simulator._validate_input(input_string)
        self._initialize_simulation()
    
    def _initialize_simulation(self) -> None:
        """Initialize the simulation with epsilon closure of initial state."""
        initial_state = self._simulator.automaton.initial_state
        initial_closure = EpsilonClosureCalculator.compute_closure_single(
            initial_state, self._simulator.automaton
        )
        
        initial_configs = {NFAConfiguration(state, 0) for state in initial_closure}
        self._configuration_sets = [initial_configs]
    
    @property
    def current_configurations(self) -> Set[NFAConfiguration]:
        """Get the current set of configurations."""
        if self._configuration_sets:
            return self._configuration_sets[-1].copy()
        return set()
    
    @property
    def current_states(self) -> Set[State]:
        """Get the current set of active states."""
        return {config.state for config in self.current_configurations}
    
    @property
    def current_position(self) -> int:
        """Get the current position in the input string."""
        return self._current_position
    
    @property
    def remaining_input(self) -> str:
        """Get the remaining unprocessed input."""
        return self._input_string[self._current_position:]
    
    @property
    def processed_input(self) -> str:
        """Get the already processed input."""
        return self._input_string[:self._current_position]
    
    @property
    def is_finished(self) -> bool:
        """Check if the simulation is finished."""
        return self._finished
    
    @property
    def is_accepted(self) -> bool:
        """Check if the string is accepted (only valid when finished)."""
        if not self._finished:
            raise ValueError("Simulation not finished yet")
        return any(config.is_accepting for config in self.current_configurations)
    
    @property
    def configuration_history(self) -> List[Set[NFAConfiguration]]:
        """Get the history of configuration sets."""
        return [configs.copy() for configs in self._configuration_sets]
    
    def step(self) -> bool:
        """
        Execute one step of the simulation.
        
        Returns:
            True if the step was successful, False if simulation is finished
        """
        if self._finished or self._current_position >= len(self._input_string):
            self._finished = True
            return False
        
        # Get the next symbol
        symbol = self._input_string[self._current_position]
        current_configs = self._configuration_sets[-1]
        next_configs = set()
        
        # Process symbol for each configuration
        for config in current_configs:
            transitions = self._simulator.automaton.get_transitions_from_state(config.state)
            for transition in transitions:
                if transition.matches_symbol(symbol):
                    new_path = config.path + [transition]
                    new_config = NFAConfiguration(
                        transition.to_state,
                        self._current_position + 1,
                        new_path
                    )
                    next_configs.add(new_config)
        
        # Compute epsilon closure
        if next_configs:
            reached_states = {config.state for config in next_configs}
            closure_states = EpsilonClosureCalculator.compute_closure(
                reached_states, self._simulator.automaton
            )
            
            # Add epsilon-reachable configurations
            final_configs = set(next_configs)
            for config in next_configs:
                epsilon_reachable = EpsilonClosureCalculator.compute_closure_single(
                    config.state, self._simulator.automaton
                )
                for state in epsilon_reachable:
                    if state != config.state:
                        final_configs.add(NFAConfiguration(
                            state, self._current_position + 1, config.path
                        ))
            
            self._configuration_sets.append(final_configs)
        else:
            self._configuration_sets.append(set())
        
        self._current_position += 1
        
        # Check if finished
        if self._current_position >= len(self._input_string):
            self._finished = True
        
        return True
    
    def run_to_completion(self) -> bool:
        """
        Run the simulation to completion.
        
        Returns:
            True if the string is accepted, False otherwise
        """
        while not self._finished:
            self.step()
        return self.is_accepted
    
    def reset(self) -> None:
        """Reset the simulation to the beginning."""
        self._current_position = 0
        self._finished = False
        self._initialize_simulation()