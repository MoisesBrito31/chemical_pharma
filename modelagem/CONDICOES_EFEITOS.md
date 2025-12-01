# Sistema de Padrões de Ligação para Efeitos Moleculares

## Visão Geral

Cada efeito (terapêutico ou colateral) possui um **conjunto único de padrões de ligação** que precisam estar presentes na molécula. Se a molécula contém **TODOS os padrões**, ela recebe o efeito.

Os padrões são **gerados aleatoriamente** para cada partida, tornando cada jogo único. Um padrão é uma ligação específica entre dois tipos de partículas com uma multiplicidade específica.

**Exemplo:**
- Efeito "Analgésico" requer:
  - Ligação: circle ↔ triangle (multiplicidade 1)
  - Ligação: square ↔ pentagon (multiplicidade 2)
- Se a molécula tiver AMBAS as ligações, ela tem o efeito Analgésico

---

## Atributos Utilizados nas Condições

### 1. **Carga (charge)**
- Soma das polaridades das partículas
- Valores: ... -2, -1, 0, +1, +2, ...
- Condição: `min <= charge <= max`

### 2. **Massa (mass)**
- Número de partículas na molécula
- Valores: 2, 3, 4, 5, 6, ...
- Condição: `min <= mass <= max`

### 3. **Topologia (topology)**
- Forma estrutural da molécula
- Valores: `'single'`, `'linear'`, `'Y'`, `'X'`, `'tree'`, `'cycle'`, `'mista'`, `'empty'`
- Condição: `topology in [lista_de_topologias_válidas]`

### 4. **Ramificações (branch_count)**
- Número de partículas com 3+ conexões
- Valores: 0, 1, 2, 3, ...
- Condição: `min <= branch_count <= max`

### 5. **Ciclo (has_cycle)**
- Se a molécula possui estrutura circular
- Valores: `True`, `False`
- Condição: `has_cycle == valor_esperado` (ou `None` = qualquer)

### 6. **Grau Máximo (max_degree)**
- Máximo número de conexões de uma partícula
- Valores: 1, 2, 3, 4, ...
- Condição: `min <= max_degree <= max`

---

## Formato das Condições

Cada efeito possui um dicionário de condições:

```python
{
    'charge': {
        'min': -2,
        'max': 2
    },
    'mass': {
        'min': 3,
        'max': 6
    },
    'topology': ['linear', 'Y', 'cycle'],
    'branch_count': {
        'min': 0,
        'max': 3
    },
    'has_cycle': True,  # ou False ou None (qualquer)
    'max_degree': {
        'min': 2,
        'max': 4
    }
}
```

---

## Exemplos de Condições

### Efeito: Analgésico
```python
{
    'charge': {'min': -1, 'max': 1},
    'mass': {'min': 3, 'max': 5},
    'topology': ['linear', 'Y'],
    'branch_count': {'min': 0, 'max': 2},
    'has_cycle': False,
    'max_degree': {'min': 2, 'max': 3}
}
```
**Interpretação:** Molécula com carga entre -1 e +1, massa 3-5, topologia linear ou Y, sem ciclos, grau máximo 2-3.

### Efeito: Cardioprotetor
```python
{
    'charge': {'min': -2, 'max': 0},
    'mass': {'min': 4, 'max': 7},
    'topology': ['cycle', 'mista'],
    'branch_count': {'min': 0, 'max': 4},
    'has_cycle': True,
    'max_degree': {'min': 2, 'max': 4}
}
```
**Interpretação:** Molécula com carga negativa ou neutra, massa 4-7, topologia circular, com ciclo.

### Efeito: Hepatotóxico
```python
{
    'charge': {'min': 1, 'max': 3},
    'mass': {'min': 5, 'max': 8},
    'topology': ['tree', 'X'],
    'branch_count': {'min': 2, 'max': 5},
    'has_cycle': None,  # Qualquer
    'max_degree': {'min': 3, 'max': 5}
}
```
**Interpretação:** Molécula com carga positiva alta, massa alta, alta ramificação, grau máximo alto.

---

## Sistema de Randomização

### Geração de Condições

1. **Seed Base:** Hash do `save_id`
2. **Seed por Efeito:** Hash de `save_id + nome_do_efeito`
3. **Randomização:** Usa a seed para gerar condições consistentes

### Propriedades da Randomização

- ✅ **Determinística:** Mesmo save_id = mesmas condições (sempre)
- ✅ **Única:** Diferentes saves = diferentes condições
- ✅ **Consistente:** Condições não mudam durante a partida
- ✅ **Balanceada:** Range de valores garante diversidade

---

## Lógica de Verificação

Uma molécula terá um efeito se e **apenas se** todas as condições forem satisfeitas:

```python
def molecule_has_effect(molecule, effect_name, profile):
    attributes = extract_molecule_attributes(molecule)
    conditions = profile['effect_conditions'][effect_name]
    
    return check_effect_conditions(attributes, conditions)
```

**Todas as condições devem ser verdadeiras:**
- ✅ Carga dentro do range
- ✅ Massa dentro do range
- ✅ Topologia na lista válida
- ✅ Ramificações dentro do range
- ✅ Ciclo corresponde (se especificado)
- ✅ Grau máximo dentro do range

---

## Efeitos Múltiplos

Uma molécula pode ter **múltiplos efeitos** simultaneamente:
- Efeitos terapêuticos múltiplos (ex: Analgésico + Anti-inflamatório)
- Efeitos colaterais múltiplos (ex: Hepatotóxico + Nefrotóxico)
- Combinação terapêutico + colateral (ex: Analgésico + Sedativo-excessivo)

**Isso cria trade-offs interessantes no gameplay!**

---

## Estratégia de Descoberta

Como as condições são aleatórias por partida, o jogador precisa:

1. **Testar múltiplas moléculas** para identificar padrões
2. **Observar propriedades comuns** entre moléculas com mesmo efeito
3. **Deduzir condições** através de experimentação
4. **Balancear benefícios vs riscos** ao criar moléculas

---

## Exemplos de Combinações

### Molécula com Efeitos Terapêuticos
```
Molécula: C³QT (massa 5, linear, carga -1)
Efeitos:
  ✅ Analgésico (satisfaz condições)
  ✅ Anti-inflamatório (satisfaz condições)
  ❌ Antibiótico (não satisfaz condições)
```

### Molécula com Efeitos Colaterais
```
Molécula: Q²T²P (massa 6, tree, carga +2)
Efeitos:
  ✅ Hepatotóxico (satisfaz condições)
  ✅ Cardiotóxico (satisfaz condições)
  ❌ Nefrotóxico (não satisfaz condições)
```

### Molécula Mista
```
Molécula: CQT²P (massa 5, cycle, carga 0)
Efeitos Terapêuticos:
  ✅ Cardioprotetor (satisfaz condições)
Efeitos Colaterais:
  ⚠️ Sedativo-excessivo (satisfaz condições)

Trade-off: Benefício cardiovascular vs risco de sedação
```

---

## Notas de Implementação

### Armazenamento
- Perfis são salvos em `data/property_profiles.json`
- Cada save tem seu próprio perfil único
- Perfis são gerados na criação do save

### Performance
- Verificação de condições é O(1) por atributo
- Cálculo total: O(k) onde k = número de efeitos (20)
- Pode ser otimizado com cache de resultados

### Extensibilidade
- Fácil adicionar novos atributos
- Fácil adicionar novos efeitos
- Condições podem ser ajustadas para balanceamento

---

**📖 Documentação criada em: 2025-01-XX**

**🔬 Chemical Pharma - Molecular Synthesis Game**

