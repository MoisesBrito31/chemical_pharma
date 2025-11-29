# 📚 Modelagem Técnica - Chemical Pharma

Documentação técnica detalhada dos algoritmos e arquitetura do sistema.

---

## 📑 Índice de Documentos

### [01 - Algoritmo de Síntese](./01_ALGORITMO_SINTESE.md)
Documentação completa do processo de síntese molecular:
- **Etapa 1**: Anulação (Annihilation)
- **Etapa 2**: Merge (Soma em Novo)
- **Etapa 3**: Rebond (Estabilização)
- **Etapa 4**: Reorganização de Posições
- Detecção de componentes desconectados
- Casos especiais e validações
- Complexidade computacional

**Conceitos-chave:**
- Comutatividade (A+B = B+A)
- Priorização inteligente no rebond
- BFS para componentes conectados

---

### [02 - Comparação Estrutural](./02_COMPARACAO_ESTRUTURAL.md)
Sistema de comparação e identificação de moléculas:
- Comparação estrutural vs fórmula molecular
- Detecção de isômeros
- Algoritmo `areMoleculesIdentical()`
- Fingerprint molecular
- Busca em lista de moléculas

**Conceitos-chave:**
- Isomorfismo de grafos
- Normalização de bonds
- Multiset de partículas

---

### [03 - Fórmula Molecular (CQTP)](./03_FORMULA_MOLECULAR.md)
Notação customizada para representação molecular:
- Sistema de símbolos (C, Q, T, P)
- Ordenação por número de conexões
- Geração de fórmula
- Parsing e validação
- Propriedades derivadas (massa, carga)

**Conceitos-chave:**
- Unicode superscripts (², ³, ⁴)
- Ordenação por complexidade
- Independência de polaridade

---

### [04 - Arquitetura do Sistema](./04_ARQUITETURA_SISTEMA.md)
Visão geral da arquitetura e tecnologias:
- Arquitetura cliente-servidor
- Frontend (Vue 3 + PixiJS)
- Backend (Flask + Python)
- REST API endpoints
- Sistema de persistência (JSON)
- Fluxo de dados
- Estratégia de visualização

**Conceitos-chave:**
- Separação frontend/backend
- Isolamento por save/jogador
- Render-to-image para WebGL
- Cache de síntese

---

## 🎯 Público-Alvo

Esta documentação é destinada a:
- **Desenvolvedores** que trabalham no projeto
- **Colaboradores** que querem entender a lógica
- **Auditores** técnicos
- **Futuros mantenedores** do código

---

## 🔬 Principais Algoritmos

### 1. Síntese Molecular
```
Complexidade: O(p² × i)
Onde: p = partículas, i = iterações (~100)

Garante: Comutatividade, Estabilidade, Detecção de falhas
```

### 2. Comparação Estrutural
```
Complexidade: O(p log p + b)
Onde: p = partículas, b = bonds

Garante: Identificação correta de isômeros
```

### 3. Detecção de Componentes (BFS)
```
Complexidade: O(p + b)
Onde: p = partículas, b = bonds

Garante: Separação de moléculas desconectadas
```

---

## 📊 Fluxo de Dados Simplificado

```
User Input
    ↓
Frontend (Vue)
    ↓
REST API (HTTP/JSON)
    ↓
Backend (Flask)
    ↓
Core Logic (Python)
    ↓
Data Layer (JSON Files)
    ↓
Response
    ↓
UI Update
```

---

## 🧪 Regras do Sistema

### Partículas
| Tipo      | Símbolo | Conexões | Polaridade |
|-----------|---------|----------|------------|
| Circle    | ○       | 1        | + ou -     |
| Square    | □       | 2        | + ou -     |
| Triangle  | △       | 3        | + ou -     |
| Pentagon  | ⬠       | 4        | + ou -     |

### Regras de Ligação
1. ✅ Partículas de **tipos diferentes** podem se ligar
2. ❌ Partículas do **mesmo tipo** NÃO podem se ligar
3. ✅ Múltiplas ligações permitidas (multiplicidade)
4. ✅ Ramificações permitidas
5. ❌ Ligação deve respeitar limites de conexão

### Regras de Síntese
1. ✅ Anulação: Mesmo tipo + polaridades opostas
2. ✅ Merge ordenado: Garante comutatividade
3. ✅ Rebond: Estabilizar por prioridade
4. ❌ Sem anulação = sem reação
5. ❌ Todas anuladas = falha
6. ❌ Não estabiliza = falha

---

## 💡 Conceitos-Chave

### Comutatividade
```
A + B = B + A

Garantida por: Ordenação determinística no merge
```

### Isômeros
```
Mesma fórmula ≠ Mesma estrutura

C²Q pode ser: ○-□-○  ou  ○=□
```

### Componentes Conectados
```
Resultado pode ser:
- 1 molécula única
- N moléculas separadas (desconectadas)
```

---

## 📈 Métricas de Qualidade

### Código
- ✅ Algoritmos documentados
- ✅ Complexidade analisada
- ✅ Casos de teste descritos
- ✅ Validações implementadas

### Sistema
- ✅ Separação de responsabilidades
- ✅ API RESTful bem definida
- ✅ Persistência isolada por jogador
- ✅ Frontend reativo

---

## 🔮 Próximas Evoluções

### Algoritmos
- [ ] Otimização do rebond (heurísticas)
- [ ] Cache inteligente de fingerprints
- [ ] Detecção de simetria molecular
- [ ] Canonical labeling para isomorfismo

### Arquitetura
- [ ] Migração para banco de dados relacional
- [ ] Sistema de autenticação real
- [ ] Cache distribuído (Redis)
- [ ] API GraphQL
- [ ] Testes automatizados

---

## 📚 Como Usar Esta Documentação

### Para Entender o Sistema
1. Comece por **04_ARQUITETURA_SISTEMA.md** (visão geral)
2. Depois **01_ALGORITMO_SINTESE.md** (core do sistema)
3. Complementar com outros documentos conforme necessário

### Para Modificar Algoritmos
1. Leia o documento específico do algoritmo
2. Entenda a complexidade e garantias
3. Verifique os casos de teste
4. Modifique com cuidado para manter garantias

### Para Adicionar Features
1. Consulte **04_ARQUITETURA_SISTEMA.md**
2. Identifique camadas afetadas
3. Atualize documentação correspondente
4. Adicione testes

---

## 🤝 Contribuindo

Ao modificar o sistema:

1. ✅ Atualize a documentação correspondente
2. ✅ Mantenha exemplos atualizados
3. ✅ Documente novos algoritmos
4. ✅ Explique decisões de design
5. ✅ Adicione casos de teste

---

## 📞 Referências Rápidas

- **Código Backend**: `backend/core/synthesis.py`
- **Código Frontend**: `frontend/src/views/Synthesis.vue`
- **API**: `backend/app.py`
- **Comparação**: `frontend/src/utils/moleculeComparison.js`
- **Dados**: `backend/data/molecules.py`

---

## 🏆 Status

| Documento | Status | Última Atualização |
|-----------|--------|-------------------|
| 01_ALGORITMO_SINTESE | ✅ Completo | 2025-11-28 |
| 02_COMPARACAO_ESTRUTURAL | ✅ Completo | 2025-11-28 |
| 03_FORMULA_MOLECULAR | ✅ Completo | 2025-11-28 |
| 04_ARQUITETURA_SISTEMA | ✅ Completo | 2025-11-28 |

---

**📖 Documentação criada e mantida pela equipe de desenvolvimento**

**🔬 Chemical Pharma - Molecular Synthesis Game**


