# Proposta: Sistema de Identificação de Moléculas

## 📋 Visão Geral

Sistema de gameplay que permite identificar moléculas através de **propriedades observáveis** como sabor, aparência e efeitos. O jogador precisa descobrir e usar essas pistas para identificar moléculas desconhecidas, criando um loop de gameplay interessante de exploração e descoberta.

---

## 🎯 Objetivos do Sistema

1. **Adicionar profundidade ao gameplay** - Transformar a descoberta em um puzzle de identificação
2. **Criar progressão natural** - Testar moléculas revela informações gradualmente
3. **Integrar com mecânicas existentes** - Usar propriedades estruturais já calculadas
4. **Adicionar estratégia** - Escolher quais testes fazer para identificar moléculas

---

## 🔬 Propriedades Observáveis

### 1. **Sabor** 👅
Baseado na **topologia estrutural** da molécula:

| Topologia | Sabor | Descrição |
|-----------|-------|-----------|
| `single` | Insípido | Partícula única |
| `linear` | Salgado | Cadeia linear simples |
| `Y` | Amargo | Ramificação Y |
| `X` | Amargo-intenso | Ramificação X |
| `tree` | Amargo-complexo | Árvore ramificada |
| `cycle` | Azedo | Ciclo/Anel fechado |
| `mista` | Azedo-amargo | Ciclo + ramificações |
| `empty` | Sem sabor | Estrutura vazia |

**Mapeamento Direto:**
- Cada topologia tem um sabor único e fixo
- Determinístico: mesma topologia = mesmo sabor
- Usa `analyze_molecule_structure()` para obter topologia

### 2. **Aparência** 👁️
Baseado nas **multiplicidades das ligações** (bonds) presentes na molécula:

| Multiplicidades | Cor | Nome | Hex Color |
|----------------|-----|------|-----------|
| Apenas `1` | Azul claro | Azul claro | `#87CEEB` |
| Apenas `2` | Verde | Verde | `#32CD32` |
| `1` e `2` | Vermelho | Vermelho | `#FF4500` |
| `1` e `3` | Laranja | Laranja | `#FF8C00` |
| `2` e `3` | Magenta | Magenta | `#FF1493` |
| `1`, `2` e `3` | Amarelo | Amarelo | `#FFD700` |

**Nota:** Não é possível ter moléculas apenas com ligações triplas (multiplicidade 3) sozinhas, pois isso tornaria a estrutura instável. Ligações triplas sempre aparecem combinadas com outras multiplicidades.

**Lógica de Determinação:**
1. Extrai todas as multiplicidades únicas das bonds
2. Cria um conjunto (set) das multiplicidades
3. Busca no mapeamento a cor correspondente
4. Retorna nome, cor hex e descrição

**Exemplos:**
- Molécula com apenas ligações simples (multiplicity=1) → **Azul claro**
- Molécula com ligações duplas e triplas (2 e 3) → **Magenta**
- Molécula com todas as ligações (1, 2, 3) → **Amarelo**

**Nota:** Sistema simplificado e determinístico. Cada combinação de multiplicidades tem uma cor única e bem definida.

---

## 🧪 Sistema de Testes

### Tipos de Testes Disponíveis

#### 1. **Teste de Sabor** 👅
- **Custo**: $10
- **Ação**: Jogador seleciona uma molécula e escolhe "Testar Sabor"
- **Resultado**: Revela o sabor da molécula
- **Nota de Laboratório**: Adiciona registro: "Sabor: [sabor]"

#### 2. **Teste de Aparência** 👁️
- **Custo**: $5
- **Ação**: Jogador visualiza propriedades visuais
- **Resultado**: Revela cor/nome da aparência baseada nas multiplicidades
- **Nota de Laboratório**: Adiciona registro: "Aparência: [nome da cor]" + código hex

#### 3. **Análise Completa** 🔬
- **Custo**: $12 (desconto de $3 vs testes separados: $10 + $5 = $15)
- **Ação**: Realiza ambos os testes de uma vez
- **Resultado**: Revela sabor e aparência
- **Nota de Laboratório**: Registra todas as propriedades

---

## 📝 Sistema de Notas de Laboratório

Cada molécula testada ganha um **Caderno de Notas** que armazena:

```json
{
  "molecule_id": "m4_1",
  "notes": {
    "flavor": "Azedo",
    "appearance": {
      "name": "Azul claro",
      "color": "#87CEEB",
      "description": "Apenas ligações simples"
    },
    "tests_performed": ["flavor", "appearance"],
    "test_dates": {
      "flavor": "2025-01-XX",
      "appearance": "2025-01-XX"
    }
  }
}
```

### Interface de Notas
- Jogador pode ver notas para qualquer molécula testada
- Notas são compartilhadas entre moléculas idênticas (mesma estrutura)
- Interface mostra quais propriedades foram descobertas e quais faltam

---

## 🎮 Mecânica de Identificação

### Modo: Identificar Molécula Desconhecida

**Cenário:**
1. Jogador encontra molécula desconhecida (síntese, simulação, etc.)
2. Sistema apresenta pistas baseadas em propriedades calculadas
3. Jogador deve testar e comparar com moléculas conhecidas

