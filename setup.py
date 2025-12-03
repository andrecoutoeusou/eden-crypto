"""
ÉDEN Crypto - Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="eden-crypto",
    version="0.1.0",
    author="André Couto",
    author_email="your.email@example.com",
    description="ÉDEN: High-Throughput Prime Generation via Decimal-Aware Wheel Sieves",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrecoutoeusou/eden-crypto",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "quantum": ["qiskit>=1.0.0", "qiskit-aer>=0.13.0"],
        "dev": ["pytest>=7.0.0", "black>=23.0.0", "flake8>=6.0.0"],
    },
    project_urls={
        "Bug Reports": "https://github.com/andrecoutoeusou/eden-crypto/issues",
        "Source": "https://github.com/andrecoutoeusou/eden-crypto",
    },
)
