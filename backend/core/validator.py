"""
Validador de Moléculas
Verifica se uma molécula segue as regras do jogo
"""

from data.molecules import PARTICLE_TYPES


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
        errors.append('Molécula vazia')
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
    
    # Verificar regra: partículas iguais não podem se ligar diretamente
    particle_map = {p['id']: p for p in particles}
    
    for bond in bonds:
        if 'from' in bond and 'to' in bond:
            p_from = particle_map.get(bond['from'])
            p_to = particle_map.get(bond['to'])
            
            if p_from and p_to:
                if p_from['type'] == p_to['type']:
                    errors.append(
                        f'Ligação inválida: partículas do mesmo tipo '
                        f'({p_from["type"]}) não podem se ligar diretamente'
                    )
    
    is_valid = len(errors) == 0
    return is_valid, errors


def quick_validate(molecule):
    """Validação rápida (só retorna True/False)"""
    is_valid, _ = validate_molecule(molecule)
    return is_valid

