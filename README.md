# Chemical Pharma - Molecular Synthesis Game

Um jogo de síntese molecular onde você combina partículas para criar novas moléculas seguindo regras químicas específicas.

## 🧪 Características

### Partículas
- **Círculo (○)**: 1 conexão
- **Quadrado (□)**: 2 conexões
- **Triângulo (△)**: 3 conexões
- **Pentágono (⬠)**: 4 conexões

Cada partícula pode ter polaridade **positiva (+)** ou **negativa (-)**.

### Regras de Síntese
1. **Anulação**: Partículas do mesmo tipo com polaridades opostas se anulam
2. **Merge**: Partículas restantes são combinadas
3. **Rebond**: Sistema tenta estabilizar a molécula criando novas ligações
4. **Validação**: 
   - Partículas do mesmo tipo não podem se ligar
   - Cada partícula deve respeitar seu limite de conexões
   - Resultado deve ser uma molécula conectada (ou múltiplas moléculas separadas)

### Funcionalidades
- ✅ Sistema de síntese com 4 etapas (anulação, merge, rebond, reorganização)
- ✅ Suporte para múltiplas ligações entre partículas
- ✅ Detecção e separação de moléculas desconectadas
- ✅ Fórmula molecular (notação CQTP baseada em conexões)
- ✅ Sistema de jogadores com saves independentes
- ✅ Biblioteca de moléculas com filtros (massa, carga, polaridade)
- ✅ Laboratório de síntese com feedback visual
- ✅ Descobertas podem ser salvas e usadas em novas sínteses
- ✅ Comutatividade garantida (A+B = B+A)
- ✅ Visualização 2D com PixiJS
- ✅ **Síntese Automática**: Teste múltiplas sínteses de uma vez com uma molécula base
  - Seleção da molécula base e grupo lado a lado para melhor usabilidade
  - Estatísticas detalhadas: Total, Sucesso, Falhas, Desconhecidas e Conhecidas
  - Filtros por massa ou seleção específica de moléculas

## 🚀 Como Executar

### Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

O servidor estará disponível em `http://localhost:5000`

### Frontend (Vue 3 + Vite)
```bash
cd frontend
npm install
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## 📁 Estrutura do Projeto

```
chemical-pharma/
├── backend/
│   ├── app.py                      # Servidor Flask
│   ├── core/
│   │   ├── synthesis.py            # Algoritmo de síntese
│   │   └── validator.py            # Validação de moléculas
│   └── data/
│       ├── molecules.py             # Database de moléculas predefinidas
│       ├── discovered_molecules.py  # Gerenciamento de descobertas
│       ├── saves.py                 # Sistema de saves/jogadores
│       └── synthesis_results.py     # Cache de sínteses
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MoleculeViewer.vue   # Visualização de moléculas
│   │   │   └── MoleculeSelector.vue # Seletor para síntese
│   │   ├── views/
│   │   │   ├── Home.vue             # Tela principal
│   │   │   ├── PlayerSelect.vue     # Seleção de jogador
│   │   │   ├── MoleculeLibrary.vue  # Biblioteca de moléculas
│   │   │   ├── Synthesis.vue        # Laboratório de síntese
│   │   │   └── AutoSynthesis.vue    # Síntese automática
│   │   ├── services/
│   │   │   └── api.js               # Cliente HTTP para backend
│   │   └── utils/
│   │       ├── moleculeComparison.js # Comparação estrutural
│   │       └── webglQueue.js        # Gerenciamento WebGL
│   └── vite.config.js
│
├── modelagem/                       # Documentação técnica
│   ├── README.md                    # Índice da documentação
│   ├── 01_ALGORITMO_SINTESE.md      # Algoritmo de síntese
│   ├── 02_COMPARACAO_ESTRUTURAL.md  # Comparação molecular
│   ├── 03_FORMULA_MOLECULAR.md      # Fórmula CQTP
│   ├── 04_ARQUITETURA_SISTEMA.md    # Arquitetura geral
│   ├── 05_ANALISE_REBOND.md         # Análise do rebond
│   ├── 06_ANALISE_COMPLETUDE_SINTESE.md # Completude
│   ├── 07_SINTESE_AUTOMATICA.md     # Síntese automática
│   └── GIT_GUIDE.md                 # Guia Git
│
└── README.md                        # Este arquivo
```

## 🎮 Como Jogar

1. **Selecione ou crie um jogador**
2. **Acesse o Laboratório de Síntese**
3. **Escolha duas moléculas conhecidas**
4. **Sintetize e observe o resultado**
5. **Salve suas descobertas na biblioteca**
6. **Use descobertas para criar moléculas ainda maiores!**

## 🔬 Exemplos de Sínteses

### Síntese Única
```
○- + □+ → Falha (sem anulação)
○+ + ○- → Sucesso: anulação completa
CQ²T + Q²P → CTP (pentagon+ com triangle- e circle-)
```

### Múltiplas Moléculas
```
4-2 + 4-1 → 2 moléculas separadas (C²Q + C²Q)
```

## 🛠️ Tecnologias

- **Backend**: Python 3, Flask, Flask-SocketIO
- **Frontend**: Vue 3, Vite, PixiJS
- **Persistência**: JSON files
- **Visualização**: PixiJS (WebGL/Canvas)

## 📊 Propriedades Moleculares

- **Massa**: Número de partículas
- **Carga**: Soma das polaridades (positiva, neutra, negativa)
- **Fórmula**: Notação CQTP baseada no número de conexões
  - Exemplo: `C²QT` = 2 circles, 1 square, 1 triangle

## 📚 Documentação Técnica

Para documentação técnica detalhada sobre algoritmos, arquitetura e análises, consulte a pasta [`modelagem/`](./modelagem/README.md):

- [Algoritmo de Síntese](./modelagem/01_ALGORITMO_SINTESE.md)
- [Comparação Estrutural](./modelagem/02_COMPARACAO_ESTRUTURAL.md)
- [Fórmula Molecular](./modelagem/03_FORMULA_MOLECULAR.md)
- [Arquitetura do Sistema](./modelagem/04_ARQUITETURA_SISTEMA.md)
- [Análise do Rebond](./modelagem/05_ANALISE_REBOND.md)
- [Análise de Completude](./modelagem/06_ANALISE_COMPLETUDE_SINTESE.md)
- [Síntese Automática](./modelagem/07_SINTESE_AUTOMATICA.md)

## 🎯 Roadmap

- [ ] Sistema de economia (dinheiro, custos de síntese)
- [ ] Objetivos e missões
- [ ] Mais tipos de partículas
- [ ] Sistema de reações em cadeia
- [ ] Multiplayer
- [ ] Melhorias visuais (animações de síntese)

## 📝 Licença

Projeto em desenvolvimento - Chemical Pharma Game

---

**Desenvolvido com ❤️ e ⚗️**



