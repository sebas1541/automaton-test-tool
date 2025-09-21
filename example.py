#!/usr/bin/env python3
"""
Example script demonstrating the DFA Test Tool library.

This script creates sample DFA automata, runs simulations,
and demonstrates step-by-step execution.
"""

from backend.models import State, Transition, Automaton
from backend.algorithms import DFASimulator, StepByStepSimulation


def create_simple_dfa():
    """Create a simple DFA that accepts strings ending with 'ab'."""
    print("=== Creating Simple DFA (accepts strings ending with 'ab') ===")
    
    # Create states
    q0 = State("q0", (100, 100), is_final=False, label="Start")
    q1 = State("q1", (250, 100), is_final=False, label="Got 'a'")
    q2 = State("q2", (400, 100), is_final=True, label="Got 'ab'")
    
    # Create transitions
    t1 = Transition(q0, q0, "b")  # Stay in q0 on 'b'
    t2 = Transition(q0, q1, "a")  # Go to q1 on 'a'
    t3 = Transition(q1, q1, "a")  # Stay in q1 on 'a'
    t4 = Transition(q1, q2, "b")  # Go to q2 on 'b' (accepting)
    t5 = Transition(q2, q1, "a")  # Go to q1 on 'a'
    t6 = Transition(q2, q0, "b")  # Go to q0 on 'b'
    
    # Create automaton
    dfa = Automaton(
        states={q0, q1, q2},
        transitions={t1, t2, t3, t4, t5, t6},
        initial_state=q0,
        final_states={q2},
        alphabet={"a", "b"}
    )
    
    print(f"Created DFA: {dfa}")
    return dfa


def create_binary_dfa():
    """Create a DFA that accepts binary strings with even number of 1s."""
    print("\n=== Creating Binary DFA (accepts even number of 1s) ===")
    
    # Create states
    even = State("even", (100, 100), is_final=True, label="Even 1s")
    odd = State("odd", (300, 100), is_final=False, label="Odd 1s")
    
    # Create transitions
    t1 = Transition(even, even, "0")  # Stay in even on '0'
    t2 = Transition(even, odd, "1")   # Go to odd on '1'
    t3 = Transition(odd, odd, "0")    # Stay in odd on '0'
    t4 = Transition(odd, even, "1")   # Go to even on '1'
    
    # Create automaton
    dfa = Automaton(
        states={even, odd},
        transitions={t1, t2, t3, t4},
        initial_state=even,
        final_states={even},
        alphabet={"0", "1"}
    )
    
    print(f"Created DFA: {dfa}")
    return dfa


def test_dfa_simulation(dfa, test_name=""):
    """Test DFA simulation with various strings."""
    print(f"\n=== Testing DFA Simulation{' - ' + test_name if test_name else ''} ===")
    
    simulator = DFASimulator(dfa)
    
    # Test strings based on DFA alphabet
    if "a" in dfa.alphabet:
        test_strings = ["ab", "aab", "bab", "abb", "a", "b", ""]
    else:
        test_strings = ["", "0", "1", "00", "01", "10", "11", "101", "110", "1001"]
    
    for test_string in test_strings:
        is_accepted = simulator.is_accepted(test_string)
        result = "ACCEPTED" if is_accepted else "REJECTED"
        print(f"String '{test_string}': {result}")


def test_step_by_step_simulation(dfa, test_string="ab"):
    """Test step-by-step DFA simulation."""
    print(f"\n=== Step-by-Step Simulation for '{test_string}' ===")
    
    simulator = DFASimulator(dfa)
    step_sim = StepByStepSimulation(simulator, test_string)
    
    print(f"Input string: '{test_string}'")
    print(f"Initial state: {dfa.initial_state.id}")
    print()
    
    step_num = 1
    while not step_sim.is_finished:
        print(f"Step {step_num}:")
        print(f"  Current state: {step_sim.current_state.id}")
        print(f"  Processed input: '{step_sim.processed_input}'")
        print(f"  Remaining input: '{step_sim.remaining_input}'")
        print()
        
        step_sim.step()
        step_num += 1
    
    # Final result
    print(f"Final state: {step_sim.current_state.id}")
    print(f"Final result: {'ACCEPTED' if step_sim.is_accepted else 'REJECTED'}")


def demonstrate_dfa_properties(dfa):
    """Demonstrate various DFA properties and methods."""
    print(f"\n=== DFA Properties Analysis ===")
    
    print(f"Number of states: {len(dfa.states)}")
    print(f"Number of transitions: {len(dfa.transitions)}")
    print(f"Alphabet: {sorted(dfa.alphabet)}")
    print(f"Initial state: {dfa.initial_state.id}")
    print(f"Final states: {[s.id for s in dfa.final_states]}")
    
    print(f"\nState details:")
    for state in sorted(dfa.states, key=lambda s: s.id):
        final_marker = " (FINAL)" if state.is_final else ""
        print(f"  {state.id}: {state.label}{final_marker}")
    
    print(f"\nTransition table:")
    for transition in sorted(dfa.transitions, key=lambda t: (t.from_state.id, t.symbol)):
        print(f"  {transition.from_state.id} --{transition.symbol}--> {transition.to_state.id}")


def main():
    """Main example execution."""
    print("🤖 DFA Test Tool - Example Demonstration")
    print("=" * 50)
    
    # Create and test first DFA (strings ending with 'ab')
    dfa1 = create_simple_dfa()
    demonstrate_dfa_properties(dfa1)
    test_dfa_simulation(dfa1, "Strings ending with 'ab'")
    test_step_by_step_simulation(dfa1, "aab")
    
    print("\n" + "=" * 50)
    
    # Create and test second DFA (even number of 1s)
    dfa2 = create_binary_dfa()
    demonstrate_dfa_properties(dfa2)
    test_dfa_simulation(dfa2, "Even number of 1s")
    test_step_by_step_simulation(dfa2, "1101")
    
    print("\n🎉 DFA demonstration completed!")
    print("\nKey features demonstrated:")
    print("  ✅ DFA creation with states and transitions")
    print("  ✅ String acceptance testing")
    print("  ✅ Step-by-step simulation")
    print("  ✅ DFA property analysis")


if __name__ == "__main__":
    main()