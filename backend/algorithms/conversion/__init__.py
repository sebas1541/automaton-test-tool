"""
Automaton conversion algorithms package.

This package provides classes and utilities for converting between different
types of automata, particularly NFA to DFA conversion using subset construction.

Classes:
    NFAToDFAConverter: Converts NFAs to equivalent DFAs using subset construction
    StateSet: Represents a set of NFA states as a single DFA state
    ConversionStep: Tracks steps in the conversion process

Usage:
    from backend.algorithms.conversion import NFAToDFAConverter, StateSet, ConversionStep
"""

from .nfa_to_dfa import NFAToDFAConverter
from .state_set import StateSet
from .conversion_step import ConversionStep

__all__ = [
    'NFAToDFAConverter',
    'StateSet',
    'ConversionStep'
]