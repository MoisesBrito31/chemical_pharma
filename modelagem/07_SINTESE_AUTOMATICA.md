# Síntese Automática - Interface e Funcionalidades

## 📋 Visão Geral

A tela de **Síntese Automática** permite testar múltiplas sínteses de uma vez usando uma molécula base (Molécula A) combinada com um grupo de moléculas (Moléculas B). Esta funcionalidade acelera significativamente a descoberta de novas moléculas ao permitir testes em lote.

---

## 🎯 Funcionalidade Principal

### Objetivo
Realizar múltiplas sínteses simultaneamente combinando:
- **1 molécula base** (Molécula A)
- **N moléculas** de um grupo (Moléculas B)

### Casos de Uso
- Descobrir todas as possibilidades de síntese com uma molécula específica
- Testar rapidamente múltiplas combinações
- Identificar novas descobertas de forma eficiente
- Explorar o espaço de soluções molecular

---

## 🖥️ Interface do Usuário

### Layout Organizado

A interface foi otimizada para melhor usabilidade com layout em duas colunas:

```
┌─────────────────────────────────────────────────────┐
│  🔬 Molécula Base    │  📦 Grupo de Moléculas      │
│                      │                              │
│  [Seletor]           │  [Modo de Seleção]          │
│                      │  • Por Massa                │
│                      │  • Específicas              │
│                      │                              │
│                      │  [Filtros/Seleção]          │
└─────────────────────────────────────────────────────┘
```

#### **Coluna Esquerda: Molécula Base**
- Seletor de molécula principal (Molécula A)
- Todas as moléculas conhecidas e descobertas disponíveis

#### **Coluna Direita: Grupo de Moléculas**
- **Modo 1: Filtrar por Massa**
  - Seleciona todas as moléculas com uma massa específica
  - Exibe contador: "Encontradas: X molécula(s)"
  
- **Modo 2: Seleção Específica**
  - Seleciona moléculas individualmente via checkboxes
  - Exibe contador: "Selecionadas: X molécula(s)"
  - Lista todas as moléculas conhecidas

### Responsividade
- **Desktop (>1024px)**: Layout em 2 colunas lado a lado
- **Mobile/Tablet (≤1024px)**: Layout em coluna única empilhado

---

## 📊 Estatísticas de Resultados

Após a execução, a interface exibe estatísticas detalhadas:

### Badges de Estatística

1. **Total** (azul)
   - Número total de sínteses testadas
   - Fonte: `results.total_tested`

2. **Sucesso** (verde)
   - Número de sínteses bem-sucedidas
   - Fonte: `results.total_successful`

3. **Falhas** (vermelho)
   - Número de sínteses que falharam
   - Calculado: `total_tested - total_successful`

4. **Desconhecidas** (laranja) ⭐ NOVO
   - Número de moléculas **novas** descobertas
   - Moléculas com status `'Desconhecida'`
   - Indica descobertas inéditas

5. **Conhecidas** (verde) ⭐ NOVO
   - Número de moléculas já conhecidas
   - Moléculas com status `'Base'` ou `'Descoberta'`
   - Indica moléculas já catalogadas

### Cálculo dos Contadores

```javascript
// Moléculas Desconhecidas
const countUnknownMolecules = computed(() => {
  if (!results.value || !results.value.results) return 0
  
  return results.value.results.filter(r => {
    return r.result.success && r.status === 'Desconhecida'
  }).length
})

// Moléculas Conhecidas
const countKnownMolecules = computed(() => {
  if (!results.value || !results.value.results) return 0
  
  return results.value.results.filter(r => {
    return r.result.success && 
           (r.status === 'Base' || r.status === 'Descoberta')
  }).length
})
```

---

## 🔄 Fluxo de Execução

### 1. Configuração
```
1. Usuário seleciona Molécula A (base)
2. Usuário escolhe modo de seleção (Massa ou Específico)
3. Usuário configura filtro/seleção do grupo
4. Sistema valida se pode executar (canExecute)
```

### 2. Execução
```
1. Clique em "🚀 Executar Sínteses Automáticas"
2. Sistema exibe barra de progresso
3. Backend processa todas as sínteses sequencialmente
4. Cada síntese é testada: A + B₁, A + B₂, ..., A + Bₙ
```

### 3. Resultados
```
1. Exibe painel de resultados
2. Mostra estatísticas resumidas (badges)
3. Lista detalhada de cada síntese:
   - Status (Sucesso/Falha)
   - Tipo da molécula (Base/Descoberta/Desconhecida)
   - Fórmula molecular
   - Visualização da molécula
   - Opção de salvar descobertas
```

---

## 📡 API Backend

### Endpoint
```
POST /api/synthesis/auto
```

### Payload
```json
{
  "mol_a_id": "m3_1",
  "mol_b_ids": ["m3_2", "m3_3", "m4_1"],
  "save_id": "save_abc123"
}
```

### Resposta
```json
{
  "success": true,
  "total_tested": 3,
  "total_successful": 2,
  "results": [
    {
      "mol_a_id": "m3_1",
      "mol_b_id": "m3_2",
      "result": {
        "success": true,
        "molecules": [...]
      },
      "status": "Desconhecida"
    },
    {
      "mol_a_id": "m3_1",
      "mol_b_id": "m3_3",
      "result": {
        "success": false,
        "error": "Nenhuma anulação possível"
      },
      "status": null
    },
    ...
  ]
}
```

### Campos do Resultado Individual

- **`result.success`**: Boolean indicando sucesso da síntese
- **`result.molecules`**: Array de moléculas resultantes (se sucesso)
- **`result.error`**: Mensagem de erro (se falhou)
- **`status`**: Status da molécula resultante
  - `'Base'`: Molécula predefinida no sistema
  - `'Descoberta'`: Molécula já descoberta pelo jogador
  - `'Desconhecida'`: Nova molécula nunca vista
  - `null`: Síntese falhou

