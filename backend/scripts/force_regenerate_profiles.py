"""
Script para FORÇAR a regeneração de todos os perfis de propriedades.

Útil quando mudanças na lógica de geração precisam ser aplicadas a todos os saves.
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.property_profiles import load_profiles, save_profiles, generate_property_profile
from datetime import datetime

def force_regenerate_all_profiles():
    """Força a regeneração de TODOS os perfis"""
    profiles = load_profiles()
    regenerated = 0
    
    for save_id in profiles.keys():
        print(f"🔄 Regenerando perfil para save: {save_id}")
        new_profile = generate_property_profile(save_id)
        new_profile['generated_at'] = datetime.now().isoformat()
        profiles[save_id] = new_profile
        regenerated += 1
    
    if regenerated > 0:
        save_profiles(profiles)
        print(f"✅ {regenerated} perfil(is) regenerado(s) com sucesso!")
    else:
        print("ℹ️ Nenhum perfil encontrado para regenerar.")
    
    return regenerated

if __name__ == '__main__':
    force_regenerate_all_profiles()

