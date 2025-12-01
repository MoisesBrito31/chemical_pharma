"""
Validador de Moléculas
Verifica se uma molécula segue as regras do jogo
"""

from data.molecules import PARTICLE_TYPES


def _is_fully_connected(adjacency, particles):
    """
    Verifica se todas as partículas estão conectadas (BFS).
    """
    if len(particles) == 0:
        return False
    
    if len(particles) == 1:
        return True
    
    # BFS a partir da primeira partícula
    start_id = particles[0]['id']
    visited = set()
    queue = [start_id]
    visited.add(start_id)
    
    while queue:
        current = queue.pop(0)
        for neighbor in adjacency.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # Se visitou todas as partículas, está conectada
    return len(visited) == len(particles)


def _check_same_type_polarity_consistency(particles):
    """
    Verifica se partículas do mesmo tipo têm a mesma polaridade.
    
    Regra: Todas as partículas de um mesmo tipo (circle, square, triangle, pentagon)
           devem ter a mesma polaridade na mesma molécula.
    
    Args:
        particles: Lista de partículas com 'type' e 'polarity'
    
    Returns:
        Lista de strings com mensagens de erro, vazia se não há violações
    """
    errors = []
    
    # Agrupar partículas por tipo
    particles_by_type = {}
    for particle in particles:
        particle_type = particle.get('type')
        if particle_type:
            if particle_type not in particles_by_type:
                particles_by_type[particle_type] = []
            particles_by_type[particle_type].append(particle)
    
    # Verificar se cada tipo tem apenas uma polaridade
    for particle_type, type_particles in particles_by_type.items():
        if len(type_particles) <= 1:
            continue  # Não há conflito possível com apenas uma partícula
        
        # Verificar se todas têm a mesma polaridade
        polarities = set(p.get('polarity') for p in type_particles if 'polarity' in p)
        
        if len(polarities) > 1:
            errors.append(
                f'Partículas do mesmo tipo ({particle_type}) têm polaridades diferentes: {polarities}. '
                f'Todas as partículas do mesmo tipo devem ter a mesma polaridade.'
            )
    
    return errors