---

## 🎨 Componentes Vue

### Estrutura do Componente

```vue
<template>
  <div class="auto-synthesis">
    <!-- Header -->
    <header>...</header>
    
    <!-- Configuração (2 colunas) -->
    <div class="config-panel">
      <div class="config-row">
        <!-- Molécula Base -->
        <div class="config-section">...</div>
        
        <!-- Grupo de Moléculas -->
        <div class="config-section">...</div>
      </div>
    </div>
    
    <!-- Botão Executar -->
    <div class="action-panel">...</div>
    
    <!-- Resultados -->
    <div class="results-panel">
      <!-- Estatísticas -->
      <div class="results-stats">
        <span class="stat-badge total">...</span>
        <span class="stat-badge success">...</span>
        <span class="stat-badge failed">...</span>
        <span class="stat-badge unknown">...</span>  ⭐ NOVO
        <span class="stat-badge known">...</span>    ⭐ NOVO
      </div>
      
      <!-- Lista de Resultados -->
      <div class="results-list">...</div>
    </div>
  </div>
</template>
```

### Computed Properties

```javascript
// Validação se pode executar
const canExecute = computed(() => {
  if (!moleculeA.value) return false
  
  if (groupMode.value === 'mass') {
    return filterMass.value !== null
  } else {
    return selectedMoleculeIds.value.length > 0
  }
})

// Contadores de estatísticas
const countUnknownMolecules = computed(() => {...})
const countKnownMolecules = computed(() => {...})
```

---

## 🎨 Estilos CSS

### Layout Responsivo

```css
.config-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: start;
}

@media (max-width: 1024px) {
  .config-row {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
```

### Badges de Estatística

```css
.stat-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.stat-badge.total {
  background-color: #3b82f6;  /* Azul */
  color: white;
}

.stat-badge.success {
  background-color: #10b981;  /* Verde */
  color: white;
}

.stat-badge.failed {
  background-color: #ef4444;  /* Vermelho */
  color: white;
}

.stat-badge.unknown {
  background-color: #f59e0b;  /* Laranja */ ⭐ NOVO
  color: white;
}

.stat-badge.known {
  background-color: #10b981;  /* Verde */ ⭐ NOVO
  color: white;
}
```

---

## 🔍 Validações

### Validação de Execução

```javascript
const canExecute = computed(() => {
  // Deve ter molécula base selecionada
  if (!moleculeA.value) return false
  
  // Modo massa: deve ter massa selecionada
  if (groupMode.value === 'mass') {
    return filterMass.value !== null
  }
  
  // Modo específico: deve ter pelo menos uma molécula selecionada
  if (groupMode.value === 'specific') {
    return selectedMoleculeIds.value.length > 0
  }
  
  return false
})
```

### Validação no Backend

O backend valida:
- Existência das moléculas A e B
- Permissões do save/jogador
- Estrutura válida dos dados

---

## 📈 Performance

### Otimizações Implementadas

1. **Progresso em Tempo Real**
   - Barra de progresso mostra execução
   - Feedback visual durante processamento

2. **Cache de Sínteses**
   - Sínteses já testadas são recuperadas do cache
   - Reduz tempo de execução para combinações repetidas

3. **Processamento Sequencial**
   - Sínteses são processadas uma por vez
   - Evita sobrecarga no backend

### Limitações

- Processamento sequencial (não paralelo)
- Depende do desempenho de cada síntese individual
- Cache ajuda mas não elimina tempo de processamento

---

## 🚀 Melhorias Futuras

### Interface
- [ ] Filtros avançados por propriedades (carga, polaridade)
- [ ] Ordenação de resultados por diferentes critérios
- [ ] Exportação de resultados para CSV/JSON
- [ ] Histórico de execuções anteriores

### Performance
- [ ] Processamento paralelo no backend
- [ ] Cancelamento de execução em andamento
- [ ] Paginação de resultados para muitos itens

### Funcionalidades
- [ ] Agendamento de sínteses automáticas
- [ ] Notificações quando novas descobertas são encontradas
- [ ] Análise de padrões entre resultados
- [ ] Sugestões inteligentes de combinações

---

## 📝 Notas de Implementação

### Histórico de Mudanças

#### Versão Atual (2025-01-XX)
- ✅ Layout em 2 colunas (molécula base + grupo lado a lado)
- ✅ Contadores de moléculas desconhecidas e conhecidas
- ✅ Badges coloridos para diferentes estatísticas
- ✅ Design responsivo para mobile

#### Versão Anterior
- Layout vertical (uma seção sobre a outra)
- Apenas estatísticas básicas (Total, Sucesso, Falhas)

---

## 🔗 Referências

- **Código Frontend**: `frontend/src/views/AutoSynthesis.vue`
- **API Backend**: `backend/app.py` (endpoint `/api/synthesis/auto`)
- **Componente Seletor**: `frontend/src/components/MoleculeSelector.vue`
- **Visualizador**: `frontend/src/components/MoleculeViewer.vue`

---

## 🎯 Resumo

A **Síntese Automática** é uma funcionalidade poderosa que permite:

1. ✅ **Testar múltiplas sínteses rapidamente**
2. ✅ **Identificar novas descobertas** (contador de desconhecidas)
3. ✅ **Visualizar estatísticas detalhadas** (Total, Sucesso, Falhas, Desconhecidas, Conhecidas)
4. ✅ **Interface otimizada** com layout em 2 colunas
5. ✅ **Design responsivo** para diferentes tamanhos de tela

---

**📖 Documentação atualizada em: 2025-01-XX**

**🔬 Chemical Pharma - Molecular Synthesis Game**

