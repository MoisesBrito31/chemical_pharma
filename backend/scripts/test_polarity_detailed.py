"""Teste detalhado para verificar consistência de polaridade"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.effect_patterns import generate_all_effect_requirements

reqs = generate_all_effect_requirements()

print("Verificando consistência de polaridade por tipo em cada efeito...\n")

all_ok = True
for effect_name, patterns in reqs.items():
    type_polarity = {}
    
    # Primeiro, coletar todas as polaridades usadas
    for req in patterns:
        type1, pol1, type2, pol2, mult = req
        
        if type1 not in type_polarity:
            type_polarity[type1] = pol1
        elif type_polarity[type1] != pol1:
            print(f"❌ {effect_name}: Conflito - {type1} tem polaridade {type_polarity[type1]} mas requisito pede {pol1}")
            print(f"   Requisito: {req}")
            all_ok = False
        
        if type2 not in type_polarity:
            type_polarity[type2] = pol2
        elif type_polarity[type2] != pol2:
            print(f"❌ {effect_name}: Conflito - {type2} tem polaridade {type_polarity[type2]} mas requisito pede {pol2}")
            print(f"   Requisito: {req}")
            all_ok = False

if all_ok:
    print("✅ Todos os efeitos respeitam a consistência de polaridade!\n")
    
    # Mostrar exemplos detalhados
    print("Exemplos detalhados:\n")
    for effect_name, patterns in list(reqs.items())[:3]:
        print(f"{effect_name}:")
        type_polarity = {}
        for req in patterns:
            type1, pol1, type2, pol2, mult = req
            type_polarity[type1] = pol1
            type_polarity[type2] = pol2
            print(f"  {type1}{pol1} ↔ {type2}{pol2} (×{mult})")
        print(f"  Resumo: {type_polarity}\n")

