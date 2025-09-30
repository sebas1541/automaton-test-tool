"""
Visualization component for DFA Test Tool.
Handles the main visualization panel with automaton graph and information.
"""

import streamlit as st
import pandas as pd
from ui.services.session_state_manager import SessionStateManager
from ui.utils.visualization_utils import VisualizationUtils


class VisualizationComponent:
    """Component for visualizing automata and their properties."""
    
    @staticmethod
    def render():
        """Render the complete visualization section."""
        st.header("📊 Visualización del AFD")
        
        current_states = SessionStateManager.get_current_states()
        
        if current_states:
            # Create and display the automaton graph
            VisualizationComponent._render_automaton_graph()
            
            # Display automaton information
            VisualizationComponent._render_automaton_info()
            
            # Display transition table
            VisualizationComponent._render_transition_table()
    
    @staticmethod
    def _render_automaton_graph():
        """Render the graphical representation of the automaton."""
        graph = VisualizationUtils.create_automaton_graph(
            SessionStateManager.get_current_states(),
            SessionStateManager.get_current_transitions(),
            SessionStateManager.get_initial_state(),
            SessionStateManager.get_final_states()
        )
        
        st.graphviz_chart(graph.source)
    
    @staticmethod
    def _render_automaton_info():
        """Render the automaton information in quintuple format."""
        current_states = SessionStateManager.get_current_states()
        current_alphabet = SessionStateManager.get_current_alphabet()
        initial_state = SessionStateManager.get_initial_state()
        final_states = SessionStateManager.get_final_states()
        
        st.markdown(f"""
        <div class="automaton-info">
            <h4>📋 Quintupla del Autómata</h4>
            <p><strong>Estados (Q):</strong> {{{', '.join(sorted(current_states))}}}</p>
            <p><strong>Alfabeto (Σ):</strong> {{{', '.join(current_alphabet)}}}</p>
            <p><strong>Estado Inicial (q₀):</strong> {initial_state}</p>
            <p><strong>Estados Finales (F):</strong> {{{', '.join(sorted(final_states)) if final_states else '∅'}}}</p>
            <p><strong>Función de Transición (δ):</strong> Ver tabla a continuación</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_transition_table():
        """Render the transition table."""
        current_transitions = SessionStateManager.get_current_transitions()
        current_states = SessionStateManager.get_current_states()
        current_alphabet = SessionStateManager.get_current_alphabet()
        
        if current_transitions and current_states and current_alphabet:
            st.subheader("📊 Tabla de Transiciones")
            
            # Create transition table
            transition_dict = {}
            for transition in current_transitions:
                key = (transition['from_state'], transition['symbol'])
                transition_dict[key] = transition['to_state']
            
            # Create table data
            table_data = []
            initial_state = SessionStateManager.get_initial_state()
            final_states = SessionStateManager.get_final_states()
            
            for state in sorted(current_states):
                row = {'Estado': state}
                
                # Mark initial and final states
                if state == initial_state:
                    row['Estado'] += ' (q₀)'
                if state in final_states:
                    row['Estado'] += ' (F)'
                
                # Add transitions for each symbol
                for symbol in sorted(current_alphabet):
                    next_state = transition_dict.get((state, symbol), '-')
                    row[f'δ({symbol})'] = next_state
                
                table_data.append(row)
            
            # Display table
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)