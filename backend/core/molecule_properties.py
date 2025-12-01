"""
Sistema de Propriedades Observáveis de Moléculas

Calcula propriedades como sabor e aparência baseadas em características estruturais.
Usado para mecânica de identificação de moléculas no gameplay.
"""

from core.molecule_analyzer import analyze_molecule_structure


# ============================================================================
# MAPEAMENTO DE SABORES POR TOPOLOGIA
# ============================================================================

TOPOLOGY_FLAVOR_MAP = {
    'linear': 'Salgado',
    'Y': 'Amargo',
    'X': 'Amargo-intenso',
    'tree': 'Amargo-complexo',
    'cycle': 'Azedo',
    'mista': 'Azedo-amargo'
}


def get_flavor_from_topology(topology):
    """
    Retorna o sabor da molécula baseado na topologia.
    
    Args:
        topology: String da topologia ('linear', 'Y', 'cycle', etc.)
    
    Returns:
        String com o sabor
    """
    return TOPOLOGY_FLAVOR_MAP.get(topology, 'Desconhecido')


# ============================================================================
# MAPEAMENTO DE CORES POR COMBINAÇÃO DE MULTIPLICIDADES
# ============================================================================

# Todas as combinações possíveis de multiplicidades (1, 2, 3)
MULTIPLICITY_COLOR_MAP = {
    # Apenas uma multiplicidade
    frozenset([1]): {
        'name': 'Azul claro',
        'color': '#87CEEB',  # Sky Blue
        'description': 'Apenas ligações simples'
    },
    frozenset([2]): {
        'name': 'Verde',
        'color': '#32CD32',  # Lime Green
        'description': 'Apenas ligações duplas'
    },
    # Nota: Não é possível ter apenas ligações triplas (multiplicidade 3)
    # pois isso tornaria a molécula estruturalmente instável
    
    # Combinações de duas multiplicidades
    frozenset([1, 2]): {
        'name': 'Vermelho',
        'color': '#FF4500',  # Orange Red
        'description': 'Ligações simples e duplas'
    },
    frozenset([1, 3]): {
        'name': 'Laranja',
        'color': '#FF8C00',  # Dark Orange
        'description': 'Ligações simples e triplas'
    },
    frozenset([2, 3]): {
        'name': 'Magenta',
        'color': '#FF1493',  # Deep Pink
        'description': 'Ligações duplas e triplas'
    },
    
    # Combinação de três multiplicidades
    frozenset([1, 2, 3]): {
        'name': 'Amarelo',
        'color': '#FFD700',  # Gold
        'description': 'Todas as ligações (simples, duplas e triplas)'
    }
}


def get_appearance_from_bonds(bonds):
    """
    Retorna a aparência (cor) da molécula baseado nas multiplicidades das ligações.
    
    Args:
        bonds: Lista de bonds da molécula [{'multiplicity': 1, ...}, ...]
    
    Returns:
        Dict com 'name', 'color', 'description'
    """
    if not bonds:
        return {
            'name': 'Incolor',
            'color': '#FFFFFF',
            'description': 'Sem ligações'
        }
    
    # Extrair multiplicidades únicas
    multiplicities = set(bond.get('multiplicity', 1) for bond in bonds)
    
    # Buscar no mapa
    appearance = MULTIPLICITY_COLOR_MAP.get(frozenset(multiplicities))
    
    if appearance:
        return appearance
    
    # Fallback (não deveria acontecer)
    return {
        'name': 'Desconhecido',
        'color': '#808080',
        'description': 'Combinação não catalogada'
    }


# ============================================================================
# FUNÇÕES PRINCIPAIS DE CÁLCULO
# ============================================================================

def calculate_flavor(molecule):
    """
    Calcula o sabor da molécula baseado na topologia.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
    
    Returns:
        String com o sabor
    """
    structure = analyze_molecule_structure(molecule)
    topology = structure.get('topology', 'linear')
    return get_flavor_from_topology(topology)


def calculate_appearance(molecule):
    """
    Calcula a aparência (cor) da molécula baseado nas multiplicidades das ligações.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
    
    Returns:
        Dict com 'name', 'color', 'description'
    """
    bonds = molecule.get('bonds', [])
    return get_appearance_from_bonds(bonds)


def calculate_molecule_observable_properties(molecule, profile=None):
    """
    Calcula todas as propriedades observáveis de uma molécula.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
        profile: Dict opcional com o perfil do save para calcular efeitos
    
    Returns:
        Dict com:
        {
            'flavor': 'Salgado',
            'appearance': {
                'name': 'Azul claro',
                'color': '#87CEEB',
                'description': 'Apenas ligações simples'
            },
            'effects': ['Analgesia', 'Anti-inflamatório', ...]  # Lista de efeitos se profile fornecido
        }
    """
    result = {
        'flavor': calculate_flavor(molecule),
        'appearance': calculate_appearance(molecule)
    }
    
    # Calcular efeitos se perfil fornecido
    if profile:
        from core.property_profiles import check_molecule_effects
        result['effects'] = check_molecule_effects(molecule, profile)
    else:
        result['effects'] = []
    
    return result


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def get_all_possible_flavors():
    """
    Retorna lista de todos os sabores possíveis.
    """
    return list(TOPOLOGY_FLAVOR_MAP.values())


def get_all_possible_appearances():
    """
    Retorna lista de todas as aparências possíveis.
    """
    return [
        {
            'multiplicities': list(multi_set),
            **appearance
        }
        for multi_set, appearance in MULTIPLICITY_COLOR_MAP.items()
    ]


def get_flavor_by_topology():
    """
    Retorna o mapeamento completo topologia -> sabor.
    """
    return TOPOLOGY_FLAVOR_MAP.copy()


def get_appearance_by_multiplicities():
    """
    Retorna o mapeamento completo multiplicidades -> aparência.
    """
    return {
        list(multi_set): appearance
        for multi_set, appearance in MULTIPLICITY_COLOR_MAP.items()
    }

