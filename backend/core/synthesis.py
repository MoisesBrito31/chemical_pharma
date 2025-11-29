"""
Sistema de Síntese de Moléculas
Realiza a mistura de duas moléculas seguindo as regras
"""

from .validator import quick_validate
import copy
from collections import deque


def synthesize(molecule_a, molecule_b):
    """
    Sintetiza duas moléculas seguindo os passos:
    
    PASSO 1: Anulação - Remove partículas com símbolos iguais e sinais opostos
    PASSO 2: Soma em novo - Junta compostos restantes com IDs renomeados
    PASSO 3: Rebonds - Reconstrói ligações faltantes
    PASSO 4: Reorganiza posições - Ajusta x,y para visualização (partículas ligadas próximas)
    
    Returns: {
        'success': bool,
        'result': molecule or None,
        'details': {...}
    }
    """
    
    initial_count_a = len(molecule_a.get('particles', []))
    initial_count_b = len(molecule_b.get('particles', []))
    initial_count = initial_count_a + initial_count_b
    
    # PASSO 1: ANULAÇÃO
    mol_a_cleaned, mol_b_cleaned, annihilated_pairs = annihilate_particles(
        copy.deepcopy(molecule_a), 
        copy.deepcopy(molecule_b)
    )
    
    # REGRA: Se nada foi anulado, não há reação química válida
    if annihilated_pairs == 0:
        return {
            'success': False,
            'result': None,
            'details': {
                'reason': 'no_reaction',
                'message': 'Nenhuma partícula anulada - não há reação química',
                'initial_count': initial_count,
                'annihilated_pairs': 0
            }
        }
    
    # Se não sobrou nada (anulação completa)
    if len(mol_a_cleaned['particles']) == 0 and len(mol_b_cleaned['particles']) == 0:
        return {
            'success': False,
            'result': None,
            'details': {
                'reason': 'complete_annihilation',
                'initial_count': initial_count,
                'annihilated_pairs': annihilated_pairs
            }
        }
    
    # PASSO 2: SOMA EM NOVO (merge das moléculas limpas)
    merged = merge_molecules(mol_a_cleaned, mol_b_cleaned)
    
    remaining_particles = len(merged['particles'])
    
    # PASSO 3: REBONDS (reconstrói ligações faltantes)
    result = rebond_molecule(merged)
    
    if result is None:
        return {
            'success': False,
            'result': None,
            'details': {
                'reason': 'cannot_rebond',
                'initial_count': initial_count,
                'remaining_particles': remaining_particles,
                'annihilated_pairs': annihilated_pairs
            }
        }
    
    # VERIFICAÇÃO: Detectar se há múltiplos componentes (moléculas separadas)
    components = find_connected_components(result)
    
    if len(components) > 1:
        # Resultado tem múltiplas moléculas desconectadas - separar cada uma
        separate_molecules = split_into_molecules(result, components)
        
        # Reorganizar posições de cada molécula separadamente
        for mol in separate_molecules:
            reorganize_positions(mol)
        
        return {
            'success': True,
            'result': separate_molecules,  # Array de moléculas
            'multiple': True,
            'details': {
                'initial_count': initial_count,
                'remaining_particles': remaining_particles,
                'annihilated_pairs': annihilated_pairs,
                'molecules_count': len(separate_molecules)
            }
        }
    
    # PASSO 4: REORGANIZA POSIÇÕES (ajusta x,y para visualização clara)
    reorganize_positions(result)
    
    return {
        'success': True,
        'result': result,  # Molécula única
        'multiple': False,
        'details': {
            'initial_count': initial_count,
            'remaining_particles': remaining_particles,
            'annihilated_pairs': annihilated_pairs
        }
    }


