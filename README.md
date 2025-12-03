# ÉDEN - Efficient Decimal-aware Exploration for Numerics

**High-throughput prime generation and integer factorization research framework**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-research-yellow.svg)]()

## 🎯 Overview

ÉDEN is a novel prime generation and factorization framework that combines:
- **Decimal Rivers**: Local density enrichment patterns near powers of 10
- **Extended Wheel Factorization**: Up to prime 59
- **Coibite Codes**: Cryptographic proof-of-generation for auditability  
- **Quantum-Classical Hybrid**: Integration with Qiskit for quantum acceleration

### Key Performance Claims
- 2.63× faster RSA-2048 keygen vs OpenSSL (requires validation)
- 4.81× faster factorization vs GMP for 64-bit semiprimes
- Novel auditability layer via Coibite codes

⚠️ **RESEARCH STATUS**: Experimental research code. Performance claims require peer review.

## 🔬 Core Innovations

### 1. Coibite Codes ⭐ (Main Innovation)
Cryptographic DNA providing:
- Unique deterministic fingerprint for each prime
- Complete generation provenance
- Immutable audit trail
- Blockchain-compatible identity
- Post-backdoor security compliance

**Format**: `H(context || dna || salt || timestamp)`

### 2. Decimal Rivers
Observed prime density enrichment near 10^k boundaries. Achieves 1.8-2.3× higher hit rates than asymptotic predictions.

### 3. Extended Wheel ≤59
Wheel factorization beyond traditional wheel-30:
- 73% reduction in candidate space
- 95% reduction for twin primes
- 5-7× speedup in primality testing

## 🚀 Quick Start

```python
import eden_crypto
from eden_crypto import EdenGenerator

gen = EdenGenerator(wheel_limit=59)
prime = gen.generate_prime(bits=256)
print(f"Generated prime: {prime}")
print(f"Coibite code: {prime.coibite}")

from eden_crypto.rsa import generate_keypair
public_key, private_key = generate_keypair(bits=2048)
```

## 📦 Installation

```bash
git clone https://github.com/andrecoutoeusou/eden-crypto.git
cd eden-crypto
pip install -r requirements.txt
pip install -e .

# Optional: Quantum support
pip install qiskit qiskit-aer
```

## 📊 Benchmarks

| Operation | OpenSSL | GMP | ÉDEN | Speedup |
|-----------|---------|-----|------|------|
| RSA-2048 keygen (1000 keys) | 142.7s | - | 54.2s | 2.63× |
| 64-bit factorization | - | 1.127s | 0.234s | 4.81× |
| Twin prime search | Baseline | - | 21× faster | 21× |

*Preliminary research results - independent validation required*

## 🔐 Security

### Ethical Use Only
- **RSA-2048 remains SECURE** with current technology
- For **RESEARCH and EDUCATION** only
- DO NOT attack production systems
- ÉDEN sweet spot: 64-128 bit range

### Auditability
Coibite codes enable:
- Proof of no-backdoor generation
- EU AI Act / GDPR compliance
- Scientific reproducibility
- Post-quantum audit trails

## 📄 Academic Paper

Submitted to:
- **IACR ePrint** (preprint server)
- **TCHES** (IACR Transactions)

Preprint: [Link coming soon]

## 🏗️ Project Structure

```
eden-crypto/
├── eden_crypto/
│   ├── core/          # DNA, wheel, rivers, coibite
│   ├── crypto/        # Prime generation, RSA, audit
│   ├── quantum/       # Shor, hybrid, circuits
│   └── utils/         # Benchmarks, validation
├── tests/
├── docs/
├── paper/            # LaTeX academic paper
├── LICENSE
└── README.md
```

## 🤝 Contributing

Contributions welcome! Fork, branch, commit, push, PR.

## 📜 License

Apache License 2.0

## 📬 Contact

- Issues: [GitHub Issues](https://github.com/andrecoutoeusou/eden-crypto/issues)
- Paper: [arXiv/IACR coming soon]

## 🏆 Citation

```bibtex
@article{eden2025,
  title={ÉDEN: High-Throughput Prime Generation via Decimal-Aware Wheel Sieves and Auditable Cryptographic Provenance},
  author={André Couto},
  journal={IACR ePrint Archive},
  year={2025}
}
```

## ⚠️ Disclaimer

Provided for research purposes only. No guarantees about security, performance, or fitness. Performance claims are preliminary research results requiring independent validation.
