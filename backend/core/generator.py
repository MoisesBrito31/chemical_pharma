"""
Sistema de Geração de Moléculas
Gera todas as moléculas possíveis com massa específica e tipos mistos
"""

from data.molecules import PARTICLE_TYPES
from .synthesis import find_connected_components, reorganize_positions
from .molecule_analyzer import analyze_molecule_structure
import itertools
import copy


def generate_molecules(particle_type, target_mass):
    """
    Gera todas as moléculas possíveis com massa específica.
    Prioriza moléculas que contêm o tipo de partícula escolhido.
    
    Args:
        particle_type: Tipo de partícula preferido (1, 2, 3, 4) ou None para todos
        target_mass: Massa total desejada (número de partículas)
        
    Returns: {
        'success': bool,
        'molecules': [lista de moléculas válidas],
        'count': int,
        'details': {...}
    }
    """
    
    # Mapear tipo numérico para forma
    type_map = {
        1: 'circle',
        2: 'square',
        3: 'triangle',
        4: 'pentagon'
    }
    
    # 0 ou None = qualquer tipo (sem filtro)
    preferred_shape = type_map.get(particle_type) if particle_type and particle_type > 0 else None
    
    # Todas as partículas têm massa 1
    num_particles = target_mass
    
    if num_particles < 1:
        return {
            'success': False,
            'molecules': [],
            'count': 0,
            'details': {'error': 'Massa deve ser maior que 0'}
        }
    
    # Limitar para evitar explosão combinatória
    if num_particles > 6:
        return {
            'success': False,
            'molecules': [],
            'count': 0,
            'details': {
                'error': f'Massa muito alta ({num_particles}). Máximo: 6 partículas',
                'num_particles': num_particles
            }
        }
    
    # PASSO 1: Gerar todas as combinações de tipos de partículas
    all_shapes = ['circle', 'square', 'triangle', 'pentagon']
    type_combinations = []
    
    # Gerar combinações de tipos (com repetição)
    for combo in itertools.product(all_shapes, repeat=num_particles):
        # Se há tipo preferido, filtrar apenas combinações que o contêm
        if preferred_shape and preferred_shape not in combo:
            continue
        
        # Normalizar (ordenar) para evitar duplicatas
        normalized = tuple(sorted(combo))
        if normalized not in type_combinations:
            type_combinations.append(normalized)
    
    # PASSO 2: Para cada combinação de tipos, gerar polaridades e ligações
    unique_molecules = []
    attempted_count = 0
    
    for types_combo in type_combinations:
        # Gerar combinações de polaridades
        polarity_combinations = generate_polarity_combinations(num_particles)
        
        for polarities in polarity_combinations:
            # Criar partículas
            particles = []
            for i in range(num_particles):
                particles.append({
                    'id': f'p{i}',
                    'type': types_combo[i],
                    'polarity': polarities[i],
                    'x': i * 2.0,
                    'y': 0.0
                })
            
            # Gerar estruturas de ligações
            bond_structures = generate_bond_structures(particles)
            
            for bonds in bond_structures:
                attempted_count += 1
                
                # Criar molécula candidata
                candidate = {
                    'particles': copy.deepcopy(particles),
                    'bonds': copy.deepcopy(bonds)
                }
                
                # Verificar se é conectada
                components = find_connected_components(candidate)
                if len(components) != 1:
                    continue
                
                # Verificar se todas as partículas estão estáveis
                if not is_molecule_stable(candidate):
                    continue
                
                # Reorganizar posições (função central)
                reorganize_positions(candidate)
                
                # Analisar características estruturais
                structure_info = analyze_molecule_structure(candidate)
                candidate['structure'] = structure_info
                
                # Verificar se já existe
                if not molecule_exists_in_list(candidate, unique_molecules):
                    unique_molecules.append(candidate)
    
    return {
        'success': True,
        'molecules': unique_molecules,
        'count': len(unique_molecules),
        'details': {
            'particle_type': particle_type,
            'preferred_shape': preferred_shape,
            'target_mass': target_mass,
            'num_particles': num_particles,
            'attempted': attempted_count,
            'type_combinations': len(type_combinations)
        }
    }


def generate_polarity_combinations(num_particles):
    """
    Gera TODAS as combinações possíveis de polaridades para N partículas.
    
    Por exemplo, para 3 partículas:
    ['+', '+', '+']
    ['+', '+', '-']
    ['+', '-', '+']
    ['-', '+', '+']
    ['+', '-', '-']
    ['-', '+', '-']
    ['-', '-', '+']
    ['-', '-', '-']
    
    Total: 2^N combinações
    """
    # Gerar todas as combinações (sem normalização)
    # A verificação de duplicatas será feita estruturalmente depois
    combinations = []
    
    for combo in itertools.product(['+', '-'], repeat=num_particles):
        combinations.append(list(combo))
    
    return combinations