def find_connected_components(molecule):
    """
    Encontra todos os componentes conectados de uma molécula.
    
    Returns: Lista de conjuntos, cada conjunto contém os IDs das partículas
             de um componente conectado.
             
    Exemplo: [{'p0', 'p1'}, {'p2', 'p3', 'p4'}] = 2 moléculas separadas
    """
    particles = molecule.get('particles', [])
    bonds = molecule.get('bonds', [])
    
    if len(particles) == 0:
        return []
    
    # Construir grafo de adjacência
    adjacency = {p['id']: [] for p in particles}
    for bond in bonds:
        adjacency[bond['from']].append(bond['to'])
        adjacency[bond['to']].append(bond['from'])
    
    # Encontrar componentes usando BFS
    visited = set()
    components = []
    
    for particle in particles:
        pid = particle['id']
        if pid in visited:
            continue
        
        # BFS para este componente
        component = set()
        queue = deque([pid])
        component.add(pid)
        visited.add(pid)
        
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        
        components.append(component)
    
    return components


def split_into_molecules(molecule, components):
    """
    Divide uma molécula em múltiplas moléculas baseado nos componentes.
    
    Args:
        molecule: Molécula original
        components: Lista de conjuntos de IDs (resultado de find_connected_components)
    
    Returns: Lista de moléculas separadas
    """
    molecules = []
    
    for component in components:
        # Filtrar partículas deste componente
        particles = [p for p in molecule['particles'] if p['id'] in component]
        
        # Filtrar bonds deste componente
        bonds = [
            b for b in molecule['bonds']
            if b['from'] in component and b['to'] in component
        ]
        
        molecules.append({
            'particles': particles,
            'bonds': bonds
        })
    
    return molecules


def annihilate_particles(molecule_a, molecule_b):
    """
    PASSO 1: Remove pares de partículas com mesmo tipo mas polaridades opostas
    
    Returns: (molecule_a_cleaned, molecule_b_cleaned, annihilated_count)
    """
    annihilated_pairs = 0
    
    particles_a = molecule_a['particles']
    particles_b = molecule_b['particles']
    bonds_a = molecule_a['bonds']
    bonds_b = molecule_b['bonds']
    
    # Marcar partículas para remoção
    to_remove_a = set()
    to_remove_b = set()
    
    for pa in particles_a:
        if pa['id'] in to_remove_a:
            continue
        
        for pb in particles_b:
            if pb['id'] in to_remove_b:
                continue
            
            # Verificar se são do mesmo tipo mas polaridades opostas
            if pa['type'] == pb['type'] and pa['polarity'] != pb['polarity']:
                to_remove_a.add(pa['id'])
                to_remove_b.add(pb['id'])
                annihilated_pairs += 1
                break
    
    # Remover partículas anuladas
    molecule_a['particles'] = [p for p in particles_a if p['id'] not in to_remove_a]
    molecule_b['particles'] = [p for p in particles_b if p['id'] not in to_remove_b]
    
    # Remover bonds que referenciam partículas anuladas
    molecule_a['bonds'] = [
        b for b in bonds_a 
        if b['from'] not in to_remove_a and b['to'] not in to_remove_a
    ]
    molecule_b['bonds'] = [
        b for b in bonds_b 
        if b['from'] not in to_remove_b and b['to'] not in to_remove_b
    ]
    
    return molecule_a, molecule_b, annihilated_pairs


