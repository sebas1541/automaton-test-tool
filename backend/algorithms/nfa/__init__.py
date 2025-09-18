"""
NFA (Nondeterministic Finite Automaton) algorithms package.

This package provides classes and utilities for working with nondeterministic
finite automata, including simulation, epsilon closure computation, and 
step-by-step execution tracking.

Classes:
    NFASimulator: Simulates NFA execution on input strings
    NFAConfiguration: Represents a configuration during NFA simulation
    EpsilonClosureCalculator: Utility for computing epsilon closures
    NFAStepByStepSimulator: Interactive step-by-step NFA simulation

Usage:
    from backend.algorithms.nfa import NFASimulator, NFAConfiguration, EpsilonClosureCalculator, NFAStepByStepSimulator
"""

from .nfa_simulator import NFASimulator
from .nfa_configuration import NFAConfiguration
from .epsilon_closure_calculator import EpsilonClosureCalculator
from .nfa_step_by_step_simulator import NFAStepByStepSimulator

__all__ = [
    'NFASimulator',
    'NFAConfiguration',
    'EpsilonClosureCalculator',
    'NFAStepByStepSimulator'
]