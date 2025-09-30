"""
Models package for automaton data structures.

This package provides the core data structures for representing finite automata:
- State: Individual automaton states
- Transition: Transitions between states
- Automaton: Complete automaton representation

Usage:
    from core.models import State, Transition, Automaton
"""

from .state import State
from .transition import Transition
from .automaton import Automaton

__all__ = ['State', 'Transition', 'Automaton']