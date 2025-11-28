"""
Gerencia o cache de resultados de síntese
"""

import json
import os
from .saves import get_active_save_id

CACHE_FILE = 'data/synthesis_cache.json'

def load_cache():
    """Carrega o cache de sínteses do arquivo JSON"""
    if not os.path.exists(CACHE_FILE):
        return {}
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    """Salva o cache no arquivo JSON"""
    os.makedirs('data', exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def get_cache_key(mol_a_id, mol_b_id, save_id):
    """Gera chave única para o cache (incluindo save_id)"""
    return f"{save_id}:{mol_a_id}+{mol_b_id}"

def get_synthesis_result(key):
    """Obtém resultado de síntese do cache"""
    cache = load_cache()
    
    # Adicionar save_id à chave se não tiver
    if ':' not in key:
        save_id = get_active_save_id()
        if save_id:
            key = f"{save_id}:{key}"
    
    return cache.get(key)

def save_synthesis_result(key, result):
    """Salva resultado de síntese no cache"""
    cache = load_cache()
    
    # Adicionar save_id à chave se não tiver
    if ':' not in key:
        save_id = get_active_save_id()
        if save_id:
            key = f"{save_id}:{key}"
    
    cache[key] = result
    save_cache(cache)

def get_all_results():
    """Retorna todos os resultados de síntese"""
    return load_cache()

def get_stats():
    """Retorna estatísticas sobre sínteses"""
    cache = load_cache()
    
    total = len(cache)
    successful = sum(1 for r in cache.values() if r.get('success'))
    failed = total - successful
    
    return {
        'total': total,
        'successful': successful,
        'failed': failed
    }

def clear_cache():
    """Limpa todo o cache de sínteses"""
    save_cache({})

