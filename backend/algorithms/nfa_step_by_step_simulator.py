"""
NFAStepByStepSimulator for interactive NFA execution.

This module provides the NFAStepByStepSimulator class which allows stepping
through an NFA simulation one symbol at a time, showing the evolution of
configuration sets and epsilon closures.
"""

from typing import Set, List, TYPE_CHECKING
from ..models.state import State
from .nfa_configuration import NFAConfiguration
from .epsilon_closure_calculator import EpsilonClosureCalculator

if TYPE_CHECKING:
    from .nfa_simulator import NFASimulator


class NFAStepByStepSimulator:
    """
    Interactive step-by-step NFA simulation.
    
    Allows stepping through an NFA simulation one symbol at a time,
    showing the evolution of configuration sets and epsilon closures.
    """
    
    def __init__(self, simulator: 'NFASimulator', input_string: str):
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