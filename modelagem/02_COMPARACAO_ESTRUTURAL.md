# Algoritmo de Comparação Estrutural de Moléculas

## 📋 Visão Geral

Sistema para identificar se duas moléculas são **estruturalmente idênticas** (isômeros), considerando não apenas a composição de partículas, mas também a topologia das ligações.

---

## ❓ Por Que Não Usar Apenas a Fórmula?

### Problema: Isômeros
Moléculas com a mesma **fórmula molecular** podem ter **estruturas diferentes**.

### Exemplo
```
Fórmula: C²QT (2 circles, 1 square, 1 triangle)

Estrutura 1:          Estrutura 2:
    ○-□-○                 ○-□
       |                  |
       △                  ○-△

Mesma fórmula, estruturas DIFERENTES!
```

---

## 🔍 Abordagem: Comparação Estrutural

### Critérios de Identidade
Duas moléculas são idênticas se e somente se:

1. ✅ **Mesmas partículas** (tipo + polaridade)
2. ✅ **Mesmas ligações** (bonds com multiplicidade)
3. ✅ **Mesma topologia** (grafo isomórfico)

---

## 🧬 Algoritmo: areMoleculesIdentical()

### Implementação
```python
def areMoleculesIdentical(mol1, mol2):
    """
    Compara duas moléculas estruturalmente
    
    Returns: True se idênticas, False caso contrário
    """
    
    # 1. Verificar tamanho
    if len(mol1.particles) != len(mol2.particles):
        return False
    
    if len(mol1.bonds) != len(mol2.bonds):
        return False
    
    # 2. Criar multisets de partículas
    particles1 = sorted([
        (p.type, p.polarity) 
        for p in mol1.particles
    ])
    
    particles2 = sorted([
        (p.type, p.polarity) 
        for p in mol2.particles
    ])
    
    if particles1 != particles2:
        return False
    
    # 3. Verificar bonds estruturalmente
    # Criar conjunto de bonds normalizados
    bonds1 = create_bond_set(mol1)
    bonds2 = create_bond_set(mol2)
    
    if bonds1 != bonds2:
        return False
    
    return True


def create_bond_set(molecule):
    """
    Cria conjunto de bonds baseado na estrutura,
    não nos IDs específicos das partículas
    """
    bonds_normalized = set()
    
    for bond in molecule.bonds:
        # Buscar tipos e polaridades das partículas
        p_from = find_particle(molecule, bond.from)
        p_to = find_particle(molecule, bond.to)
        
        # Criar tupla ordenada (menor tipo primeiro)
        bond_tuple = (
            (p_from.type, p_from.polarity),
            (p_to.type, p_to.polarity),
            bond.multiplicity
        )
        
        # Normalizar ordem
        if bond_tuple[0] > bond_tuple[1]:
            bond_tuple = (bond_tuple[1], bond_tuple[0], bond_tuple[2])
        
        bonds_normalized.add(bond_tuple)
    
    return bonds_normalized
```

---

## 📊 Exemplo Detalhado

### Molécula 1
```json
{
  "particles": [
    {"id": "p0", "type": "circle", "polarity": "-"},
    {"id": "p1", "type": "square", "polarity": "+"},
    {"id": "p2", "type": "triangle", "polarity": "-"}
  ],
  "bonds": [
    {"from": "p0", "to": "p1", "multiplicity": 1},
    {"from": "p1", "to": "p2", "multiplicity": 2}
  ]
}
```

### Molécula 2
```json
{
  "particles": [
    {"id": "a", "type": "circle", "polarity": "-"},
    {"id": "b", "type": "triangle", "polarity": "-"},
    {"id": "c", "type": "square", "polarity": "+"}
  ],
  "bonds": [
    {"from": "a", "to": "c", "multiplicity": 1},
    {"from": "c", "to": "b", "multiplicity": 2}
  ]
}
```

