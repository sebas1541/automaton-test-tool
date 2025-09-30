"""
Automaton builder service for DFA Test Tool.
Handles building Automaton objects from session state and data dictionaries.
"""

import sys
import os
from typing import Dict, Set, List

# Add the core directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))

from core.models.automaton import Automaton
from core.models.state import State
from core.models.transition import Transition
from ui.services.session_state_manager import SessionStateManager


class AutomatonBuilder:
    """Service for building Automaton objects from various sources."""
    
    @staticmethod
    def build_from_session_state() -> Automaton:
        """Build an Automaton object from the current session state."""
        # Create State objects
        states_set = set()
        state_objects = {}
        
        for state_id in SessionStateManager.get_current_states():
            is_final = state_id in SessionStateManager.get_final_states()
            state_obj = State(state_id, is_final=is_final)
            states_set.add(state_obj)
            state_objects[state_id] = state_obj
        
        # Create Transition objects
        transitions_set = set()
        for transition_dict in SessionStateManager.get_current_transitions():
            from_state = state_objects[transition_dict['from_state']]
            to_state = state_objects[transition_dict['to_state']]
            symbol = transition_dict['symbol']
            
            transition_obj = Transition(from_state, to_state, symbol)
            transitions_set.add(transition_obj)
        
        # Get initial state object
        initial_state = state_objects.get(SessionStateManager.get_initial_state())
        
        # Get final states set
        final_states_set = {
            state_objects[state_id] 
            for state_id in SessionStateManager.get_final_states() 
            if state_id in state_objects
        }
        
        # Create and return automaton
        return Automaton(
            states=states_set,
            transitions=transitions_set,
            initial_state=initial_state,
            final_states=final_states_set,
            alphabet=set(SessionStateManager.get_current_alphabet())
        )
    
    @staticmethod
    def load_from_dict(data: dict):
        """Load automaton data into session state from dictionary."""
        # Clear current session state completely and reinitialize
        SessionStateManager.clear_session_state()
        
        # Load alphabet
        if 'alphabet' in data and data['alphabet']:
            SessionStateManager.update_alphabet(list(data['alphabet']))
        
        # Load states
        if 'states' in data and data['states']:
            state_ids = set()
            final_state_ids = set()
            for state_data in data['states']:
                state_id = state_data['id']
                state_ids.add(state_id)
                if state_data.get('is_final', False):
                    final_state_ids.add(state_id)
            SessionStateManager.update_states(state_ids)
            SessionStateManager.update_final_states(final_state_ids)
        
        # Load initial state
        current_states = SessionStateManager.get_current_states()
        if 'initial_state_id' in data and data['initial_state_id'] and data['initial_state_id'] in current_states:
            SessionStateManager.update_initial_state(data['initial_state_id'])
        elif current_states:
            # Set first state as initial if none specified
            SessionStateManager.update_initial_state(sorted(list(current_states))[0])
        
        # Load transitions
        if 'transitions' in data and data['transitions']:
            transitions = []
            for transition_data in data['transitions']:
                # Validate that states exist
                from_state = transition_data['from_state_id']
                to_state = transition_data['to_state_id']
                if from_state in current_states and to_state in current_states:
                    transitions.append({
                        'from_state': from_state,
                        'to_state': to_state,
                        'symbol': transition_data['symbol']
                    })
            SessionStateManager.update_transitions(transitions)