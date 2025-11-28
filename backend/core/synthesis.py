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
    
    Usa BFS para distribuir partículas em 2D:
    - Partículas ligadas ficam próximas
    - Ramificações usam o eixo Y
    - Evita sobreposições
    """
    import math
    
    if not molecule['particles']:
        return
    
    # Resetar todas as posições primeiro
    for particle in molecule['particles']:
        particle['x'] = 0
        particle['y'] = 0
    
    # Construir grafo de adjacências
    adjacency = {p['id']: [] for p in molecule['particles']}
    for bond in molecule['bonds']:
        adjacency[bond['from']].append(bond['to'])
        adjacency[bond['to']].append(bond['from'])
    
    # BFS para posicionar partículas
    visited = set()
    start_id = molecule['particles'][0]['id']
    
    # Fila: (id, x, y, parent_id)
    queue = [(start_id, 0, 0, None)]
    visited.add(start_id)
    
    # Mapa de posições para evitar sobreposições
    position_map = {}
    
    # Direções expandidas para ramificações
    directions = [
        (2, 0),   # Direita
        (-2, 0),  # Esquerda
        (0, 2),   # Cima
        (0, -2),  # Baixo
        (1.5, 1.5),   # Diagonal SE
        (1.5, -1.5),  # Diagonal NE
        (-1.5, 1.5),  # Diagonal SW
        (-1.5, -1.5), # Diagonal NW
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
                    # Posições circulares para muitas ramificações
                    angle = angle_offset * (2 * math.pi / max(len(neighbors), 8))
                    radius = 2 + (angle_offset // 8) * 1.5
                    dx = radius * math.cos(angle)
                    dy = radius * math.sin(angle)
                    angle_offset += 1
                
                new_x = x + dx
                new_y = y + dy
                
                # Verificar se posição está livre
                if (new_x, new_y) not in position_map:
                    queue.append((neighbor_id, new_x, new_y, current_id))
                    pos_found = True
                else:
                    dir_idx += 1
                    attempts += 1
            
            # Se não achou posição livre, usar qualquer uma
            if not pos_found:
                dx, dy = directions[dir_idx % len(directions)]
                new_x = x + dx + (attempts * 0.3)
                new_y = y + dy + (attempts * 0.3)
                queue.append((neighbor_id, new_x, new_y, current_id))
            
            dir_idx += 1
    
    # Centralizar molécula (mover para que o centro seja próximo de 0,0)
    if molecule['particles']:
        avg_x = sum(p['x'] for p in molecule['particles']) / len(molecule['particles'])
        avg_y = sum(p['y'] for p in molecule['particles']) / len(molecule['particles'])
        
        for particle in molecule['particles']:
            particle['x'] -= avg_x
            particle['y'] -= avg_y

