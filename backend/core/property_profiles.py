"""
Sistema de Perfis de Propriedades Aleatórios por Partida

Cada save/partida tem um perfil único que define:
- Mapeamento aleatório de topologias -> sabores
- Mapeamento aleatório de multiplicidades -> cores
- Condições para efeitos baseadas em atributos

Isso torna cada partida única, forçando o jogador a descobrir os mapeamentos.
"""

import random
import json
from typing import Dict, List, Optional


# ============================================================================
# LISTAS BASE (disponíveis para randomização)
# ============================================================================

# Sabores disponíveis
AVAILABLE_FLAVORS = [
    'Insípido', 'Salgado', 'Amargo', 'Amargo-intenso', 'Amargo-complexo',
    'Azedo', 'Azedo-amargo', 'Doce', 'Picante', 'Metálico', 'Ácido', 'Adstringente'
]

# Topologias possíveis
AVAILABLE_TOPOLOGIES = [
    'linear', 'Y', 'X', 'tree', 'cycle', 'mista'
]

# Cores disponíveis (com seus hex codes)
AVAILABLE_COLORS = [
    {'name': 'Azul claro', 'color': '#87CEEB'},
    {'name': 'Verde', 'color': '#32CD32'},
    {'name': 'Vermelho', 'color': '#FF4500'},
    {'name': 'Laranja', 'color': '#FF8C00'},
    {'name': 'Magenta', 'color': '#FF1493'},
    {'name': 'Amarelo', 'color': '#FFD700'},
    {'name': 'Ciano', 'color': '#00CED1'},
    {'name': 'Rosa', 'color': '#FF69B4'},
    {'name': 'Lavanda', 'color': '#E6E6FA'},
    {'name': 'Coral', 'color': '#FF7F50'},
    {'name': 'Turquesa', 'color': '#40E0D0'},
    {'name': 'Lima', 'color': '#00FF00'}
]

# Multiplicidades possíveis
AVAILABLE_MULTIPLICITY_SETS = [
    frozenset([1]),
    frozenset([2]),
    frozenset([1, 2]),
    frozenset([1, 3]),
    frozenset([2, 3]),
    frozenset([1, 2, 3])
]


# ============================================================================
# SISTEMA DE PADRÕES DE LIGAÇÃO PARA EFEITOS
# ============================================================================

# Efeitos terapêuticos (10)
THERAPEUTIC_EFFECTS = [
    'Analgésico',
    'Anti-inflamatório',
    'Antibiótico',
    'Regenerativo',
    'Antioxidante',
    'Imunomodulador',
    'Vasodilatador',
    'Hepatoprotetor',
    'Cardioprotetor',
    'Neuroprotetor'
]

# Efeitos colaterais (10)
SIDE_EFFECTS = [
    'Hepatotóxico',
    'Nefrotóxico',
    'Neurotóxico',
    'Carcinogênico',
    'Teratogênico',
    'Mutagênico',
    'Cardiotóxico',
    'Alergênico',
    'Hemorrágico',
    'Sedativo-excessivo'
]

# Todos os efeitos
ALL_EFFECTS = THERAPEUTIC_EFFECTS + SIDE_EFFECTS


def generate_effect_patterns(effect_name: str, seed: Optional[int] = None, num_patterns: int = 2) -> List:
    """
    Gera padrões de ligação aleatórios para um efeito.
    
    Cada efeito terá um conjunto de 2-3 padrões de ligação que devem estar presentes.
    Um padrão é uma tupla: (tipo1, tipo2, multiplicidade)
    
    Args:
        effect_name: Nome do efeito
        seed: Seed para randomização (opcional)
        num_patterns: Número de padrões necessários (2-3, default 2)
    
    Returns:
        Lista de tuplas (tipo1, tipo2, multiplicidade) normalizadas
    """
    from core.effect_patterns import generate_effect_patterns as gen_patterns
    
    if seed is not None:
        effect_hash = hash(f"{seed}_{effect_name}")
    else:
        effect_hash = hash(effect_name)
    
    return gen_patterns(effect_name, num_patterns=num_patterns, seed=effect_hash)


# ============================================================================
# GERAÇÃO DE PERFIL ÚNICO POR SAVE
# ============================================================================

