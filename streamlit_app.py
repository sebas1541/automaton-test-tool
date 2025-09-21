"""
DFA Test Tool - Streamlit Web App

A comprehensive tool for creating, visualizing, and testing Deterministic Finite Automata (DFA).
Built using Streamlit for the UI and the existing backend classes for logic.
Includes import/export functionality for XML and JSON formats.
"""

import streamlit as st
import graphviz
import pandas as pd
from typing import Dict, List, Set, Optional
import sys
import os
import json
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO
import base64

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

# Custom CSS for better styling and fixing sidebar issues
st.markdown("""
<style>
    /* Fix for sidebar visibility issues */
    .css-1d391kg {display: block !important;}
    .css-1cypcdb {display: block !important;}
    section[data-testid="stSidebar"] {display: block !important;}
    
    /* Hide unwanted Streamlit elements but keep sidebar functional */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stActionButton {display:none;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
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
    .import-export-section {
        background-color: #e0f2fe;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #0277bd;
    }
    @media (prefers-color-scheme: dark) {
        .automaton-info, .simulation-result {
            background-color: #262730 !important;
            color: #fff !important;
        }
        .import-export-section {
            background-color: #1a365d !important;
            color: #fff !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def create_automaton_graph(states: Set, transitions: List, initial_state: str, final_states: Set[str]) -> graphviz.Digraph:
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
    if initial_state:
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
    if not st.session_state.states:
        raise ValueError("No states defined")
    
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
        if (transition_dict['from_state'] in state_objects and 
            transition_dict['to_state'] in state_objects):
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
        alphabet=set(st.session_state.alphabet) if st.session_state.alphabet else set()
    )

def load_automaton_to_session_state(automaton: Automaton):
    """Load an Automaton object into the session state."""
    # Clear existing state first to avoid conflicts
    st.session_state.states = set()
    st.session_state.transitions = []
    st.session_state.final_states = set()
    
    # Load states
    st.session_state.states = {state.id for state in automaton.states}
    
    # Load alphabet
    st.session_state.alphabet = list(automaton.alphabet) if automaton.alphabet else ['0', '1']
    
    # Load transitions
    st.session_state.transitions = []
    for transition in automaton.transitions:
        st.session_state.transitions.append({
            'from_state': transition.from_state.id,
            'to_state': transition.to_state.id,
            'symbol': transition.symbol
        })
    
    # Load initial state
    st.session_state.initial_state = automaton.initial_state.id if automaton.initial_state else (list(st.session_state.states)[0] if st.session_state.states else None)
    
    # Load final states
    st.session_state.final_states = {state.id for state in automaton.final_states}
    
    # Force widget refresh by incrementing a counter
    if 'refresh_counter' not in st.session_state:
        st.session_state.refresh_counter = 0
    st.session_state.refresh_counter += 1
    
    # Set import flag to trigger UI update
    st.session_state.imported = True

def export_automaton_to_json() -> str:
    """Export current automaton to JSON format."""
    try:
        automaton = build_automaton_from_session_state()
        return json.dumps(automaton.to_dict(), indent=2)
    except Exception as e:
        return None

def export_automaton_to_xml() -> str:
    """Export current automaton to XML format."""
    try:
        automaton = build_automaton_from_session_state()
        data = automaton.to_dict()
        
        # Create XML structure
        root = ET.Element("automaton")
        
        # Add states
        states_elem = ET.SubElement(root, "states")
        for state_data in data['states']:
            state_elem = ET.SubElement(states_elem, "state")
            state_elem.set("id", state_data['id'])
            state_elem.set("is_final", str(state_data['is_final']).lower())
        
        # Add alphabet
        alphabet_elem = ET.SubElement(root, "alphabet")
        for symbol in data['alphabet']:
            symbol_elem = ET.SubElement(alphabet_elem, "symbol")
            symbol_elem.text = symbol
        
        # Add transitions
        transitions_elem = ET.SubElement(root, "transitions")
        for transition_data in data['transitions']:
            transition_elem = ET.SubElement(transitions_elem, "transition")
            transition_elem.set("from", transition_data['from_state_id'])
            transition_elem.set("to", transition_data['to_state_id'])
            transition_elem.set("symbol", transition_data['symbol'])
        
        # Add initial state
        if data['initial_state_id']:
            initial_elem = ET.SubElement(root, "initial_state")
            initial_elem.text = data['initial_state_id']
        
        # Add final states
        final_states_elem = ET.SubElement(root, "final_states")
        for final_state_id in data['final_state_ids']:
            final_elem = ET.SubElement(final_states_elem, "final_state")
            final_elem.text = final_state_id
        
        # Convert to string
        return ET.tostring(root, encoding='unicode')
    except Exception as e:
        return None

def import_automaton_from_json(json_content: str) -> bool:
    """Import automaton from JSON format."""
    try:
        # Clean up JSON content
        json_content = json_content.strip()
        data = json.loads(json_content)
        
        # Validate required fields
        if 'states' not in data or not data['states']:
            st.error("No valid states found in JSON")
            return False
        
        # Create and load automaton
        automaton = Automaton.from_dict(data)
        load_automaton_to_session_state(automaton)
        
        # Force update of session state
        st.session_state.imported = True
        
        return True
        
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Error importing from JSON: {str(e)}")
        return False

def import_automaton_from_xml(xml_content: str) -> bool:
    """Import automaton from XML format."""
    try:
        # Clean up XML content
        xml_content = xml_content.strip()
        root = ET.fromstring(xml_content)
        
        # Parse states
        states_data = []
        states_elem = root.find('states')
        if states_elem is not None:
            for state_elem in states_elem.findall('state'):
                state_id = state_elem.get('id')
                if state_id:
                    states_data.append({
                        'id': state_id,
                        'is_final': state_elem.get('is_final', 'false').lower() == 'true'
                    })
        
        if not states_data:
            st.error("No valid states found in XML")
            return False
        
        # Parse alphabet
        alphabet = []
        alphabet_elem = root.find('alphabet')
        if alphabet_elem is not None:
            for symbol_elem in alphabet_elem.findall('symbol'):
                if symbol_elem.text is not None and symbol_elem.text.strip():
                    alphabet.append(symbol_elem.text.strip())
        
        # If no alphabet specified, default to common symbols
        if not alphabet:
            alphabet = ['0', '1', 'a', 'b']
        
        # Parse transitions
        transitions_data = []
        transitions_elem = root.find('transitions')
        if transitions_elem is not None:
            for transition_elem in transitions_elem.findall('transition'):
                from_state = transition_elem.get('from')
                to_state = transition_elem.get('to')
                symbol = transition_elem.get('symbol')
                
                if from_state and to_state and symbol is not None:
                    transitions_data.append({
                        'from_state_id': from_state,
                        'to_state_id': to_state,
                        'symbol': symbol
                    })
        
        # Parse initial state
        initial_state_id = None
        initial_elem = root.find('initial_state')
        if initial_elem is not None and initial_elem.text:
            initial_state_id = initial_elem.text.strip()
        
        # If no initial state specified, use first state
        if not initial_state_id and states_data:
            initial_state_id = states_data[0]['id']
        
        # Parse final states
        final_state_ids = []
        final_states_elem = root.find('final_states')
        if final_states_elem is not None:
            for final_elem in final_states_elem.findall('final_state'):
                if final_elem.text and final_elem.text.strip():
                    final_state_ids.append(final_elem.text.strip())
        
        # Alternative: check states marked as final in states section
        for state_data in states_data:
            if state_data['is_final'] and state_data['id'] not in final_state_ids:
                final_state_ids.append(state_data['id'])
        
        # Create data dictionary
        data = {
            'states': states_data,
            'transitions': transitions_data,
            'initial_state_id': initial_state_id,
            'final_state_ids': final_state_ids,
            'alphabet': alphabet
        }
        
        # Create and load automaton
        automaton = Automaton.from_dict(data)
        load_automaton_to_session_state(automaton)
        
        # Force update of session state
        st.session_state.imported = True
        
        return True
        
    except ET.ParseError as e:
        st.error(f"XML parsing error: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Error importing from XML: {str(e)}")
        return False

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
    if 'imported' not in st.session_state:
        st.session_state.imported = False
    if 'last_upload_key' not in st.session_state:
        st.session_state.last_upload_key = None
    if 'refresh_counter' not in st.session_state:
        st.session_state.refresh_counter = 0

def create_sample_dfa():
    """Create a sample DFA that accepts strings ending with '01'."""
    # Clear existing state first
    st.session_state.states = set()
    st.session_state.transitions = []
    st.session_state.final_states = set()
    
    # Set new automaton
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
    
    # Force widget refresh
    if 'refresh_counter' not in st.session_state:
        st.session_state.refresh_counter = 0
    st.session_state.refresh_counter += 1

def clear_automaton():
    """Clear the current automaton."""
    st.session_state.states = {'q0'}
    st.session_state.alphabet = ['0', '1']
    st.session_state.transitions = []
    st.session_state.initial_state = 'q0'
    st.session_state.final_states = set()
    st.session_state.imported = False
    
    # Force widget refresh
    if 'refresh_counter' not in st.session_state:
        st.session_state.refresh_counter = 0
    st.session_state.refresh_counter += 1

def main():
    """Main Streamlit app."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 DFA Test Tool</h1>', unsafe_allow_html=True)
    st.markdown("**Interactive Deterministic Finite Automata Visualization and Simulation**")
    
    # Handle import success message
    if st.session_state.imported:
        st.success("✅ Automaton imported successfully!")
        st.session_state.imported = False
    
    # Sidebar for automaton configuration
    with st.sidebar:
        st.header("⚙️ DFA Configuration")
        
        # Import/Export Section
        with st.expander("📁 Import/Export", expanded=False):            
            # Import section
            st.subheader("📤 Import Automaton")
            
            uploaded_file = st.file_uploader(
                "Choose JSON or XML file", 
                type=["json", "xml"],
                key="file_upload"
            )
            
            # Process uploaded file
            if uploaded_file is not None:
                # Check if this is a new file upload
                current_upload_key = f"{uploaded_file.name}_{uploaded_file.size}"
                if current_upload_key != st.session_state.last_upload_key:
                    st.session_state.last_upload_key = current_upload_key
                    
                    try:
                        content = uploaded_file.read().decode('utf-8')
                        
                        # Auto-detect format and import
                        success = False
                        file_extension = uploaded_file.name.lower().split('.')[-1] if '.' in uploaded_file.name else ''
                        
                        # Clear any previous import flags
                        st.session_state.imported = False
                        
                        # Try based on file extension first, then content
                        if file_extension == 'json':
                            success = import_automaton_from_json(content)
                            if success:
                                st.success("✅ JSON automaton imported successfully!")
                        elif file_extension == 'xml':
                            success = import_automaton_from_xml(content)
                            if success:
                                st.success("✅ XML automaton imported successfully!")
                        else:
                            # Try to detect by content
                            content_trimmed = content.strip()
                            if content_trimmed.startswith('{'):
                                success = import_automaton_from_json(content)
                                if success:
                                    st.success("✅ JSON automaton imported successfully!")
                            elif content_trimmed.startswith('<'):
                                success = import_automaton_from_xml(content)
                                if success:
                                    st.success("✅ XML automaton imported successfully!")
                        
                        # If nothing worked, try both formats
                        if not success:
                            # Try JSON first
                            if not success:
                                success = import_automaton_from_json(content)
                                if success:
                                    st.success("✅ JSON automaton imported successfully!")
                            
                            # Try XML if JSON failed
                            if not success:
                                success = import_automaton_from_xml(content)
                                if success:
                                    st.success("✅ XML automaton imported successfully!")
                        
                        # If neither worked, show error
                        if not success:
                            st.error("❌ File format not recognized. Please upload a valid JSON or XML automaton file.")
                            
                    except Exception as e:
                        st.error(f"❌ Error reading file: {str(e)}")
            
            st.divider()
            
            # Export section
            st.subheader("📥 Export Automaton")
            
            col1, col2 = st.columns(2)
            
            with col1:
                json_content = export_automaton_to_json()
                if json_content:
                    st.download_button(
                        label="📥 Export JSON",
                        data=json_content,
                        file_name="automaton.json",
                        mime="application/json",
                        key="download_json"
                    )
                else:
                    st.button("📥 Export JSON", disabled=True, help="Cannot export - invalid automaton")
            
            with col2:
                xml_content = export_automaton_to_xml()
                if xml_content:
                    st.download_button(
                        label="📥 Export XML",
                        data=xml_content,
                        file_name="automaton.xml",
                        mime="application/xml",
                        key="download_xml"
                    )
                else:
                    st.button("📥 Export XML", disabled=True, help="Cannot export - invalid automaton")
        
        # Sample automata buttons
        if st.button("📘 Sample DFA", help="Create a DFA that accepts strings ending with '01'"):
            create_sample_dfa()
        
        if st.button("🗑️ Clear Automaton", help="Clear current automaton"):
            clear_automaton()
        
        st.divider()
        
        # Alphabet configuration
        st.subheader("Alphabet")
        alphabet_str = st.text_input("Symbols (comma-separated)", 
                                   value=",".join(st.session_state.alphabet),
                                   key=f"alphabet_input_{st.session_state.get('refresh_counter', 0)}")
        new_alphabet = [s.strip() for s in alphabet_str.split(",") if s.strip()]
        if new_alphabet != st.session_state.alphabet:
            st.session_state.alphabet = new_alphabet
        
        # States configuration
        st.subheader("States")
        states_str = st.text_input("States (comma-separated)", 
                                 value=",".join(sorted(st.session_state.states)),
                                 key=f"states_input_{st.session_state.get('refresh_counter', 0)}")
        new_states = set(s.strip() for s in states_str.split(",") if s.strip())
        if new_states != st.session_state.states:
            st.session_state.states = new_states
            # Update initial state if needed
            if st.session_state.initial_state not in st.session_state.states:
                if st.session_state.states:
                    st.session_state.initial_state = list(st.session_state.states)[0]
                else:
                    st.session_state.initial_state = None
            # Filter final states
            st.session_state.final_states = st.session_state.final_states.intersection(st.session_state.states)
        
        # Initial state
        if st.session_state.states:
            current_states = list(sorted(st.session_state.states))
            current_initial = st.session_state.initial_state
            
            if current_initial not in st.session_state.states and current_states:
                current_initial = current_states[0]
                st.session_state.initial_state = current_initial
            
            if current_initial in current_states:
                initial_index = current_states.index(current_initial)
            else:
                initial_index = 0
            
            initial_state = st.selectbox("Initial State", 
                                       current_states,
                                       index=initial_index,
                                       key=f"initial_state_select_{st.session_state.get('refresh_counter', 0)}")
            if initial_state != st.session_state.initial_state:
                st.session_state.initial_state = initial_state
        
        # Final states
        final_states = st.multiselect("Final States", 
                                    sorted(st.session_state.states),
                                    default=list(st.session_state.final_states),
                                    key=f"final_states_select_{st.session_state.get('refresh_counter', 0)}")
        if set(final_states) != st.session_state.final_states:
            st.session_state.final_states = set(final_states)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 DFA Visualization")
        
        if st.session_state.states:
            try:
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
            except Exception as e:
                st.error(f"Error displaying automaton: {str(e)}")
        
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
                        # Check if transition already exists
                        exists = any(
                            t['from_state'] == from_state and 
                            t['to_state'] == to_state and 
                            t['symbol'] == symbol 
                            for t in st.session_state.transitions
                        )
                        if not exists:
                            st.session_state.transitions.append(new_transition)
                        else:
                            st.warning("Transition already exists!")
            
            # Display existing transitions
            if st.session_state.transitions:
                st.write("**Current Transitions:**")
                transitions_to_remove = []
                for i, transition in enumerate(st.session_state.transitions):
                    col_transition, col_delete = st.columns([4, 1])
                    with col_transition:
                        st.write(f"{transition['from_state']} → {transition['to_state']} : {transition['symbol']}")
                    with col_delete:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete transition"):
                            transitions_to_remove.append(i)
                
                # Remove transitions (in reverse order to maintain indices)
                for i in reversed(transitions_to_remove):
                    st.session_state.transitions.pop(i)
                if transitions_to_remove:
                    st.rerun()
    
    with col2:
        st.header("🧪 Testing & Simulation")
        
        # Test string input
        test_string = st.text_input("Test String", placeholder="Enter string to test...")
        
        if st.button("🚀 Run Simulation", disabled=not st.session_state.states):
            if test_string is not None:  # Allow empty string
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
        if st.button("👣 Step-by-Step Simulation", disabled=not st.session_state.states):
            if test_string is not None:  # Allow empty string
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
        
        # Quick test section
        st.subheader("🧪 Quick Tests")
        st.write("Test common patterns:")
        
        quick_tests = ["", "0", "1", "01", "10", "001", "101", "0101", "1010"]
        
        for test in quick_tests:
            if st.button(f"Test: '{test}' {'' if test else '(empty)'}", key=f"quick_test_{test}_btn", disabled=not st.session_state.states):
                try:
                    automaton = build_automaton_from_session_state()
                    simulator = DFASimulator(automaton)
                    result = simulator.simulate(test)
                    result_emoji = "✅" if result[0] else "❌"
                    st.write(f"'{test}' → {result_emoji}")
                except Exception as e:
                    st.error(f"Quick test failed: {str(e)}")

if __name__ == "__main__":
    main()