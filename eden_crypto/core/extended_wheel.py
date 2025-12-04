"""  
ÉDEN Framework - Extended Wheel Factorization Module

Implements optimized wheel factorization with decimal-aware enhancements.
Wheel factorization reduces candidate prime testing by pre-computing
residue classes that cannot contain primes.

Author: Sidney André França Couto Florencio
Email: andrecouto@eusoueden.com
License: Apache-2.0
"""

import numpy as np
from typing import List, Tuple, Set, Iterator
from functools import lru_cache
import math


class ExtendedWheel:
    """Extended wheel factorization with decimal-aware optimizations."""
    
    # Pre-computed basis primes for common wheel sizes
    WHEEL_BASIS = {
        6: [2, 3],
        30: [2, 3, 5],
        210: [2, 3, 5, 7],
        2310: [2, 3, 5, 7, 11],
        30030: [2, 3, 5, 7, 11, 13]
    }
    
    def __init__(self, wheel_size: int = 30, decimal_aware: bool = True):
        """Initialize wheel with specified size.
        
        Args:
            wheel_size: Size of wheel (6, 30, 210, 2310, or 30030)
            decimal_aware: Enable decimal rivers optimization
        """
        if wheel_size not in self.WHEEL_BASIS:
            raise ValueError(f"Wheel size must be one of {list(self.WHEEL_BASIS.keys())}")
        
        self.wheel_size = wheel_size
        self.basis_primes = self.WHEEL_BASIS[wheel_size]
        self.decimal_aware = decimal_aware
        
        # Generate wheel pattern
        self.spokes = self._generate_spokes()
        self.spoke_count = len(self.spokes)
        
        # Decimal optimization
        if decimal_aware:
            self.decimal_weights = self._compute_decimal_weights()
    
    def _generate_spokes(self) -> List[int]:
        """Generate wheel spoke pattern (coprime residues)."""
        spokes = []
        for i in range(1, self.wheel_size):
            if all(i % p != 0 for p in self.basis_primes):
                spokes.append(i)
        return spokes
    
    def _compute_decimal_weights(self) -> dict:
        """Compute weights for decimal endings based on frequency."""
        # Empirical weights from prime distribution analysis
        # These favor endings that appear more frequently in primes
        return {
            1: 1.02,
            3: 0.98,
            7: 1.01,
            9: 0.99,
            # Invalid endings get zero weight
            0: 0.0, 2: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 8: 0.0
        }
    
    def generate_candidates(self, start: int, end: int) -> Iterator[int]:
        """Generate prime candidates using wheel sieve.
        
        Args:
            start: Start of range
            end: End of range
            
        Yields:
            Candidate prime numbers
        """
        # Handle basis primes
        for p in self.basis_primes:
            if start <= p <= end:
                yield p
        
        # Start from first full wheel after basis primes
        wheel_start = ((start - 1) // self.wheel_size + 1) * self.wheel_size
        
        # Generate candidates from wheel
        current_wheel = wheel_start
        while current_wheel <= end:
            for spoke in self.spokes:
                candidate = current_wheel + spoke
                if start <= candidate <= end:
                    if self.decimal_aware:
                        # Apply decimal weighting
                        last_digit = candidate % 10
                        weight = self.decimal_weights.get(last_digit, 0.5)
                        if weight > 0.5:  # Only yield candidates with good decimal profiles
                            yield candidate
                    else:
                        yield candidate
                elif candidate > end:
                    return
            current_wheel += self.wheel_size
    
    def sieve(self, start: int, end: int) -> List[int]:
        """Generate primes using segmented sieve with wheel optimization.
        
        Args:
            start: Start of range
            end: End of range
            
        Returns:
            List of prime numbers in range
        """
        if end < 2:
            return []
        
        # Handle small ranges
        if end - start < 10000:
            return self._simple_sieve(start, end)
        
        # Segmented sieve for large ranges
        return self._segmented_sieve(start, end)
    
    def _simple_sieve(self, start: int, end: int) -> List[int]:
        """Simple sieve for small ranges."""
        # Generate candidates
        candidates = list(self.generate_candidates(max(2, start), end))
        
        # Sieve out composites
        limit = int(end ** 0.5) + 1
        small_primes = self._get_small_primes(limit)
        
        primes = []
        for candidate in candidates:
            is_prime = True
            for p in small_primes:
                if p * p > candidate:
                    break
                if candidate % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(candidate)
        
        return primes
    
    def _segmented_sieve(self, start: int, end: int, segment_size: int = 100000) -> List[int]:
        """Segmented sieve for large ranges."""
        primes = []
        
        # Get small primes for sieving
        limit = int(end ** 0.5) + 1
        small_primes = self._get_small_primes(limit)
        
        # Process in segments
        current = start
        while current <= end:
            segment_end = min(current + segment_size, end)
            
            # Generate candidates for this segment
            candidates = list(self.generate_candidates(current, segment_end))
            
            # Sieve segment
            is_prime = [True] * len(candidates)
            
            for p in small_primes:
                # Find first candidate divisible by p
                start_idx = 0
                for i, c in enumerate(candidates):
                    if c % p == 0 and c != p:
                        start_idx = i
                        break
                
                # Mark multiples
                for i in range(start_idx, len(candidates), 1):
                    if candidates[i] % p == 0 and candidates[i] != p:
                        is_prime[i] = False
            
            # Collect primes from segment
            primes.extend([candidates[i] for i in range(len(candidates)) if is_prime[i]])
            
            current = segment_end + 1
        
        return primes
    
    @lru_cache(maxsize=128)
    def _get_small_primes(self, limit: int) -> List[int]:
        """Get all primes up to limit using simple sieve."""
        if limit < 2:
            return []
        
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        
        for i in range(2, int(limit ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False
        
        return [i for i in range(2, limit + 1) if is_prime[i]]
    
    def get_efficiency(self) -> Tuple[int, float]:
        """Calculate wheel efficiency metrics.
        
        Returns:
            Tuple of (spoke_count, reduction_percentage)
        """
        reduction = (1 - self.spoke_count / self.wheel_size) * 100
        return self.spoke_count, reduction
    
    def __repr__(self) -> str:
        spokes, reduction = self.get_efficiency()
        return (f"ExtendedWheel(size={self.wheel_size}, "
                f"spokes={spokes}, reduction={reduction:.1f}%, "
                f"decimal_aware={self.decimal_aware})")


def generate_primes(n: int, wheel_size: int = 30) -> List[int]:
    """Convenience function to generate first n primes.
    
    Args:
        n: Number of primes to generate
        wheel_size: Wheel size to use
        
    Returns:
        List of first n primes
    """
    if n <= 0:
        return []
    
    wheel = ExtendedWheel(wheel_size)
    primes = []
    
    # Estimate upper bound using prime number theorem
    if n < 6:
        limit = 15
    else:
        limit = int(n * (math.log(n) + math.log(math.log(n))))
    
    while len(primes) < n:
        primes = wheel.sieve(2, limit)
        if len(primes) < n:
            limit = int(limit * 1.5)
    
    return primes[:n]


def is_prime_wheel(n: int, wheel_size: int = 30) -> bool:
    """Check if number is prime using wheel-based trial division.
    
    Args:
        n: Number to test
        wheel_size: Wheel size to use
        
    Returns:
        True if n is prime, False otherwise
    """
    if n < 2:
        return False
    
    wheel = ExtendedWheel(wheel_size)
    
    # Check against basis primes
    if n in wheel.basis_primes:
        return True
    
    # Check divisibility by basis primes
    for p in wheel.basis_primes:
        if n % p == 0:
            return False
    
    # Check divisibility using wheel
    limit = int(n ** 0.5) + 1
    for candidate in wheel.generate_candidates(2, limit):
        if candidate * candidate > n:
            break
        if n % candidate == 0:
            return False
    
    return True
