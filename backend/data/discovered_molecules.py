"""
Gerencia moléculas descobertas pelos jogadores
Cada save tem suas próprias descobertas
"""

import json
import os
import uuid
from datetime import datetime

DISCOVERIES_FILE = 'data/discovered_molecules.json'

def load_discoveries():
    """Carrega todas as descobertas de todos os saves"""
    if not os.path.exists(DISCOVERIES_FILE):
        return {}
    
    try:
        with open(DISCOVERIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_discoveries(discoveries):
    """Salva as descobertas no arquivo JSON"""
    os.makedirs('data', exist_ok=True)
    with open(DISCOVERIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(discoveries, f, indent=2, ensure_ascii=False)

def get_next_discovery_name_count(save_id):
    """Obtém o próximo número para nomes padrão (Descoberta #1, #2, etc)"""
    discoveries = load_discoveries()
    save_discoveries = discoveries.get(save_id, {})
    
    count = 1
    while True:
        name = f"Descoberta #{count}"
        exists = any(d.get('name') == name for d in save_discoveries.values())
        if not exists:
            return count
        count += 1

def add_discovery(save_id, molecule, formula=None, name=None):
    """
    Adiciona uma nova descoberta para um save específico
    
    Returns: discovery_id
    """
    discoveries = load_discoveries()
    
    # Garantir que existe dicionário para este save
    if save_id not in discoveries:
        discoveries[save_id] = {}
    
    # Gerar ID único
    discovery_id = f"disc_{uuid.uuid4().hex[:8]}"
    
    # Gerar nome padrão se não fornecido
    if not name:
        count = get_next_discovery_name_count(save_id)
        name = f"Descoberta #{count}"
    
    # Criar descoberta
    discovery = {
        'id': discovery_id,
        'molecule': molecule,
        'formula': formula or '',
        'name': name,
        'discovered_at': datetime.now().isoformat()
    }
    
    discoveries[save_id][discovery_id] = discovery
    save_discoveries(discoveries)
    
    return discovery_id

def get_discovery(save_id, discovery_id):
    """Obtém uma descoberta específica"""
    discoveries = load_discoveries()
    save_discoveries = discoveries.get(save_id, {})
    return save_discoveries.get(discovery_id)

def get_all_discoveries(save_id):
    """Retorna todas as descobertas de um save"""
    discoveries = load_discoveries()
    save_discoveries = discoveries.get(save_id, {})
    return list(save_discoveries.values())

def clear_discoveries(save_id):
    """Limpa todas as descobertas de um save"""
    discoveries = load_discoveries()
    if save_id in discoveries:
        discoveries[save_id] = {}
        save_discoveries(discoveries)

def delete_discovery(save_id, discovery_id):
    """Deleta uma descoberta específica"""
    discoveries = load_discoveries()
    
    if save_id in discoveries and discovery_id in discoveries[save_id]:
        del discoveries[save_id][discovery_id]
        save_discoveries(discoveries)
        return True
    
    return False

def get_stats(save_id):
    """Retorna estatísticas sobre descobertas de um save"""
    discoveries = get_all_discoveries(save_id)
    
    return {
        'total': len(discoveries),
        'recent': discoveries[-5:] if len(discoveries) > 0 else []
    }

def find_discovery_by_id(discovery_id):
    """Busca uma descoberta por ID em todos os saves"""
    discoveries = load_discoveries()
    
    for save_id, save_discoveries in discoveries.items():
        if discovery_id in save_discoveries:
            return save_discoveries[discovery_id]
    
    return None