def generate_property_profile(save_id: str) -> Dict:
    """
    Gera um perfil único de propriedades para um save.
    
    O perfil inclui:
    - Mapeamento topologia -> sabor
    - Mapeamento multiplicidades -> cor
    - Condições para cada efeito
    
    Args:
        save_id: ID do save (usado como seed)
    
    Returns:
        Dict com o perfil completo
    """
    # Usar hash do save_id como seed para consistência
    seed = hash(save_id)
    random.seed(seed)
    
    # 1. Gerar mapeamento de topologia -> sabor
    # Cada topologia recebe um sabor único aleatório
    shuffled_flavors = random.sample(AVAILABLE_FLAVORS[:8], k=8)  # Usar 8 sabores para 8 topologias
    topology_flavor_map = {}
    for i, topology in enumerate(AVAILABLE_TOPOLOGIES):
        topology_flavor_map[topology] = shuffled_flavors[i] if i < len(shuffled_flavors) else shuffled_flavors[0]
    
    # 2. Gerar mapeamento de multiplicidades -> cor
    # Cada combinação de multiplicidades recebe uma cor única aleatória
    shuffled_colors = random.sample(AVAILABLE_COLORS, k=len(AVAILABLE_MULTIPLICITY_SETS))
    multiplicity_color_map = {}
    for i, multi_set in enumerate(AVAILABLE_MULTIPLICITY_SETS):
        color = shuffled_colors[i] if i < len(shuffled_colors) else AVAILABLE_COLORS[0]
        # Usar tupla ordenada como chave (lista não é hashable)
        mult_key = tuple(sorted(multi_set))
        multiplicity_color_map[mult_key] = {
            'name': color['name'],
            'color': color['color'],
            'description': f'Ligações {_format_multiplicities(multi_set)}'
        }
    
    # 3. Gerar padrões de ligação para cada efeito
    # Cada efeito terá 2-3 padrões de ligação necessários
    effect_patterns = {}
    for effect in ALL_EFFECTS:
        # Usar hash combinado do save_id + nome do efeito como seed
        effect_seed = hash(f"{save_id}_{effect}")
        # Determinar número de padrões: 2 para maioria, 3 para alguns
        num_patterns = 2 if hash(effect) % 3 != 0 else 3
        effect_patterns[effect] = generate_effect_patterns(effect, seed=effect_seed, num_patterns=num_patterns)
    
    # Reset random seed
    random.seed()
    
    return {
        'save_id': save_id,
        'topology_flavor_map': topology_flavor_map,
        'multiplicity_color_map': multiplicity_color_map,
        'effect_patterns': effect_patterns,  # Mudou de effect_conditions para effect_patterns
        'generated_at': None  # Será preenchido quando salvo
    }


def _format_multiplicities(multi_set: frozenset) -> str:
    """Formata multiplicidades em string descritiva"""
    mults = sorted(list(multi_set))
    if len(mults) == 1:
        if mults[0] == 1:
            return 'simples'
        elif mults[0] == 2:
            return 'duplas'
    elif len(mults) == 2:
        return f'simples e {"duplas" if 2 in mults else "triplas"}'
    else:
        return 'simples, duplas e triplas'


# ============================================================================
# CARREGAMENTO E SALVAMENTO DE PERFIS
# ============================================================================

PROFILES_FILE = 'data/property_profiles.json'


def _serialize_profile_for_json(profile: Dict) -> Dict:
    """
    Converte um perfil para formato JSON-safe (tuplas -> strings/listas).
    Função robusta que garante conversão completa.
    """
    if not isinstance(profile, dict):
        return profile
    
    serialized = {}
    
    # Processar cada campo do perfil
    for key, value in profile.items():
        if key == 'multiplicity_color_map':
            # Converter dicionário com tuplas como chaves
            new_map = {}
            if isinstance(value, dict):
                for map_key, map_value in value.items():
                    # Converter tupla/lista para string JSON
                    if isinstance(map_key, tuple):
                        key_str = json.dumps(sorted(map_key), sort_keys=True)
                    elif isinstance(map_key, list):
                        key_str = json.dumps(sorted(map_key), sort_keys=True)
                    else:
                        key_str = str(map_key)
                    new_map[key_str] = map_value
            serialized[key] = new_map
            
        elif key == 'effect_patterns':
            # Converter lista de padrões (cada padrão é uma tupla)
            new_patterns = {}
            if isinstance(value, dict):
                for effect_name, patterns in value.items():
                    if isinstance(patterns, list):
                        new_patterns[effect_name] = [
                            list(pattern) if isinstance(pattern, tuple) else pattern
                            for pattern in patterns
                        ]
                    else:
                        new_patterns[effect_name] = patterns
            serialized[key] = new_patterns
            
        else:
            # Campos simples - copiar direto
            serialized[key] = value
    
    return serialized


def _restore_tuples_from_json(obj, is_multiplicity_key=False):
    """
    Função recursiva para restaurar tuplas a partir do formato JSON-safe.
    Para chaves de multiplicity_color_map, tenta parsear strings JSON de volta para tuplas.
    """
    if isinstance(obj, list):
        # Listas podem ser padrões de efeito - converter para tuplas se tiver 3 elementos
        if len(obj) == 3 and all(isinstance(x, (str, int)) for x in obj):
            return tuple(obj)
        else:
            return [_restore_tuples_from_json(item, False) for item in obj]
    elif isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            # Tentar converter chaves string JSON de volta para tuplas
            restored_key = key
            if isinstance(key, str) and is_multiplicity_key:
                try:
                    key_list = json.loads(key)
                    if isinstance(key_list, list):
                        restored_key = tuple(sorted(key_list))
                except:
                    pass  # Manter como string se não conseguir parsear
            
            # Processar recursivamente
            is_mult_key = (restored_key == 'multiplicity_color_map')
            new_dict[restored_key] = _restore_tuples_from_json(value, is_mult_key)
        return new_dict
    else:
        return obj


