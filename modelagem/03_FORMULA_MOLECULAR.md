# Sistema de Fórmula Molecular (Notação CQTP)

## 📋 Visão Geral

Sistema de notação para representar a composição molecular baseado no **número de conexões** de cada tipo de partícula, não na ordem alfabética tradicional.

---

## 🎯 Objetivos

1. **Representação compacta** da composição
2. **Ordenação por complexidade** (menos conexões → mais conexões)
3. **Fácil identificação** visual de tipos de partículas
4. **Independente de polaridade** (carga vem separada)

---

## 🔤 Mapeamento de Símbolos

| Partícula | Símbolo | Conexões | Razão da Ordem |
|-----------|---------|----------|----------------|
| Circle    | **C**   | 1        | Menos complexa |
| Square    | **Q**   | 2        | 2ª mais simples |
| Triangle  | **T**   | 3        | 3ª mais simples |
| Pentagon  | **P**   | 4        | Mais complexa |

### Por Que "Q" para Square?
- **C** já usado para Circle
- **Q** lembra visualmente um quadrado
- **S** seria confuso (Sulfur, Silicon em química real)

---

## 📐 Algoritmo de Geração

### Implementação
```python
def calculate_molecular_formula(molecule):
    """
    Gera fórmula molecular no padrão CQTP
    
    Args:
        molecule: Objeto com partículas
        
    Returns: String no formato "CQTP" com expoentes
    
    Exemplos:
        - C²QT: 2 circles, 1 square, 1 triangle
        - P³: 3 pentagons
        - CQ²TP²: 1 circle, 2 squares, 1 triangle, 2 pentagons
    """
    
    # 1. Contar partículas por tipo
    particle_counts = {}
    for particle in molecule.particles:
        ptype = particle.type
        particle_counts[ptype] = particle_counts.get(ptype, 0) + 1
    
    # 2. Ordenar por número de conexões
    type_order = [
        ('circle', 'C', 1),
        ('square', 'Q', 2),
        ('triangle', 'T', 3),
        ('pentagon', 'P', 4)
    ]
    
    # 3. Construir fórmula
    formula_parts = []
    for type_name, symbol, _ in type_order:
        count = particle_counts.get(type_name, 0)
        
        if count == 0:
            continue  # Não incluir
        elif count == 1:
            formula_parts.append(symbol)  # C, Q, T, P
        else:
            formula_parts.append(f"{symbol}{to_superscript(count)}")  # C², Q³
    
    return ''.join(formula_parts)


def to_superscript(number):
    """
    Converte número para Unicode superscript
    
    Examples:
        2 → ²
        3 → ³
        10 → ¹⁰
    """
    superscript_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    
    return ''.join(superscript_map[d] for d in str(number))
```

---

## 📊 Exemplos

### Exemplo 1: Molécula Simples
```json
{
  "particles": [
    {"type": "circle", "polarity": "-"},
    {"type": "square", "polarity": "+"}
  ]
}
```
**Fórmula:** `CQ`

---

### Exemplo 2: Com Repetições
```json
{
  "particles": [
    {"type": "circle", "polarity": "+"},
    {"type": "circle", "polarity": "-"},
    {"type": "square", "polarity": "+"}
  ]
}
```
**Fórmula:** `C²Q`

---

### Exemplo 3: Múltiplos Tipos
```json
{
  "particles": [
    {"type": "circle", "polarity": "+"},
    {"type": "square", "polarity": "-"},
    {"type": "square", "polarity": "+"},
    {"type": "triangle", "polarity": "-"}
  ]
}
```
**Fórmula:** `CQ²T`

---

### Exemplo 4: Todos os Tipos
```json
{
  "particles": [
    {"type": "circle", "polarity": "+"},
    {"type": "square", "polarity": "-"},
    {"type": "triangle", "polarity": "+"},
    {"type": "pentagon", "polarity": "-"}
  ]
}
```
**Fórmula:** `CQTP`

---

### Exemplo 5: Pentágonos Dominantes
```json
{
  "particles": [
    {"type": "pentagon", "polarity": "+"},
    {"type": "pentagon", "polarity": "-"},
    {"type": "pentagon", "polarity": "+"}
  ]
}
```
**Fórmula:** `P³`

---

## 🔬 Propriedades Adicionais

### Massa Molecular
```python
def get_molecular_mass(molecule):
    """
    Massa = número total de partículas
    """
    return len(molecule.particles)
```

### Carga Molecular
```python
def get_molecular_charge(molecule):
    """
    Carga = soma das polaridades
    
    Returns:
        > 0: Positiva
        < 0: Negativa
        = 0: Neutra
    """
    charge = 0
    for particle in molecule.particles:
        charge += 1 if particle.polarity == '+' else -1
    
    return charge


def get_charge_label(charge):
    """
    Retorna label legível
    """
    if charge > 0:
        return f"+{charge} (positiva)"
    elif charge < 0:
        return f"{charge} (negativa)"
    else:
        return "0 (neutra)"
```

---

## 📈 Ordenação e Comparação

### Ordenação de Fórmulas
Fórmulas podem ser ordenadas lexicograficamente:

```python
formulas = ["CQ²T", "C²Q", "P", "CQTP", "C³"]

# Ordem natural (string)
sorted(formulas)
# Resultado: ['C²Q', 'C³', 'CQ²T', 'CQTP', 'P']

# Ordem por massa
sorted(formulas, key=lambda f: parse_mass(f))
# Resultado: ['P', 'C²Q', 'CQ²T', 'C³', 'CQTP']
```

