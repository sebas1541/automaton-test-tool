"""
Backend package for DFA test tool.

This package provides a complete Deterministic Finite Automata (DFA) library with:
- Core data structures (State, Transition, Automaton)
- DFA simulation algorithms
- API endpoints for web interface

Usage:
    from backend.models import State, Transition, Automaton
    from backend.algorithms import DFASimulator
"""

from .models import State, Transition, Automaton
from .algorithms import DFASimulator

__version__ = "1.0.0"
__author__ = "DFA Test Tool"

__all__ = [
    'State', 'Transition', 'Automaton',
    'DFASimulator'
]