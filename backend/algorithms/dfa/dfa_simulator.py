"""
DFA Simulator for deterministic finite automaton execution.

This module provides the DFASimulator class which simulates the execution
of deterministic finite automata on input strings. It implements the
standard DFA simulation algorithm with step-by-step execution tracking.
"""

from typing import List, Optional, Tuple
from ...models.automaton import Automaton
from ...models.state import State
from ...models.transition import Transition
from .simulation_step import SimulationStep
from .step_by_step_simulation import StepByStepSimulation

class DFASimulator:
    """
    Simulates execution of deterministic finite automata.
    
    This simulator processes input strings step-by-step through a DFA,
    tracking the execution path and determining acceptance. It validates
    that the automaton is deterministic before simulation.
    """
    
    def __init__(self, automaton: Automaton):
        """
        Initialize the DFA simulator.
        
        Args:
            automaton: The automaton to simulate
            
        Raises:
            ValueError: If the automaton is not deterministic or has no initial state
        """
        if not automaton.is_deterministic():
            raise ValueError("Automaton must be deterministic for DFA simulation")
        
        if automaton.initial_state is None:
            raise ValueError("Automaton must have an initial state")
        
        self._automaton = automaton
    
    @property
    def automaton(self) -> Automaton:
        """Get the automaton being simulated."""
        return self._automaton
    
    def simulate(self, input_string: str) -> Tuple[bool, List[SimulationStep]]:
        """
        Simulate the DFA on an input string.
        
        Args:
            input_string: The string to process
            
        Returns:
            Tuple of (is_accepted, simulation_steps)
            - is_accepted: True if the string is accepted, False otherwise
            - simulation_steps: List of steps taken during simulation
            
        Raises:
            ValueError: If input contains symbols not in the alphabet
        """
        # Validate input string
        self._validate_input(input_string)
        
        # Initialize simulation
        current_state = self._automaton.initial_state
        steps = [SimulationStep(current_state, 0)]
        
        # Process each symbol in the input
        for i, symbol in enumerate(input_string):
            # Find the transition for this symbol from current state
            transition = self._find_transition(current_state, symbol)
            
            if transition is None:
                # No transition found - string is rejected
                steps.append(SimulationStep(current_state, i + 1, symbol, None))
                return False, steps
            
            # Take the transition
            current_state = transition.to_state
            steps.append(SimulationStep(current_state, i + 1, symbol, transition))
        
        # Check if we ended in a final state
        is_accepted = current_state in self._automaton.final_states
        return is_accepted, steps
    
    def is_accepted(self, input_string: str) -> bool:
        """
        Check if an input string is accepted by the DFA.
        
        Args:
            input_string: The string to test
            
        Returns:
            True if the string is accepted, False otherwise
        """
        accepted, _ = self.simulate(input_string)
        return accepted
    
    def simulate_step_by_step(self, input_string: str) -> 'StepByStepSimulation':
        """
        Create a step-by-step simulation for interactive execution.
        
        Args:
            input_string: The string to simulate
            
        Returns:
            StepByStepSimulation object for interactive stepping
        """
        return StepByStepSimulation(self, input_string)
    
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
    
    def _find_transition(self, state: State, symbol: str) -> Optional[Transition]:
        """
        Find the transition from a state on a given symbol.
        
        Args:
            state: The source state
            symbol: The input symbol
            
        Returns:
            The transition if found, None otherwise
        """
        transitions = self._automaton.get_transitions_from_state(state)
        for transition in transitions:
            if transition.matches_symbol(symbol):
                return transition
        return None