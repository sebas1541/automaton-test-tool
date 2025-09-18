"""
NFA Simulator for nondeterministic finite automaton execution.

This module provides the NFASimulator class which simulates the execution
of nondeterministic finite automata on input strings. It handles epsilon
transitions, multiple computation paths, and implements the standard
NFA simulation algorithm with epsilon closure computation.
"""

from typing import Set, List, Dict, Tuple
from ..models.automaton import Automaton
from ..models.state import State
from ..models.transition import Transition
from .nfa_configuration import NFAConfiguration
from .epsilon_closure_calculator import EpsilonClosureCalculator
from .nfa_step_by_step_simulator import NFAStepByStepSimulator


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
        initial_closure = EpsilonClosureCalculator.compute_closure_single(
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
                closure_states = EpsilonClosureCalculator.compute_closure(
                    reached_states, self._automaton
                )
                
                # Create configurations for all states in closure
                current_configs = set()
                for config in next_configs:
                    # Add the direct configuration
                    current_configs.add(config)
                    
                    # Add configurations for epsilon-reachable states
                    epsilon_reachable = EpsilonClosureCalculator.compute_closure_single(
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
    
    def create_step_by_step_simulator(self, input_string: str) -> 'NFAStepByStepSimulator':
        """
        Create a step-by-step simulator for the given input string.
        
        Args:
            input_string: The string to simulate
            
        Returns:
            NFAStepByStepSimulator instance
        """
        return NFAStepByStepSimulator(self, input_string)
    
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