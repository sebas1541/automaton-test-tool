"""
Main Flask application for the Automaton Test Tool.

This module sets up the Flask application with CORS support,
registers API routes, and provides the main entry point for
the backend server.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from .api.routes import api_bp


def create_app(config=None):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config: Optional configuration object
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Configure CORS for frontend communication
    CORS(app, origins=['http://localhost:3000', 'http://localhost:5173'])
    
    # Basic app configuration
    app.config.update({
        'JSON_SORT_KEYS': False,
        'JSONIFY_PRETTYPRINT_REGULAR': True
    })
    
    # Apply custom configuration if provided
    if config:
        app.config.update(config)
    
    # Register API blueprint
    app.register_blueprint(api_bp)
    
    # Root endpoint
    @app.route('/')
    def root():
        """Root endpoint with API information."""
        return jsonify({
            'name': 'Automaton Test Tool API',
            'version': '1.0.0',
            'description': 'REST API for finite automata operations',
            'endpoints': {
                'health': '/api/health',
                'create_automaton': '/api/automaton/create',
                'simulate_dfa': '/api/automaton/simulate/dfa',
                'simulate_nfa': '/api/automaton/simulate/nfa',
                'convert_nfa_to_dfa': '/api/automaton/convert/nfa-to-dfa',
                'analyze_automaton': '/api/automaton/analyze',
                'test_strings': '/api/automaton/test-strings'
            }
        })
    
    return app


def main():
    """Main entry point for running the Flask app."""
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()