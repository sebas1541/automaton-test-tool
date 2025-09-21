"""
Test script to verify the quintuple display functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.algorithms.dfa.dfa_simulator import DFASimulator
from backend.algorithms.dfa.step_by_step_simulation import StepByStepSimulation
from backend.models.automaton import Automaton
from backend.models.state import State
from backend.models.transition import Transition

def create_test_dfa():
    """Create a simple DFA for testing the quintuple display."""
    # Create states
    q0 = State("q0", is_final=False)
    q1 = State("q1", is_final=False) 
    q2 = State("q2", is_final=True)
    
    states = {q0, q1, q2}
    
    # Create transitions
    transitions = {
        Transition(q0, q1, "0"),
        Transition(q0, q0, "1"),
        Transition(q1, q1, "0"),
        Transition(q1, q2, "1"),
        Transition(q2, q1, "0"),
        Transition(q2, q0, "1")
    }
    
    alphabet = {"0", "1"}
    final_states = {q2}
    
    return Automaton(states, transitions, q0, final_states, alphabet)

def test_simulation(dfa, test_string):
    """Test the step-by-step simulation."""
    print(f"\n🔍 Evaluando la cadena: \"{test_string}\"")
    
    simulator = DFASimulator(dfa)
    step_simulator = StepByStepSimulation(simulator, test_string)
    step_simulator.run_to_completion()
    steps = step_simulator.steps
    
    if len(steps) > 1:
        for i in range(1, len(steps)):
            step = steps[i]
            prev_state = steps[i-1].current_state.id
            curr_state = step.current_state.id
            symbol = step.symbol if step.symbol else 'ε'
            
            print(f"{i}. Desde el estado ({prev_state}) con el símbolo '{symbol}' se transita al estado ({curr_state}).")
    
    final_state = steps[-1].current_state.id
    is_accepted = step_simulator.is_accepted
    result_text = "ACEPTADA ✅" if is_accepted else "RECHAZADA ❌"
    
    print(f"Proceso finalizado. El estado final es ({final_state}).")
    print(f"Resultado: La cadena \"{test_string}\" es {result_text}")

if __name__ == "__main__":
    # Create test DFA
    dfa = create_test_dfa()
    
    print("📋 Quintuple of the Automaton")
    print(f"Estados (Q): {{q0, q1, q2}}")
    print(f"Alfabeto (Σ): {{0, 1}}")
    print(f"Estado Inicial (q₀): q0")
    print(f"Estados Finales (F): {{q2}}")
    print(f"Función de Transición (δ): Ver transiciones")
    
    # Test with different strings
    test_strings = ["01", "101", "001", "11"]
    
    for test_string in test_strings:
        test_simulation(dfa, test_string)
        print("-" * 50)