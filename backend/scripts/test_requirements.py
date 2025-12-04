"""Script para testar se os requisitos gerados são válidos"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.effect_patterns import generate_all_effect_requirements
from data.molecules import PARTICLE_TYPES

# Limites de conexões
MAX_CONNECTIONS = {
    'circle': PARTICLE_TYPES['circle']['connections'],
    'square': PARTICLE_TYPES['square']['connections'],
    'triangle': PARTICLE_TYPES['triangle']['connections'],
    'pentagon': PARTICLE_TYPES['pentagon']['connections']
}

reqs = generate_all_effect_requirements()

print(f"Total de efeitos: {len(reqs)}")
print(f"Total de requisitos: {sum(len(patterns) for patterns in reqs.values())}")

# Verificar cada requisito
errors = []
for effect_name, patterns in reqs.items():
    for req in patterns:
        type1, pol1, type2, pol2, mult = req
        
        # 1. Mesmo tipo?
        if type1 == type2:
            errors.append((effect_name, req, "Mesmo tipo"))
        
        # 2. Mesma polaridade?
        if pol1 == pol2:
            errors.append((effect_name, req, "Mesma polaridade"))
        
        # 3. Multiplicidade excede conexões?
        max_mult = min(MAX_CONNECTIONS[type1], MAX_CONNECTIONS[type2])
        if mult > max_mult:
            errors.append((effect_name, req, f"Multiplicidade {mult} > max {max_mult}"))

if errors:
    print(f"\n❌ ERROS ENCONTRADOS: {len(errors)}")
    for effect, req, reason in errors[:10]:
        print(f"  {effect}: {req} - {reason}")
else:
    print("\n✅ Todos os requisitos são válidos!")
    print("\nExemplos de requisitos válidos:")
    for i, (effect, patterns) in enumerate(list(reqs.items())[:3]):
        print(f"\n{effect}:")
        for req in patterns:
            type1, pol1, type2, pol2, mult = req
            max_mult = min(MAX_CONNECTIONS[type1], MAX_CONNECTIONS[type2])
            print(f"  {type1}{pol1} ↔ {type2}{pol2} (×{mult}) [max: {max_mult}]")

