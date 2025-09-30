"""
Algorithms package for automaton operations.

This package provides algorithms for working with Deterministic Finite Automata (DFA):

DFA (Deterministic Finite Automata):
- DFASimulator: Deterministic finite automaton simulation
- SimulationStep: Individual simulation step tracking
- StepByStepSimulation: Interactive step-by-step DFA simulation

Usage:
    # Import from domain package
    from core.algorithms.dfa import DFASimulator, SimulationStep, StepByStepSimulation
    
    # Or import from main package (convenience)
    from core.algorithms import DFASimulator
"""

# Import from DFA domain package for convenience
from .dfa import DFASimulator, SimulationStep, StepByStepSimulation

__all__ = [
    # DFA domain only
    'DFASimulator', 'SimulationStep', 'StepByStepSimulation'
]