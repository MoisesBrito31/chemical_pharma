"""
Sistema de Perfis de Propriedades por Save

Cada save tem um perfil único que mapeia:
- Topologias -> Sabores (randomizado por save)
- Multiplicidades -> Cores (randomizado por save)  
- Padrões de ligação -> Efeitos (3 requisitos específicos por efeito)

Os perfis são salvos em JSON e são consistentes para cada save.
"""

import random
import json
import os
from typing import Dict, List, Optional, Tuple

# ============================================================================
# LISTAS DE ELEMENTOS PARA RANDOMIZAÇÃO
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

# Topologias disponíveis (sem 'single' e 'empty')
AVAILABLE_TOPOLOGIES = ['linear', 'Y', 'X', 'tree', 'cycle', 'mista']

# Sabores disponíveis
AVAILABLE_FLAVORS = [
    'Salgado', 'Amargo', 'Amargo-intenso', 'Amargo-complexo',
    'Azedo', 'Azedo-amargo', 'Doce', 'Umami'
]

# Cores disponíveis para aparência
AVAILABLE_COLORS = [
    {'name': 'Azul claro', 'color': '#87CEEB', 'description': 'Apenas ligações simples'},
    {'name': 'Verde', 'color': '#32CD32', 'description': 'Apenas ligações duplas'},
    {'name': 'Vermelho', 'color': '#FF4500', 'description': 'Ligações simples e duplas'},
    {'name': 'Laranja', 'color': '#FF8C00', 'description': 'Ligações simples e triplas'},
    {'name': 'Magenta', 'color': '#FF1493', 'description': 'Ligações duplas e triplas'},
    {'name': 'Amarelo', 'color': '#FFD700', 'description': 'Todas as ligações (simples, duplas e triplas)'}
]

# Combinações de multiplicidades
AVAILABLE_MULTIPLICITY_SETS = [
    frozenset([1]),
    frozenset([2]),
    frozenset([1, 2]),
    frozenset([1, 3]),
    frozenset([2, 3]),
    frozenset([1, 2, 3])
]


# ============================================================================
# GERAÇÃO DE PERFIL ÚNICO POR SAVE
# ============================================================================

def generate_property_profile(save_id: str) -> Dict:
    """
    Gera um perfil único de propriedades para um save.
    
    O perfil inclui:
    - Mapeamento topologia -> sabor
    - Mapeamento multiplicidades -> cor
    - Condições para cada efeito (3 requisitos específicos por efeito)
    
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
    shuffled_flavors = random.sample(AVAILABLE_FLAVORS[:6], k=6)  # 6 sabores para 6 topologias
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
    # Cada efeito terá 3 requisitos específicos de ligação (tipo, polaridade, multiplicidade)
    from core.effect_patterns import generate_all_effect_requirements
    effect_patterns = generate_all_effect_requirements()
    
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
            # Converter lista de padrões (cada padrão é uma tupla de 5 elementos: tipo1, pol1, tipo2, pol2, mult)
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
        # Listas podem ser padrões de efeito - converter para tuplas se tiver 3 ou 5 elementos
        # Formato antigo: (tipo1, tipo2, multiplicidade) - 3 elementos
        # Formato novo: (tipo1, polaridade1, tipo2, polaridade2, multiplicidade) - 5 elementos
        if len(obj) in [3, 5] and all(isinstance(x, (str, int)) for x in obj):
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
                    tuple(pattern) if isinstance(pattern, list) and len(pattern) in [3, 5] else pattern
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


def save_profiles(profiles: Dict) -> None:
    """Salva todos os perfis"""
    import os
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(PROFILES_FILE), exist_ok=True)
    
    # Serializar cada perfil antes de salvar
    serialized_profiles = {}
    for save_id, profile in profiles.items():
        serialized_profiles[save_id] = _serialize_profile_for_json(profile)
    
    try:
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(serialized_profiles, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar perfis: {e}")


# ============================================================================
# VERIFICAÇÃO DE EFEITOS
# ============================================================================

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
        try:
            # Verificar se os padrões são do formato antigo (3 elementos) ou novo (5 elementos)
            if not patterns or len(patterns) == 0:
                continue
            
            # Verificar formato do primeiro padrão
            first_pattern = patterns[0] if patterns else None
            
            # Se for formato antigo (3 elementos), pular (perfis antigos precisam ser regenerados)
            if first_pattern and len(first_pattern) == 3:
                # Formato antigo - pular por enquanto ou tentar migrar
                continue
            
            # Formato novo (5 elementos)
            if molecule_has_effect(molecule, patterns):
                effects.append(effect_name)
        except Exception as e:
            # Em caso de erro, continuar verificando outros efeitos
            print(f"Erro ao verificar efeito {effect_name}: {e}")
            continue
    
    return effects


def get_or_create_profile(save_id: str) -> Dict:
    """
    Obtém o perfil de um save, criando um novo se não existir.
    Se o perfil existir mas tiver padrões antigos (formato de 3 elementos),
    regenera o perfil com o novo formato (5 elementos com polaridade).
    
    Args:
        save_id: ID do save
    
    Returns:
        Dict com o perfil
    """
    profiles = load_profiles()
    
    # Verificar se precisa criar ou atualizar perfil
    needs_regeneration = False
    
    if save_id not in profiles:
        # Criar novo perfil
        needs_regeneration = True
    else:
        # Verificar se o perfil tem padrões antigos (3 elementos) e precisa ser atualizado
        profile = profiles[save_id]
        effect_patterns = profile.get('effect_patterns', {})
        
        # Se não há padrões, precisa regenerar
        if not effect_patterns or len(effect_patterns) == 0:
            needs_regeneration = True
        else:
            # Verificar se algum padrão está no formato antigo
            for effect_name, patterns in effect_patterns.items():
                if not patterns:
                    needs_regeneration = True
                    break
                    
                # Converter para lista se for tupla
                if isinstance(patterns, tuple):
                    patterns = list(patterns)
                
                # Verificar se tem exatamente 3 requisitos (novo formato)
                if isinstance(patterns, list):
                    # Se não tem exatamente 3 requisitos, está no formato antigo
                    if len(patterns) != 3:
                        needs_regeneration = True
                        break
                    
                    # Verificar formato de cada padrão individual
                    for pattern in patterns:
                        if not pattern:
                            needs_regeneration = True
                            break
                        
                        # Converter para lista se necessário
                        pattern_list = list(pattern) if isinstance(pattern, tuple) else pattern
                        
                        if isinstance(pattern_list, list):
                            # Se o padrão tem 3 elementos, está no formato antigo
                            if len(pattern_list) == 3:
                                needs_regeneration = True
                                break
                            # Se o padrão não tem exatamente 5 elementos, está no formato antigo
                            elif len(pattern_list) != 5:
                                needs_regeneration = True
                                break
                    
                    if needs_regeneration:
                        break
    
    if needs_regeneration:
        # Gerar novo perfil com formato atualizado
        profile = generate_property_profile(save_id)
        profile['generated_at'] = __import__('datetime').datetime.now().isoformat()
        profiles[save_id] = profile
        save_profiles(profiles)
        return profile
    
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


def delete_profile(save_id: str) -> bool:
    """
    Deleta o perfil de um save.
    
    Args:
        save_id: ID do save
    
    Returns:
        True se deletado com sucesso, False caso contrário
    """
    profiles = load_profiles()
    
    if save_id in profiles:
        del profiles[save_id]
        save_profiles(profiles)
        return True
    
    return False