def _deserialize_profile_from_json(profile_data: Dict) -> Dict:
    """
    Converte um perfil do formato JSON de volta (strings -> tuplas onde necessário).
    """
    # Converter multiplicity_color_map (strings -> tuplas)
    if 'multiplicity_color_map' in profile_data:
        new_map = {}
        for key_str, value in profile_data['multiplicity_color_map'].items():
            try:
                key_list = json.loads(key_str)
                key_tuple = tuple(sorted(key_list)) if isinstance(key_list, list) else key_str
                new_map[key_tuple] = value
            except:
                # Se não conseguir parsear, manter como está
                new_map[key_str] = value
        profile_data['multiplicity_color_map'] = new_map
    
    # Converter effect_patterns (listas -> tuplas)
    if 'effect_patterns' in profile_data:
        new_patterns = {}
        for effect_name, patterns in profile_data['effect_patterns'].items():
            if isinstance(patterns, list):
                new_patterns[effect_name] = [
                    tuple(pattern) if isinstance(pattern, list) and len(pattern) == 3 else pattern
                    for pattern in patterns
                ]
            else:
                new_patterns[effect_name] = patterns
        profile_data['effect_patterns'] = new_patterns
    
    return profile_data


def load_profiles() -> Dict:
    """Carrega todos os perfis salvos"""
    import os
    
    if not os.path.exists(PROFILES_FILE):
        return {}
    
    try:
        with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
            profiles_data = json.load(f)
            # Deserializar cada perfil
            deserialized_profiles = {}
            for save_id, profile_data in profiles_data.items():
                deserialized_profiles[save_id] = _deserialize_profile_from_json(profile_data)
            return deserialized_profiles
    except Exception as e:
        print(f"Erro ao carregar perfis: {e}")
        return {}


def _convert_tuples_for_json(obj):
    """
    Função recursiva para converter todas as tuplas encontradas para formatos JSON-safe.
    """
    if isinstance(obj, tuple):
        return list(obj)
    elif isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            # Converter chaves que são tuplas para strings
            if isinstance(key, tuple):
                key_str = json.dumps(sorted(key), sort_keys=True)
            elif isinstance(key, list):
                key_str = json.dumps(sorted(key), sort_keys=True)
            else:
                key_str = key
            new_dict[key_str] = _convert_tuples_for_json(value)
        return new_dict
    elif isinstance(obj, list):
        return [_convert_tuples_for_json(item) for item in obj]
    else:
        return obj


def save_profiles(profiles: Dict):
    """Salva todos os perfis"""
    import os
    
    os.makedirs('data', exist_ok=True)
    
    # Converter todas as tuplas recursivamente
    json_safe_profiles = _convert_tuples_for_json(profiles)
    
    try:
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(json_safe_profiles, f, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        print(f"Erro ao salvar perfis: {e}")
        import traceback
        traceback.print_exc()
        raise


def check_molecule_effects(molecule: Dict, profile: Dict) -> List[str]:
    """
    Verifica quais efeitos uma molécula possui baseado nos padrões de ligação.
    
    Os padrões são projetados para requerer múltiplas ligações e partículas diferentes,
    garantindo que apenas moléculas maiores (massa > 5) possam satisfazer todos os padrões.
    
    Args:
        molecule: Dict com 'particles' e 'bonds'
        profile: Perfil do save com effect_patterns
    
    Returns:
        Lista de nomes dos efeitos que a molécula possui
    """
    from core.effect_patterns import molecule_has_effect
    
    effects = []
    effect_patterns = profile.get('effect_patterns', {})
    
    for effect_name, patterns in effect_patterns.items():
        if molecule_has_effect(molecule, patterns):
            effects.append(effect_name)
    
    return effects


def get_or_create_profile(save_id: str) -> Dict:
    """
    Obtém o perfil de um save, criando um novo se não existir.
    
    Args:
        save_id: ID do save
    
    Returns:
        Dict com o perfil
    """
    profiles = load_profiles()
    
    if save_id not in profiles:
        # Criar novo perfil
        profile = generate_property_profile(save_id)
        profile['generated_at'] = __import__('datetime').datetime.now().isoformat()
        profiles[save_id] = profile
        save_profiles(profiles)
    
    return profiles[save_id]


def get_profile(save_id: str) -> Optional[Dict]:
    """
    Obtém o perfil de um save (retorna None se não existir).
    
    Args:
        save_id: ID do save
    
    Returns:
        Dict com o perfil ou None
    """
    profiles = load_profiles()
    return profiles.get(save_id)


def delete_profile(save_id: str):
    """Deleta o perfil de um save"""
    profiles = load_profiles()
    if save_id in profiles:
        del profiles[save_id]
        save_profiles(profiles)

