"""
Algorithms package for automaton operations.

This package provides algorithms for working with finite automata:
- DFASimulator: Deterministic finite automaton simulation
- NFASimulator: Nondeterministic finite automaton simulation
- NFAToDFAConverter: NFA to DFA conversion using subset construction

Usage:
    from backend.algorithms import DFASimulator, NFASimulator, NFAToDFAConverter
"""

from .dfa_simulator import DFASimulator
from .simulation_step import SimulationStep
from .step_by_step_simulation import StepByStepSimulation
from .nfa_simulator import NFASimulator
from .nfa_configuration import NFAConfiguration
from .epsilon_closure_calculator import EpsilonClosureCalculator
from .nfa_step_by_step_simulator import NFAStepByStepSimulator
from .nfa_to_dfa import NFAToDFAConverter
from .state_set import StateSet
from .conversion_step import ConversionStep

__all__ = [
    'DFASimulator', 'SimulationStep', 'StepByStepSimulation',
    'NFASimulator', 'NFAConfiguration', 'EpsilonClosureCalculator', 'NFAStepByStepSimulator',
    'NFAToDFAConverter', 'StateSet', 'ConversionStep'
]