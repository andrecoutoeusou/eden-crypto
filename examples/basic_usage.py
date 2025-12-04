examples/basic_usage.py#!/usr/bin/env python3
"""
Basic Usage Example for ÉDEN Crypto Framework

Author: Sidney André França Couto Florencio
Email: andrecouto@eusoueden.com
License: Apache 2.0
"""

from eden_crypto.core.prime_generator import generate_prime, generate_rsa_primes

# Example 1: Generate a simple 256-bit prime
print("ÉDEN Crypto - Basic Usage Examples")
print("="*50)

print("\nExample 1: Generate a 256-bit prime")
prime = generate_prime(256)
print(f"Generated prime: {prime}")
print(f"Bit length: {prime.bit_length()}")
print(f"Is odd: {prime % 2 == 1}")

# Example 2: Generate RSA key primes
print("\nExample 2: Generate RSA-2048 primes")
p, q = generate_rsa_primes(1024)  # 1024 bits each for RSA-2048
n = p * q
print(f"p (first prime): {p.bit_length()} bits")
print(f"q (second prime): {q.bit_length()} bits")
print(f"n = p*q: {n.bit_length()} bits")
print(f"p and q are different: {p != q}")

# Example 3: Using the full PrimeGenerator class
print("\nExample 3: Using PrimeGenerator class")
from eden_crypto.core.prime_generator import PrimeGenerator

generator = PrimeGenerator(
    wheel_size=30030,
    use_decimal_rivers=True,
    track_provenance=True
)

prime, coibite_code = generator.generate_prime(512)
print(f"Generated 512-bit prime: {prime.bit_length()} bits")

if coibite_code:
    print("\nProvenance information (Coibite Code):")
    data = coibite_code.to_dict()
    print(f"  Timestamp: {data['timestamp_iso']}")
    print(f"  Wheel size: {data['metadata']['wheel_size']}")
    print(f"  Decimal Rivers: {data['metadata']['decimal_rivers_enabled']}")
    print(f"  Generation time: {data['metadata']['generation_time_seconds']:.4f}s")

print("\n" + "="*50)
print("Examples completed successfully!")
