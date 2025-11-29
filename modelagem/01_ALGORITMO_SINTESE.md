# Algoritmo de Síntese Molecular

## 📋 Visão Geral

O algoritmo de síntese combina duas moléculas seguindo um processo de 4 etapas para criar uma nova molécula estável ou detectar falhas na reação.

---

## 🔄 Fluxo Principal

```
Molécula A + Molécula B
        ↓
   [1] ANULAÇÃO
        ↓
   [2] MERGE (SOMA)
        ↓
   [3] REBOND (ESTABILIZAÇÃO)
        ↓
   [4] REORGANIZAÇÃO
        ↓
   Resultado Final
```

---

## 📊 Etapa 1: Anulação (Annihilation)

### Objetivo
Remover pares de partículas com **mesmo tipo** mas **polaridades opostas**.

### Algoritmo
```python
def annihilate_particles(molecule_a, molecule_b):
    to_remove_a = set()
    to_remove_b = set()
    annihilated_pairs = 0
    
    for particle_a in molecule_a.particles:
        if particle_a.id in to_remove_a:
            continue
            
        for particle_b in molecule_b.particles:
            if particle_b.id in to_remove_b:
                continue
            
            # Anular se mesmo tipo e polaridades opostas
            if (particle_a.type == particle_b.type and 
                particle_a.polarity != particle_b.polarity):
                to_remove_a.add(particle_a.id)
                to_remove_b.add(particle_b.id)
                annihilated_pairs += 1
                break  # Próxima partícula de A
    
    # Remover partículas e bonds associados
    molecule_a = remove_particles(molecule_a, to_remove_a)
    molecule_b = remove_particles(molecule_b, to_remove_b)
    
    return molecule_a, molecule_b, annihilated_pairs
```

### Regras de Validação
1. **Se annihilated_pairs == 0**: Falha `no_reaction`
   - Não há reação química válida
   
2. **Se todas as partículas foram anuladas**: Falha `complete_annihilation`
   - Nada sobrou para formar molécula

### Exemplo
```
Molécula A: ○+ □- △+
Molécula B: ○- □+ ⬠-

Anulação:
  ○+ com ○-  → ANULADO
  □- com □+  → ANULADO

Resultado:
  Molécula A: △+
  Molécula B: ⬠-
  Pares anulados: 2
```

---

## 🔗 Etapa 2: Merge (Soma em Novo)

### Objetivo
Combinar as moléculas restantes em uma única estrutura, renomeando IDs de forma ordenada para garantir **comutatividade** (A+B = B+A).

### Algoritmo
```python
def merge_molecules(molecule_a, molecule_b):
    all_particles = []
    all_bonds = []
    
    # Coletar todas as partículas com origem
    for particle in molecule_a.particles:
        all_particles.append({
            'origin': 'a',
            'old_id': particle.id,
            'type': particle.type,
            'polarity': particle.polarity,
            'x': particle.x,
            'y': particle.y
        })
    
    for particle in molecule_b.particles:
        all_particles.append({
            'origin': 'b',
            'old_id': particle.id,
            'type': particle.type,
            'polarity': particle.polarity,
            'x': particle.x,
            'y': particle.y
        })
    
    # ORDENAR para garantir comutatividade
    # Ordem: tipo (circle < square < triangle < pentagon), depois polaridade
    type_order = {'circle': 0, 'square': 1, 'triangle': 2, 'pentagon': 3}
    all_particles.sort(key=lambda p: (type_order[p.type], p.polarity))
    
    # Renomear IDs em ordem
    id_map = {}
    new_particles = []
    for idx, particle in enumerate(all_particles):
        new_id = f'p{idx}'
        old_key = f"{particle.origin}_{particle.old_id}"
        id_map[old_key] = new_id
        
        new_particles.append({
            'id': new_id,
            'type': particle.type,
            'polarity': particle.polarity,
            'x': particle.x,
            'y': particle.y
        })
    
    # Atualizar bonds com novos IDs
    new_bonds = []
    for bond in all_bonds:
        from_key = f"{bond.origin}_{bond.from}"
        to_key = f"{bond.origin}_{bond.to}"
        
        new_bonds.append({
            'from': id_map[from_key],
            'to': id_map[to_key],
            'multiplicity': bond.multiplicity
        })
    
    return {'particles': new_particles, 'bonds': new_bonds}
```