### Passo 1: Comparar Partículas
```python
# Molécula 1
particles1 = sorted([
    ('circle', '-'),
    ('square', '+'),
    ('triangle', '-')
])
# Resultado: [('circle', '-'), ('square', '+'), ('triangle', '-')]

# Molécula 2
particles2 = sorted([
    ('circle', '-'),
    ('triangle', '-'),
    ('square', '+')
])
# Resultado: [('circle', '-'), ('square', '+'), ('triangle', '-')]

particles1 == particles2  # ✅ True
```

### Passo 2: Normalizar Bonds
```python
# Molécula 1
bonds1 = {
    (('circle', '-'), ('square', '+'), 1),
    (('square', '+'), ('triangle', '-'), 2)
}

# Molécula 2
bonds2 = {
    (('circle', '-'), ('square', '+'), 1),
    (('square', '+'), ('triangle', '-'), 2)
}

bonds1 == bonds2  # ✅ True
```

### Resultado
```
✅ Moléculas IDÊNTICAS
(Mesmo que IDs das partículas sejam diferentes)
```

---

## 🔬 Fingerprint Molecular

### Conceito
Criar uma **string única** que representa a estrutura da molécula, usada para comparações rápidas.

### Implementação
```python
def getMoleculeFingerprint(molecule):
    """
    Gera impressão digital única da estrutura molecular
    
    Format: "particles|bonds"
    """
    
    # 1. Ordenar partículas
    particles_str = ','.join(sorted([
        f"{p.type}:{p.polarity}"
        for p in molecule.particles
    ]))
    
    # 2. Ordenar bonds
    bonds_list = []
    for bond in molecule.bonds:
        p_from = find_particle(molecule, bond.from)
        p_to = find_particle(molecule, bond.to)
        
        # Criar tupla ordenada
        bond_key = tuple(sorted([
            f"{p_from.type}:{p_from.polarity}",
            f"{p_to.type}:{p_to.polarity}"
        ]))
        
        bonds_list.append(f"{bond_key[0]}~{bond_key[1]}*{bond.multiplicity}")
    
    bonds_str = ','.join(sorted(bonds_list))
    
    return f"{particles_str}|{bonds_str}"
```

### Exemplo
```python
molecule = {
    "particles": [
        {"id": "p0", "type": "circle", "polarity": "-"},
        {"id": "p1", "type": "square", "polarity": "+"}
    ],
    "bonds": [
        {"from": "p0", "to": "p1", "multiplicity": 2}
    ]
}

fingerprint = getMoleculeFingerprint(molecule)
# Resultado: "circle:-,square:+|circle:-~square:+*2"
```

### Uso
```python
# Comparação rápida
if getMoleculeFingerprint(mol1) == getMoleculeFingerprint(mol2):
    print("Moléculas idênticas!")
```

---

## 🎯 Casos de Teste

### Caso 1: Moléculas Idênticas
```python
mol1 = {
    "particles": [
        {"id": "p0", "type": "circle", "polarity": "+"},
        {"id": "p1", "type": "triangle", "polarity": "-"}
    ],
    "bonds": [
        {"from": "p0", "to": "p1", "multiplicity": 1}
    ]
}

mol2 = {
    "particles": [
        {"id": "a", "type": "triangle", "polarity": "-"},
        {"id": "b", "type": "circle", "polarity": "+"}
    ],
    "bonds": [
        {"from": "b", "to": "a", "multiplicity": 1}
    ]
}

areMoleculesIdentical(mol1, mol2)  # ✅ True
```

### Caso 2: Mesma Fórmula, Estrutura Diferente
```python
mol1 = {
    "particles": [
        {"id": "p0", "type": "circle", "polarity": "-"},
        {"id": "p1", "type": "square", "polarity": "+"},
        {"id": "p2", "type": "circle", "polarity": "-"}
    ],
    "bonds": [
        {"from": "p0", "to": "p1", "multiplicity": 1},
        {"from": "p1", "to": "p2", "multiplicity": 1}
    ]
}

mol2 = {
    "particles": [
        {"id": "p0", "type": "circle", "polarity": "-"},
        {"id": "p1", "type": "square", "polarity": "+"},
        {"id": "p2", "type": "circle", "polarity": "-"}
    ],
    "bonds": [
        {"from": "p0", "to": "p2", "multiplicity": 2}  # Diferente!
    ]
}

areMoleculesIdentical(mol1, mol2)  # ❌ False
```

