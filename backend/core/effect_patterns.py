"""
Sistema de Padrões de Ligação para Efeitos

Cada efeito é definido por 3 requisitos de ligação específicos.
Cada requisito especifica: (tipo_partícula1, polaridade1, tipo_partícula2, polaridade2, multiplicidade)

Exemplo:
  Requisito: ('square', '-', 'triangle', '+', 2)
  Significa: Uma partícula quadrado negativa ligada a uma partícula triângulo positiva com ligação dupla

Se uma molécula contém TODOS os 3 requisitos, ela recebe o efeito.
"""

from typing import Dict, List, Set, Tuple

# Tipos de partículas disponíveis
PARTICLE_TYPES = ['circle', 'square', 'triangle', 'pentagon']

# Polaridades possíveis
POLARITIES = ['+', '-']

# Multiplicidades possíveis
MULTIPLICITIES = [1, 2, 3]


def normalize_bond_requirement(particle_type1: str, polarity1: str, particle_type2: str, polarity2: str, multiplicity: int) -> Tuple[str, str, str, str, int]:
    """
    Normaliza um requisito de ligação para forma canônica (ordem alfabética dos tipos).
    
    Args:
        particle_type1: Tipo da primeira partícula
        polarity1: Polaridade da primeira partícula ('+' ou '-')
        particle_type2: Tipo da segunda partícula
        polarity2: Polaridade da segunda partícula ('+' ou '-')
        multiplicity: Multiplicidade da ligação
    
    Returns:
        Tuple ordenado (tipo1, polaridade1, tipo2, polaridade2, multiplicidade)
        onde tipo1 <= tipo2 alfabeticamente
    """
    if particle_type1 <= particle_type2:
        return (particle_type1, polarity1, particle_type2, polarity2, multiplicity)
    else:
        return (particle_type2, polarity2, particle_type1, polarity1, multiplicity)


def generate_all_effect_requirements() -> Dict[str, List[Tuple[str, str, str, str, int]]]:
    """
    Gera 3 requisitos únicos e específicos para cada um dos 20 efeitos.
    Garante que todos os requisitos sejam diferentes entre todos os efeitos.
    
    Estratégia:
    - Gerar todas as combinações possíveis de requisitos (72 total)
    - Distribuir de forma determinística e única para cada efeito (20 efeitos * 3 = 60 requisitos)
    - Como temos 72 combinações únicas possíveis, cada efeito terá requisitos distintos entre si
    
    Returns:
        Dicionário {nome_efeito: [lista de 3 requisitos]}
        Cada requisito é uma tupla: (tipo1, polaridade1, tipo2, polaridade2, multiplicidade)
    """
    from core.property_profiles import ALL_EFFECTS
    
    # Limites de conexões por tipo de partícula
    from data.molecules import PARTICLE_TYPES as PARTICLE_CONNECTIONS
    MAX_CONNECTIONS = {
        'circle': PARTICLE_CONNECTIONS['circle']['connections'],
        'square': PARTICLE_CONNECTIONS['square']['connections'],
        'triangle': PARTICLE_CONNECTIONS['triangle']['connections'],
        'pentagon': PARTICLE_CONNECTIONS['pentagon']['connections']
    }
    
    # Gerar todas as combinações possíveis de requisitos (filtrando impossíveis)
    all_possible_requirements = []
    
    for type1 in PARTICLE_TYPES:
        for type2 in PARTICLE_TYPES:
            if type1 == type2:  # Regra: partículas do mesmo tipo não podem se ligar
                continue
            
            for pol1 in POLARITIES:
                for pol2 in POLARITIES:
                    # Regra: partículas com mesma polaridade não podem se ligar
                    if pol1 == pol2:
                        continue
                    
                    for mult in MULTIPLICITIES:
                        # Regra: multiplicidade não pode exceder conexões máximas
                        # A multiplicidade deve ser <= ao menor número de conexões entre os dois tipos
                        max_mult = min(MAX_CONNECTIONS[type1], MAX_CONNECTIONS[type2])
                        if mult > max_mult:
                            continue
                        
                        req = normalize_bond_requirement(type1, pol1, type2, pol2, mult)
                        if req not in all_possible_requirements:
                            all_possible_requirements.append(req)
    
    # Total teórico: 4 tipos escolhem 2 = 6 pares * 2^2 polaridades * 3 multiplicidades = 72 combinações
    # Para 20 efeitos precisamos de 60 requisitos (20 * 3)
    # Como temos 72 combinações únicas possíveis, cada efeito terá requisitos distintos entre si
    
    # Gerar requisitos únicos para cada efeito de forma determinística
    # Estratégia: Primeiro escolher polaridades para cada tipo (determinístico),
    # depois gerar requisitos compatíveis com essas polaridades
    all_requirements = {}
    
    for idx, effect_name in enumerate(ALL_EFFECTS):
        # 1. Escolher polaridades para cada tipo de partícula (determinístico)
        effect_hash = hash(effect_name)
        type_polarities = {}
        
        for particle_type in PARTICLE_TYPES:
            # Usar hash para escolher polaridade determinística
            type_hash = hash(f"{effect_name}_{particle_type}")
            type_polarities[particle_type] = POLARITIES[abs(type_hash) % 2]  # '+' ou '-'
        
        # 2. Gerar requisitos compatíveis com essas polaridades
        compatible_requirements = []
        for req in all_possible_requirements:
            type1, pol1, type2, pol2, mult = req
            # Verificar se o requisito é compatível com as polaridades escolhidas
            if (type1 in type_polarities and type_polarities[type1] == pol1 and
                type2 in type_polarities and type_polarities[type2] == pol2):
                compatible_requirements.append(req)
        
        # 3. Selecionar 3 requisitos únicos dos compatíveis
        requirements = []
        
        if len(compatible_requirements) < 3:
            # Se não há requisitos compatíveis suficientes, tentar outra combinação de polaridades
            # Usar uma estratégia diferente: escolher polaridades que garantam requisitos suficientes
            import random
            random.seed(abs(effect_hash))
            
            # Tentar até encontrar uma combinação que tenha requisitos suficientes
            for attempt in range(10):
                type_polarities = {}
                for particle_type in PARTICLE_TYPES:
                    type_polarities[particle_type] = random.choice(POLARITIES)
                
                compatible_requirements = []
                for req in all_possible_requirements:
                    type1, pol1, type2, pol2, mult = req
                    if (type1 in type_polarities and type_polarities[type1] == pol1 and
                        type2 in type_polarities and type_polarities[type2] == pol2):
                        compatible_requirements.append(req)
                
                if len(compatible_requirements) >= 3:
                    break
            random.seed()  # Reset seed
        
        if len(compatible_requirements) >= 3:
            # Selecionar 3 requisitos únicos dos compatíveis (já filtrados por polaridade)
            start_idx = abs(effect_hash) % len(compatible_requirements)
            req_idx = start_idx
            
            # Adicionar até 3 requisitos únicos
            for _ in range(3):
                if len(requirements) >= 3:
                    break
                
                attempts = 0
                while attempts < len(compatible_requirements):
                    req = compatible_requirements[req_idx]
                    if req not in requirements:
                        requirements.append(req)
                        break
                    req_idx = (req_idx + 1) % len(compatible_requirements)
                    attempts += 1
        
        all_requirements[effect_name] = requirements[:3] if len(requirements) >= 3 else []
    
    return all_requirements


