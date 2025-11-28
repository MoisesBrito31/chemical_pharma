"""
Gerencia saves dos jogadores
"""

import json
import os
import uuid
from datetime import datetime

SAVES_FILE = 'data/saves.json'

# Save ativo atualmente
_active_save_id = None

def load_saves():
    """Carrega todos os saves do arquivo JSON"""
    if not os.path.exists(SAVES_FILE):
        return {'saves': {}, 'active_save': None}
    
    try:
        with open(SAVES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Compatibilidade com formato antigo - garantir estrutura correta
            if 'saves' not in data:
                data['saves'] = {}
            if 'active_save' not in data:
                data['active_save'] = None
            
            return data
    except:
        return {'saves': {}, 'active_save': None}

def save_saves(data):
    """Salva os saves no arquivo JSON"""
    os.makedirs('data', exist_ok=True)
    with open(SAVES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_save(player_name):
    """
    Cria um novo save para um jogador
    
    Returns: save_id
    """
    data = load_saves()
    
    # Gerar ID único
    save_id = f"save_{uuid.uuid4().hex[:8]}"
    
    # Criar save
    new_save = {
        'id': save_id,
        'player_name': player_name,
        'created_at': datetime.now().isoformat(),
        'last_played': datetime.now().isoformat(),
        'money': 1000,
        'discoveries_count': 0,
        'syntheses_count': 0
    }
    
    data['saves'][save_id] = new_save
    save_saves(data)
    
    return save_id

def get_all_saves():
    """Retorna todos os saves"""
    data = load_saves()
    return list(data['saves'].values())

def get_save(save_id):
    """Obtém um save específico"""
    data = load_saves()
    return data['saves'].get(save_id)

def delete_save(save_id):
    """Deleta um save"""
    global _active_save_id
    
    data = load_saves()
    
    if save_id in data['saves']:
        del data['saves'][save_id]
        
        # Se era o save ativo, desativar
        if data['active_save'] == save_id:
            data['active_save'] = None
            _active_save_id = None
        
        save_saves(data)
        
        # Limpar descobertas deste save
        from .discovered_molecules import clear_discoveries
        clear_discoveries(save_id)
        
        return True
    
    return False

def set_active_save(save_id):
    """Define qual save está ativo"""
    global _active_save_id
    
    data = load_saves()
    
    if save_id not in data['saves']:
        return False
    
    # Atualizar last_played
    data['saves'][save_id]['last_played'] = datetime.now().isoformat()
    
    data['active_save'] = save_id
    _active_save_id = save_id
    
    save_saves(data)
    return True

def get_active_save_id():
    """Retorna o ID do save ativo"""
    global _active_save_id
    
    # Se já está em memória, retornar
    if _active_save_id:
        return _active_save_id
    
    # Carregar do arquivo
    data = load_saves()
    _active_save_id = data.get('active_save')
    return _active_save_id

def get_active_save():
    """Retorna os dados do save ativo"""
    save_id = get_active_save_id()
    if not save_id:
        return None
    
    return get_save(save_id)

def update_save_stats(save_id, money_increment=0, discoveries_increment=0, syntheses_increment=0):
    """Atualiza estatísticas de um save"""
    data = load_saves()
    
    if save_id not in data['saves']:
        return False
    
    save = data['saves'][save_id]
    
    if money_increment:
        save['money'] = save.get('money', 0) + money_increment
    
    if discoveries_increment:
        save['discoveries_count'] = save.get('discoveries_count', 0) + discoveries_increment
    
    if syntheses_increment:
        save['syntheses_count'] = save.get('syntheses_count', 0) + syntheses_increment
    
    save['last_played'] = datetime.now().isoformat()
    
    save_saves(data)
    return True

def add_discovery_to_save(save_id, molecule, formula=None, name=None):
    """
    Adiciona uma descoberta ao save e atualiza contadores
    
    Returns: discovery_id
    """
    from .discovered_molecules import add_discovery
    
    # Adicionar descoberta
    discovery_id = add_discovery(save_id, molecule, formula, name)
    
    # Atualizar estatísticas
    update_save_stats(save_id, discoveries_increment=1, money_increment=100)
    
    return discovery_id

