"""
DFA (Deterministic Finite Automaton) algorithms package.

This package provides classes and utilities for working with deterministic
finite automata, including simulation, step-by-step execution tracking,
and string generation.

Classes:
    DFASimulator: Simulates DFA execution on input strings
    SimulationStep: Represents a single step in DFA simulation
    StepByStepSimulation: Interactive step-by-step DFA simulation
    DFAStringGenerator: Generates strings accepted by a DFA

Usage:
    from core.algorithms.dfa import DFASimulator, SimulationStep, StepByStepSimulation, DFAStringGenerator
"""

from .dfa_simulator import DFASimulator
from .simulation_step import SimulationStep
from .step_by_step_simulation import StepByStepSimulation
from .string_generator import DFAStringGenerator

__all__ = [
    'DFASimulator',
    'SimulationStep', 
    'StepByStepSimulation',
    'DFAStringGenerator'
]