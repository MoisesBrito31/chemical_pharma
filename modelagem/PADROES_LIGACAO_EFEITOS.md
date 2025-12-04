# Sistema de Padrões de Ligação para Efeitos Moleculares

## Visão Geral

Cada efeito (terapêutico ou colateral) possui um **conjunto único de padrões de ligação** que precisam estar presentes na molécula. Se a molécula contém **TODOS os padrões**, ela recebe o efeito.

Os padrões são **gerados aleatoriamente** para cada partida, tornando cada jogo único e forçando o jogador a descobrir empiricamente quais ligações produzem quais efeitos.

---

## O que é um Padrão de Ligação?

Um padrão de ligação é uma **ligação específica** entre dois tipos de partículas com uma **multiplicidade específica**.

**Formato:**
```
(tipo_partícula1, tipo_partícula2, multiplicidade)
```

**Exemplo:**
```python
('circle', 'triangle', 1)  # Ligação simples entre círculo e triângulo
('square', 'pentagon', 2)  # Ligação dupla entre quadrado e pentágono
```

**Regras:**
- Partículas do mesmo tipo não podem se ligar (regra do sistema)
- Multiplicidades possíveis: 1 (simples), 2 (dupla), 3 (tripla)
- Ordem não importa: `(circle, triangle, 1)` = `(triangle, circle, 1)`

---

## Como Funciona

### Para Cada Efeito:
1. Sistema gera 2-3 padrões de ligação aleatórios
2. Esses padrões são únicos para cada partida (baseado em seed)
3. Molécula precisa ter **TODOS** os padrões para ter o efeito

### Exemplo Prático:

**Efeito: Analgésico**
- Padrão 1: `circle ↔ triangle` (multiplicidade 1)
- Padrão 2: `square ↔ pentagon` (multiplicidade 2)

**Molécula que TEM o efeito:**
```
Partículas: circle, triangle, square, pentagon
Ligações:
  - circle ↔ triangle (mult. 1) ✓
  - square ↔ pentagon (mult. 2) ✓

Resultado: ✅ TEM efeito Analgésico
```

**Molécula que NÃO TEM o efeito:**
```
Partículas: circle, triangle, square
Ligações:
  - circle ↔ triangle (mult. 1) ✓
  - circle ↔ square (mult. 1) ✗ (faltou square ↔ pentagon)

Resultado: ❌ NÃO TEM efeito Analgésico
```

---

## Vantagens do Sistema

### ✅ Simplicidade
- Fácil de entender: "precisa ter essas ligações"
- Visual: jogador pode ver as ligações na estrutura

### ✅ Flexibilidade
- Moléculas podem ter múltiplos efeitos
- Não precisa ser grande: 2-3 ligações específicas são suficientes

### ✅ Unicidade por Partida
- Cada save tem padrões diferentes
- Força descoberta experimental
- Sem "receita de bolo" fixa

### ✅ Balanceamento
- Efeitos com 2 padrões: mais comuns
- Efeitos com 3 padrões: mais raros/poderosos

---

## Tipos de Partículas

```
circle    ○  - 1 conexão
square    □  - 2 conexões
triangle  △  - 3 conexões
pentagon  ⬠  - 4 conexões
```

**Ligações possíveis:**
- circle ↔ square
- circle ↔ triangle
- circle ↔ pentagon
- square ↔ triangle
- square ↔ pentagon
- triangle ↔ pentagon

**Total:** 6 tipos de ligações × 3 multiplicidades = 18 padrões possíveis

---

## Efeitos Múltiplos

Uma molécula pode ter **múltiplos efeitos** simultaneamente:

**Exemplo:**
```
Molécula com ligações:
  - circle ↔ triangle (mult. 1)
  - square ↔ pentagon (mult. 2)
  - triangle ↔ pentagon (mult. 3)

Efeitos possíveis:
  ✅ Analgésico (se precisar de circle-triangle + square-pentagon)
  ✅ Anti-inflamatório (se precisar de triangle-pentagon + outra)
  ✅ Cardioprotetor (se precisar de circle-triangle + triangle-pentagon)
```

**Trade-offs:**
- Efeitos terapêuticos + colaterais podem coexistir
- Jogador precisa balancear benefícios vs riscos

