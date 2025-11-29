"""
Sistema de Análise de Características Moleculares

Detecta propriedades estruturais das moléculas:
- Presença de ciclos (cadeias circulares)
- Topologia (Linear, Y, X, Tree, Star, etc)
- Grau de ramificação
"""

from collections import deque


def analyze_molecule(molecule):
    """
    Analisa uma molécula e retorna suas características estruturais.
    
    Returns: {
        'has_cycle': bool,
        'topology': str,  # 'linear', 'Y', 'X', 'star', 'tree', 'complex'
        'cycle_size': int or None,
        'max_degree': int,  # Grau máximo de conexão
        'branches': int  # Número de ramificações
    }
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    if len(particles) == 0:
        return {
            'has_cycle': False,
            'topology': 'empty',
            'cycle_size': None,
            'max_degree': 0,
            'branches': 0
        }
    
    if len(particles) == 1:
        return {
            'has_cycle': False,
            'topology': 'single',
            'cycle_size': None,
            'max_degree': 0,
            'branches': 0
        }
    
    # Construir grafo de adjacências
    adjacency = {p['id']: [] for p in particles}
    for bond in bonds:
        adjacency[bond['from']].append(bond['to'])
        adjacency[bond['to']].append(bond['from'])
    
    # Calcular graus (número de conexões de cada partícula)
    degrees = {pid: len(neighbors) for pid, neighbors in adjacency.items()}
    max_degree = max(degrees.values()) if degrees else 0
    
    # Detectar ciclo
    has_cycle, cycle_size = detect_cycle_info(adjacency, particles)
    
    # Classificar topologia
    topology = classify_topology(adjacency, particles, degrees, has_cycle)
    
    # Contar ramificações (nós com grau >= 3)
    branches = sum(1 for d in degrees.values() if d >= 3)
    
    return {
        'has_cycle': has_cycle,
        'topology': topology,
        'cycle_size': cycle_size,
        'max_degree': max_degree,
        'branches': branches
    }


def detect_cycle_info(adjacency, particles):
    """
    Detecta se há ciclo e retorna tamanho do ciclo.
    
    Returns: (has_cycle: bool, cycle_size: int or None)
    """
    if len(particles) < 3:
        return False, None
    
    visited = set()
    parent = {}
    
    def dfs(node, par):
        visited.add(node)
        parent[node] = par
        
        for neighbor in adjacency[node]:
            if neighbor not in visited:
                result = dfs(neighbor, node)
                if result[0]:
                    return result
            elif neighbor != par:
                # Ciclo encontrado - calcular tamanho
                cycle_nodes = [neighbor, node]
                current = node
                while parent[current] != neighbor and parent[current] is not None:
                    current = parent[current]
                    cycle_nodes.insert(1, current)
                return True, len(cycle_nodes)
        return False, None
    
    for particle in particles:
        if particle['id'] not in visited:
            has_cycle, size = dfs(particle['id'], None)
            if has_cycle:
                return has_cycle, size
    
    return False, None


def classify_topology(adjacency, particles, degrees, has_cycle):
    """
    Classifica a topologia da molécula.
    
    Topologias:
    - 'linear': Cadeia reta (A-B-C-D)
    - 'Y': 3 pontas, 1 hub central
    - 'X': 4 pontas, 1 hub central (cruz)
    - 'star': Hub central com 4+ pontas
    - 'tree': Estrutura ramificada sem ciclos
    - 'ring': Ciclo simples sem ramificações
    - 'complex': Ciclos com ramificações ou múltiplos hubs
    """
    n = len(particles)
    
    # Contar partículas por grau
    degree_count = {}
    for d in degrees.values():
        degree_count[d] = degree_count.get(d, 0) + 1
    
    # Identificar hubs (grau >= 3)
    hubs = [pid for pid, d in degrees.items() if d >= 3]
    
    # Identificar pontas (grau == 1)
    tips = [pid for pid, d in degrees.items() if d == 1]
    
    # Se tem ciclo
    if has_cycle:
        if len(hubs) == 0:
            return 'ring'  # Ciclo puro sem ramificações
        else:
            return 'complex'  # Ciclo com ramificações
    
    # Sem ciclo
    if n == 2:
        return 'linear'
    
    # Linear: todos têm grau 1 ou 2, com exatamente 2 pontas
    if len(tips) == 2 and len(hubs) == 0:
        return 'linear'
    
    # Única ramificação (hub central)
    if len(hubs) == 1:
        hub_degree = degrees[hubs[0]]
        
        if hub_degree == 3:
            return 'Y'
        elif hub_degree == 4:
            return 'X'
        elif hub_degree >= 5:
            return 'star'
    
    # Múltiplas ramificações
    if len(hubs) >= 2:
        return 'tree'
    
    return 'tree'  # Default para estruturas ramificadas


def get_molecule_properties(molecule):
    """
    Retorna propriedades completas da molécula incluindo características estruturais.
    
    Returns: {
        'mass': int,
        'charge': int,
        'formula': str,
        'has_cycle': bool,
        'topology': str,
        'cycle_size': int or None,
        'max_degree': int,
        'branches': int
    }
    """
    from data.molecules import calculate_molecule_properties
    
    # Propriedades básicas
    basic_props = calculate_molecule_properties(molecule)
    
    # Características estruturais
    structural = analyze_molecule(molecule)
    
    # Combinar
    return {
        **basic_props,
        **structural
    }

