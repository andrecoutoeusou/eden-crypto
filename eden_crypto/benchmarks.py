#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ÉDEN Crypto - Benchmarks Module

Performance comparison benchmarks for ÉDEN prime generation
versus standard library and other implementations.

Author: Sidney André França Couto Florencio
Email: andrecouto@eusoueden.com
License: Apache 2.0
"""

import time
import statistics
from typing import List, Dict, Callable, Tuple
from .core.prime_generator import PrimeGenerator, generate_prime
import secrets


class Benchmark:
    """
    Performance benchmarking suite for prime generation.
    
    Compares ÉDEN framework against baseline implementations.
    """
    
    def __init__(self, warmup_rounds: int = 3, test_rounds: int = 10):
        """
        Initialize benchmark suite.
        
        Args:
            warmup_rounds: Number of warmup iterations
            test_rounds: Number of test iterations for averaging
        """
        self.warmup_rounds = warmup_rounds
        self.test_rounds = test_rounds
        self.results = {}
        
    def run_benchmark(self, 
                     name: str, 
                     func: Callable, 
                     *args, 
                     **kwargs) -> Dict[str, float]:
        """
        Run a single benchmark test.
        
        Args:
            name: Benchmark name
            func: Function to benchmark
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Dictionary with timing statistics
        """
        print(f"Running benchmark: {name}...")
        
        # Warmup
        for _ in range(self.warmup_rounds):
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"  Warmup error: {e}")
                return {"error": str(e)}
        
        # Actual benchmark
        times = []
        for i in range(self.test_rounds):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                end = time.perf_counter()
                times.append(end - start)
            except Exception as e:
                print(f"  Test round {i+1} error: {e}")
                return {"error": str(e)}
        
        # Calculate statistics
        stats = {
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "min": min(times),
            "max": max(times),
            "rounds": len(times)
        }
        
        self.results[name] = stats
        
        print(f"  Mean: {stats['mean']:.4f}s")
        print(f"  Median: {stats['median']:.4f}s")
        print(f"  StdDev: {stats['stdev']:.4f}s")
        
        return stats
    
    def compare(self, baseline: str, comparison: str) -> Dict[str, float]:
        """
        Compare two benchmark results.
        
        Args:
            baseline: Name of baseline benchmark
            comparison: Name of comparison benchmark
            
        Returns:
            Dictionary with comparison metrics
        """
        if baseline not in self.results or comparison not in self.results:
            raise ValueError("Both benchmarks must be run first")
        
        base_time = self.results[baseline]["mean"]
        comp_time = self.results[comparison]["mean"]
        
        speedup = base_time / comp_time
        improvement = ((base_time - comp_time) / base_time) * 100
        
        return {
            "speedup": speedup,
            "improvement_percent": improvement,
            "baseline_mean": base_time,
            "comparison_mean": comp_time
        }
    
    def print_summary(self):
        """
        Print benchmark results summary.
        """
        print("\n" + "="*60)
        print("BENCHMARK SUMMARY")
        print("="*60)
        
        for name, stats in self.results.items():
            if "error" in stats:
                print(f"\n{name}: ERROR - {stats['error']}")
            else:
                print(f"\n{name}:")
                print(f"  Mean:   {stats['mean']:.6f}s")
                print(f"  Median: {stats['median']:.6f}s")
                print(f"  StdDev: {stats['stdev']:.6f}s")
                print(f"  Range:  {stats['min']:.6f}s - {stats['max']:.6f}s")


def baseline_prime_generation(bits: int) -> int:
    """
    Baseline prime generation using simple trial division.
    
    Args:
        bits: Bit length of prime
        
    Returns:
        A prime number
    """
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        
        if is_prime_trial_division(candidate):
            return candidate


def is_prime_trial_division(n: int, limit: int = 10000) -> bool:
    """
    Simple trial division primality test.
    
    Args:
        n: Number to test
        limit: Maximum divisor to test
        
    Returns:
        True if likely prime, False if composite
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Check small primes
    for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        if n == p:
            return True
        if n % p == 0:
            return False
    
    # Trial division up to sqrt(n) or limit
    i = 53
    while i * i <= n and i <= limit:
        if n % i == 0:
            return False
        i += 2
    
    return True


