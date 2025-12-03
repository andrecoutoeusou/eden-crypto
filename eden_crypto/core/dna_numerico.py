"""
ÉDEN Crypto - DNA Numérico Core Module
Implements the DNANumerico class for prime analysis and generation
"""

class DNANumerico:
    """Extrai o DNA de um número baseado na cosmologia 1-3-7-9-6"""
    
    def __init__(self, n: int):
        self.n = n
        self.familia = n % 10  # Família decimal
        self.res6 = n % 6      # Resíduo mod 6 (ponte-6)
        self.res59 = n % 59    # Resíduo mod 59 (fractal)
        self.soma_digitos = sum(int(d) for d in str(n))
    
    def __repr__(self):
        return f"DNA(fam={self.familia}, res6={self.res6}, res59={self.res59}, soma={self.soma_digitos})"
    
    def get_offsets_eden(self) -> list[int]:
        """Retorna offsets baseados na família e ponte-6"""
        # Famílias 1,3,7,9 são candidatas a primos
        if self.familia in [1, 3, 7, 9]:
            return [-1, 1, -3, 3, -7, 7, -9, 9]
        elif self.familia in [2, 4, 6, 8, 0]:
            # Aplicar ponte-6
            return [-6, 6, -12, 12, -18, 18]
        else:
            return [-1, 1, -2, 2, -3, 3]
