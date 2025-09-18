"""
Backend package for automaton test tool.

This package provides a complete finite automata library with:
- Core data structures (State, Transition, Automaton)
- Simulation algorithms (DFA, NFA)
- Conversion algorithms (NFA to DFA)
- API endpoints for web interface

Usage:
    from backend.models import State, Transition, Automaton
    from backend.algorithms import DFASimulator, NFASimulator, NFAToDFAConverter
"""

from .models import State, Transition, Automaton
from .algorithms import DFASimulator, NFASimulator, NFAToDFAConverter

__version__ = "1.0.0"
__author__ = "Automaton Test Tool"

__all__ = [
    'State', 'Transition', 'Automaton',
    'DFASimulator', 'NFASimulator', 'NFAToDFAConverter'
]