def validate_molecule(molecule):
    """
    Valida uma molécula completa
    
    Returns: (is_valid, errors)
    """
    errors = []
    
    # Verificar estrutura básica
    if 'particles' not in molecule:
        errors.append('Molécula não possui partículas')
        return False, errors
    
    if 'bonds' not in molecule:
        errors.append('Molécula não possui ligações')
        return False, errors
    
    particles = molecule['particles']
    bonds = molecule['bonds']
    
    # Verificar se há partículas
    if len(particles) == 0:
        errors.append('Molécula vazia: uma molécula válida deve ter pelo menos 2 partículas')
        return False, errors
    
    # Verificar se há pelo menos 2 partículas (molécula válida)
    if len(particles) == 1:
        errors.append('Molécula inválida: uma molécula válida deve ter pelo menos 2 partículas')
        return False, errors
    
    # Verificar cada partícula
    for particle in particles:
        if 'id' not in particle:
            errors.append('Partícula sem ID')
            continue
        
        if 'type' not in particle:
            errors.append(f'Partícula {particle["id"]} sem tipo')
            continue
        
        if particle['type'] not in PARTICLE_TYPES:
            errors.append(f'Partícula {particle["id"]} com tipo inválido: {particle["type"]}')
            continue
        
        if 'polarity' not in particle:
            errors.append(f'Partícula {particle["id"]} sem polaridade')
            continue
        
        if particle['polarity'] not in ['+', '-']:
            errors.append(f'Partícula {particle["id"]} com polaridade inválida: {particle["polarity"]}')
    
    # Se já há erros básicos, retornar
    if errors:
        return False, errors
    
    # Verificar regra: partículas do mesmo tipo devem ter a mesma polaridade
    consistency_errors = _check_same_type_polarity_consistency(particles)
    errors.extend(consistency_errors)
    
    # Se há erros de consistência, continuar validando mas já sabemos que é inválida
    # (não retornar aqui para coletar todos os erros)
    
    # Verificar ligações
    particle_ids = {p['id'] for p in particles}
    
    for bond in bonds:
        if 'from' not in bond or 'to' not in bond:
            errors.append('Ligação sem origem/destino')
            continue
        
        if bond['from'] not in particle_ids:
            errors.append(f'Ligação referencia partícula inexistente: {bond["from"]}')
        
        if bond['to'] not in particle_ids:
            errors.append(f'Ligação referencia partícula inexistente: {bond["to"]}')
        
        if 'multiplicity' not in bond:
            errors.append(f'Ligação entre {bond["from"]} e {bond["to"]} sem multiplicidade')
        elif bond['multiplicity'] < 1:
            errors.append(f'Ligação com multiplicidade inválida: {bond["multiplicity"]}')
    
    # Verificar conexões (cada partícula deve respeitar seu limite)
    connection_count = {p['id']: 0 for p in particles}
    
    for bond in bonds:
        if 'from' in bond and 'to' in bond and 'multiplicity' in bond:
            connection_count[bond['from']] += bond['multiplicity']
            connection_count[bond['to']] += bond['multiplicity']
    
    for particle in particles:
        pid = particle['id']
        ptype = particle['type']
        max_connections = PARTICLE_TYPES[ptype]['connections']
        actual_connections = connection_count[pid]
        
        if actual_connections > max_connections:
            errors.append(
                f'Partícula {pid} ({ptype}) excede limite de conexões: '
                f'{actual_connections}/{max_connections}'
            )
        elif actual_connections < max_connections:
            errors.append(
                f'Partícula {pid} ({ptype}) não está estável: '
                f'{actual_connections}/{max_connections} conexões'
            )
    
    # Verificar regras de ligação
    particle_map = {p['id']: p for p in particles}
    
    for bond in bonds:
        if 'from' in bond and 'to' in bond:
            p_from = particle_map.get(bond['from'])
            p_to = particle_map.get(bond['to'])
            
            if p_from and p_to:
                # Regra: partículas do mesmo tipo não podem se ligar
                if p_from['type'] == p_to['type']:
                    errors.append(
                        f'Ligação inválida: partículas do mesmo tipo '
                        f'({p_from["type"]}) não podem se ligar diretamente'
                    )
                
                # Regra: partículas só se ligam com polaridades opostas
                if p_from['polarity'] == p_to['polarity']:
                    errors.append(
                        f'Ligação inválida: partículas com mesma polaridade '
                        f'({p_from["polarity"]}) não podem se ligar'
                    )
    
    # Verificar conectividade (todas as partículas devem estar conectadas)
    if len(particles) > 1:
        # Construir grafo de adjacências
        adjacency = {p['id']: [] for p in particles}
        for bond in bonds:
            if 'from' in bond and 'to' in bond:
                adjacency[bond['from']].append(bond['to'])
                adjacency[bond['to']].append(bond['from'])
        
        if not _is_fully_connected(adjacency, particles):
            errors.append('Molécula não está conectada: há partículas isoladas')
    
    # Verificar se é possível estabilizar todas as partículas
    # A soma das conexões necessárias deve ser par (cada ligação conecta 2 partículas)
    total_needed = 0
    for particle in particles:
        pid = particle['id']
        ptype = particle['type']
        max_connections = PARTICLE_TYPES[ptype]['connections']
        actual_connections = connection_count.get(pid, 0)
        needed = max_connections - actual_connections
        if needed > 0:
            total_needed += needed
    
    # Se há conexões faltando, verificar se é possível criar
    if total_needed > 0:
        # Contar partículas por tipo e polaridade
        positive_by_type = {}
        negative_by_type = {}
        
        for particle in particles:
            ptype = particle['type']
            polarity = particle['polarity']
            actual = connection_count.get(particle['id'], 0)
            max_conn = PARTICLE_TYPES[ptype]['connections']
            needed = max_conn - actual
            
            if needed > 0:
                if polarity == '+':
                    positive_by_type[ptype] = positive_by_type.get(ptype, 0) + needed
                else:
                    negative_by_type[ptype] = negative_by_type.get(ptype, 0) + needed
        
        # Verificar se há partículas de tipos opostos que podem se ligar
        can_stabilize = False
        for pos_type, pos_needed in positive_by_type.items():
            for neg_type, neg_needed in negative_by_type.items():
                if pos_type != neg_type:  # Tipos diferentes podem se ligar
                    can_stabilize = True
                    break
            if can_stabilize:
                break
        
        if not can_stabilize and total_needed > 0:
            errors.append(
                f'Impossível estabilizar: faltam {total_needed} conexões, '
                f'mas não há partículas compatíveis para criar ligações'
            )
    
    is_valid = len(errors) == 0
    return is_valid, errors


def quick_validate(molecule):
    """Validação rápida (só retorna True/False)"""
    is_valid, _ = validate_molecule(molecule)
    return is_valid

