"""
DFA Test Tool - Streamlit Web App

A comprehensive tool for creating, visualizing, and testing Deterministic Finite Automata (DFA).
Built using Streamlit for the UI and the existing backend classes for logic.
"""

import streamlit as st
import graphviz
import pandas as pd
from typing import Dict, List, Set, Optional
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# =============================================================================
# IMPORTS PARA AUTÓMATAS FINITOS DETERMINISTAS (DFA)
# =============================================================================
from backend.algorithms.dfa.dfa_simulator import DFASimulator
from backend.algorithms.dfa.step_by_step_simulation import StepByStepSimulation
from backend.models.automaton import Automaton
from backend.models.state import State
from backend.models.transition import Transition

# Configure Streamlit page
st.set_page_config(
    page_title="Automaton Test Tool",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .automaton-info, .simulation-result {
        background-color: #f1f5f9;
        color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        transition: background 0.2s, color 0.2s;
    }
    .accepted {
        background-color: #dcfce7;
        border-left: 4px solid #16a34a;
    }
    .rejected {
        background-color: #fef2f2;
        border-left: 4px solid #dc2626;
    }
    @media (prefers-color-scheme: dark) {
        .automaton-info, .simulation-result {
            background-color: #262730 !important;
            color: #fff !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def create_automaton_graph(states: Dict, transitions: List, initial_state: str, final_states: Set[str]) -> graphviz.Digraph:
    """Create a graphviz representation of the DFA."""
    dot = graphviz.Digraph(comment='Automaton', format='svg')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')
    
    # Add an invisible start node to show initial state
    dot.node('start', '', shape='none', width='0', height='0')
    
    # Add states
    for state in states:
        if state in final_states:
            dot.node(state, state, shape='doublecircle')
        else:
            dot.node(state, state)
    
    # Add initial state arrow
    dot.edge('start', initial_state)
    
    # Group transitions by (from_state, to_state) to combine symbols
    transition_groups = {}
    for transition in transitions:
        key = (transition['from_state'], transition['to_state'])
        if key not in transition_groups:
            transition_groups[key] = []
        transition_groups[key].append(transition['symbol'])
    
    # Add transitions
    for (from_state, to_state), symbols in transition_groups.items():
        label = ', '.join(sorted(symbols))
        dot.edge(from_state, to_state, label=label)
    
    return dot

def build_automaton_from_session_state() -> Automaton:
    """Build an Automaton object from the current session state."""
    # Create State objects
    states_set = set()
    state_objects = {}
    
    for state_id in st.session_state.states:
        is_final = state_id in st.session_state.final_states
        state_obj = State(state_id, is_final=is_final)
        states_set.add(state_obj)
        state_objects[state_id] = state_obj
    
    # Create Transition objects
    transitions_set = set()
    for transition_dict in st.session_state.transitions:
        from_state = state_objects[transition_dict['from_state']]
        to_state = state_objects[transition_dict['to_state']]
        symbol = transition_dict['symbol']
        
        transition_obj = Transition(from_state, to_state, symbol)
        transitions_set.add(transition_obj)
    
    # Get initial state object
    initial_state = state_objects.get(st.session_state.initial_state)
    
    # Get final states set
    final_states_set = {state_objects[state_id] for state_id in st.session_state.final_states if state_id in state_objects}
    
    # Create and return automaton
    return Automaton(
        states=states_set,
        transitions=transitions_set,
        initial_state=initial_state,
        final_states=final_states_set,
        alphabet=set(st.session_state.alphabet)
    )

def initialize_session_state():
    """Initialize session state variables for DFA only."""
    if 'states' not in st.session_state:
        st.session_state.states = {'q0'}
    if 'alphabet' not in st.session_state:
        st.session_state.alphabet = ['0', '1']
    if 'transitions' not in st.session_state:
        st.session_state.transitions = []
    if 'initial_state' not in st.session_state:
        st.session_state.initial_state = 'q0'
    if 'final_states' not in st.session_state:
        st.session_state.final_states = set()
    if 'current_automaton' not in st.session_state:
        st.session_state.current_automaton = None

def create_sample_dfa():
    """Create a sample DFA that accepts strings ending with '01'."""
    st.session_state.states = {'q0', 'q1', 'q2'}
    st.session_state.alphabet = ['0', '1']
    st.session_state.transitions = [
        {'from_state': 'q0', 'to_state': 'q1', 'symbol': '0'},
        {'from_state': 'q0', 'to_state': 'q0', 'symbol': '1'},
        {'from_state': 'q1', 'to_state': 'q1', 'symbol': '0'},
        {'from_state': 'q1', 'to_state': 'q2', 'symbol': '1'},
        {'from_state': 'q2', 'to_state': 'q1', 'symbol': '0'},
        {'from_state': 'q2', 'to_state': 'q0', 'symbol': '1'}
    ]
    st.session_state.initial_state = 'q0'
    st.session_state.final_states = {'q2'}

def main():
    """Main Streamlit app."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 DFA Test Tool</h1>', unsafe_allow_html=True)
    st.markdown("**Interactive Deterministic Finite Automata Visualization and Simulation**")
    
    # Sidebar for automaton configuration
    with st.sidebar:
        st.header("⚙️ DFA Configuration")
        
        # Sample automata buttons
        if st.button("📘 Sample DFA", help="Create a DFA that accepts strings ending with '01'"):
            create_sample_dfa()
            st.rerun()
        st.divider()
        
        # Alphabet configuration
        st.subheader("Alphabet")
        alphabet_str = st.text_input("Symbols (comma-separated)", 
                                   value=",".join(st.session_state.alphabet))
        st.session_state.alphabet = [s.strip() for s in alphabet_str.split(",") if s.strip()]
        
        # States configuration
        st.subheader("States")
        states_str = st.text_input("States (comma-separated)", 
                                 value=",".join(sorted(st.session_state.states)))
        st.session_state.states = set(s.strip() for s in states_str.split(",") if s.strip())
        
        # Initial state
        if st.session_state.states:
            initial_state = st.selectbox("Initial State", 
                                       sorted(st.session_state.states),
                                       index=0 if st.session_state.initial_state not in st.session_state.states 
                                       else list(sorted(st.session_state.states)).index(st.session_state.initial_state))
            st.session_state.initial_state = initial_state
        
        # Final states
        final_states = st.multiselect("Final States", 
                                    sorted(st.session_state.states),
                                    default=list(st.session_state.final_states))
        st.session_state.final_states = set(final_states)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 DFA Visualization")
        
        if st.session_state.states:
            # Create and display the automaton graph
            graph = create_automaton_graph(
                st.session_state.states,
                st.session_state.transitions,
                st.session_state.initial_state,
                st.session_state.final_states
            )
            
            st.graphviz_chart(graph.source)
            
            # Automaton information
            st.markdown(f"""
            <div class="automaton-info">
                <h4>📋 DFA Information</h4>
                <p><strong>States:</strong> {len(st.session_state.states)} ({', '.join(sorted(st.session_state.states))})</p>
                <p><strong>Alphabet:</strong> {{{', '.join(st.session_state.alphabet)}}}</p>
                <p><strong>Initial State:</strong> {st.session_state.initial_state}</p>
                <p><strong>Final States:</strong> {{{', '.join(sorted(st.session_state.final_states))}}}</p>
                <p><strong>Transitions:</strong> {len(st.session_state.transitions)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Transitions editor
        st.subheader("🔄 Transitions")
        
        if st.session_state.states and st.session_state.alphabet:
            with st.expander("Add New Transition", expanded=len(st.session_state.transitions) == 0):
                col_from, col_symbol, col_to, col_add = st.columns([2, 2, 2, 1])
                
                with col_from:
                    from_state = st.selectbox("From", sorted(st.session_state.states), key="from_state")
                with col_symbol:
                    symbol = st.selectbox("Symbol", st.session_state.alphabet, key="symbol")
                with col_to:
                    to_state = st.selectbox("To", sorted(st.session_state.states), key="to_state")
                with col_add:
                    if st.button("➕ Add", key="add_transition"):
                        new_transition = {
                            'from_state': from_state,
                            'to_state': to_state,
                            'symbol': symbol
                        }
                        if new_transition not in st.session_state.transitions:
                            st.session_state.transitions.append(new_transition)
                            st.rerun()
            
            # Display existing transitions
            if st.session_state.transitions:
                st.write("**Current Transitions:**")
                for i, transition in enumerate(st.session_state.transitions):
                    col_transition, col_delete = st.columns([4, 1])
                    with col_transition:
                        st.write(f"{transition['from_state']} → {transition['to_state']} : {transition['symbol']}")
                    with col_delete:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete transition"):
                            st.session_state.transitions.pop(i)
                            st.rerun()
    
    with col2:
        st.header("🧪 Testing & Simulation")
        
        # Test string input
        test_string = st.text_input("Test String", placeholder="Enter string to test...")
        
        if st.button("🚀 Run Simulation", disabled=not test_string or not st.session_state.states):
            try:
                # Build automaton from session state
                automaton = build_automaton_from_session_state()
                
                # Always use DFA simulator
                simulator = DFASimulator(automaton)
                result = simulator.simulate(test_string)
                
                # Display result
                result_class = "accepted" if result[0] else "rejected"
                result_text = "ACCEPTED ✅" if result[0] else "REJECTED ❌"
                
                st.markdown(f"""
                <div class="simulation-result {result_class}">
                    <h4>🎯 Simulation Result</h4>
                    <p><strong>Input:</strong> "{test_string}"</p>
                    <p><strong>Result:</strong> {result_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Simulation failed: {str(e)}")
        
        # Step-by-step simulation
        if st.button("👣 Step-by-Step Simulation", disabled=not test_string or not st.session_state.states):
            try:
                # Build automaton from session state
                automaton = build_automaton_from_session_state()
                
                # Always use DFA step-by-step simulation
                simulator = DFASimulator(automaton)
                step_simulator = StepByStepSimulation(simulator, test_string)
                step_simulator.run_to_completion()
                steps = step_simulator.steps
                
                # Display steps
                st.subheader("📝 Execution Steps")
                for i, step in enumerate(steps):
                    with st.expander(f"Step {i + 1}: {step.current_state} → {step.input_symbol if step.input_symbol else 'ε'}"):
                        st.write(f"**Current State:** {step.current_state}")
                        st.write(f"**Input Symbol:** {step.input_symbol if step.input_symbol else 'ε'}")
                        st.write(f"**Remaining Input:** {step.remaining_input}")
                        
            except Exception as e:
                st.error(f"Step-by-step simulation failed: {str(e)}")

if __name__ == "__main__":
    main()