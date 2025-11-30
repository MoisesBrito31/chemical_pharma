"""
Funções para comparar moléculas considerando estrutura completa
(partículas + ligações)
"""

def are_molecules_identical(mol1, mol2):
    """
    Compara duas moléculas verificando se são idênticas estruturalmente
    Considera: tipos de partículas, polaridades E estrutura de ligações
    """
    if not mol1 or not mol2:
        return False
    
    # Verificar se são dicionários (moléculas)
    if not isinstance(mol1, dict) or not isinstance(mol2, dict):
        return False
    
    # Verificar quantidade de partículas
    if len(mol1.get('particles', [])) != len(mol2.get('particles', [])):
        return False
    
    # Verificar quantidade de ligações
    if len(mol1.get('bonds', [])) != len(mol2.get('bonds', [])):
        return False
    
    # Criar "impressão digital" molecular (fingerprint)
    fingerprint1 = create_molecular_fingerprint(mol1)
    fingerprint2 = create_molecular_fingerprint(mol2)
    
    return fingerprint1 == fingerprint2


def create_molecular_fingerprint(molecule):
    """
    Cria uma "impressão digital" única da molécula
    baseada na estrutura completa (partículas + ligações)
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    # 1. Criar representação das partículas (ordenada)
    particles_signature = ','.join(sorted([
        f"{p['type']}{p['polarity']}" for p in particles
    ]))
    
    # 2. Criar representação das ligações (normalizada)
    bonds_signature_parts = []
    for bond in bonds:
        particle_from = next((p for p in particles if p['id'] == bond['from']), None)
        particle_to = next((p for p in particles if p['id'] == bond['to']), None)
        
        if not particle_from or not particle_to:
            continue
        
        from_str = f"{particle_from['type']}{particle_from['polarity']}"
        to_str = f"{particle_to['type']}{particle_to['polarity']}"
        mult = f"x{bond.get('multiplicity', 1)}"
        
        # Ordenar para que A-B seja igual a B-A
        first, second = sorted([from_str, to_str])
        bonds_signature_parts.append(f"{first}-{second}{mult}")
    
    bonds_signature = '|'.join(sorted(bonds_signature_parts))
    
    # 3. Combinar tudo em uma única string
    return f"{particles_signature}::{bonds_signature}"


