"""
Session state management service for DFA Test Tool.
Handles initialization and management of Streamlit session state.
"""

import streamlit as st
from typing import Set, List, Dict, Any


class SessionStateManager:
    """Manages the session state for the DFA application."""
    
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
    def get_current_states() -> Set[str]:
        """Get current states from session state."""
        return st.session_state.states
    
    @staticmethod
    def get_current_alphabet() -> List[str]:
        """Get current alphabet from session state."""
        return st.session_state.alphabet
    
    @staticmethod
    def get_current_transitions() -> List[Dict[str, str]]:
        """Get current transitions from session state."""
        return st.session_state.transitions
    
    @staticmethod
    def get_initial_state() -> str:
        """Get initial state from session state."""
        return st.session_state.initial_state
    
    @staticmethod
    def get_final_states() -> Set[str]:
        """Get final states from session state."""
        return st.session_state.final_states
    
    @staticmethod
    def update_states(states: Set[str]):
        """Update states in session state."""
        st.session_state.states = states
    
    @staticmethod
    def update_alphabet(alphabet: List[str]):
        """Update alphabet in session state."""
        st.session_state.alphabet = alphabet
    
    @staticmethod
    def update_transitions(transitions: List[Dict[str, str]]):
        """Update transitions in session state."""
        st.session_state.transitions = transitions
    
    @staticmethod
    def update_initial_state(initial_state: str):
        """Update initial state in session state."""
        st.session_state.initial_state = initial_state
    
    @staticmethod
    def update_final_states(final_states: Set[str]):
        """Update final states in session state."""
        st.session_state.final_states = final_states
    
    @staticmethod
    def clear_session_state():
        """Clear current session state completely and reinitialize."""
        st.session_state.states = set()
        st.session_state.alphabet = []
        st.session_state.transitions = []
        st.session_state.initial_state = None
        st.session_state.final_states = set()