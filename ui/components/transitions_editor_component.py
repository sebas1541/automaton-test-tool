"""
Transitions editor component for DFA Test Tool.
Handles adding, displaying, and deleting transitions.
"""

import streamlit as st
from ui.services.session_state_manager import SessionStateManager


class TransitionsEditorComponent:
    """Component for managing transitions in the automaton."""
    
    @staticmethod
    def render():
        """Render the transitions editor section."""
        st.subheader("🔄 Transiciones")
        
        current_states = SessionStateManager.get_current_states()
        current_alphabet = SessionStateManager.get_current_alphabet()
        
        if current_states and current_alphabet:
            # Add new transition form
            TransitionsEditorComponent._render_add_transition_form()
            
            # Display existing transitions
            TransitionsEditorComponent._render_existing_transitions()
    
    @staticmethod
    def _render_add_transition_form():
        """Render the form for adding new transitions."""
        current_transitions = SessionStateManager.get_current_transitions()
        current_states = SessionStateManager.get_current_states()
        current_alphabet = SessionStateManager.get_current_alphabet()
        
        with st.expander("Agregar Nueva Transición", expanded=len(current_transitions) == 0):
            col_from, col_symbol, col_to, col_add = st.columns([2, 2, 2, 1])
            
            with col_from:
                from_state = st.selectbox("Desde", sorted(current_states), key="from_state")
            with col_symbol:
                symbol = st.selectbox("Símbolo", current_alphabet, key="symbol")
            with col_to:
                to_state = st.selectbox("Hacia", sorted(current_states), key="to_state")
            with col_add:
                if st.button("➕ Agregar", key="add_transition"):
                    new_transition = {
                        'from_state': from_state,
                        'to_state': to_state,
                        'symbol': symbol
                    }
                    if new_transition not in current_transitions:
                        updated_transitions = current_transitions + [new_transition]
                        SessionStateManager.update_transitions(updated_transitions)
                        st.rerun()
    
    @staticmethod
    def _render_existing_transitions():
        """Render the list of existing transitions with delete functionality."""
        current_transitions = SessionStateManager.get_current_transitions()
        
        if current_transitions:
            st.write("**Transiciones Actuales:**")
            for i, transition in enumerate(current_transitions):
                col_transition, col_delete = st.columns([4, 1])
                with col_transition:
                    st.write(f"{transition['from_state']} → {transition['to_state']} : {transition['symbol']}")
                with col_delete:
                    if st.button("🗑️", key=f"delete_{i}", help="Eliminar transición"):
                        updated_transitions = current_transitions.copy()
                        updated_transitions.pop(i)
                        SessionStateManager.update_transitions(updated_transitions)
                        st.rerun()