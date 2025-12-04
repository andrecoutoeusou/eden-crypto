# -*- coding: utf-8 -*-
"""
ÉDEN Crypto - Prime Generator Module

Main interface for the ÉDEN prime generation framework.
Integrates all ÉDEN components into a unified API.

Author: Sidney André França Couto Florencio
Email: andrecouto@eusoueden.com
License: Apache 2.0
"""

import secrets
import random
from typing import Optional, Tuple, Dict, Any
from .decimal_rivers import DecimalRivers
from .extended_wheel import ExtendedWheel
from .coibite_codes import CoibiteCode
import time


class PrimeGenerator:
    """
    ÉDEN Prime Generator - Main interface.
    
    Combines Decimal Rivers analysis, Extended Wheel factorization,
    and Coibite Code provenance tracking for secure prime generation.
    
    Features:
    - Cryptographically secure random number generation
    - Decimal-aware prime candidate selection
    - Optimized wheel factorization
    - Provenance tracking with Coibite Codes
    - Miller-Rabin primality testing
    """
    
    def __init__(self, 
                 wheel_size: int = 30030,
                 use_decimal_rivers: bool = True,
                 track_provenance: bool = True,
                 miller_rabin_rounds: int = 64):
        """
        Initialize the ÉDEN Prime Generator.
        
        Args:
            wheel_size: Wheel size for factorization (6, 30, 210, 2310, 30030)
            use_decimal_rivers: Enable Decimal Rivers optimization
            track_provenance: Enable Coibite Code tracking
            miller_rabin_rounds: Number of Miller-Rabin test rounds (default 64)
        """
        self.wheel = ExtendedWheel(wheel_size)
        self.decimal_rivers = DecimalRivers() if use_decimal_rivers else None
        self.track_provenance = track_provenance
        self.miller_rabin_rounds = miller_rabin_rounds
        
    def generate_prime(self, bits: int) -> Tuple[int, Optional[CoibiteCode]]:
        """
        Generate a cryptographically secure prime number.
        
        Args:
            bits: Bit length of the prime (minimum 16 bits)
            
        Returns:
            Tuple of (prime, coibite_code or None)
            
        Raises:
            ValueError: If bits < 16
        """
        if bits < 16:
            raise ValueError("Prime must be at least 16 bits")
            
        start_time = time.time()
        
        # Generate prime using ÉDEN framework
        prime = self._generate_prime_internal(bits)
        
        generation_time = time.time() - start_time
        
        # Create Coibite Code for provenance tracking
        coibite_code = None
        if self.track_provenance:
            metadata = {
                "bits": bits,
                "wheel_size": self.wheel.size,
                "decimal_rivers_enabled": self.decimal_rivers is not None,
                "miller_rabin_rounds": self.miller_rabin_rounds,
                "generation_time_seconds": generation_time
            }
            coibite_code = CoibiteCode(prime, metadata)
            
        return prime, coibite_code
    
    def generate_prime_pair(self, bits: int) -> Tuple[int, int, Optional[CoibiteCode], Optional[CoibiteCode]]:
        """
        Generate a pair of distinct primes (useful for RSA).
        
        Args:
            bits: Bit length for each prime
            
        Returns:
            Tuple of (p, q, coibite_p, coibite_q)
        """
        p, coibite_p = self.generate_prime(bits)
        
        # Ensure q != p
        q, coibite_q = self.generate_prime(bits)
        while q == p:
            q, coibite_q = self.generate_prime(bits)
            
        return p, q, coibite_p, coibite_q
    
    def _generate_prime_internal(self, bits: int) -> int:
        """
        Internal prime generation using ÉDEN framework.
        
        Args:
            bits: Bit length of prime
            
        Returns:
            A prime number
        """
        while True:
            # Generate random odd number of correct bit length
            candidate = self._generate_candidate(bits)
            
            # Apply Decimal Rivers filtering if enabled
            if self.decimal_rivers:
                decimal_weight = self.decimal_rivers.calculate_prime_weight(candidate)
                if decimal_weight < 0.3:  # Threshold for filtering
                    continue
            
            # Quick divisibility check with wheel
            if not self.wheel.is_prime_wheel(candidate):
                continue
            
            # Final Miller-Rabin primality test
            if self._miller_rabin(candidate, self.miller_rabin_rounds):
                return candidate
    
    def _generate_candidate(self, bits: int) -> int:
        """
        Generate a random odd number with specified bit length.
        
        Args:
            bits: Bit length
            
        Returns:
            Random odd integer
        """
        # Ensure correct bit length: MSB and LSB set to 1
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1  # Set MSB and LSB
        return candidate
    
    def _miller_rabin(self, n: int, rounds: int) -> bool:
        """
        Miller-Rabin primality test.
        
        Args:
            n: Number to test
            rounds: Number of test rounds
            
        Returns:
            True if probably prime, False if composite
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Witness loop
        for _ in range(rounds):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get generator configuration and statistics.
        
        Returns:
            Dictionary with generator info
        """
        return {
            "wheel_size": self.wheel.size,
            "decimal_rivers_enabled": self.decimal_rivers is not None,
            "provenance_tracking_enabled": self.track_provenance,
            "miller_rabin_rounds": self.miller_rabin_rounds,
            "wheel_efficiency": self.wheel.get_efficiency_metrics()
        }


def generate_prime(bits: int, **kwargs) -> int:
    """
    Convenience function to generate a single prime.
    
    Args:
        bits: Bit length of the prime
        **kwargs: Additional arguments for PrimeGenerator
        
    Returns:
        A prime number
    """
    generator = PrimeGenerator(**kwargs)
    prime, _ = generator.generate_prime(bits)
    return prime


def generate_prime_with_provenance(bits: int, **kwargs) -> Tuple[int, CoibiteCode]:
    """
    Generate a prime with Coibite Code provenance.
    
    Args:
        bits: Bit length of the prime
        **kwargs: Additional arguments for PrimeGenerator
        
    Returns:
        Tuple of (prime, coibite_code)
    """
    kwargs['track_provenance'] = True
    generator = PrimeGenerator(**kwargs)
    return generator.generate_prime(bits)


def generate_rsa_primes(bits_per_prime: int, **kwargs) -> Tuple[int, int]:
    """
    Generate a pair of primes for RSA.
    
    Args:
        bits_per_prime: Bit length for each prime (e.g., 1024 for RSA-2048)
        **kwargs: Additional arguments for PrimeGenerator
        
    Returns:
        Tuple of (p, q)
    """
    generator = PrimeGenerator(**kwargs)
    p, q, _, _ = generator.generate_prime_pair(bits_per_prime)
    return p, q
