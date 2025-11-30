# Base de dados de moléculas do jogo

PARTICLE_TYPES = {
    'circle': {'name': 'Círculo', 'symbol': '○', 'connections': 1},
    'square': {'name': 'Quadrado', 'symbol': '□', 'connections': 2},
    'triangle': {'name': 'Triângulo', 'symbol': '△', 'connections': 3},
    'pentagon': {'name': 'Pentágono', 'symbol': '⬠', 'connections': 4}
}

# Base de dados de moléculas organizadas por massa
MOLECULES_DATABASE = {
    3: [
        {
            'id': 'm3_1',
            'name': 'Molécula 3-1',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '-', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm3_2',
            'name': 'Molécula 3-2',
            'particles': [
                {'id': 'p0', 'type': 'square', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'triangle', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '-', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm3_3',
            'name': 'Molécula 3-3',
            'particles': [
                {'id': 'p0', 'type': 'square', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'square', 'polarity': '-', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 2}
            ]
        },        {
            'id': 'm3_4',
            'name': 'Molécula 3-4',
            'particles': [
                {'id': 'p0', 'type': 'triangle', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '-', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 3},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm3_5',
            'name': 'Molécula 3-5',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '+', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm3_6',
            'name': 'Molécula 3-6',
            'particles': [
                {'id': 'p0', 'type': 'square', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'triangle', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '+', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm3_7',
            'name': 'Molécula 3-7',
            'particles': [
                {'id': 'p0', 'type': 'square', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'square', 'polarity': '+', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 2}
            ]
        },        {
            'id': 'm3_8',
            'name': 'Molécula 3-8',
            'particles': [
                {'id': 'p0', 'type': 'triangle', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '+', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 3},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1}
            ]
        }                      
    ],
    4: [
        {
            'id': 'm4_1',
            'name': 'Molécula 4-1',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'triangle', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '-', 'x': 1, 'y': 1},
                {'id': 'p3', 'type': 'circle', 'polarity': '-', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p2', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p3', 'to': 'p1', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm4_2',
            'name': 'Molécula 4-2',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'triangle', 'polarity': '-', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'square', 'polarity': '+', 'x': 3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p2', 'to': 'p3', 'multiplicity': 2}
            ]
        },
        {
            'id': 'm4_3',
            'name': 'Molécula 4-3',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '-', 'x': 1, 'y': 1},
                {'id': 'p3', 'type': 'square', 'polarity': '-', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p3', 'multiplicity': 2},
                {'from': 'p2', 'to': 'p1', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm4_4',
            'name': 'Molécula 4-4',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'pentagon', 'polarity': '-', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'triangle', 'polarity': '+', 'x': 3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p2', 'to': 'p3', 'multiplicity': 3}
            ]
        },
        {
            'id': 'm4_5',
            'name': 'Molécula 4-5',
            'particles': [
                {'id': 'p0', 'type': 'square', 'polarity': '-', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '+', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'triangle', 'polarity': '-', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'circle', 'polarity': '+', 'x': 3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 2},
                {'from': 'p2', 'to': 'p3', 'multiplicity': 1}
            ]
        },
        # Versões invertidas (sinais opostos)
        {
            'id': 'm4_6',
            'name': 'Molécula 4-6',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'triangle', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '+', 'x': 1, 'y': 1},
                {'id': 'p3', 'type': 'circle', 'polarity': '+', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p2', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p3', 'to': 'p1', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm4_7',
            'name': 'Molécula 4-7',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'triangle', 'polarity': '+', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'square', 'polarity': '-', 'x': 3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p2', 'to': 'p3', 'multiplicity': 2}
            ]
        },
        {
            'id': 'm4_8',
            'name': 'Molécula 4-8',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'circle', 'polarity': '+', 'x': 1, 'y': 1},
                {'id': 'p3', 'type': 'square', 'polarity': '+', 'x': 2, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p3', 'multiplicity': 2},
                {'from': 'p2', 'to': 'p1', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm4_9',
            'name': 'Molécula 4-9',
            'particles': [
                {'id': 'p0', 'type': 'circle', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'pentagon', 'polarity': '+', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'triangle', 'polarity': '-', 'x': 3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p2', 'to': 'p3', 'multiplicity': 3}
            ]
        },
        {
            'id': 'm4_10',
            'name': 'Molécula 4-10',
            'particles': [
                {'id': 'p0', 'type': 'square', 'polarity': '+', 'x': 0, 'y': 0},
                {'id': 'p1', 'type': 'pentagon', 'polarity': '-', 'x': 1, 'y': 0},
                {'id': 'p2', 'type': 'triangle', 'polarity': '+', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'circle', 'polarity': '-', 'x': 3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p1', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 2},
                {'from': 'p2', 'to': 'p3', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm4_11',
            'name': 'Molécula 4-11',
            'particles': [
                {'id': 'p0', 'type': 'pentagon', 'polarity': '+', 'x': -2, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '+', 'x': 6, 'y': 0},
                {'id': 'p2', 'type': 'triangle', 'polarity': '-', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'triangle', 'polarity': '-', 'x': -6, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p0', 'to': 'p3', 'multiplicity': 3},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 2}
            ]
        },
        {
            'id': 'm4_12',
            'name': 'Molécula 4-12',
            'particles': [
                {'id': 'p0', 'type': 'pentagon', 'polarity': '+', 'x': 0, 'y': -3},
                {'id': 'p1', 'type': 'square', 'polarity': '+', 'x': 0, 'y': 3},
                {'id': 'p2', 'type': 'triangle', 'polarity': '-', 'x': 3, 'y': 0},
                {'id': 'p3', 'type': 'triangle', 'polarity': '-', 'x': -3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p2', 'multiplicity': 2},
                {'from': 'p0', 'to': 'p3', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p3', 'multiplicity': 1}
            ]
        },
        {
            'id': 'm4_13',
            'name': 'Molécula 4-13',
            'particles': [
                {'id': 'p0', 'type': 'pentagon', 'polarity': '-', 'x': -2, 'y': 0},
                {'id': 'p1', 'type': 'square', 'polarity': '-', 'x': 6, 'y': 0},
                {'id': 'p2', 'type': 'triangle', 'polarity': '+', 'x': 2, 'y': 0},
                {'id': 'p3', 'type': 'triangle', 'polarity': '+', 'x': -6, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p0', 'to': 'p3', 'multiplicity': 3},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 2}
            ]
        },
        {
            'id': 'm4_14',
            'name': 'Molécula 4-14',
            'particles': [
                {'id': 'p0', 'type': 'pentagon', 'polarity': '-', 'x': 0, 'y': -3},
                {'id': 'p1', 'type': 'square', 'polarity': '-', 'x': 0, 'y': 3},
                {'id': 'p2', 'type': 'triangle', 'polarity': '+', 'x': 3, 'y': 0},
                {'id': 'p3', 'type': 'triangle', 'polarity': '+', 'x': -3, 'y': 0}
            ],
            'bonds': [
                {'from': 'p0', 'to': 'p2', 'multiplicity': 2},
                {'from': 'p0', 'to': 'p3', 'multiplicity': 2},
                {'from': 'p1', 'to': 'p2', 'multiplicity': 1},
                {'from': 'p1', 'to': 'p3', 'multiplicity': 1}
            ]
        },
        
    ],
    5: [],
    6: []
}


def get_molecules_by_mass(mass):
    """Retorna todas as moléculas de uma determinada massa"""
    return MOLECULES_DATABASE.get(mass, [])


def get_all_molecules():
    """Retorna todas as moléculas do banco de dados"""
    all_molecules = []
    for mass, molecules in MOLECULES_DATABASE.items():
        all_molecules.extend(molecules)
    return all_molecules


def get_molecule_by_id(molecule_id):
    """Busca uma molécula específica por ID"""
    for mass, molecules in MOLECULES_DATABASE.items():
        for molecule in molecules:
            if molecule['id'] == molecule_id:
                return molecule
    return None


def calculate_molecule_properties(molecule):
    """Calcula propriedades da molécula (massa, carga)"""
    mass = len(molecule['particles'])
    
    # Calcular carga
    charge = 0
    for particle in molecule['particles']:
        charge += 1 if particle['polarity'] == '+' else -1
    
    charge_label = 'Positiva' if charge > 0 else ('Negativa' if charge < 0 else 'Neutra')
    
    # Calcular fórmula molecular
    formula = calculate_molecular_formula(molecule)
    
    return {
        'mass': mass,
        'charge': charge,
        'charge_label': charge_label,
        'formula': formula
    }


def calculate_molecular_formula(molecule):
    """
    Calcula a fórmula molecular no formato CQTP
    C = Círculo (1 ligação)
    Q = Quadrado (2 ligações)
    T = Triângulo (3 ligações)
    P = Pentágono (4 ligações)
    
    Ordem: do menor número de ligações para o maior
    Usa sobrescrito para quantidade > 1
    """
    # Mapeamento de tipo para símbolo
    type_to_symbol = {
        'circle': 'C',
        'square': 'Q',
        'triangle': 'T',
        'pentagon': 'P'
    }
    
    # Ordem de prioridade (por número de ligações)
    order = ['circle', 'square', 'triangle', 'pentagon']
    
    # Contar partículas de cada tipo
    count = {ptype: 0 for ptype in order}
    for particle in molecule['particles']:
        ptype = particle['type']
        if ptype in count:
            count[ptype] += 1
    
    # Construir fórmula
    formula_parts = []
    for ptype in order:
        quantity = count[ptype]
        if quantity > 0:
            symbol = type_to_symbol[ptype]
            if quantity == 1:
                formula_parts.append(symbol)
            else:
                # Usar caracteres Unicode para sobrescrito
                superscript = convert_to_superscript(quantity)
                formula_parts.append(f"{symbol}{superscript}")
    
    return ''.join(formula_parts)


def convert_to_superscript(number):
    """Converte número para caracteres sobrescritos Unicode"""
    superscripts = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    return ''.join(superscripts[digit] for digit in str(number))


def get_available_masses():
    """Retorna lista de massas disponíveis"""
    return [mass for mass, molecules in MOLECULES_DATABASE.items() if len(molecules) > 0]


def find_molecule(molecule_id):
    """
    Busca uma molécula por ID tanto no banco predefinido quanto nas descobertas
    
    Returns: molecule dict ou None
    """
    # Buscar nas moléculas predefinidas
    for mass, molecules in MOLECULES_DATABASE.items():
        for mol in molecules:
            if mol['id'] == molecule_id:
                return mol
    
    # Buscar nas descobertas
    from .discovered_molecules import find_discovery_by_id
    discovery = find_discovery_by_id(molecule_id)
    
    if discovery:
        return discovery['molecule']
    
    return None