### Comparação
```python
def formulas_equal(formula1, formula2):
    """
    Compara fórmulas (mesmo conteúdo)
    """
    return formula1 == formula2


def same_composition(mol1, mol2):
    """
    Verifica se duas moléculas têm a mesma composição
    (mas podem ter estruturas diferentes - isômeros)
    """
    return calculate_molecular_formula(mol1) == \
           calculate_molecular_formula(mol2)
```

---

## 🎨 Visualização

### Display no Frontend
```javascript
// Exemplo em Vue
<div class="molecule-formula">
  {{ formula }}
</div>

// CSS para melhor visualização
.molecule-formula {
  font-family: 'Courier New', monospace;
  font-size: 1.5rem;
  font-weight: bold;
  color: #3b82f6;
}
```

### Com Propriedades
```javascript
<div class="molecule-card">
  <div class="formula">{{ formula }}</div>
  <div class="properties">
    <span>Massa: {{ mass }}</span>
    <span>Carga: {{ charge }}</span>
  </div>
</div>

// Exemplo:
// CQ²T
// Massa: 4 | Carga: -2 (negativa)
```

---

## 🔍 Parsing e Validação

### Parse de Fórmula
```python
def parse_formula(formula_str):
    """
    Converte fórmula string para contagem
    
    Args:
        formula_str: String como "C²Q³T"
        
    Returns: Dict {'circle': 2, 'square': 3, 'triangle': 1}
    """
    
    symbol_to_type = {
        'C': 'circle',
        'Q': 'square',
        'T': 'triangle',
        'P': 'pentagon'
    }
    
    superscript_to_number = {
        '²': 2, '³': 3, '⁴': 4, '⁵': 5,
        '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9
    }
    
    counts = {}
    i = 0
    
    while i < len(formula_str):
        symbol = formula_str[i]
        
        if symbol not in symbol_to_type:
            i += 1
            continue
        
        # Contar (default 1)
        count = 1
        
        # Verificar se há superscript
        if i + 1 < len(formula_str):
            next_char = formula_str[i + 1]
            if next_char in superscript_to_number:
                count = superscript_to_number[next_char]
                i += 1  # Pular superscript
        
        particle_type = symbol_to_type[symbol]
        counts[particle_type] = counts.get(particle_type, 0) + count
        i += 1
    
    return counts
```

### Validação
```python
def is_valid_formula(formula_str):
    """
    Valida se fórmula está no formato correto
    """
    
    # Regex: C²?Q²?T²?P²? (ordem obrigatória)
    import re
    pattern = r'^C[²³⁴⁵⁶⁷⁸⁹]?Q[²³⁴⁵⁶⁷⁸⁹]?T[²³⁴⁵⁶⁷⁸⁹]?P[²³⁴⁵⁶⁷⁸⁹]?$'
    
    return bool(re.match(pattern, formula_str))
```

---

## 📊 Estatísticas

### Distribuição por Tipo
```python
def get_composition_stats(molecule_list):
    """
    Analisa composição de uma lista de moléculas
    """
    
    stats = {
        'circle': 0,
        'square': 0,
        'triangle': 0,
        'pentagon': 0
    }
    
    for molecule in molecule_list:
        for particle in molecule.particles:
            stats[particle.type] += 1
    
    return stats


# Exemplo
stats = get_composition_stats(all_molecules)
# {'circle': 45, 'square': 32, 'triangle': 28, 'pentagon': 15}
```

---

## 🎯 Casos de Uso

### 1. Identificação Rápida
```python
# Buscar molécula por fórmula
def find_by_formula(formula, molecule_list):
    return [
        mol for mol in molecule_list
        if calculate_molecular_formula(mol) == formula
    ]
```

### 2. Filtros na Biblioteca
```javascript
// Filtrar por fórmula
const filteredMolecules = molecules.filter(mol => 
  mol.formula.includes('P')  // Contém pentagon
)
```

### 3. Sugestões de Síntese
```python
# Sugerir pares que podem gerar fórmula alvo
def suggest_synthesis(target_formula):
    # Parsear fórmula alvo
    target_counts = parse_formula(target_formula)
    
    # Buscar combinações...
```

---

## 🔬 Comparação com Química Real

### Química Tradicional
- **H₂O**: 2 hidrogênios, 1 oxigênio
- **C₆H₁₂O₆**: 6 carbonos, 12 hidrogênios, 6 oxigênios
- Ordem alfabética: C, H, O

### Nossa Notação
- **C²Q**: 2 circles, 1 square
- **CQ²TP³**: 1 circle, 2 squares, 1 triangle, 3 pentagons
- Ordem por conexões: C, Q, T, P

---

## 💡 Vantagens do Sistema

1. ✅ **Intuitivo**: C < Q < T < P em complexidade
2. ✅ **Compacto**: Usa superscripts Unicode
3. ✅ **Ordenado**: Sempre na mesma sequência
4. ✅ **Único**: Uma fórmula = uma composição
5. ✅ **Extensível**: Fácil adicionar novos tipos

---

## 🚀 Melhorias Futuras

### 1. Notação Extendida com Carga
```
C²Q⁺² (2 circles, 1 square, carga +2)
P³⁻¹ (3 pentagons, carga -1)
```

### 2. Notação de Estrutura
```
C-Q=T (indica bonds entre tipos)
C(Q²)T (indica ramificação)
```

### 3. Notação de Isômeros
```
CQ²T-iso1
CQ²T-iso2
(Mesma fórmula, estruturas diferentes)
```

---

**Implementações:**
- Backend: `backend/data/molecules.py` (função `calculate_molecular_formula`)
- Frontend: `frontend/src/services/api.js` (função `calculateMolecularFormula`)


