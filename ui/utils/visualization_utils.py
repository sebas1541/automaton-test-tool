"""
Visualization utilities for DFA Test Tool.
Handles graph creation and visualization of automata.
"""

import graphviz
from typing import Dict, List, Set


class VisualizationUtils:
    """Utility class for creating visualizations of automata."""
    
    @staticmethod
    def create_automaton_graph(
        states: Dict, 
        transitions: List, 
        initial_state: str, 
        final_states: Set[str]
    ) -> graphviz.Digraph:
        """Create a graphviz representation of the DFA."""
        dot = graphviz.Digraph(comment='Automaton', format='svg')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle')
        
        # Add an invisible start node to show initial state
        dot.node('start', '', shape='none', width='0', height='0')
        
        # Add states
        for state in states:
            if state in final_states:
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state)
        
        # Add initial state arrow
        dot.edge('start', initial_state)
        
        # Group transitions by (from_state, to_state) to combine symbols
        transition_groups = {}
        for transition in transitions:
            key = (transition['from_state'], transition['to_state'])
            if key not in transition_groups:
                transition_groups[key] = []
            transition_groups[key].append(transition['symbol'])
        
        # Add transitions
        for (from_state, to_state), symbols in transition_groups.items():
            label = ', '.join(sorted(symbols))
            dot.edge(from_state, to_state, label=label)
        
        return dot