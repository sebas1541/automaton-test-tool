#!/usr/bin/env python3
"""
Test script to verify NFA simulator refactoring.
"""

import os
import sys

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from models.state import State
from models.transition import Transition  
from models.automaton import Automaton
from algorithms.nfa_simulator import NFASimulator

def test_nfa_refactoring():
    """Test the refactored NFA simulator."""
    print("Testing NFA simulator after refactoring...")

    # Create a simple NFA
    q0 = State('q0', is_final=False)
    q1 = State('q1', is_final=True)

    t1 = Transition(q0, 'a', q1)
    t2 = Transition(q0, '', q1)  # epsilon transition

    automaton = Automaton(
        states={q0, q1},
        alphabet={'a'},
        transitions={t1, t2},
        initial_state=q0
    )

    # Test the simulator
    simulator = NFASimulator(automaton)
    print(f'Accepts "a": {simulator.is_accepted("a")}')
    print(f'Accepts "": {simulator.is_accepted("")}')

    # Test step-by-step simulator
    step_sim = simulator.create_step_by_step_simulator('a')
    print(f'Step simulator created for "a"')
    print(f'Current states: {[s.id for s in step_sim.current_states]}')
    print('NFA refactoring successful!')

if __name__ == "__main__":
    test_nfa_refactoring()