"""
Script para regenerar todos os perfis de propriedades com o novo formato.

Força a regeneração de todos os perfis que têm padrões antigos (3 elementos)
para o novo formato (4 requisitos de 5 elementos).
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.property_profiles import load_profiles, save_profiles, generate_property_profile
from datetime import datetime

def regenerate_all_profiles():
    """Regenera todos os perfis que têm padrões antigos"""
    profiles = load_profiles()
    regenerated = 0
    
    for save_id, profile in profiles.items():
        effect_patterns = profile.get('effect_patterns', {})
        needs_regeneration = False
        
        # Verificar se tem padrões antigos
        for effect_name, patterns in effect_patterns.items():
            if not patterns:
                needs_regeneration = True
                break
            
            if isinstance(patterns, list):
                # Verificar se tem menos de 4 requisitos
                if len(patterns) != 4:
                    needs_regeneration = True
                    break
                
                # Verificar formato dos padrões
                for pattern in patterns:
                    if not pattern:
                        needs_regeneration = True
                        break
                    
                    pattern_list = list(pattern) if isinstance(pattern, tuple) else pattern
                    
                    if isinstance(pattern_list, list):
                        # Se tem 3 elementos, está no formato antigo
                        if len(pattern_list) == 3:
                            needs_regeneration = True
                            break
                        # Se não tem 5 elementos, está no formato antigo
                        elif len(pattern_list) != 5:
                            needs_regeneration = True
                            break
                
                if needs_regeneration:
                    break
        
        if needs_regeneration:
            print(f"🔄 Regenerando perfil para save: {save_id}")
            new_profile = generate_property_profile(save_id)
            new_profile['generated_at'] = datetime.now().isoformat()
            profiles[save_id] = new_profile
            regenerated += 1
    
    if regenerated > 0:
        save_profiles(profiles)
        print(f"✅ {regenerated} perfil(is) regenerado(s) com sucesso!")
    else:
        print("✅ Todos os perfis já estão no formato novo!")
    
    return regenerated

if __name__ == '__main__':
    regenerate_all_profiles()

