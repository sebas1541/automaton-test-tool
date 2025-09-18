"""
DFA Simulator for deterministic finite automaton execution.

This module provides the DFASimulator class which simulates the execution
of deterministic finite automata on input strings. It implements the
standard DFA simulation algorithm with step-by-step execution tracking.
"""

from typing import List, Optional, Tuple
from ..models.automaton import Automaton
from ..models.state import State
from ..models.transition import Transition


class SimulationStep:
    """
    Represents a single step in DFA simulation.
    
    Tracks the current state, input position, and the symbol being processed
    during each step of the simulation.
    """
    
    def __init__(
        self, 
        current_state: State, 
        input_position: int, 
        symbol: Optional[str] = None,
        transition_used: Optional[Transition] = None
    ):
        """
        Initialize a simulation step.
        
        Args:
            current_state: The state the automaton is in at this step
            input_position: Current position in the input string
            symbol: The symbol being processed (None for initial step)
            transition_used: The transition taken to reach this step (None for initial)
        """
        self.current_state = current_state
        self.input_position = input_position
        self.symbol = symbol
        self.transition_used = transition_used
    
    def __str__(self) -> str:
        """Return string representation of the simulation step."""
        if self.symbol is None:
            return f"Initial: {self.current_state.id}"
        return f"Step {self.input_position}: '{self.symbol}' -> {self.current_state.id}"
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"SimulationStep(state={self.current_state.id}, "
                f"position={self.input_position}, symbol={self.symbol!r})")


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


class StepByStepSimulation:
    """
    Interactive step-by-step DFA simulation.
    
    Allows stepping through a DFA simulation one symbol at a time,
    useful for educational purposes and debugging.
    """
    
    def __init__(self, simulator: DFASimulator, input_string: str):
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