### Garantia de Comutatividade
A ordenação garante que independente da ordem de entrada (A+B ou B+A), as partículas sempre terão os mesmos IDs finais.

### Exemplo
```
A: △+ (p0)          B: ○- (p0)
   ⬠- (p1)             □+ (p1)

Merge Ordenado:
  1. circle-  → p0
  2. square+  → p1
  3. triangle+ → p2
  4. pentagon- → p3

Resultado idêntico para A+B ou B+A ✓
```

---

## ⚡ Etapa 3: Rebond (Estabilização)

### Objetivo
Criar novas ligações para estabilizar partículas que ficaram com **conexões insuficientes**.

### Regras de Conexão
| Partícula | Conexões Necessárias |
|-----------|---------------------|
| Círculo   | 1                   |
| Quadrado  | 2                   |
| Triângulo | 3                   |
| Pentágono | 4                   |

### Algoritmo
```python
def rebond_molecule(molecule):
    max_iterations = 100
    
    for iteration in range(max_iterations):
        # Calcular conexões atuais
        connection_count = calculate_connections(molecule)
        
        # Encontrar partículas instáveis
        unstable = []
        for particle in molecule.particles:
            max_connections = PARTICLE_TYPES[particle.type].connections
            current_connections = connection_count.get(particle.id, 0)
            
            if current_connections < max_connections:
                unstable.append({
                    'id': particle.id,
                    'type': particle.type,
                    'missing': max_connections - current_connections
                })
        
        # Se todas estáveis, sucesso!
        if not unstable:
            return molecule
        
        # ORDENAR por conexões faltantes (maior primeiro)
        # Isso prioriza partículas que precisam de mais conexões
        unstable.sort(key=lambda x: x.missing, reverse=True)
        
        # Tentar criar UMA ligação
        bond_created = False
        
        for u1 in unstable:
            if bond_created:
                break
            
            for u2 in unstable:
                if u1.id == u2.id:
                    continue
                
                # Mesmo tipo não pode se ligar
                if u1.type == u2.type:
                    continue
                
                # Verificar se já existe bond
                existing_bond = find_bond(molecule, u1.id, u2.id)
                
                if existing_bond:
                    # Aumentar multiplicidade
                    existing_bond.multiplicity += 1
                    bond_created = True
                    break
                else:
                    # Criar nova ligação
                    molecule.bonds.append({
                        'from': u1.id,
                        'to': u2.id,
                        'multiplicity': 1
                    })
                    bond_created = True
                    break
        
        # Se não conseguiu criar ligação, falha
        if not bond_created:
            return None  # Falha: cannot_rebond
    
    return None  # Timeout
```

### Priorização Inteligente
A ordenação por `missing` (conexões faltantes) garante que partículas que precisam de **mais conexões** sejam atendidas primeiro, evitando situações onde uma partícula fica isolada.

### Exemplo
```
Após Merge: ○- △- ⬠+
Conexões necessárias:
  ○-: 1 (falta 1)
  △-: 3 (falta 3)  ← PRIORIDADE
  ⬠+: 4 (falta 4)  ← PRIORIDADE

Iteração 1: ⬠+-△- (mult=3)
Iteração 2: ⬠+-○- (mult=1)

Resultado: Todas estáveis ✓
```

---

## 🔍 Etapa 3.5: Detecção de Componentes

### Objetivo
Verificar se o resultado é uma **molécula única conectada** ou **múltiplas moléculas separadas**.

### Algoritmo (BFS - Breadth-First Search)
```python
def find_connected_components(molecule):
    # Construir grafo de adjacência
    adjacency = {p.id: [] for p in molecule.particles}
    for bond in molecule.bonds:
        adjacency[bond.from].append(bond.to)
        adjacency[bond.to].append(bond.from)
    
    visited = set()
    components = []
    
    for particle in molecule.particles:
        if particle.id in visited:
            continue
        
        # BFS para este componente
        component = set()
        queue = deque([particle.id])
        component.add(particle.id)
        visited.add(particle.id)
        
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        
        components.append(component)
    
    return components
```

### Resultado
- **1 componente**: Molécula única → Continuar
- **2+ componentes**: Múltiplas moléculas → Separar cada uma

### Exemplo
```
Bonds: p0-p1, p2-p3

BFS:
  Componente 1: {p0, p1}
  Componente 2: {p2, p3}

Resultado: 2 moléculas separadas
```

---

## 📐 Etapa 4: Reorganização de Posições