---

## Geração Aleatória por Partida

### Seed Base
- Cada save tem um ID único
- ID é usado como seed para randomização

### Consistência
- Mesmo save = mesmos padrões (sempre)
- Diferentes saves = padrões diferentes

### Randomização
```
Seed = hash(save_id + nome_efeito)

Para cada efeito:
  - Gerar 2-3 padrões aleatórios únicos
  - Usar tipos de partículas aleatórios
  - Usar multiplicidades aleatórias
  - Garantir que padrões sejam distintos
```

---

## Exemplos de Padrões por Efeito

### Efeitos Terapêuticos

**Analgésico:**
- circle ↔ triangle (mult. 1)
- square ↔ pentagon (mult. 2)

**Anti-inflamatório:**
- circle ↔ triangle (mult. 2)
- triangle ↔ pentagon (mult. 1)

**Antibiótico:**
- square ↔ triangle (mult. 1)
- pentagon ↔ square (mult. 1)
- circle ↔ pentagon (mult. 3)

**Cardioprotetor:**
- circle ↔ pentagon (mult. 2)
- square ↔ triangle (mult. 2)

### Efeitos Colaterais

**Hepatotóxico:**
- triangle ↔ pentagon (mult. 3)
- circle ↔ square (mult. 2)

**Neurotóxico:**
- circle ↔ pentagon (mult. 1)
- square ↔ triangle (mult. 3)

**Carcinogênico:**
- pentagon ↔ square (mult. 1)
- triangle ↔ pentagon (mult. 2)
- circle ↔ triangle (mult. 3)

---

## Estratégia de Descoberta

### Como o Jogador Descobre Padrões?

1. **Testar múltiplas moléculas**
   - Criar moléculas com diferentes ligações
   - Testar efeitos de cada uma

2. **Observar padrões comuns**
   - Moléculas com mesmo efeito têm ligações em comum
   - Deduzir quais ligações são necessárias

3. **Experimentos controlados**
   - Criar moléculas que diferem em apenas uma ligação
   - Comparar efeitos para isolar padrões

4. **Documentação**
   - Anotar quais ligações produzem quais efeitos
   - Construir "biblioteca" de conhecimento

---

## Implementação Técnica

### Estrutura de Dados

```python
# Padrão de ligação
pattern = ('circle', 'triangle', 1)

# Efeito com seus padrões
effect_patterns = {
    'Analgésico': [
        ('circle', 'triangle', 1),
        ('square', 'pentagon', 2)
    ]
}
```

### Verificação

```python
def molecule_has_effect(molecule, effect_patterns):
    """
    Verifica se molécula tem TODOS os padrões necessários
    """
    for pattern in effect_patterns:
        if not molecule_has_pattern(molecule, pattern):
            return False
    return True
```

### Normalização

Padrões são normalizados (ordem alfabética):
- `(circle, triangle, 1)` = `(triangle, circle, 1)`
- Garante comparação consistente

---

## Balanceamento

### Número de Padrões por Efeito

- **2 padrões:** Efeitos mais comuns
  - Mais fáceis de sintetizar
  - Podem aparecer em moléculas pequenas (massa 3-4)

- **3 padrões:** Efeitos mais raros
  - Mais difíceis de sintetizar
  - Geralmente requerem moléculas maiores (massa 4-6)

### Distribuição Sugerida

- 70% dos efeitos: 2 padrões
- 30% dos efeitos: 3 padrões

Isso cria:
- Efeitos básicos acessíveis
- Efeitos avançados como objetivos

---

## Notas de Design

### Por que Padrões de Ligação?

1. **Simplicidade Visual**
   - Jogador vê diretamente na estrutura molecular
   - Não precisa entender atributos abstratos

2. **Intuitivo**
   - "Precisa ter essas ligações" é fácil de entender
   - Similar a receitas químicas reais

3. **Flexível**
   - Moléculas podem ter múltiplos efeitos
   - Não restringe tamanho excessivamente

4. **Único por Partida**
   - Cada jogo é diferente
   - Rejogabilidade alta

---

**📖 Documentação criada em: 2025-01-XX**

**🔬 Chemical Pharma - Molecular Synthesis Game**