def run_standard_benchmarks(bits: int = 512) -> Benchmark:
    """
    Run standard benchmark suite.
    
    Args:
        bits: Bit length for prime generation tests
        
    Returns:
        Benchmark object with results
    """
    bench = Benchmark(warmup_rounds=2, test_rounds=5)
    
    print(f"\nRunning benchmarks for {bits}-bit primes...\n")
    
    # Benchmark ÉDEN with all optimizations
    bench.run_benchmark(
        "EDEN_Full",
        generate_prime,
        bits,
        wheel_size=30030,
        use_decimal_rivers=True,
        track_provenance=False
    )
    
    # Benchmark ÉDEN without Decimal Rivers
    bench.run_benchmark(
        "EDEN_NoRivers",
        generate_prime,
        bits,
        wheel_size=30030,
        use_decimal_rivers=False,
        track_provenance=False
    )
    
    # Benchmark ÉDEN with small wheel
    bench.run_benchmark(
        "EDEN_SmallWheel",
        generate_prime,
        bits,
        wheel_size=210,
        use_decimal_rivers=True,
        track_provenance=False
    )
    
    # Benchmark baseline (only for smaller bit sizes)
    if bits <= 64:
        bench.run_benchmark(
            "Baseline_TrialDivision",
            baseline_prime_generation,
            bits
        )
    
    bench.print_summary()
    
    # Print comparisons
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISONS")
    print("="*60)
    
    try:
        comp = bench.compare("EDEN_NoRivers", "EDEN_Full")
        print(f"\nÉDEN Full vs No Rivers:")
        print(f"  Speedup: {comp['speedup']:.2f}x")
        print(f"  Improvement: {comp['improvement_percent']:.1f}%")
    except:
        pass
    
    try:
        comp = bench.compare("EDEN_SmallWheel", "EDEN_Full")
        print(f"\nÉDEN Full vs Small Wheel:")
        print(f"  Speedup: {comp['speedup']:.2f}x")
        print(f"  Improvement: {comp['improvement_percent']:.1f}%")
    except:
        pass
    
    return bench


def run_scaling_benchmark(bit_sizes: List[int] = None) -> Dict[int, Benchmark]:
    """
    Run benchmarks across different bit sizes.
    
    Args:
        bit_sizes: List of bit sizes to test (default: [256, 512, 1024])
        
    Returns:
        Dictionary mapping bit size to benchmark results
    """
    if bit_sizes is None:
        bit_sizes = [256, 512, 1024]
    
    results = {}
    
    print("\n" + "="*60)
    print("SCALING BENCHMARK")
    print("="*60)
    
    for bits in bit_sizes:
        print(f"\n{'='*60}")
        print(f"Testing {bits}-bit primes")
        print(f"{'='*60}")
        
        bench = run_standard_benchmarks(bits)
        results[bits] = bench
    
    # Print scaling summary
    print("\n" + "="*60)
    print("SCALING SUMMARY")
    print("="*60)
    
    for bits in bit_sizes:
        if "EDEN_Full" in results[bits].results:
            mean_time = results[bits].results["EDEN_Full"]["mean"]
            print(f"{bits:4d} bits: {mean_time:.6f}s")
    
    return results


if __name__ == "__main__":
    # Run standard benchmarks
    print("ÉDEN Crypto Framework - Performance Benchmarks")
    print("="*60)
    
    # Quick benchmark for demonstration
    run_standard_benchmarks(bits=256)
    
    # Uncomment for full scaling test:
    # run_scaling_benchmark([256, 512, 1024, 2048])
