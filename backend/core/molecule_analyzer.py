"""
Analisador de Características Estruturais de Moléculas

Detecta propriedades estruturais que podem ser usadas para:
- Debug e visualização
- Efeitos e propriedades químicas (ex: cadeia circular = sabor azedo)
"""

def analyze_molecule_structure(molecule):
    """
    Analisa a estrutura de uma molécula e retorna suas características.
    
    Returns: {
        'has_cycle': bool,           # Tem cadeia circular?
        'topology': str,             # linear, Y, X, tree, star, complex
        'branch_count': int,         # Número de ramificações
        'max_degree': int,           # Grau máximo (máx conexões de uma partícula)
        'is_connected': bool         # Molécula é conectada?
    }
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    if len(particles) == 0:
        return {
            'has_cycle': False,
            'topology': 'empty',
            'branch_count': 0,
            'max_degree': 0,
            'is_connected': False
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
    has_cycle = _has_cycle_dfs(adjacency, particles)
    
    # Detectar conectividade
    is_connected = _is_fully_connected(adjacency, particles)
    
    # Classificar topologia
    topology = _classify_topology(adjacency, particles, degrees, has_cycle)
    
    # Contar ramificações (partículas com grau >= 3)
    branch_count = sum(1 for degree in degrees.values() if degree >= 3)
    
    return {
        'has_cycle': has_cycle,
        'topology': topology,
        'branch_count': branch_count,
        'max_degree': max_degree,
        'is_connected': is_connected
    }


def _has_cycle_dfs(adjacency, particles):
    """
    Detecta se há ciclo usando DFS.
    """
    if len(particles) < 3:
        return False
    
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in adjacency[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # Encontrou ciclo
        return False
    
    for particle in particles:
        if particle['id'] not in visited:
            if dfs(particle['id'], None):
                return True
    
    return False


def _is_fully_connected(adjacency, particles):
    """
    Verifica se o grafo é totalmente conectado (BFS).
    """
    if len(particles) == 0:
        return False
    
    visited = set()
    queue = [particles[0]['id']]
    visited.add(particles[0]['id'])
    
    while queue:
        current = queue.pop(0)
        for neighbor in adjacency[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return len(visited) == len(particles)


def _classify_topology(adjacency, particles, degrees, has_cycle):
    """
    Classifica a topologia da molécula baseado nas EXTREMIDADES (partículas com grau 1).
    
    Tipos:
    - single: 1 partícula
    - linear: 2 extremidades
    - Y: 3 extremidades
    - X: 4 extremidades
    - tree: mais de 4 extremidades
    - cycle: ciclo simples (anel fechado, 0 extremidades)
    - mista: tem ciclo + qualquer número de extremidades
    """
    n = len(particles)
    
    # Caso: 1 partícula
    if n == 1:
        return 'single'
    
    # Contar extremidades (partículas com grau 1)
    endpoints = sum(1 for degree in degrees.values() if degree == 1)
    
    # COM CICLO - verificar se tem extremidades
    if has_cycle:
        # Se tem ciclo mas NÃO tem extremidades → anel puro (cycle)
        if endpoints == 0:
            return 'cycle'
        # Se tem ciclo E tem extremidades → estrutura mista
        else:
            return 'mista'
    
    # SEM CICLO - classificar por número de extremidades
    if endpoints == 0:
        # Sem extremidades = ciclo fechado (mas sem ciclo detectado? pode ser grafo completo)
        # Se todos têm grau 2, é um ciclo
        if all(d == 2 for d in degrees.values()):
            return 'cycle'
        # Caso especial: grafo completo ou estrutura sem extremidades
        return 'tree'
    
    elif endpoints == 2:
        return 'linear'
    
    elif endpoints == 3:
        return 'Y'
    
    elif endpoints == 4:
        return 'X'
    
    else:  # endpoints > 4
        return 'tree'


def get_topology_emoji(topology):
    """
    Retorna emoji/ícone para cada topologia.
    """
    emoji_map = {
        'single': '●',
        'linear': '━',
        'Y': 'Y',
        'X': 'X',
        'tree': '⋈',
        'cycle': '○',
        'mista': '◈',
        'empty': '∅'
    }
    return emoji_map.get(topology, '?')


def get_topology_description(topology):
    """
    Retorna descrição em português para cada topologia.
    """
    descriptions = {
        'single': 'Partícula única',
        'linear': 'Cadeia linear',
        'Y': 'Ramificação Y',
        'X': 'Ramificação X',
        'tree': 'Árvore ramificada',
        'cycle': 'Ciclo/Anel',
        'mista': 'Estrutura mista',
        'empty': 'Vazio'
    }
    return descriptions.get(topology, 'Desconhecido')

