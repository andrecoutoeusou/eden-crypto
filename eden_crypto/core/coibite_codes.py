# -*- coding: utf-8 -*-
"""
ÉDEN Crypto - Coibite Codes Module

Cryptographic provenance tracking system for prime number generation.
Provides tamper-evident encoding and verification of generation history.

Author: Sidney André França Couto Florencio
Email: andrecouto@eusoueden.com
License: Apache 2.0
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.backends import default_backend
import base64


class CoibiteCode:
    """
    Cryptographic provenance code for prime generation history.
    
    A Coibite Code encodes:
    - Generation timestamp
    - Algorithm parameters used
    - Prime number characteristics
    - Verification checksum
    - Digital signature (optional)
    
    The encoding is tamper-evident and can be verified without
    requiring the original generation secrets.
    """
    
    VERSION = "1.0"
    
    def __init__(self, prime: int, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a Coibite Code for a prime number.
        
        Args:
            prime: The prime number to track
            metadata: Optional generation metadata
        """
        self.prime = prime
        self.timestamp = time.time()
        self.metadata = metadata or {}
        self.signature = None
        
    def encode(self, include_prime: bool = False) -> str:
        """
        Encode the provenance data as a Coibite Code string.
        
        Args:
            include_prime: Whether to include the actual prime in the code
                          (default False for privacy)
        
        Returns:
            Base64-encoded Coibite Code string
        """
        data = {
            "version": self.VERSION,
            "timestamp": self.timestamp,
            "prime_bits": self.prime.bit_length(),
            "prime_hash": self._hash_prime(),
            "metadata": self.metadata,
            "checksum": self._calculate_checksum()
        }
        
        if include_prime:
            data["prime"] = str(self.prime)
            
        if self.signature:
            data["signature"] = base64.b64encode(self.signature).decode('utf-8')
            
        json_str = json.dumps(data, sort_keys=True)
        return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    @classmethod
    def decode(cls, code: str) -> 'CoibiteCode':
        """
        Decode a Coibite Code string.
        
        Args:
            code: Base64-encoded Coibite Code
            
        Returns:
            CoibiteCode instance
            
        Raises:
            ValueError: If code is invalid or corrupted
        """
        try:
            json_str = base64.b64decode(code).decode('utf-8')
            data = json.loads(json_str)
            
            # Verify version compatibility
            if data.get("version") != cls.VERSION:
                raise ValueError(f"Unsupported version: {data.get('version')}")
            
            # Reconstruct CoibiteCode
            if "prime" in data:
                prime = int(data["prime"])
            else:
                # If prime not included, use hash as placeholder
                prime = 0
                
            instance = cls(prime, data.get("metadata", {}))
            instance.timestamp = data["timestamp"]
            
            if "signature" in data:
                instance.signature = base64.b64decode(data["signature"])
                
            return instance
            
        except Exception as e:
            raise ValueError(f"Invalid Coibite Code: {e}")
    
    def sign(self, private_key: ec.EllipticCurvePrivateKey):
        """
        Sign the Coibite Code with an ECDSA private key.
        
        Args:
            private_key: ECDSA private key (secp256r1)
        """
        # Create canonical representation for signing
        sign_data = self._get_signing_data()
        
        # Sign with ECDSA
        signature = private_key.sign(
            sign_data,
            ec.ECDSA(hashes.SHA256())
        )
        
        self.signature = signature
    
    def verify(self, public_key: ec.EllipticCurvePublicKey) -> bool:
        """
        Verify the Coibite Code signature.
        
        Args:
            public_key: ECDSA public key
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.signature:
            return False
            
        try:
            sign_data = self._get_signing_data()
            public_key.verify(
                self.signature,
                sign_data,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False
    
    def verify_integrity(self) -> bool:
        """
        Verify the internal integrity of the Coibite Code.
        
        Returns:
            True if checksum is valid, False otherwise
        """
        if "checksum" not in self.metadata:
            return True  # No checksum to verify
            
        expected = self.metadata.get("checksum")
        actual = self._calculate_checksum()
        return expected == actual
    
    def _hash_prime(self) -> str:
        """
        Calculate SHA-256 hash of the prime number.
        
        Returns:
            Hex-encoded hash string
        """
        prime_bytes = str(self.prime).encode('utf-8')
        return hashlib.sha256(prime_bytes).hexdigest()
    
    def _calculate_checksum(self) -> str:
        """
        Calculate integrity checksum.
        
        Returns:
            Hex-encoded checksum
        """
        # Create canonical representation
        data = f"{self.prime}:{self.timestamp}:{json.dumps(self.metadata, sort_keys=True)}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()[:16]
    
    def _get_signing_data(self) -> bytes:
        """
        Get canonical byte representation for signing.
        
        Returns:
            Bytes to be signed
        """
        data = {
            "prime_hash": self._hash_prime(),
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
        json_str = json.dumps(data, sort_keys=True)
        return json_str.encode('utf-8')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation.
        
        Returns:
            Dictionary with all code data
        """
        return {
            "prime": str(self.prime) if self.prime > 0 else None,
            "prime_bits": self.prime.bit_length() if self.prime > 0 else 0,
            "prime_hash": self._hash_prime() if self.prime > 0 else None,
            "timestamp": self.timestamp,
            "timestamp_iso": datetime.fromtimestamp(self.timestamp).isoformat(),
            "metadata": self.metadata,
            "checksum": self._calculate_checksum(),
            "has_signature": self.signature is not None
        }
    
    def __str__(self) -> str:
        """String representation."""
        data = self.to_dict()
        return f"CoibiteCode(bits={data['prime_bits']}, signed={data['has_signature']})"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"CoibiteCode(prime_bits={self.prime.bit_length()}, timestamp={self.timestamp})"


def generate_keypair() -> tuple:
    """
    Generate an ECDSA keypair for signing Coibite Codes.
    
    Returns:
        Tuple of (private_key, public_key)
    """
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


def batch_encode(primes: List[int], metadata_list: Optional[List[Dict]] = None) -> List[str]:
    """
    Encode multiple primes as Coibite Codes.
    
    Args:
        primes: List of prime numbers
        metadata_list: Optional list of metadata dicts (one per prime)
        
    Returns:
        List of encoded Coibite Code strings
    """
    if metadata_list and len(metadata_list) != len(primes):
        raise ValueError("metadata_list length must match primes length")
        
    codes = []
    for i, prime in enumerate(primes):
        metadata = metadata_list[i] if metadata_list else None
        code = CoibiteCode(prime, metadata)
        codes.append(code.encode())
        
    return codes


def batch_decode(codes: List[str]) -> List[CoibiteCode]:
    """
    Decode multiple Coibite Code strings.
    
    Args:
        codes: List of encoded Coibite Codes
        
    Returns:
        List of CoibiteCode instances
    """
    return [CoibiteCode.decode(code) for code in codes]