def merge_molecules(molecule_a, molecule_b):
    """
    PASSO 2: Junta as duas moléculas em uma nova, renomeando IDs
    
    Para garantir comutatividade (A+B = B+A), combinamos e ordenamos
    todas as partículas antes de atribuir novos IDs
    """
    # Coletar todas as partículas de ambas as moléculas
    all_particles = []
    all_bonds = []
    
    # Marcar origem de cada partícula e bond para mapeamento posterior
    for particle in molecule_a['particles']:
        all_particles.append({
            'origin': 'a',
            'old_id': particle['id'],
            'type': particle['type'],
            'polarity': particle['polarity'],
            'x': particle.get('x', 0),
            'y': particle.get('y', 0)
        })
    
    for bond in molecule_a['bonds']:
        all_bonds.append({
            'origin': 'a',
            'from': bond['from'],
            'to': bond['to'],
            'multiplicity': bond['multiplicity']
        })
    
    for particle in molecule_b['particles']:
        all_particles.append({
            'origin': 'b',
            'old_id': particle['id'],
            'type': particle['type'],
            'polarity': particle['polarity'],
            'x': particle.get('x', 0),
            'y': particle.get('y', 0)
        })
    
    for bond in molecule_b['bonds']:
        all_bonds.append({
            'origin': 'b',
            'from': bond['from'],
            'to': bond['to'],
            'multiplicity': bond['multiplicity']
        })
    
    # Ordenar partículas para garantir ordem consistente
    # Ordem: tipo, depois polaridade
    type_order = {'circle': 0, 'square': 1, 'triangle': 2, 'pentagon': 3}
    all_particles.sort(key=lambda p: (type_order.get(p['type'], 999), p['polarity']))
    
    # Criar mapeamento de IDs antigos para novos
    id_map = {}
    new_particles = []
    
    for idx, particle in enumerate(all_particles):
        new_id = f'p{idx}'
        old_key = f"{particle['origin']}_{particle['old_id']}"
        id_map[old_key] = new_id
        
        new_particles.append({
            'id': new_id,
            'type': particle['type'],
            'polarity': particle['polarity'],
            'x': particle['x'],
            'y': particle['y']
        })
    
    # Atualizar bonds com novos IDs
    new_bonds = []
    for bond in all_bonds:
        from_key = f"{bond['origin']}_{bond['from']}"
        to_key = f"{bond['origin']}_{bond['to']}"
        
        new_bonds.append({
            'from': id_map[from_key],
            'to': id_map[to_key],
            'multiplicity': bond['multiplicity']
        })
    
    return {
        'particles': new_particles,
        'bonds': new_bonds
    }


def rebond_molecule(molecule):
    """
    PASSO 3: Reconstrói ligações para estabilizar partículas instáveis
    
    Tenta criar ligações entre partículas que estão abaixo do limite de conexões,
    seguindo as regras:
    - Partículas do mesmo tipo não podem se ligar
    - Uma partícula pode aumentar multiplicidade de bond existente
    - Adiciona uma ligação por vez, testando todas possibilidades
    """
    from data.molecules import PARTICLE_TYPES
    
    MAX_ITERATIONS = 100
    iteration = 0
    
    while iteration < MAX_ITERATIONS:
        iteration += 1
        
        # Calcular conexões atuais
        connection_count = calculate_connections(molecule)
        
        # Encontrar partículas instáveis (abaixo do limite)
        unstable = []
        for particle in molecule['particles']:
            pid = particle['id']
            ptype = particle['type']
            max_conn = PARTICLE_TYPES[ptype]['connections']
            current_conn = connection_count.get(pid, 0)
            
            if current_conn < max_conn:
                unstable.append({
                    'id': pid,
                    'type': ptype,
                    'missing': max_conn - current_conn
                })
        
        # Ordenar por quantidade de conexões faltantes (maior primeiro)
        # Isso prioriza partículas que precisam de mais conexões
        unstable.sort(key=lambda x: x['missing'], reverse=True)
        
        # Se não há partículas instáveis, molécula está estável!
        if not unstable:
            return molecule
        
        # Tentar criar UMA nova ligação
        bond_created = False
        
        for u1 in unstable:
            if bond_created:
                break
            
            p1 = next(p for p in molecule['particles'] if p['id'] == u1['id'])
            
            for u2 in unstable:
                if u1['id'] == u2['id']:
                    continue
                
                p2 = next(p for p in molecule['particles'] if p['id'] == u2['id'])
                
                # Verificar se podem se ligar (tipos diferentes)
                if p1['type'] == p2['type']:
                    continue
                
                # Verificar se já existe bond entre eles
                existing_bond = find_bond(molecule, u1['id'], u2['id'])
                
                if existing_bond:
                    # Tentar aumentar multiplicidade
                    max_multiplicity = min(u1['missing'], u2['missing'])
                    if max_multiplicity > 0:
                        existing_bond['multiplicity'] += 1
                        bond_created = True
                        break
                else:
                    # Criar nova ligação
                    molecule['bonds'].append({
                        'from': u1['id'],
                        'to': u2['id'],
                        'multiplicity': 1
                    })
                    bond_created = True
                    break
        
        # Se não conseguiu criar nenhuma ligação, falhou
        if not bond_created:
            return None
    
    # Excedeu iterações máximas
    return None