**Fluxo:**
```
1. Molécula desconhecida aparece
   ↓
2. Sistema mostra pistas básicas:
   - Massa: 4
   - Carga: Neutra
   - Fórmula: C²QT (mas não revela qual isômero)
   ↓
3. Jogador escolhe ação:
   a) Testar propriedades (gastar dinheiro)
   b) Tentar identificar comparando com notas conhecidas
   c) Sintetizar outras moléculas para comparar
   ↓
4. Após testes, sistema permite:
   - Comparar com moléculas conhecidas
   - Filtrar por propriedades similares
   - Sugerir possíveis candidatos
   ↓
5. Jogador tenta identificar:
   - Seleciona molécula candidata
   - Sistema compara todas as propriedades
   - Se match perfeito → Identificação bem-sucedida!
   - Se parcial → Mostra diferenças
```

### Sistema de Pontuação de Identificação

**Match Perfeito:**
- Todas as propriedades conhecidas batem
- Identificação bem-sucedida
- Recompensa: $50 + experiência

**Match Parcial:**
- Algumas propriedades batem, outras não
- Sistema mostra: "Similar, mas sabor difere"
- Permite tentar novamente

**Match Nenhum:**
- Propriedades não batem
- Sistema mostra diferenças
- Não gasta tentativa (permite testar mais)

---

## 🔍 Algoritmo de Geração de Propriedades

### Código para Sabor

```python
from core.molecule_analyzer import analyze_molecule_structure

TOPOLOGY_FLAVOR_MAP = {
    'single': 'Insípido',
    'linear': 'Salgado',
    'Y': 'Amargo',
    'X': 'Amargo-intenso',
    'tree': 'Amargo-complexo',
    'cycle': 'Azedo',
    'mista': 'Azedo-amargo',
    'empty': 'Sem sabor'
}

def calculate_flavor(molecule):
    """Calcula sabor baseado na topologia."""
    structure = analyze_molecule_structure(molecule)
    topology = structure.get('topology', 'empty')
    return TOPOLOGY_FLAVOR_MAP.get(topology, 'Desconhecido')
```

### Código para Aparência

```python
MULTIPLICITY_COLOR_MAP = {
    frozenset([1]): {
        'name': 'Azul claro',
        'color': '#87CEEB',
        'description': 'Apenas ligações simples'
    },
    frozenset([2]): {
        'name': 'Verde',
        'color': '#32CD32',
        'description': 'Apenas ligações duplas'
    },
    frozenset([3]): {
        'name': 'Roxo',
        'color': '#9370DB',
        'description': 'Apenas ligações triplas'
    },
    frozenset([1, 2]): {
        'name': 'Vermelho',
        'color': '#FF4500',
        'description': 'Ligações simples e duplas'
    },
    frozenset([1, 3]): {
        'name': 'Laranja',
        'color': '#FF8C00',
        'description': 'Ligações simples e triplas'
    },
    frozenset([2, 3]): {
        'name': 'Magenta',
        'color': '#FF1493',
        'description': 'Ligações duplas e triplas'
    },
    frozenset([1, 2, 3]): {
        'name': 'Amarelo',
        'color': '#FFD700',
        'description': 'Todas as ligações'
    }
}

def calculate_appearance(molecule):
    """Calcula aparência baseado nas multiplicidades das bonds."""
    bonds = molecule.get('bonds', [])
    
    if not bonds:
        return {
            'name': 'Incolor',
            'color': '#FFFFFF',
            'description': 'Sem ligações'
        }
    
    # Extrair multiplicidades únicas
    multiplicities = set(bond.get('multiplicity', 1) for bond in bonds)
    
    # Buscar no mapa
    appearance = MULTIPLICITY_COLOR_MAP.get(frozenset(multiplicities))
    
    return appearance or {
        'name': 'Desconhecido',
        'color': '#808080',
        'description': 'Combinação não catalogada'
    }
```

---

## 🗄️ Estrutura de Dados

### Armazenamento de Notas

```python
# backend/data/molecule_notes.py

MOLECULE_NOTES = {
    "save_id": {
        "molecule_id_or_structure_hash": {
            "flavor": "Azedo",
            "appearance": {
                "name": "Azul claro",
                "color": "#87CEEB",
                "description": "Apenas ligações simples"
            },
            "tests_performed": ["flavor", "appearance"],
            "test_dates": {
                "flavor": "2025-01-XX",
                "appearance": "2025-01-XX"
            },
            "cost_spent": 15,
            "identified": False  # Se já foi identificada corretamente
        }
    }
}
```

### API Endpoints Propostos

```
POST /api/molecules/test/flavor
  Body: { molecule: {...}, save_id: "..." }
  Response: { flavor: "azedo-picante", cost: 10, money_remaining: 90 }

POST /api/molecules/test/appearance
  Body: { molecule: {...}, save_id: "..." }
  Response: { appearance: "Opaco, cristalino", cost: 5, money_remaining: 85 }

POST /api/molecules/test/full
  Body: { molecule: {...}, save_id: "..." }
  Response: { flavor, appearance: {name, color, description}, cost: 12, money_remaining: 88 }

GET /api/molecules/notes/:molecule_id
  Response: { notes: {...} }

POST /api/molecules/identify
  Body: { unknown_molecule: {...}, candidate_id: "m4_1", save_id: "..." }
  Response: { 
    match_percentage: 100,
    matched_properties: ["flavor", "appearance", "effects"],
    success: true,
    reward: 50
  }

GET /api/molecules/search/by-properties
  Query: ?flavor=azedo&appearance=azul_claro
  Response: { matches: [...] }
```