### Caso 3: Multiplicidade Diferente
```python
mol1 = {
    "particles": [...],  # Mesmas
    "bonds": [
        {"from": "p0", "to": "p1", "multiplicity": 1}
    ]
}

mol2 = {
    "particles": [...],  # Mesmas
    "bonds": [
        {"from": "p0", "to": "p1", "multiplicity": 2}  # Diferente!
    ]
}

areMoleculesIdentical(mol1, mol2)  # ❌ False
```

---

## 🔍 Busca em Lista

### Função: moleculeExistsInList()
```python
def moleculeExistsInList(molecule, molecule_list):
    """
    Verifica se molécula existe na lista (estruturalmente)
    
    Args:
        molecule: Molécula a buscar
        molecule_list: Lista de moléculas
        
    Returns: True se encontrada, False caso contrário
    """
    
    for existing_mol in molecule_list:
        if areMoleculesIdentical(molecule, existing_mol):
            return True
    
    return False
```

### Uso no Sistema
```python
# Verificar se é nova descoberta
def isNewDiscovery(synthesized_molecule, known_molecules):
    return not moleculeExistsInList(
        synthesized_molecule,
        known_molecules
    )
```

---

## 📈 Complexidade

### areMoleculesIdentical()
```
- Comparar tamanhos: O(1)
- Ordenar partículas: O(p log p)
- Criar bond sets: O(b)
- Comparar sets: O(b)

Total: O(p log p + b)
onde p = partículas, b = bonds
```

### moleculeExistsInList()
```
O(n × (p log p + b))
onde n = tamanho da lista
```

### Otimização com Fingerprint
```
O(n × h)
onde h = custo do hash (muito menor)
```

---

## 🎨 Limitações e Melhorias Futuras

### Limitações Atuais
1. **Não detecta simetria molecular** (rotações/reflexões)
2. **Comparação linear na lista** (O(n))

### Melhorias Possíveis
1. **Usar hash table com fingerprints**
   - Busca O(1) em vez de O(n)
   
2. **Canonical labeling** 
   - Detectar isomorfismo de grafos completo
   
3. **Cache de fingerprints**
   - Calcular uma vez, reusar várias vezes

---

## 🔬 Testes de Validação

### Suite de Testes
```python
def test_identical_molecules():
    # Mesma estrutura, IDs diferentes
    assert areMoleculesIdentical(mol1, mol2) == True

def test_different_structure():
    # Mesma fórmula, estrutura diferente
    assert areMoleculesIdentical(mol1, mol2) == False

def test_different_multiplicity():
    # Mesma topologia, multiplicidade diferente
    assert areMoleculesIdentical(mol1, mol2) == False

def test_different_polarities():
    # Mesma topologia, polaridades diferentes
    assert areMoleculesIdentical(mol1, mol2) == False

def test_exists_in_list():
    known = [mol1, mol2, mol3]
    assert moleculeExistsInList(mol4, known) == False
    assert moleculeExistsInList(mol1_copy, known) == True
```

---

## 💡 Insights

### Por Que Isso É Importante?
1. **Evitar duplicatas** na biblioteca
2. **Identificar novas descobertas** corretamente
3. **Detectar isômeros** (mesma fórmula, estrutura diferente)
4. **Validar sínteses** (resultado esperado vs obtido)

### Exemplo Real
```
Síntese: A + B

Resultado esperado: ○-□
Resultado obtido: □-○

Sem comparação estrutural: "Nova molécula!"
Com comparação estrutural: "Já conhecida!" ✓
```

---

**Implementação**: `frontend/src/utils/moleculeComparison.js`