def find_bond(molecule, id1, id2):
    """Encontra um bond entre duas partículas (bidirecional)"""
    for bond in molecule['bonds']:
        if (bond['from'] == id1 and bond['to'] == id2) or \
           (bond['from'] == id2 and bond['to'] == id1):
            return bond
    return None


def calculate_connections(molecule):
    """Calcula o número de conexões de cada partícula"""
    connection_count = {p['id']: 0 for p in molecule['particles']}
    
    for bond in molecule['bonds']:
        connection_count[bond['from']] += bond['multiplicity']
        connection_count[bond['to']] += bond['multiplicity']
    
    return connection_count


def reorganize_positions(molecule):
    """
    PASSO 4: Reorganiza posições das partículas para visualização clara
    
    Estratégias de layout:
    - Detecta ciclos e os posiciona como polígonos regulares
    - Usa BFS para estruturas em árvore/estrela
    - Evita sobreposições e colisões
    """
    import math
    
    if not molecule['particles']:
        return
    
    # Construir grafo de adjacências (usado por todas as estratégias)
    adjacency = {p['id']: [] for p in molecule['particles']}
    for bond in molecule['bonds']:
        adjacency[bond['from']].append(bond['to'])
        adjacency[bond['to']].append(bond['from'])
    
    # ESTRATÉGIA 1: Detectar ciclos (estruturas circulares)
    cycle = _detect_cycle(adjacency, molecule['particles'])
    
    if cycle:
        # Layout circular para ciclos
        _layout_as_polygon(molecule, cycle, adjacency)
    else:
        # ESTRATÉGIA 2: Layout BFS melhorado para grafos densos
        _layout_as_tree(molecule, adjacency)
    
    # Otimização final: centralizar partículas com múltiplas conexões
    _optimize_centered_particles(molecule, adjacency)


def _detect_cycle(adjacency, particles):
    """
    Detecta ciclos usando DFS e retorna lista de IDs do ciclo.
    Retorna None se não houver ciclo.
    """
    if len(particles) < 3:
        return None
    
    visited = set()
    parent = {}
    
    def dfs(node, par):
        visited.add(node)
        parent[node] = par
        
        for neighbor in adjacency[node]:
            if neighbor not in visited:
                cycle = dfs(neighbor, node)
                if cycle:
                    return cycle
            elif neighbor != par:
                # Ciclo encontrado - reconstruir caminho
                cycle_nodes = [neighbor, node]
                current = node
                while parent[current] != neighbor and parent[current] is not None:
                    current = parent[current]
                    cycle_nodes.insert(1, current)
                return cycle_nodes
        return None
    
    # Tentar DFS a partir de cada partícula
    for particle in particles:
        if particle['id'] not in visited:
            cycle = dfs(particle['id'], None)
            if cycle:
                return cycle
    
    return None


