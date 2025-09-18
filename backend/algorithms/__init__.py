"""
Algorithms package for automaton operations.

This package provides algorithms for working with finite automata:
- DFASimulator: Deterministic finite automaton simulation
- NFASimulator: Nondeterministic finite automaton simulation
- NFAToDFAConverter: NFA to DFA conversion using subset construction

Usage:
    from backend.algorithms import DFASimulator, NFASimulator, NFAToDFAConverter
"""

from .dfa_simulator import DFASimulator, SimulationStep, StepByStepSimulation
from .nfa_simulator import NFASimulator, NFAConfiguration, EpsilonClosureCalculator, NFAStepByStepSimulator
from .nfa_to_dfa import NFAToDFAConverter, StateSet, ConversionStep

__all__ = [
    'DFASimulator', 'SimulationStep', 'StepByStepSimulation',
    'NFASimulator', 'NFAConfiguration', 'EpsilonClosureCalculator', 'NFAStepByStepSimulator',
    'NFAToDFAConverter', 'StateSet', 'ConversionStep'
]