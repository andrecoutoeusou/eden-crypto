"""  
ÉDEN Framework - Decimal Rivers Analysis Module

This module implements the Decimal Rivers approach for analyzing
prime number distribution patterns based on decimal digit endings.

Author: Sidney André França Couto Florencio
Email: andrecouto@eusoueden.com
License: Apache-2.0
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict, Counter


class DecimalRivers:
    """Analyze and exploit decimal digit patterns in prime number distribution."""
    
    def __init__(self):
        self.transition_matrix = defaultdict(Counter)
        self.digit_frequencies = Counter()
        self.prime_cache = []
        
    def analyze_primes(self, primes: List[int]) -> Dict:
        """Analyze decimal patterns in a list of primes.
        
        Args:
            primes: List of prime numbers to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        self.prime_cache = primes
        
        # Analyze digit endings
        for prime in primes:
            if prime > 5:  # Skip 2, 3, 5
                last_digit = prime % 10
                self.digit_frequencies[last_digit] += 1
        
        # Analyze transitions
        for i in range(len(primes) - 1):
            if primes[i] > 5 and primes[i+1] > 5:
                curr_digit = primes[i] % 10
                next_digit = primes[i+1] % 10
                self.transition_matrix[curr_digit][next_digit] += 1
        
        return self._compile_analysis()
    
    def _compile_analysis(self) -> Dict:
        """Compile analysis results into structured format."""
        total_primes = sum(self.digit_frequencies.values())
        
        # Calculate digit probabilities
        digit_probs = {
            digit: count / total_primes 
            for digit, count in self.digit_frequencies.items()
        }
        
        # Calculate transition probabilities
        transition_probs = {}
        for from_digit, transitions in self.transition_matrix.items():
            total_transitions = sum(transitions.values())
            transition_probs[from_digit] = {
                to_digit: count / total_transitions
                for to_digit, count in transitions.items()
            }
        
        return {
            'digit_frequencies': dict(self.digit_frequencies),
            'digit_probabilities': digit_probs,
            'transition_matrix': dict(self.transition_matrix),
            'transition_probabilities': transition_probs,
            'total_primes_analyzed': total_primes
        }
    
    def get_river_score(self, candidate: int) -> float:
        """Calculate decimal river score for a candidate prime.
        
        Args:
            candidate: Number to evaluate
            
        Returns:
            Score indicating likelihood based on decimal patterns (0-1)
        """
        last_digit = candidate % 10
        
        # Check if digit is valid for primes > 5
        if last_digit not in [1, 3, 7, 9]:
            return 0.0
        
        # If we have no data, return neutral score
        if not self.digit_frequencies:
            return 0.5
        
        # Calculate score based on digit frequency
        total = sum(self.digit_frequencies.values())
        freq = self.digit_frequencies[last_digit]
        
        return freq / total if total > 0 else 0.5
    
    def optimize_candidates(self, candidates: List[int]) -> List[int]:
        """Optimize candidate list using decimal river analysis.
        
        Args:
            candidates: List of candidate numbers
            
        Returns:
            Filtered and prioritized candidate list
        """
        # Score all candidates
        scored = [(c, self.get_river_score(c)) for c in candidates]
        
        # Sort by score (descending)
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Return optimized list
        return [c for c, score in scored if score > 0.2]
    
    def generate_statistics(self) -> str:
        """Generate human-readable statistics report."""
        analysis = self._compile_analysis()
        
        report = []
        report.append("=== DECIMAL RIVERS ANALYSIS ===")
        report.append(f"\nTotal primes analyzed: {analysis['total_primes_analyzed']}")
        
        report.append("\nDigit Ending Frequencies:")
        for digit in sorted(analysis['digit_frequencies'].keys()):
            freq = analysis['digit_frequencies'][digit]
            prob = analysis['digit_probabilities'][digit]
            report.append(f"  {digit}: {freq} ({prob*100:.2f}%)")
        
        report.append("\nTop Transition Patterns:")
        for from_digit, transitions in analysis['transition_probabilities'].items():
            top_transitions = sorted(transitions.items(), key=lambda x: x[1], reverse=True)[:3]
            report.append(f"  {from_digit} → {', '.join(f'{to}:{prob*100:.1f}%' for to, prob in top_transitions)}")
        
        return "\n".join(report)


def analyze_prime_range(start: int, end: int, sieve_func=None) -> DecimalRivers:
    """Convenience function to analyze primes in a range.
    
    Args:
        start: Start of range
        end: End of range
        sieve_func: Optional sieve function to generate primes
        
    Returns:
        DecimalRivers instance with completed analysis
    """
    if sieve_func is None:
        # Simple trial division for small ranges
        def is_prime(n):
            if n < 2:
                return False
            if n == 2:
                return True
            if n % 2 == 0:
                return False
            for i in range(3, int(n**0.5) + 1, 2):
                if n % i == 0:
                    return False
            return True
        
        primes = [n for n in range(start, end + 1) if is_prime(n)]
    else:
        primes = sieve_func(start, end)
    
    analyzer = DecimalRivers()
    analyzer.analyze_primes(primes)
    return analyzer