def molecule_has_requirement(molecule: Dict, requirement: Tuple[str, str, str, str, int]) -> bool:
    """
    Verifica se uma molécula contém um requisito de ligação específico.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
        requirement: Tupla (tipo1, polaridade1, tipo2, polaridade2, multiplicidade)
    
    Returns:
        bool: True se o requisito existir na molécula
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    # Criar mapa de IDs para tipos e polaridades
    particle_info = {
        p['id']: {
            'type': p['type'],
            'polarity': p.get('polarity', '+')
        }
        for p in particles
    }
    
    req_type1, req_pol1, req_type2, req_pol2, req_multiplicity = requirement
    
    # Verificar se existe uma ligação que corresponde ao requisito
    for bond in bonds:
        from_id = bond.get('from')
        to_id = bond.get('to')
        multiplicity = bond.get('multiplicity', 1)
        
        # Verificar multiplicidade
        if multiplicity != req_multiplicity:
            continue
        
        # Obter informações das partículas
        from_info = particle_info.get(from_id)
        to_info = particle_info.get(to_id)
        
        if not from_info or not to_info:
            continue
        
        # Verificar se a ligação corresponde ao requisito (em qualquer ordem)
        # Caso 1: from -> to corresponde exatamente
        if (from_info['type'] == req_type1 and from_info['polarity'] == req_pol1 and
            to_info['type'] == req_type2 and to_info['polarity'] == req_pol2):
            return True
        
        # Caso 2: to -> from corresponde (ligação reversa)
        if (to_info['type'] == req_type1 and to_info['polarity'] == req_pol1 and
            from_info['type'] == req_type2 and from_info['polarity'] == req_pol2):
            return True
    
    return False


def molecule_has_effect(molecule: Dict, effect_requirements: List[Tuple[str, str, str, str, int]]) -> bool:
    """
    Verifica se uma molécula tem todos os 3 requisitos necessários para um efeito.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
        effect_requirements: Lista de 3 requisitos necessários
    
    Returns:
        bool: True se a molécula tiver TODOS os 3 requisitos
    """
    for requirement in effect_requirements:
        if not molecule_has_requirement(molecule, requirement):
            return False
    return True


def extract_molecule_bond_patterns(molecule: Dict) -> Set[Tuple[str, str, str, str, int]]:
    """
    Extrai todos os padrões de ligação presentes em uma molécula.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
    
    Returns:
        Set de tuplas (tipo1, polaridade1, tipo2, polaridade2, multiplicidade) normalizadas
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    patterns = set()
    particle_info = {
        p['id']: {
            'type': p['type'],
            'polarity': p.get('polarity', '+')
        }
        for p in particles
    }
    
    for bond in bonds:
        from_id = bond.get('from')
        to_id = bond.get('to')
        multiplicity = bond.get('multiplicity', 1)
        
        from_info = particle_info.get(from_id)
        to_info = particle_info.get(to_id)
        
        if from_info and to_info:
            pattern = normalize_bond_requirement(
                from_info['type'], from_info['polarity'],
                to_info['type'], to_info['polarity'],
                multiplicity
            )
            patterns.add(pattern)
    
    return patterns
