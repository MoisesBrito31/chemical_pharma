"""Script para testar se os requisitos respeitam a consistência de polaridade por tipo"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.effect_patterns import generate_all_effect_requirements

reqs = generate_all_effect_requirements()

print(f"Total de efeitos: {len(reqs)}")
print(f"Total de requisitos: {sum(len(patterns) for patterns in reqs.values())}\n")

# Verificar consistência de polaridade dentro de cada efeito
errors = []
for effect_name, patterns in reqs.items():
    # Mapa para rastrear polaridades por tipo
    type_polarity = {}
    
    for req in patterns:
        type1, pol1, type2, pol2, mult = req
        
        # Verificar tipo1
        if type1 in type_polarity:
            if type_polarity[type1] != pol1:
                errors.append((effect_name, req, f"Tipo {type1} já tem polaridade {type_polarity[type1]}, mas requisito pede {pol1}"))
        else:
            type_polarity[type1] = pol1
        
        # Verificar tipo2
        if type2 in type_polarity:
            if type_polarity[type2] != pol2:
                errors.append((effect_name, req, f"Tipo {type2} já tem polaridade {type_polarity[type2]}, mas requisito pede {pol2}"))
        else:
            type_polarity[type2] = pol2

if errors:
    print(f"❌ ERROS ENCONTRADOS: {len(errors)}")
    for effect, req, reason in errors[:10]:
        print(f"\n  {effect}:")
        print(f"    Requisito: {req}")
        print(f"    Erro: {reason}")
else:
    print("✅ Todos os requisitos respeitam a consistência de polaridade por tipo!")
    print("\nExemplos de efeitos com requisitos consistentes:")
    for i, (effect, patterns) in enumerate(list(reqs.items())[:3]):
        print(f"\n{effect}:")
        type_pol = {}
        for req in patterns:
            type1, pol1, type2, pol2, mult = req
            type_pol[type1] = pol1
            type_pol[type2] = pol2
            print(f"  {type1}{pol1} ↔ {type2}{pol2} (×{mult})")
        print(f"  Polaridades usadas: {type_pol}")

