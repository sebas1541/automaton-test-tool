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
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from io import StringIO

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# =============================================================================
# IMPORTS PARA AUTÓMATAS FINITOS DETERMINISTAS (DFA)
# =============================================================================
from backend.algorithms.dfa.dfa_simulator import DFASimulator
from backend.algorithms.dfa.step_by_step_simulation import StepByStepSimulation
from backend.algorithms.dfa.string_generator import DFAStringGenerator
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

# Custom CSS for better styling and hiding unwanted menu items
st.markdown("""
<style>
    /* Hide Streamlit's default menu items */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stActionButton {display:none;}
    header {visibility: hidden;}
    
    /* Hide the hamburger menu completely */
    .css-1rs6os.edgvbvh3 {display: none;}
    .css-10trblm.e16nr0p30 {display: none;}
    
    /* Hide Print, Deploy, Record, Clear cache options */
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

def export_to_json() -> str:
    """Export current DFA to JSON format."""
    try:
        automaton = build_automaton_from_session_state()
        data = automaton.to_dict()
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error exporting to JSON: {str(e)}")
        return ""

def export_to_xml() -> str:
    """Export current DFA to XML format."""
    try:
        automaton = build_automaton_from_session_state()
        data = automaton.to_dict()
        
        # Create root element
        root = ET.Element("automaton")
        
        # Add alphabet
        alphabet_elem = ET.SubElement(root, "alphabet")
        for symbol in data['alphabet']:
            symbol_elem = ET.SubElement(alphabet_elem, "symbol")
            symbol_elem.text = symbol
        
        # Add states
        states_elem = ET.SubElement(root, "states")
        for state_data in data['states']:
            state_elem = ET.SubElement(states_elem, "state")
            state_elem.set("id", state_data['id'])
            state_elem.set("is_final", str(state_data['is_final']).lower())
        
        # Add initial state
        if data['initial_state_id']:
            initial_elem = ET.SubElement(root, "initial_state")
            initial_elem.text = data['initial_state_id']
        
        # Add final states
        final_states_elem = ET.SubElement(root, "final_states")
        for state_id in data['final_state_ids']:
            final_state_elem = ET.SubElement(final_states_elem, "final_state")
            final_state_elem.text = state_id
        
        # Add transitions
        transitions_elem = ET.SubElement(root, "transitions")
        for transition_data in data['transitions']:
            transition_elem = ET.SubElement(transitions_elem, "transition")
            transition_elem.set("from", transition_data['from_state_id'])
            transition_elem.set("to", transition_data['to_state_id'])
            transition_elem.set("symbol", transition_data['symbol'])
        
        # Convert to pretty printed string
        xml_str = ET.tostring(root, encoding='unicode')
        dom = xml.dom.minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ")
    except Exception as e:
        st.error(f"Error exporting to XML: {str(e)}")
        return ""

def import_from_json(json_content: str) -> bool:
    """Import DFA from JSON content."""
    try:
        data = json.loads(json_content)
        load_automaton_from_dict(data)
        return True
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON format: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Error importing JSON: {str(e)}")
        return False

def import_from_xml(xml_content: str) -> bool:
    """Import DFA from XML content."""
    try:
        root = ET.fromstring(xml_content)
        
        # Parse alphabet
        alphabet = []
        alphabet_elem = root.find('alphabet')
        if alphabet_elem is not None:
            for symbol_elem in alphabet_elem.findall('symbol'):
                if symbol_elem.text:
                    alphabet.append(symbol_elem.text)
        
        # Parse states
        states = []
        states_elem = root.find('states')
        if states_elem is not None:
            for state_elem in states_elem.findall('state'):
                state_id = state_elem.get('id', '')
                is_final = state_elem.get('is_final', 'false').lower() == 'true'
                states.append({'id': state_id, 'is_final': is_final})
        
        # Parse initial state
        initial_state_id = None
        initial_elem = root.find('initial_state')
        if initial_elem is not None and initial_elem.text:
            initial_state_id = initial_elem.text
        
        # Parse final states
        final_state_ids = []
        final_states_elem = root.find('final_states')
        if final_states_elem is not None:
            for final_state_elem in final_states_elem.findall('final_state'):
                if final_state_elem.text:
                    final_state_ids.append(final_state_elem.text)
        
        # Parse transitions
        transitions = []
        transitions_elem = root.find('transitions')
        if transitions_elem is not None:
            for transition_elem in transitions_elem.findall('transition'):
                from_state = transition_elem.get('from', '')
                to_state = transition_elem.get('to', '')
                symbol = transition_elem.get('symbol', '')
                transitions.append({
                    'from_state_id': from_state,
                    'to_state_id': to_state,
                    'symbol': symbol
                })
        
        # Create data dictionary
        data = {
            'states': states,
            'transitions': transitions,
            'initial_state_id': initial_state_id,
            'final_state_ids': final_state_ids,
            'alphabet': alphabet
        }
        
        load_automaton_from_dict(data)
        return True
    except ET.ParseError as e:
        st.error(f"Invalid XML format: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Error importing XML: {str(e)}")
        return False

def load_automaton_from_dict(data: dict):
    """Load automaton data into session state."""
    # Clear current session state completely and reinitialize
    st.session_state.states = set()
    st.session_state.alphabet = []
    st.session_state.transitions = []
    st.session_state.initial_state = None
    st.session_state.final_states = set()
    
    # Load alphabet
    if 'alphabet' in data and data['alphabet']:
        st.session_state.alphabet = list(data['alphabet'])
    
    # Load states
    if 'states' in data and data['states']:
        state_ids = set()
        final_state_ids = set()
        for state_data in data['states']:
            state_id = state_data['id']
            state_ids.add(state_id)
            if state_data.get('is_final', False):
                final_state_ids.add(state_id)
        st.session_state.states = state_ids
        st.session_state.final_states = final_state_ids
    
    # Load initial state
    if 'initial_state_id' in data and data['initial_state_id'] and data['initial_state_id'] in st.session_state.states:
        st.session_state.initial_state = data['initial_state_id']
    elif st.session_state.states:
        # Set first state as initial if none specified
        st.session_state.initial_state = sorted(list(st.session_state.states))[0]
    
    # Load transitions
    if 'transitions' in data and data['transitions']:
        transitions = []
        for transition_data in data['transitions']:
            # Validate that states exist
            from_state = transition_data['from_state_id']
            to_state = transition_data['to_state_id']
            if from_state in st.session_state.states and to_state in st.session_state.states:
                transitions.append({
                    'from_state': from_state,
                    'to_state': to_state,
                    'symbol': transition_data['symbol']
                })
        st.session_state.transitions = transitions

def import_automaton_file(uploaded_file) -> bool:
    """Import automaton from uploaded file (JSON or XML)."""
    if uploaded_file is None:
        return False
    
    try:
        # Read file content
        content = uploaded_file.getvalue()
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        
        # Try to detect file type and parse accordingly
        content = content.strip()
        
        # Try JSON first
        if content.startswith('{') and content.endswith('}'):
            return import_from_json(content)
        
        # Try XML
        elif content.startswith('<') and content.endswith('>'):
            return import_from_xml(content)
        
        else:
            st.error("File format not recognized. Please upload a valid JSON or XML file.")
            return False
    
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return False

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
        
        # Import/Export section
        st.subheader("📁 Import/Export")
        
        # Import section
        uploaded_file = st.file_uploader(
            "Import Automaton", 
            type=['json', 'xml'],
            help="Upload a JSON or XML file containing an automaton",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            # Use session state to track if file was already processed
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            
            if 'last_imported_file' not in st.session_state:
                st.session_state.last_imported_file = None
            
            # Only process if it's a different file
            if st.session_state.last_imported_file != file_id:
                if import_automaton_file(uploaded_file):
                    st.session_state.last_imported_file = file_id
                    st.success("✅ Automaton imported successfully!")
                    st.rerun()
                else:
                    st.session_state.last_imported_file = file_id
        
        # Export buttons
        col_export1, col_export2 = st.columns(2)
        with col_export1:
            if st.session_state.states:  # Only show if there are states to export
                json_content = export_to_json()
                if json_content:
                    st.download_button(
                        label="📤 Export JSON",
                        data=json_content,
                        file_name="automaton.json",
                        mime="application/json",
                        key="export_json"
                    )
        
        with col_export2:
            if st.session_state.states:  # Only show if there are states to export
                xml_content = export_to_xml()
                if xml_content:
                    st.download_button(
                        label="📤 Export XML",
                        data=xml_content,
                        file_name="automaton.xml",
                        mime="application/xml",
                        key="export_xml"
                    )
        
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
            
            # Automaton information - Quintuple format
            st.markdown(f"""
            <div class="automaton-info">
                <h4>📋 Quintuple of the Automaton</h4>
                <p><strong>Estados (Q):</strong> {{{', '.join(sorted(st.session_state.states))}}}</p>
                <p><strong>Alfabeto (Σ):</strong> {{{', '.join(st.session_state.alphabet)}}}</p>
                <p><strong>Estado Inicial (q₀):</strong> {st.session_state.initial_state}</p>
                <p><strong>Estados Finales (F):</strong> {{{', '.join(sorted(st.session_state.final_states)) if st.session_state.final_states else '∅'}}}</p>
                <p><strong>Función de Transición (δ):</strong> Ver tabla a continuación</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Transition table
            if st.session_state.transitions and st.session_state.states and st.session_state.alphabet:
                st.subheader("📊 Tabla de Transiciones")
                
                # Create transition table
                transition_dict = {}
                for transition in st.session_state.transitions:
                    key = (transition['from_state'], transition['symbol'])
                    transition_dict[key] = transition['to_state']
                
                # Create table data
                table_data = []
                for state in sorted(st.session_state.states):
                    row = {'Estado': state}
                    
                    # Mark initial and final states
                    if state == st.session_state.initial_state:
                        row['Estado'] += ' (q₀)'
                    if state in st.session_state.final_states:
                        row['Estado'] += ' (F)'
                    
                    # Add transitions for each symbol
                    for symbol in sorted(st.session_state.alphabet):
                        next_state = transition_dict.get((state, symbol), '-')
                        row[f'δ({symbol})'] = next_state
                    
                    table_data.append(row)
                
                # Display table
                import pandas as pd
                df = pd.DataFrame(table_data)
                st.dataframe(df, width='stretch', hide_index=True)
        
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
        
        # Create two tabs for better organization
        tab1, tab2 = st.tabs(["🚀 Simulation", "📝 Generate Strings"])
        
        with tab1:
            if st.button("🚀 Run Simulation", disabled=not test_string or not st.session_state.states):
                try:
                    # Build automaton from session state
                    automaton = build_automaton_from_session_state()
                    
                    # Always use DFA simulator
                    simulator = DFASimulator(automaton)
                    
                    # Run step-by-step simulation to get detailed path
                    step_simulator = StepByStepSimulation(simulator, test_string)
                    step_simulator.run_to_completion()
                    steps = step_simulator.steps
                    
                    # Display detailed evaluation process
                    st.subheader(f"🔍 Evaluando la cadena: \"{test_string}\"")
                    
                    if len(steps) > 1:  # More than just initial step
                        for i in range(1, len(steps)):  # Skip initial step
                            step = steps[i]
                            prev_state = steps[i-1].current_state.id if hasattr(steps[i-1].current_state, 'id') else str(steps[i-1].current_state)
                            curr_state = step.current_state.id if hasattr(step.current_state, 'id') else str(step.current_state)
                            symbol = step.symbol if step.symbol else 'ε'
                            
                            st.write(f"**{i}.** Desde el estado ({prev_state}) con el símbolo '{symbol}' se transita al estado ({curr_state}).")
                    
                    # Final result
                    final_state = steps[-1].current_state.id if hasattr(steps[-1].current_state, 'id') else str(steps[-1].current_state)
                    is_accepted = step_simulator.is_accepted
                    result_text = "ACEPTADA ✅" if is_accepted else "RECHAZADA ❌"
                    result_class = "accepted" if is_accepted else "rejected"
                    
                    st.write(f"**Proceso finalizado.** El estado final es ({final_state}).")
                    
                    st.markdown(f"""
                    <div class="simulation-result {result_class}">
                        <h4>🎯 Resultado Final</h4>
                        <p><strong>Resultado:</strong> La cadena "{test_string}" es {result_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Simulation failed: {str(e)}")
        
        with tab2:
            st.write("Genera automáticamente las primeras 10 cadenas aceptadas por el autómata:")
            
            if st.button("🎯 Generate Accepted Strings", disabled=not st.session_state.states):
                try:
                    # Build automaton from session state
                    automaton = build_automaton_from_session_state()
                    
                    # Generate strings
                    generator = DFAStringGenerator(automaton)
                    strings_by_length = generator.generate_strings_by_length(max_count=10, max_length=15)
                    
                    if not strings_by_length:
                        st.warning("No se encontraron cadenas aceptadas en los primeros 15 caracteres.")
                    else:
                        st.subheader("📋 Cadenas Aceptadas (ordenadas por longitud)")
                        
                        total_shown = 0
                        for length, strings in strings_by_length:
                            if total_shown >= 10:
                                break
                                
                            # Show strings for this length
                            remaining_slots = 10 - total_shown
                            strings_to_show = strings[:remaining_slots]
                            
                            if length == 0:
                                st.markdown(f"**Longitud {length}:** cadena vacía (ε)")
                            else:
                                strings_display = ", ".join(f'"{s}"' for s in strings_to_show)
                                st.markdown(f"**Longitud {length}:** {strings_display}")
                            
                            total_shown += len(strings_to_show)
                        
                        st.success(f"✅ Se encontraron {total_shown} cadenas aceptadas")
                        
                except Exception as e:
                    st.error(f"Error generating strings: {str(e)}")

if __name__ == "__main__":
    main()