### Objetivo
Ajustar coordenadas (x, y) das partículas para visualização clara, mantendo partículas ligadas próximas.

### Algoritmo (BFS com Posicionamento)
```python
def reorganize_positions(molecule):
    if len(molecule.particles) == 0:
        return
    
    # Resetar posições
    for particle in molecule.particles:
        particle.x = 0
        particle.y = 0
    
    # Construir grafo de adjacência
    adjacency = build_adjacency(molecule.bonds)
    
    # BFS começando da primeira partícula
    visited = set()
    queue = deque([(molecule.particles[0].id, 0, 0)])  # (id, x, y)
    visited.add(molecule.particles[0].id)
    
    # Direções para posicionar vizinhos
    directions = [
        (1, 0),   # Direita
        (-1, 0),  # Esquerda
        (0, 1),   # Cima
        (0, -1),  # Baixo
    ]
    
    while queue:
        current_id, x, y = queue.popleft()
        
        # Atualizar posição
        particle = find_particle(molecule, current_id)
        particle.x = x
        particle.y = y
        
        # Posicionar vizinhos
        dir_idx = 0
        for neighbor_id in adjacency[current_id]:
            if neighbor_id in visited:
                continue
            
            visited.add(neighbor_id)
            
            # Usar próxima direção
            dx, dy = directions[dir_idx % len(directions)]
            new_x = x + dx
            new_y = y + dy
            
            queue.append((neighbor_id, new_x, new_y))
            dir_idx += 1
```

### Coordenadas Lógicas
As coordenadas são **lógicas** (ex: 0, 1, 2) e não visuais. O frontend multiplica por um fator de espaçamento para visualização.

---

## 📊 Fluxo Completo com Exemplo

### Entrada
```
Molécula A: □+ (p0, com ○-, p1)
Molécula B: □- (p0, com △-, p1)
```

### Etapa 1: Anulação
```
□+ com □-  → ANULADO

Resultado:
  A: ○- (p1)
  B: △- (p1)
  Pares anulados: 1
```

### Etapa 2: Merge
```
Ordenação: circle-, triangle-
Novos IDs:
  ○-: p0
  △-: p1
```

### Etapa 3: Rebond
```
Conexões:
  p0 (○-): 0/1 (falta 1)
  p1 (△-): 0/3 (falta 3) ← PRIORIDADE

Criar bonds:
  p1-p0 (mult=1)

Resultado:
  p0: 1/1 ✓
  p1: 1/3 ✗

Falha: cannot_rebond
```

### Resultado Final
```
Sucesso: False
Razão: cannot_rebond
```

---

## 🎯 Casos Especiais

### Caso 1: Molécula Única
```
Resultado normal com 1 molécula
{
  "success": true,
  "multiple": false,
  "result": {...}
}
```

### Caso 2: Múltiplas Moléculas
```
Resultado com N moléculas separadas
{
  "success": true,
  "multiple": true,
  "result": [{...}, {...}],
  "details": {"molecules_count": 2}
}
```

### Caso 3: Sem Reação
```
Nenhuma partícula anulada
{
  "success": false,
  "details": {"reason": "no_reaction"}
}
```

### Caso 4: Anulação Completa
```
Todas as partículas anuladas
{
  "success": false,
  "details": {"reason": "complete_annihilation"}
}
```

### Caso 5: Não Estabilizou
```
Rebond não conseguiu estabilizar
{
  "success": false,
  "details": {"reason": "cannot_rebond"}
}
```

---

## 📈 Complexidade

| Etapa | Complexidade | Observações |
|-------|-------------|-------------|
| Anulação | O(n × m) | n = partículas A, m = partículas B |
| Merge | O((n+m) log(n+m)) | Ordenação dominante |
| Rebond | O(p² × i) | p = partículas, i = iterações (~100) |
| Detecção | O(p + b) | p = partículas, b = bonds (BFS) |
| Reorganização | O(p + b) | BFS para posicionamento |

**Total**: O(p² × i) dominado pelo Rebond

---

## 🔬 Validações Implementadas

✅ Anulação obrigatória (no_reaction se zero)  
✅ Comutatividade (A+B = B+A)  
✅ Priorização inteligente no rebond  
✅ Detecção de moléculas desconectadas  
✅ Limite de iterações no rebond (100)  
✅ Validação de tipos diferentes para bonds  
✅ Suporte para múltiplas ligações (multiplicidade)  

---

**Implementação**: `backend/core/synthesis.py`


