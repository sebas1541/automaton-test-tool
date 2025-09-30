"""
DFA Test Tool - Streamlit Web App

A comprehensive tool for creating, visualizing, and testing Deterministic Finite Automata (DFA).
Built using Streamlit for the UI and modular components for clean architecture.

This is the main entry point that orchestrates all components following SOLID principles.
"""

import streamlit as st
import sys
import os

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(__file__))

# Import UI components and services
from ui.styles.app_styles import apply_custom_styles
from ui.services.session_state_manager import SessionStateManager
from ui.components.sidebar_component import SidebarComponent
from ui.components.visualization_component import VisualizationComponent
from ui.components.transitions_editor_component import TransitionsEditorComponent
from ui.components.simulation_component import SimulationComponent


def configure_streamlit():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Herramienta de Pruebas AFD",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def render_header():
    """Render the main application header."""
    st.markdown('<h1 class="main-header">Herramienta de Pruebas AFD</h1>', unsafe_allow_html=True)
    st.markdown("**Visualización y Simulación Interactiva de Autómatas Finitos Deterministas**")


def render_main_content():
    """Render the main content area with visualization and transitions."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Render visualization and transitions editor
        VisualizationComponent.render()
        TransitionsEditorComponent.render()
    
    with col2:
        # Render simulation component
        SimulationComponent.render()


def main():
    """Main application entry point."""
    # Configure Streamlit
    configure_streamlit()
    
    # Apply custom styles
    apply_custom_styles()
    
    # Initialize session state
    SessionStateManager.initialize_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar
    SidebarComponent.render()
    
    # Render main content
    render_main_content()


if __name__ == "__main__":
    main()