"""
Algorithms package for automaton operations.

This package provides algorithms for working with finite automata organized
by domain:

DFA (Deterministic Finite Automata):
- DFASimulator: Deterministic finite automaton simulation
- SimulationStep: Individual simulation step tracking
- StepByStepSimulation: Interactive step-by-step DFA simulation

NFA (Nondeterministic Finite Automata):
- NFASimulator: Nondeterministic finite automaton simulation
- NFAConfiguration: NFA simulation configuration tracking
- EpsilonClosureCalculator: Epsilon closure computation utility
- NFAStepByStepSimulator: Interactive step-by-step NFA simulation

Conversion:
- NFAToDFAConverter: NFA to DFA conversion using subset construction
- StateSet: Set of NFA states representation for DFA construction
- ConversionStep: Conversion process step tracking

Usage:
    # Import by domain
    from backend.algorithms.dfa import DFASimulator, SimulationStep, StepByStepSimulation
    from backend.algorithms.nfa import NFASimulator, NFAConfiguration, EpsilonClosureCalculator, NFAStepByStepSimulator
    from backend.algorithms.conversion import NFAToDFAConverter, StateSet, ConversionStep
    
    # Or import from main package (convenience)
    from backend.algorithms import DFASimulator, NFASimulator, NFAToDFAConverter
"""

# Import from domain packages for convenience
from .dfa import DFASimulator, SimulationStep, StepByStepSimulation
from .nfa import NFASimulator, NFAConfiguration, EpsilonClosureCalculator, NFAStepByStepSimulator
from .conversion import NFAToDFAConverter, StateSet, ConversionStep

__all__ = [
    # DFA domain
    'DFASimulator', 'SimulationStep', 'StepByStepSimulation',
    # NFA domain
    'NFASimulator', 'NFAConfiguration', 'EpsilonClosureCalculator', 'NFAStepByStepSimulator',
    # Conversion domain
    'NFAToDFAConverter', 'StateSet', 'ConversionStep'
]