def _layout_as_polygon(molecule, cycle_ids, adjacency):
    """
    Posiciona ciclo como polígono regular (triângulo, quadrado, pentágono, etc).
    
    Lógica para partículas extras:
    - Se conecta com 1 partícula do ciclo → FORA do ciclo
    - Se conecta com 2+ partículas do ciclo → DENTRO do ciclo
    """
    import math
    
    n = len(cycle_ids)
    RADIUS = 3.0
    
    # Posicionar partículas do ciclo em círculo (coordenadas inteiras)
    angle_step = (2 * math.pi) / n
    for i, pid in enumerate(cycle_ids):
        angle = i * angle_step - math.pi / 2  # Começar do topo
        particle = next(p for p in molecule['particles'] if p['id'] == pid)
        particle['x'] = round(RADIUS * math.cos(angle))
        particle['y'] = round(RADIUS * math.sin(angle))
    
    positioned = set(cycle_ids)
    
    # Identificar partículas não posicionadas
    unpositioned = [p['id'] for p in molecule['particles'] if p['id'] not in positioned]
    
    # Para cada partícula não posicionada
    for pid in unpositioned:
        # Contar conexões com o ciclo
        connections_to_cycle = [n for n in adjacency[pid] if n in cycle_ids]
        num_connections = len(connections_to_cycle)
        
        if num_connections == 0:
            # Sem conexão com ciclo, pular (BFS vai posicionar depois)
            continue
        
        if num_connections == 1:
            # REGRA 1: Conecta com apenas 1 → colocar FORA do ciclo
            cycle_neighbor_id = connections_to_cycle[0]
            cycle_neighbor = next(p for p in molecule['particles'] if p['id'] == cycle_neighbor_id)
            
            # Direção para fora (radial)
            angle_to_center = math.atan2(cycle_neighbor['y'], cycle_neighbor['x'])
            
            particle = next(p for p in molecule['particles'] if p['id'] == pid)
            particle['x'] = round(cycle_neighbor['x'] + RADIUS * 1.2 * math.cos(angle_to_center))
            particle['y'] = round(cycle_neighbor['y'] + RADIUS * 1.2 * math.sin(angle_to_center))
            positioned.add(pid)
            
        else:
            # REGRA 2: Conecta com 2+ → colocar DENTRO do ciclo (centro)
            # Calcular centroide das partículas do ciclo conectadas
            connected_particles = [
                next(p for p in molecule['particles'] if p['id'] == cid) 
                for cid in connections_to_cycle
            ]
            
            center_x = sum(p['x'] for p in connected_particles) / len(connected_particles)
            center_y = sum(p['y'] for p in connected_particles) / len(connected_particles)
            
            # Posicionar no centroide (DENTRO do ciclo)
            particle = next(p for p in molecule['particles'] if p['id'] == pid)
            particle['x'] = round(center_x)
            particle['y'] = round(center_y)
            positioned.add(pid)


