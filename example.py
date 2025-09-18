#!/usr/bin/env python3
"""
Example script demonstrating the Automaton Test Tool library.

This script creates sample DFA and NFA automata, runs simulations,
and demonstrates the NFA to DFA conversion algorithm.
"""

from backend.models import State, Transition, Automaton
from backend.algorithms import DFASimulator, NFASimulator, NFAToDFAConverter


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


def create_simple_nfa():
    """Create a simple NFA with epsilon transitions."""
    print("\n=== Creating Simple NFA (with epsilon transitions) ===")
    
    # Create states
    q0 = State("q0", (100, 100), is_final=False, label="Start")
    q1 = State("q1", (250, 100), is_final=False, label="Middle")
    q2 = State("q2", (400, 100), is_final=True, label="Accept")
    
    # Create transitions (including epsilon transitions)
    t1 = Transition(q0, q1, "a")      # Go to q1 on 'a'
    t2 = Transition(q0, q1, "")       # Epsilon transition to q1
    t3 = Transition(q1, q2, "b")      # Go to q2 on 'b'
    t4 = Transition(q1, q0, "a")      # Back to q0 on 'a'
    
    # Create automaton
    nfa = Automaton(
        states={q0, q1, q2},
        transitions={t1, t2, t3, t4},
        initial_state=q0,
        final_states={q2},
        alphabet={"a", "b"}
    )
    
    print(f"Created NFA: {nfa}")
    return nfa


def test_dfa_simulation(dfa):
    """Test DFA simulation with various strings."""
    print("\n=== Testing DFA Simulation ===")
    
    simulator = DFASimulator(dfa)
    test_strings = ["ab", "aab", "bab", "abb", "a", "b", ""]
    
    for test_string in test_strings:
        is_accepted = simulator.is_accepted(test_string)
        result = "ACCEPTED" if is_accepted else "REJECTED"
        print(f"String '{test_string}': {result}")


def test_nfa_simulation(nfa):
    """Test NFA simulation with various strings."""
    print("\n=== Testing NFA Simulation ===")
    
    simulator = NFASimulator(nfa)
    test_strings = ["b", "ab", "aab", "a", ""]
    
    for test_string in test_strings:
        is_accepted = simulator.is_accepted(test_string)
        result = "ACCEPTED" if is_accepted else "REJECTED"
        print(f"String '{test_string}': {result}")


def test_nfa_to_dfa_conversion(nfa):
    """Test NFA to DFA conversion."""
    print("\n=== Testing NFA to DFA Conversion ===")
    
    converter = NFAToDFAConverter()
    
    # Analyze the conversion
    analysis = converter.analyze_conversion(nfa)
    
    print("Conversion Analysis:")
    print(f"  NFA: {analysis['nfa_stats']['states']} states, {analysis['nfa_stats']['transitions']} transitions")
    print(f"  DFA: {analysis['dfa_stats']['states']} states, {analysis['dfa_stats']['transitions']} transitions")
    print(f"  State explosion ratio: {analysis['conversion_metrics']['state_explosion_ratio']:.2f}")
    
    # Get the converted DFA
    dfa, state_mapping = converter.convert_with_state_mapping(nfa)
    
    print("\nState Mapping:")
    for dfa_state_id, state_set in state_mapping.items():
        nfa_state_ids = [state.id for state in state_set.states]
        print(f"  DFA state {dfa_state_id} represents NFA states {nfa_state_ids}")
    
    return dfa


def test_equivalence(nfa, converted_dfa):
    """Test that NFA and converted DFA are equivalent."""
    print("\n=== Testing NFA-DFA Equivalence ===")
    
    nfa_sim = NFASimulator(nfa)
    dfa_sim = DFASimulator(converted_dfa)
    
    test_strings = ["", "a", "b", "ab", "ba", "aab", "abb", "aabb"]
    
    all_equivalent = True
    for test_string in test_strings:
        nfa_result = nfa_sim.is_accepted(test_string)
        dfa_result = dfa_sim.is_accepted(test_string)
        
        if nfa_result == dfa_result:
            status = "✓"
        else:
            status = "✗"
            all_equivalent = False
        
        print(f"  '{test_string}': NFA={nfa_result}, DFA={dfa_result} {status}")
    
    print(f"\nEquivalence test: {'PASSED' if all_equivalent else 'FAILED'}")


def main():
    """Main example execution."""
    print("🤖 Automaton Test Tool - Example Demonstration")
    print("=" * 50)
    
    # Create and test DFA
    dfa = create_simple_dfa()
    test_dfa_simulation(dfa)
    
    # Create and test NFA
    nfa = create_simple_nfa()
    test_nfa_simulation(nfa)
    
    # Convert NFA to DFA
    converted_dfa = test_nfa_to_dfa_conversion(nfa)
    
    # Test equivalence
    test_equivalence(nfa, converted_dfa)
    
    print("\n🎉 Example demonstration completed!")


if __name__ == "__main__":
    main()