"""
Simulation component for DFA Test Tool.
Handles string testing and simulation functionality.
"""

import streamlit as st
import sys
import os

# Add the core directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))

from core.algorithms.dfa.dfa_simulator import DFASimulator
from core.algorithms.dfa.step_by_step_simulation import StepByStepSimulation
from core.algorithms.dfa.string_generator import DFAStringGenerator
from ui.services.session_state_manager import SessionStateManager
from ui.services.automaton_builder import AutomatonBuilder


class SimulationComponent:
    """Component for simulation and testing functionality."""
    
    @staticmethod
    def render():
        """Render the simulation component."""
        st.header("🧪 Pruebas y Simulación")
        
        # Test string input
        test_string = st.text_input("Cadena de Prueba", placeholder="Ingresa la cadena a probar...")
        
        # Create two tabs for better organization
        tab1, tab2 = st.tabs(["🚀 Simulación", "📝 Generar Cadenas"])
        
        with tab1:
            SimulationComponent._render_simulation_tab(test_string)
        
        with tab2:
            SimulationComponent._render_string_generation_tab()
    
    @staticmethod
    def _render_simulation_tab(test_string: str):
        """Render the simulation tab."""
        current_states = SessionStateManager.get_current_states()
        
        if st.button("🚀 Ejecutar Simulación", disabled=not test_string or not current_states):
            try:
                # Build automaton from session state
                automaton = AutomatonBuilder.build_from_session_state()
                
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
                st.error(f"La simulación falló: {str(e)}")
    
    @staticmethod
    def _render_string_generation_tab():
        """Render the string generation tab."""
        st.write("Genera automáticamente las primeras 10 cadenas aceptadas por el autómata:")
        
        current_states = SessionStateManager.get_current_states()
        
        if st.button("🎯 Generar Cadenas Aceptadas", disabled=not current_states):
            try:
                # Build automaton from session state
                automaton = AutomatonBuilder.build_from_session_state()
                
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
                    
                    st.success(f"[OK] Se encontraron {total_shown} cadenas aceptadas")
                    
            except Exception as e:
                st.error(f"Error generando cadenas: {str(e)}")