def _layout_as_tree(molecule, adjacency):
    """
    Layout BFS melhorado para estruturas em árvore e grafos densos.
    Usa espaçamento adaptativo baseado no número de conexões.
    """
    import math
    
    # Resetar posições
    for particle in molecule['particles']:
        particle['x'] = 0
        particle['y'] = 0
    
    # Encontrar partícula com mais conexões como ponto inicial
    # Em caso de empate, usa prioridade por tipo (pentagon > triangle > square > circle)
    type_priority = {'pentagon': 4, 'triangle': 3, 'square': 2, 'circle': 1}
    
    start_particle = max(
        molecule['particles'],
        key=lambda p: (len(adjacency[p['id']]), type_priority.get(p['type'], 0))
    )
    start_id = start_particle['id']
    
    # BFS para posicionar partículas
    visited = set()
    queue = [(start_id, 0, 0, None)]
    visited.add(start_id)
    
    # Mapa de posições para evitar sobreposições
    position_map = {}
    
    # Espaçamento aumentado para grafos densos
    BASE_SPACING = 4  # Aumentado de 2 para 4
    
    # Direções expandidas (coordenadas inteiras)
    directions = [
        (BASE_SPACING, 0),               # Direita
        (-BASE_SPACING, 0),              # Esquerda
        (0, BASE_SPACING),               # Cima
        (0, -BASE_SPACING),              # Baixo
        (BASE_SPACING, BASE_SPACING),    # Diagonal SE
        (BASE_SPACING, -BASE_SPACING),   # Diagonal NE
        (-BASE_SPACING, BASE_SPACING),   # Diagonal SW
        (-BASE_SPACING, -BASE_SPACING),  # Diagonal NW
    ]
    
    while queue:
        current_id, x, y, parent_id = queue.pop(0)
        
        # Atualizar posição da partícula
        particle = next(p for p in molecule['particles'] if p['id'] == current_id)
        particle['x'] = x
        particle['y'] = y
        position_map[(x, y)] = current_id
        
        # Obter vizinhos não visitados
        neighbors = [n for n in adjacency[current_id] if n not in visited]
        
        # Posicionar cada vizinho
        dir_idx = 0
        angle_offset = 0
        
        for neighbor_id in neighbors:
            visited.add(neighbor_id)
            
            # Tentar diferentes posições até achar uma livre
            pos_found = False
            attempts = 0
            max_attempts = 20
            
            while not pos_found and attempts < max_attempts:
                if dir_idx < len(directions):
                    dx, dy = directions[dir_idx]
                else:
                    # Posições circulares para muitas ramificações (coordenadas inteiras)
                    angle = angle_offset * (2 * math.pi / max(len(neighbors), 8))
                    radius = 2 + (angle_offset // 8) * 2
                    dx = round(radius * math.cos(angle))
                    dy = round(radius * math.sin(angle))
                    angle_offset += 1
                
                new_x = round(x + dx)
                new_y = round(y + dy)
                
                # Verificar se posição está livre
                if (new_x, new_y) not in position_map:
                    queue.append((neighbor_id, new_x, new_y, current_id))
                    pos_found = True
                else:
                    dir_idx += 1
                    attempts += 1
            
            # Se não achou posição livre, usar qualquer uma (coordenadas inteiras)
            if not pos_found:
                dx, dy = directions[dir_idx % len(directions)]
                new_x = round(x + dx + attempts)
                new_y = round(y + dy + attempts)
                queue.append((neighbor_id, new_x, new_y, current_id))
            
            dir_idx += 1
    
    # Centralizar molécula (manter coordenadas inteiras)
    if molecule['particles']:
        avg_x = sum(p['x'] for p in molecule['particles']) / len(molecule['particles'])
        avg_y = sum(p['y'] for p in molecule['particles']) / len(molecule['particles'])
        
        for particle in molecule['particles']:
            particle['x'] = round(particle['x'] - avg_x)
            particle['y'] = round(particle['y'] - avg_y)


def _optimize_centered_particles(molecule, adjacency):
    """
    Otimização final: centraliza partículas com 3+ conexões entre seus vizinhos.
    Usa iterações suaves com verificação de colisão.
    """
    import math
    
    ITERATIONS = 5
    DAMPING = 0.15
    MIN_DISTANCE = 2.0
    
    for iteration in range(ITERATIONS):
        forces = {p['id']: {'x': 0, 'y': 0} for p in molecule['particles']}
        
        # Calcular forças de centralização
        for particle in molecule['particles']:
            pid = particle['id']
            neighbors = adjacency[pid]
            
            # Apenas para partículas com múltiplas conexões
            if len(neighbors) < 3:
                continue
            
            # Centroide dos vizinhos
            center_x = sum(next(p for p in molecule['particles'] if p['id'] == nid)['x'] 
                          for nid in neighbors) / len(neighbors)
            center_y = sum(next(p for p in molecule['particles'] if p['id'] == nid)['y'] 
                          for nid in neighbors) / len(neighbors)
            
            # Força suave em direção ao centroide
            forces[pid]['x'] = (center_x - particle['x']) * DAMPING
            forces[pid]['y'] = (center_y - particle['y']) * DAMPING
        
        # Aplicar forças com verificação de colisão (manter coordenadas inteiras)
        for particle in molecule['particles']:
            new_x = round(particle['x'] + forces[particle['id']]['x'])
            new_y = round(particle['y'] + forces[particle['id']]['y'])
            
            # Verificar colisões
            collision = False
            for other in molecule['particles']:
                if other['id'] == particle['id']:
                    continue
                
                dist = math.sqrt((new_x - other['x'])**2 + (new_y - other['y'])**2)
                if dist < MIN_DISTANCE:
                    collision = True
                    break
            
            # Aplicar movimento se seguro
            if not collision:
                particle['x'] = new_x
                particle['y'] = new_y

