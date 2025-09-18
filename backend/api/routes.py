"""
Flask API routes for automaton operations.

This module provides REST API endpoints for:
- Creating and managing automata
- Running DFA and NFA simulations
- Converting NFAs to DFAs
- Analyzing automaton properties
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
from ..models import State, Transition, Automaton
from ..algorithms import DFASimulator, NFASimulator, NFAToDFAConverter

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Automaton API is running'})


@api_bp.route('/automaton/create', methods=['POST'])
def create_automaton():
    """Create a new automaton from JSON data."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        automaton = Automaton.from_dict(data)
        
        return jsonify({
            'success': True,
            'automaton': automaton.to_dict(),
            'properties': {
                'is_deterministic': automaton.is_deterministic(),
                'state_count': len(automaton.states),
                'transition_count': len(automaton.transitions),
                'alphabet_size': len(automaton.alphabet)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_bp.route('/automaton/simulate/dfa', methods=['POST'])
def simulate_dfa():
    """Simulate DFA execution on input string."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Create automaton and simulator
        automaton = Automaton.from_dict(data['automaton'])
        simulator = DFASimulator(automaton)
        
        input_string = data.get('input_string', '')
        
        # Run simulation
        is_accepted, steps = simulator.simulate(input_string)
        
        # Convert steps to serializable format
        steps_data = []
        for step in steps:
            step_data = {
                'current_state': step.current_state.id,
                'input_position': step.input_position,
                'symbol': step.symbol,
                'transition_used': step.transition_used.to_dict() if step.transition_used else None
            }
            steps_data.append(step_data)
        
        return jsonify({
            'accepted': is_accepted,
            'steps': steps_data,
            'total_steps': len(steps_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_bp.route('/automaton/simulate/nfa', methods=['POST'])
def simulate_nfa():
    """Simulate NFA execution on input string."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Create automaton and simulator
        automaton = Automaton.from_dict(data['automaton'])
        simulator = NFASimulator(automaton)
        
        input_string = data.get('input_string', '')
        
        # Get detailed simulation results
        simulation_details = simulator.simulate_with_details(input_string)
        
        return jsonify({
            'accepted': simulation_details['accepted'],
            'total_steps': simulation_details['total_steps'],
            'configuration_counts': simulation_details['configuration_counts'],
            'states_by_step': simulation_details['states_by_step'],
            'accepting_paths_count': simulation_details['accepting_paths_count'],
            'is_deterministic': simulation_details['is_deterministic']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_bp.route('/automaton/convert/nfa-to-dfa', methods=['POST'])
def convert_nfa_to_dfa():
    """Convert NFA to equivalent DFA using subset construction."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Create NFA
        nfa = Automaton.from_dict(data['nfa'])
        
        # Convert to DFA
        converter = NFAToDFAConverter()
        conversion_analysis = converter.analyze_conversion(nfa)
        
        dfa, state_mapping = converter.convert_with_state_mapping(nfa)
        
        # Convert state mapping to serializable format
        state_mapping_data = {}
        for dfa_state_id, state_set in state_mapping.items():
            state_mapping_data[dfa_state_id] = {
                'nfa_states': [state.id for state in state_set.states],
                'label': state_set.id
            }
        
        return jsonify({
            'dfa': dfa.to_dict(),
            'state_mapping': state_mapping_data,
            'conversion_analysis': {
                'nfa_stats': conversion_analysis['nfa_stats'],
                'dfa_stats': conversion_analysis['dfa_stats'],
                'conversion_metrics': conversion_analysis['conversion_metrics']
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_bp.route('/automaton/analyze', methods=['POST'])
def analyze_automaton():
    """Analyze automaton properties and characteristics."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        automaton = Automaton.from_dict(data['automaton'])
        
        # Basic properties
        analysis = {
            'basic_properties': {
                'is_deterministic': automaton.is_deterministic(),
                'state_count': len(automaton.states),
                'transition_count': len(automaton.transitions),
                'final_state_count': len(automaton.final_states),
                'alphabet_size': len(automaton.alphabet),
                'alphabet': sorted(list(automaton.alphabet))
            },
            'states': {
                'initial_state': automaton.initial_state.id if automaton.initial_state else None,
                'final_states': [state.id for state in automaton.final_states],
                'all_states': [state.id for state in automaton.states]
            },
            'transitions': {
                'total': len(automaton.transitions),
                'epsilon_transitions': len([t for t in automaton.transitions if t.is_epsilon]),
                'by_symbol': {}
            }
        }
        
        # Count transitions by symbol
        for transition in automaton.transitions:
            symbol = transition.symbol if not transition.is_epsilon else 'ε'
            if symbol not in analysis['transitions']['by_symbol']:
                analysis['transitions']['by_symbol'][symbol] = 0
            analysis['transitions']['by_symbol'][symbol] += 1
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_bp.route('/automaton/test-strings', methods=['POST'])
def test_strings():
    """Test multiple strings against an automaton."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        automaton = Automaton.from_dict(data['automaton'])
        test_strings = data.get('test_strings', [])
        
        # Choose appropriate simulator
        if automaton.is_deterministic():
            simulator = DFASimulator(automaton)
        else:
            simulator = NFASimulator(automaton)
        
        results = []
        for test_string in test_strings:
            try:
                is_accepted = simulator.is_accepted(test_string)
                results.append({
                    'string': test_string,
                    'accepted': is_accepted,
                    'error': None
                })
            except Exception as e:
                results.append({
                    'string': test_string,
                    'accepted': False,
                    'error': str(e)
                })
        
        return jsonify({
            'results': results,
            'automaton_type': 'DFA' if automaton.is_deterministic() else 'NFA'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@api_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({'error': 'Method not allowed'}), 405


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500