---

## 🎨 Interface Proposta

### Tela de Teste de Molécula

```
┌─────────────────────────────────────────┐
│  🧪 Teste de Molécula                   │
├─────────────────────────────────────────┤
│                                         │
│  [Visualização da Molécula]            │
│                                         │
│  Propriedades Conhecidas:              │
│  ✓ Massa: 4                            │
│  ✓ Carga: Neutra                       │
│  ✓ Fórmula: C²QT                       │
│                                         │
│  Testes Disponíveis:                   │
│  ┌───────────────────────────────────┐ │
│  │ 👅 Teste de Sabor     $10         │ │
│  │ [X] Já testado: "Azedo-picante"   │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ 👁️ Teste de Aparência  $5         │ │
│  │ [ ] Não testado                   │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ ⚡ Teste de Efeitos    $15         │ │
│  │ [ ] Não testado                   │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ 🔬 Análise Completa   $25         │ │
│  │ (Economia de $5)                  │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [💰 Dinheiro: $100]                   │
│                                         │
│  [Cancelar]  [Executar Teste Selecionado] │
└─────────────────────────────────────────┘
```

### Tela de Identificação

```
┌─────────────────────────────────────────┐
│  🔍 Identificar Molécula Desconhecida   │
├─────────────────────────────────────────┤
│                                         │
│  Molécula Alvo:                        │
│  [Visualização]                        │
│                                         │
│  Propriedades Conhecidas:              │
│  • Sabor: Azedo-picante                │
│  • Aparência: Opaco, cristalino        │
│  • Efeitos: Efervescente, Reativo      │
│  • Massa: 4                            │
│  • Carga: Neutra                       │
│  • Fórmula: C²QT                       │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 🔍 Buscar Candidatos              │ │
│  │ [Buscar por propriedades]         │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Candidatos Encontrados (3):           │
│  ┌───────────────────────────────────┐ │
│  │ [Molécula] m4_1                   │ │
│  │ ✓ Sabor ✓ Aparência ✓ Efeitos    │ │
│  │ Match: 100%                       │ │
│  │ [Tentar Identificar]              │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ [Molécula] m4_5                   │ │
│  │ ✓ Sabor ✗ Aparência ✓ Efeitos    │ │
│  │ Match: 67%                        │ │
│  │ [Tentar Identificar]              │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Cancelar]                             │
└─────────────────────────────────────────┘
```

---

## 🚀 Implementação Sugerida (Fases)

### Fase 1: Sistema Base
1. ✅ Criar módulo `backend/core/molecule_properties.py` com funções de cálculo
2. ✅ Implementar cálculo de sabor, aparência e efeitos
3. ✅ Criar endpoints de teste básicos
4. ✅ Sistema de persistência de notas

### Fase 2: Interface
1. ✅ Tela de teste de moléculas
2. ✅ Visualização de notas
3. ✅ Integração com biblioteca de moléculas

### Fase 3: Identificação
1. ✅ Sistema de busca por propriedades
2. ✅ Interface de identificação
3. ✅ Sistema de pontuação e recompensas

### Fase 4: Refinamento
1. ✅ Balanceamento de custos
2. ✅ Adicionar mais variações de propriedades
3. ✅ Sistema de dicas e tutoriais

---

## 💡 Vantagens desta Abordagem

1. **Reutiliza código existente** - Usa `analyze_molecule_structure` e `calculate_molecule_properties`
2. **Integração natural** - Se encaixa no fluxo de gameplay atual
3. **Progressão clara** - Testes custam dinheiro, criando decisões estratégicas
4. **Exploração encorajada** - Incentiva testar múltiplas moléculas
5. **Identificação como puzzle** - Transforma descoberta em desafio mental

---

## ❓ Questões para Discussão

1. **Custos dos testes** - Os valores ($5, $10, $15, $25) estão adequados?
2. **Complexidade das propriedades** - Devemos adicionar mais variações?
3. **Sistema de recompensas** - $50 por identificação é suficiente?
4. **Moléculas base conhecidas** - Devem vir com propriedades já reveladas?
5. **Sistema de dicas** - Devemos ter um sistema que sugere testes baseado em probabilidade?

---

## 📝 Notas de Design

- **Determinístico**: Mesma estrutura = mesmas propriedades sempre
- **Observável**: Propriedades derivam de características estruturais já calculadas
- **Progressive Disclosure**: Jogador descobre informações gradualmente
- **Econômico**: Custo de testes cria trade-offs interessantes
- **Exploratório**: Incentiva experimentação

---

**📖 Proposta criada em: 2025-01-XX**

**🔬 Chemical Pharma - Molecular Synthesis Game**

