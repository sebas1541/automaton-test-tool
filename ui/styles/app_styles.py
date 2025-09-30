"""
App styles module for the DFA Test Tool.
Contains all CSS styling definitions for the Streamlit application.
"""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
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