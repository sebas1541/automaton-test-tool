"""
DFA (Deterministic Finite Automaton) algorithms package.

This package provides classes and utilities for working with deterministic
finite automata, including simulation and step-by-step execution tracking.

Classes:
    DFASimulator: Simulates DFA execution on input strings
    SimulationStep: Represents a single step in DFA simulation
    StepByStepSimulation: Interactive step-by-step DFA simulation

Usage:
    from backend.algorithms.dfa import DFASimulator, SimulationStep, StepByStepSimulation
"""

from .dfa_simulator import DFASimulator
from .simulation_step import SimulationStep
from .step_by_step_simulation import StepByStepSimulation

__all__ = [
    'DFASimulator',
    'SimulationStep', 
    'StepByStepSimulation'
]