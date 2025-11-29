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
    Classifica a topologia da molécula.
    
    Tipos:
    - single: 1 partícula
    - linear: cadeia reta (graus: 1-2-1 ou 1-2-2-...-2-1)
    - Y: ramificação simples (1 partícula com grau 3)
    - X: ramificação dupla (1 partícula com grau 4)
    - tree: árvore (sem ciclos, múltiplas ramificações)
    - cycle: ciclo simples (anel)
    - mista: estrutura mista (ciclos + ramificações)
    """
    n = len(particles)
    
    # Caso: 1 partícula
    if n == 1:
        return 'single'
    
    # Caso: 2 partículas
    if n == 2:
        return 'linear'
    
    # Contar distribuição de graus
    degree_counts = {}
    for degree in degrees.values():
        degree_counts[degree] = degree_counts.get(degree, 0) + 1
    
    max_degree = max(degrees.values())
    
    # Linear: apenas graus 1 e 2
    if set(degrees.values()).issubset({1, 2}):
        if not has_cycle:
            return 'linear'
        else:
            return 'cycle'  # Ciclo simples (anel)
    
    # SEM CICLO - classificar por ramificações
    if not has_cycle:
        # Y: Exatamente 1 partícula com grau 3
        if degree_counts.get(3, 0) >= 1 and max_degree == 3:
            return 'Y'
        
        # X: Exatamente 1 partícula com grau 4
        if degree_counts.get(4, 0) >= 1 and max_degree == 4:
            return 'X'
        
        # Tree: Múltiplas partículas com grau >= 3
        hubs = sum(1 for d in degrees.values() if d >= 3)
        if hubs > 1:
            return 'tree'
        
        # Se tem grau 3 ou 4 mas não caiu nos casos acima, é tree
        if max_degree >= 3:
            return 'tree'
        
        return 'linear'  # Fallback
    
    # COM CICLO - estrutura mista (ciclo + ramificações)
    return 'mista'


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

