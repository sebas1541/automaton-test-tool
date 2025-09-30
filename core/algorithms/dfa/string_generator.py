"""
String Generator for DFA

This module provides functionality to generate strings that are accepted by a DFA,
ordered by length from shortest to longest.
"""

from typing import List, Set, Tuple
from collections import deque
from ...models.automaton import Automaton
from ...models.state import State


class DFAStringGenerator:
    """
    Generates strings accepted by a DFA in order of increasing length.
    
    Uses breadth-first search to systematically explore all possible paths
    through the automaton, ensuring shorter strings are found before longer ones.
    """
    
    def __init__(self, automaton: Automaton):
        """
        Initialize the string generator.
        
        Args:
            automaton: The DFA to generate strings for
        """
        self.automaton = automaton
        
    def generate_accepted_strings(self, max_count: int = 10, max_length: int = 50) -> List[str]:
        """
        Generate strings accepted by the DFA.
        
        Args:
            max_count: Maximum number of strings to generate
            max_length: Maximum length of strings to consider
            
        Returns:
            List of accepted strings ordered by length
        """
        accepted_strings = []
        visited_states_at_length = set()
        
        # Queue stores tuples of (current_state, string_so_far, length)
        queue = deque([(self.automaton.initial_state, "", 0)])
        
        while queue and len(accepted_strings) < max_count:
            current_state, current_string, length = queue.popleft()
            
            # Skip if we've exceeded max length
            if length > max_length:
                continue
                
            # Create a unique identifier for this state at this string
            state_string_key = (current_state.id, current_string)
            if state_string_key in visited_states_at_length:
                continue
            visited_states_at_length.add(state_string_key)
            
            # Check if current state is accepting
            if current_state in self.automaton.final_states:
                if current_string not in accepted_strings:
                    accepted_strings.append(current_string)
                    if len(accepted_strings) >= max_count:
                        break
            
            # Explore all possible transitions from current state
            for transition in self.automaton.transitions:
                if transition.from_state == current_state:
                    new_string = current_string + transition.symbol
                    new_length = length + 1
                    
                    # Add to queue for further exploration
                    queue.append((transition.to_state, new_string, new_length))
        
        return accepted_strings
    
    def generate_strings_by_length(self, max_count: int = 10, max_length: int = 20) -> List[Tuple[int, List[str]]]:
        """
        Generate strings grouped by length.
        
        Args:
            max_count: Maximum total number of strings to generate
            max_length: Maximum length to consider
            
        Returns:
            List of tuples (length, strings_of_that_length)
        """
        all_strings = self.generate_accepted_strings(max_count, max_length)
        
        # Group by length
        by_length = {}
        for string in all_strings:
            length = len(string)
            if length not in by_length:
                by_length[length] = []
            by_length[length].append(string)
        
        # Sort by length and return
        return [(length, strings) for length, strings in sorted(by_length.items())]
    
    def check_if_empty_string_accepted(self) -> bool:
        """
        Check if the empty string is accepted by the automaton.
        
        Returns:
            True if empty string is accepted, False otherwise
        """
        return self.automaton.initial_state in self.automaton.final_states