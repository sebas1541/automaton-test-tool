"""
StepByStepSimulation class for interactive DFA execution.

This module provides the StepByStepSimulation class which allows stepping
through a DFA simulation one symbol at a time, useful for educational
purposes and debugging.
"""

from typing import List, TYPE_CHECKING
from ...models.state import State
from .simulation_step import SimulationStep

if TYPE_CHECKING:
    from .dfa_simulator import DFASimulator


class StepByStepSimulation:
    """
    Interactive step-by-step DFA simulation.
    
    Allows stepping through a DFA simulation one symbol at a time,
    useful for educational purposes and debugging.
    """
    
    def __init__(self, simulator: 'DFASimulator', input_string: str):
        """
        Initialize step-by-step simulation.
        
        Args:
            simulator: The DFA simulator to use
            input_string: The string to simulate
        """
        self._simulator = simulator
        self._input_string = input_string
        self._current_position = 0
        self._current_state = simulator.automaton.initial_state
        self._steps = [SimulationStep(self._current_state, 0)]
        self._finished = False
        self._accepted = False
        
        # Validate input
        self._simulator._validate_input(input_string)
    
    @property
    def current_state(self) -> State:
        """Get the current state in the simulation."""
        return self._current_state
    
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
        return self._accepted
    
    @property
    def steps(self) -> List[SimulationStep]:
        """Get all simulation steps taken so far."""
        return self._steps.copy()
    
    def step(self) -> bool:
        """
        Execute one step of the simulation.
        
        Returns:
            True if the step was successful, False if simulation is finished or stuck
        """
        if self._finished:
            return False
        
        if self._current_position >= len(self._input_string):
            # End of input reached
            self._finished = True
            self._accepted = self._current_state in self._simulator.automaton.final_states
            return False
        
        # Get the next symbol
        symbol = self._input_string[self._current_position]
        
        # Find transition
        transition = self._simulator._find_transition(self._current_state, symbol)
        
        if transition is None:
            # No transition found - simulation stuck
            self._steps.append(SimulationStep(
                self._current_state, 
                self._current_position + 1, 
                symbol, 
                None
            ))
            self._finished = True
            self._accepted = False
            return False
        
        # Take the transition
        self._current_state = transition.to_state
        self._current_position += 1
        self._steps.append(SimulationStep(
            self._current_state, 
            self._current_position, 
            symbol, 
            transition
        ))
        
        # Check if we've processed all input
        if self._current_position >= len(self._input_string):
            self._finished = True
            self._accepted = self._current_state in self._simulator.automaton.final_states
        
        return True
    
    def run_to_completion(self) -> bool:
        """
        Run the simulation to completion.
        
        Returns:
            True if the string is accepted, False otherwise
        """
        while not self._finished:
            self.step()
        return self._accepted
    
    def reset(self) -> None:
        """Reset the simulation to the beginning."""
        self._current_position = 0
        self._current_state = self._simulator.automaton.initial_state
        self._steps = [SimulationStep(self._current_state, 0)]
        self._finished = False
        self._accepted = False