def generate_bond_structures(particles):
    """
    Gera estruturas de ligações válidas para um conjunto de partículas mistas.
    
    Uma estrutura válida:
    - Cada partícula respeita seu limite de conexões (circle=1, square=2, etc)
    - Partículas do mesmo tipo não se ligam
    - Partículas só se ligam com polaridades opostas (+ com -)
    - A estrutura forma um grafo conectado (verificado externamente)
    """
    n = len(particles)
    
    if n == 1:
        return [[]]
    
    # Gerar todas as ligações possíveis entre pares válidos
    all_bonds = []
    for i in range(n):
        for j in range(i + 1, n):
            p1 = particles[i]
            p2 = particles[j]
            
            # REGRA 1: Tipos iguais não se ligam
            if p1['type'] == p2['type']:
                continue
            
            # REGRA 2: Polaridades opostas obrigatórias
            if p1['polarity'] == p2['polarity']:
                continue
            
            # Obter limites de conexão
            max_conn_i = PARTICLE_TYPES[p1['type']]['connections']
            max_conn_j = PARTICLE_TYPES[p2['type']]['connections']
            
            # Multiplicidade máxima possível
            max_mult = min(max_conn_i, max_conn_j, 3)
            
            for mult in range(1, max_mult + 1):
                all_bonds.append({
                    'from': p1['id'],
                    'to': p2['id'],
                    'multiplicity': mult
                })
    
    if len(all_bonds) == 0:
        return [[]]  # Nenhuma ligação possível
    
    # Gerar combinações de ligações (limite para evitar explosão)
    valid_structures = []
    max_bonds_to_try = min(len(all_bonds), n * 2)
    
    for r in range(1, max_bonds_to_try + 1):
        for bond_combo in itertools.combinations(all_bonds, r):
            bonds_list = list(bond_combo)
            
            if is_valid_bond_structure(bonds_list, particles):
                valid_structures.append(bonds_list)
    
    return valid_structures


def is_valid_bond_structure(bonds, particles):
    """
    Verifica se uma estrutura de ligações é válida.
    """
    connection_count = {p['id']: 0 for p in particles}
    seen_pairs = set()
    
    for bond in bonds:
        # Verificar duplicatas
        pair = tuple(sorted([bond['from'], bond['to']]))
        if pair in seen_pairs:
            return False
        seen_pairs.add(pair)
        
        # Contar conexões
        connection_count[bond['from']] += bond['multiplicity']
        connection_count[bond['to']] += bond['multiplicity']
    
    # Verificar se alguma partícula excedeu seu limite
    for particle in particles:
        pid = particle['id']
        max_conn = PARTICLE_TYPES[particle['type']]['connections']
        if connection_count[pid] > max_conn:
            return False
    
    return True


def is_molecule_stable(molecule):
    """
    Verifica se todas as partículas estão estáveis (atingiram seu limite de conexões).
    """
    connection_count = {p['id']: 0 for p in molecule['particles']}
    
    for bond in molecule['bonds']:
        connection_count[bond['from']] += bond['multiplicity']
        connection_count[bond['to']] += bond['multiplicity']
    
    for particle in molecule['particles']:
        max_conn = PARTICLE_TYPES[particle['type']]['connections']
        if connection_count[particle['id']] != max_conn:
            return False
    
    return True


def molecule_exists_in_list(molecule, molecule_list):
    """
    Verifica se uma molécula já existe na lista (comparação estrutural).
    """
    for existing in molecule_list:
        if are_molecules_identical(molecule, existing):
            return True
    return False


def are_molecules_identical(mol1, mol2):
    """
    Compara duas moléculas estruturalmente.
    Duas moléculas são idênticas se têm a mesma composição e estrutura de ligações.
    """
    # Verificar número de partículas
    if len(mol1['particles']) != len(mol2['particles']):
        return False
    
    # Verificar número de ligações
    if len(mol1['bonds']) != len(mol2['bonds']):
        return False
    
    # Contar tipos e polaridades de partículas
    def get_particle_signature(mol):
        particles = mol['particles']
        signature = {}
        for p in particles:
            key = (p['type'], p['polarity'])
            signature[key] = signature.get(key, 0) + 1
        return signature
    
    if get_particle_signature(mol1) != get_particle_signature(mol2):
        return False
    
    # Contar estrutura de ligações (tipos de partículas + multiplicidade)
    def get_bond_signature(mol):
        bonds = mol['bonds']
        particles = {p['id']: (p['type'], p['polarity']) for p in mol['particles']}
        
        bond_sig = []
        for bond in bonds:
            from_type = particles[bond['from']]
            to_type = particles[bond['to']]
            # Normalizar ordem
            pair = tuple(sorted([from_type, to_type]))
            bond_sig.append((pair, bond['multiplicity']))
        
        return sorted(bond_sig)
    
    return get_bond_signature(mol1) == get_bond_signature(mol2)
