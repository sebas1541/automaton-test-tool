"""
Sidebar component for DFA Test Tool.
Contains all sidebar functionality including configuration and import/export.
"""

import streamlit as st
from ui.services.session_state_manager import SessionStateManager
from ui.services.import_export_service import ImportExportService


class SidebarComponent:
    """Component for managing the sidebar interface."""
    
    @staticmethod
    def render():
        """Render the complete sidebar interface."""
        with st.sidebar:
            st.header("Configuración del AFD")
            
            # Sample automata buttons
            if st.button("📘 AFD de Ejemplo", help="Crear un AFD que acepta cadenas terminadas en '01'"):
                SessionStateManager.create_sample_dfa()
            st.divider()
            
            # Import/Export section
            SidebarComponent._render_import_export_section()
            st.divider()
            
            # Configuration section
            SidebarComponent._render_configuration_section()
    
    @staticmethod
    def _render_import_export_section():
        """Render the import/export section of the sidebar."""
        st.subheader("📁 Importar/Exportar")
        
        # Import section
        uploaded_file = st.file_uploader(
            "Importar Autómata", 
            type=['json', 'xml'],
            help="Sube un archivo JSON o XML que contenga un autómata",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            # Use session state to track if file was already processed
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            
            if 'last_imported_file' not in st.session_state:
                st.session_state.last_imported_file = None
            
            # Only process if it's a different file
            if st.session_state.last_imported_file != file_id:
                if ImportExportService.import_from_file(uploaded_file):
                    st.session_state.last_imported_file = file_id
                    st.success("✅ ¡Autómata importado exitosamente!")
                else:
                    st.session_state.last_imported_file = file_id
        
        # Export buttons
        col_export1, col_export2 = st.columns(2)
        with col_export1:
            if SessionStateManager.get_current_states():  # Only show if there are states to export
                json_content = ImportExportService.export_to_json()
                if json_content:
                    st.download_button(
                        label="📤 Exportar JSON",
                        data=json_content,
                        file_name="automaton.json",
                        mime="application/json",
                        key="export_json"
                    )
        
        with col_export2:
            if SessionStateManager.get_current_states():  # Only show if there are states to export
                xml_content = ImportExportService.export_to_xml()
                if xml_content:
                    st.download_button(
                        label="📤 Exportar XML",
                        data=xml_content,
                        file_name="automaton.xml",
                        mime="application/xml",
                        key="export_xml"
                    )
    
    @staticmethod
    def _render_configuration_section():
        """Render the configuration section of the sidebar."""
        # Alphabet configuration
        st.subheader("Alfabeto")
        alphabet_str = st.text_input(
            "Símbolos (separados por comas)", 
            value=",".join(SessionStateManager.get_current_alphabet())
        )
        new_alphabet = [s.strip() for s in alphabet_str.split(",") if s.strip()]
        SessionStateManager.update_alphabet(new_alphabet)
        
        # States configuration
        st.subheader("Estados")
        states_str = st.text_input(
            "Estados (separados por comas)", 
            value=",".join(sorted(SessionStateManager.get_current_states()))
        )
        new_states = set(s.strip() for s in states_str.split(",") if s.strip())
        SessionStateManager.update_states(new_states)
        
        # Initial state
        current_states = SessionStateManager.get_current_states()
        current_initial = SessionStateManager.get_initial_state()
        
        if current_states:
            initial_state = st.selectbox(
                "Estado Inicial", 
                sorted(current_states),
                index=0 if current_initial not in current_states 
                else list(sorted(current_states)).index(current_initial)
            )
            SessionStateManager.update_initial_state(initial_state)
        
        # Final states
        current_final_states = SessionStateManager.get_final_states()
        final_states = st.multiselect(
            "Estados Finales", 
            sorted(current_states),
            default=list(current_final_states)
        )
        SessionStateManager.update_final_states(set(final_states))