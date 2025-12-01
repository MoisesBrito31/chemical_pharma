"""
Sistema de Padrões de Ligação para Efeitos

Cada efeito é definido por um conjunto único de padrões de ligações.
Se uma molécula contém TODOS os padrões, ela recebe o efeito.

Exemplo:
  Efeito "Analgésico" requer:
    - Ligação: circle-triangle (multiplicidade 1)
    - Ligação: square-pentagon (multiplicidade 2)
  
  Se a molécula tiver AMBAS as ligações, ela tem o efeito.
"""

import random
from typing import Dict, List, Set, Optional, Tuple

# Tipos de partículas disponíveis
PARTICLE_TYPES = ['circle', 'square', 'triangle', 'pentagon']

# Multiplicidades possíveis
MULTIPLICITIES = [1, 2, 3]


def normalize_bond_pattern(particle_type1: str, particle_type2: str, multiplicity: int) -> Tuple[str, str, int]:
    """
    Normaliza um padrão de ligação para forma canônica (ordem alfabética).
    
    Args:
        particle_type1: Tipo da primeira partícula
        particle_type2: Tipo da segunda partícula
        multiplicity: Multiplicidade da ligação
    
    Returns:
        Tuple ordenado (tipo1, tipo2, multiplicidade) onde tipo1 <= tipo2 alfabeticamente
    """
    if particle_type1 <= particle_type2:
        return (particle_type1, particle_type2, multiplicity)
    else:
        return (particle_type2, particle_type1, multiplicity)


def generate_effect_patterns(effect_name: str, num_patterns: int = 2, seed: Optional[int] = None) -> List[Tuple[str, str, int]]:
    """
    Gera padrões de ligação aleatórios para um efeito.
    
    IMPORTANTE: Os padrões são projetados para exigir múltiplas partículas diferentes,
    garantindo que apenas moléculas com massa > 5 possam satisfazer todos os padrões.
    
    Estratégia:
    - Para 2 padrões: Garantir que usem pelo menos 3 tipos diferentes de partículas
    - Para 3 padrões: Garantir que usem todos os 4 tipos de partículas
    Isso naturalmente força moléculas maiores, pois precisam ter múltiplos tipos diferentes.
    
    Args:
        effect_name: Nome do efeito
        num_patterns: Número de padrões necessários (2-3)
        seed: Seed para randomização
    
    Returns:
        Lista de tuplas (tipo1, tipo2, multiplicidade) normalizadas
    """
    if seed is not None:
        random.seed(seed)
    
    # Usar hash do nome do efeito como seed base
    effect_hash = hash(effect_name)
    random.seed(effect_hash)
    
    patterns = []
    used_combinations = set()
    used_particle_types = set()
    
    # Determinar quantos tipos diferentes de partículas são necessários
    # Para garantir que molécula precise ter pelo menos 6 partículas
    # Estratégia: sempre exigir pelo menos 4 tipos diferentes
    if num_patterns == 2:
        # 2 padrões: usar todos os 4 tipos diferentes
        # Exemplo: (circle-triangle) + (square-pentagon) usa 4 tipos
        min_unique_types = 4
    else:  # num_patterns == 3
        # 3 padrões: usar todos os 4 tipos
        min_unique_types = 4
    
    # Gerar padrões garantindo diversidade de tipos
    max_attempts = 200
    attempts = 0
    
    while len(patterns) < num_patterns and attempts < max_attempts:
        attempts += 1
        
        type1 = random.choice(PARTICLE_TYPES)
        type2 = random.choice(PARTICLE_TYPES)
        
        # Partículas do mesmo tipo não podem se ligar (regra do sistema)
        if type1 == type2:
            continue
        
        multiplicity = random.choice(MULTIPLICITIES)
        pattern = normalize_bond_pattern(type1, type2, multiplicity)
        
        # Evitar padrões duplicados (mesma ligação e multiplicidade)
        if pattern in used_combinations:
            continue
        
        # Calcular tipos únicos que este padrão adicionaria
        new_types = {type1, type2}
        total_types = used_particle_types | new_types
        
        # Verificar se ainda precisamos de mais tipos diferentes
        if len(patterns) == num_patterns - 1:
            # Último padrão: garantir que temos tipos suficientes
            if len(total_types) < min_unique_types:
                # Não atingiu o mínimo, tentar outro padrão
                continue
        else:
            # Padrões intermediários: preferir tipos novos, mas aceitar se necessário
            if len(patterns) > 0 and len(new_types - used_particle_types) == 0:
                # Não adiciona tipo novo, mas pode ser aceito se ainda temos espaço
                pass
        
        # Adicionar padrão
        patterns.append(pattern)
        used_combinations.add(pattern)
        used_particle_types.update(new_types)
    
    # Fallback: se não conseguiu com restrições, gerar padrões válidos simples
    while len(patterns) < num_patterns:
        type1 = random.choice(PARTICLE_TYPES)
        type2 = random.choice(PARTICLE_TYPES)
        
        if type1 == type2:
            continue
        
        multiplicity = random.choice(MULTIPLICITIES)
        pattern = normalize_bond_pattern(type1, type2, multiplicity)
        
        if pattern not in used_combinations:
            patterns.append(pattern)
            used_combinations.add(pattern)
            used_particle_types.add(type1)
            used_particle_types.add(type2)
    
    random.seed()
    return patterns


def molecule_has_pattern(molecule: Dict, pattern: Tuple[str, str, int]) -> bool:
    """
    Verifica se uma molécula contém um padrão de ligação específico.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
        pattern: Tupla (tipo1, tipo2, multiplicidade)
    
    Returns:
        bool: True se o padrão existir na molécula
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    # Criar mapa de IDs para tipos
    particle_types = {p['id']: p['type'] for p in particles}
    
    type1, type2, required_multiplicity = pattern
    
    # Verificar se existe uma ligação que corresponde ao padrão
    for bond in bonds:
        from_id = bond.get('from')
        to_id = bond.get('to')
        multiplicity = bond.get('multiplicity', 1)
        
        # Obter tipos das partículas
        from_type = particle_types.get(from_id)
        to_type = particle_types.get(to_id)
        
        if not from_type or not to_type:
            continue
        
        # Normalizar para comparar
        normalized = normalize_bond_pattern(from_type, to_type, multiplicity)
        
        # Verificar se corresponde ao padrão
        if normalized == pattern:
            return True
    
    return False


def molecule_has_effect(molecule: Dict, effect_patterns: List[Tuple[str, str, int]]) -> bool:
    """
    Verifica se uma molécula tem todos os padrões necessários para um efeito.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
        effect_patterns: Lista de padrões necessários
    
    Returns:
        bool: True se a molécula tiver TODOS os padrões
    """
    for pattern in effect_patterns:
        if not molecule_has_pattern(molecule, pattern):
            return False
    return True


def extract_molecule_bond_patterns(molecule: Dict) -> Set[Tuple[str, str, int]]:
    """
    Extrai todos os padrões de ligação presentes em uma molécula.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
    
    Returns:
        Set de tuplas (tipo1, tipo2, multiplicidade) normalizadas
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    patterns = set()
    particle_types = {p['id']: p['type'] for p in particles}
    
    for bond in bonds:
        from_id = bond.get('from')
        to_id = bond.get('to')
        multiplicity = bond.get('multiplicity', 1)
        
        from_type = particle_types.get(from_id)
        to_type = particle_types.get(to_id)
        
        if from_type and to_type:
            pattern = normalize_bond_pattern(from_type, to_type, multiplicity)
            patterns.add(pattern)
    
    return patterns

