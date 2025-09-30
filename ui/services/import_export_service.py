"""
Import/Export service for DFA Test Tool.
Handles JSON and XML import/export functionality.
"""

import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import streamlit as st
from typing import Optional

from ui.services.automaton_builder import AutomatonBuilder


class ImportExportService:
    """Service for importing and exporting automaton data."""
    
    @staticmethod
    def export_to_json() -> str:
        """Export current DFA to JSON format."""
        try:
            automaton = AutomatonBuilder.build_from_session_state()
            data = automaton.to_dict()
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Error exportando a JSON: {str(e)}")
            return ""
    
    @staticmethod
    def export_to_xml() -> str:
        """Export current DFA to XML format."""
        try:
            automaton = AutomatonBuilder.build_from_session_state()
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
            st.error(f"Error exportando a XML: {str(e)}")
            return ""
    
    @staticmethod
    def import_from_json(json_content: str) -> bool:
        """Import DFA from JSON content."""
        try:
            data = json.loads(json_content)
            AutomatonBuilder.load_from_dict(data)
            return True
        except json.JSONDecodeError as e:
            st.error(f"Formato JSON inválido: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Error importando JSON: {str(e)}")
            return False
    
    @staticmethod
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
            
            AutomatonBuilder.load_from_dict(data)
            return True
        except ET.ParseError as e:
            st.error(f"Formato XML inválido: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Error importando XML: {str(e)}")
            return False
    
    @staticmethod
    def import_from_file(uploaded_file) -> bool:
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
                return ImportExportService.import_from_json(content)
            
            # Try XML
            elif content.startswith('<') and content.endswith('>'):
                return ImportExportService.import_from_xml(content)
            
            else:
                st.error("Formato de archivo no reconocido. Por favor sube un archivo JSON o XML válido.")
                return False
        
        except Exception as e:
            st.error(f"Error leyendo el archivo: {str(e)}")
            return False