# Arquitetura do Sistema Chemical Pharma

## 📐 Visão Geral

Arquitetura **cliente-servidor** com separação clara entre frontend (Vue 3) e backend (Flask), comunicando-se via REST API.

---

## 🏗️ Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND (Vue 3)                  │
│  ┌──────────────────────────────────────────────┐   │
│  │            Views (Screens)                   │   │
│  │  • Home                                      │   │
│  │  • PlayerSelect                              │   │
│  │  • MoleculeLibrary                           │   │
│  │  • Synthesis                                 │   │
│  └──────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌──────────────────────────────────────────────┐   │
│  │         Components                           │   │
│  │  • MoleculeViewer (PixiJS)                   │   │
│  │  • MoleculeSelector                          │   │
│  └──────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌──────────────────────────────────────────────┐   │
│  │         Services & Utils                     │   │
│  │  • api.js (HTTP client)                      │   │
│  │  • moleculeComparison.js                     │   │
│  │  • webglQueue.js                             │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                       ↕ REST API (HTTP/JSON)
┌─────────────────────────────────────────────────────┐
│                  BACKEND (Flask)                     │
│  ┌──────────────────────────────────────────────┐   │
│  │           REST API (app.py)                  │   │
│  │  • /api/molecules                            │   │
│  │  • /api/synthesis/mix                        │   │
│  │  • /api/discoveries                          │   │
│  │  • /api/saves                                │   │
│  └──────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌──────────────────────────────────────────────┐   │
│  │            Core Logic                        │   │
│  │  • synthesis.py (Algoritmo de síntese)       │   │
│  │  • validator.py (Validação)                  │   │
│  └──────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌──────────────────────────────────────────────┐   │
│  │          Data Layer                          │   │
│  │  • molecules.py (DB de moléculas)            │   │
│  │  • discovered_molecules.py                   │   │
│  │  • saves.py (Sistema de jogadores)           │   │
│  │  • synthesis_results.py (Cache)              │   │
│  └──────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌──────────────────────────────────────────────┐   │
│  │         Persistence (JSON)                   │   │
│  │  • molecules.py (hardcoded)                  │   │
│  │  • discovered_molecules.json                 │   │
│  │  • saves.json                                │   │
│  │  • synthesis_cache.json                      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Frontend (Vue 3 + Vite)

### Tecnologias
- **Vue 3**: Framework reativo
- **Vue Router**: Navegação SPA
- **Vite**: Build tool rápido
- **PixiJS**: Renderização 2D (WebGL/Canvas)
- **Axios** (via fetch): Cliente HTTP

### Estrutura de Pastas
```
frontend/
├── src/
│   ├── main.js                  # Entry point
│   ├── App.vue                  # Root component
│   ├── router/
│   │   └── index.js             # Rotas
│   ├── views/                   # Páginas
│   │   ├── Home.vue
│   │   ├── PlayerSelect.vue
│   │   ├── MoleculeLibrary.vue
│   │   └── Synthesis.vue
│   ├── components/              # Componentes reutilizáveis
│   │   ├── MoleculeViewer.vue
│   │   └── MoleculeSelector.vue
│   ├── services/                # Lógica de negócio
│   │   └── api.js
│   └── utils/                   # Utilitários
│       ├── moleculeComparison.js
│       └── webglQueue.js
├── index.html
├── package.json
└── vite.config.js
```

### Fluxo de Dados
```
User Action → View → Service (api.js) → Backend API
                ↓
          State Update → Component Re-render
```

---

## ⚙️ Backend (Flask + Python)

### Tecnologias
- **Flask**: Framework web
- **Flask-CORS**: Cross-origin requests
- **Flask-SocketIO**: WebSocket support (futuro)
- **Python 3.10+**: Linguagem

### Estrutura de Pastas
```
backend/
├── app.py                       # Servidor Flask
├── requirements.txt             # Dependências
├── core/                        # Lógica central
│   ├── __init__.py
│   ├── synthesis.py             # Algoritmo de síntese
│   └── validator.py             # Validação
├── data/                        # Camada de dados
│   ├── __init__.py
│   ├── molecules.py             # DB de moléculas predefinidas
│   ├── discovered_molecules.py  # Gerenciamento de descobertas
│   ├── discovered_molecules.json
│   ├── saves.py                 # Sistema de saves/jogadores
│   ├── saves.json
│   ├── synthesis_results.py     # Cache de sínteses
│   └── synthesis_cache.json
└── (tests/)                     # Testes (futuro)
```

### Fluxo de Requisição
```
HTTP Request → Flask Route → Business Logic → Data Layer → JSON File
                     ↓
            HTTP Response (JSON)
```

---

## 🔄 REST API Endpoints

### Moléculas
```
GET  /api/molecules              # Listar todas
GET  /api/molecules/mass/<int>   # Filtrar por massa
```

### Síntese
```
POST /api/synthesis/mix          # Sintetizar duas moléculas
  Body: {"mol_a_id": "m3_1", "mol_b_id": "m3_2"}
  
GET  /api/synthesis/results      # Histórico de sínteses
GET  /api/synthesis/stats        # Estatísticas
POST /api/synthesis/cache/clear  # Limpar cache
```

### Descobertas
```
GET    /api/discoveries          # Listar descobertas do jogador
POST   /api/discoveries          # Salvar nova descoberta
  Body: {"molecule": {...}, "name": "...", "formula": "..."}
  
DELETE /api/discoveries/<id>     # Deletar descoberta
POST   /api/discoveries/clear    # Limpar todas
GET    /api/discoveries/stats    # Estatísticas
```

### Saves/Jogadores
```
GET    /api/saves                # Listar todos os saves
POST   /api/saves                # Criar novo save
  Body: {"player_name": "..."}
  
POST   /api/saves/<id>/select    # Selecionar save ativo
GET    /api/saves/current        # Get save atual
DELETE /api/saves/<id>           # Deletar save
```

---

## 💾 Sistema de Persistência

### Formato: JSON Files

#### 1. Moléculas Predefinidas (Hardcoded)
```python
# backend/data/molecules.py
MOLECULES_DATABASE = {
    'm3_1': {
        'id': 'm3_1',
        'name': 'Molécula 3-1',
        'particles': [...],
        'bonds': [...]
    },
    # ...
}
```

#### 2. Descobertas (discovered_molecules.json)
```json
{
  "save_abc123": [
    {
      "id": "discovery_1234567890",
      "molecule": {
        "particles": [...],
        "bonds": [...]
      },
      "name": "Minha Descoberta",
      "formula": "CQ²T",
      "timestamp": "2025-11-28T12:00:00",
      "discoverer": "save_abc123"
    }
  ]
}
```

#### 3. Saves (saves.json)
```json
{
  "saves": {
    "save_abc123": {
      "id": "save_abc123",
      "player_name": "Moises",
      "created_at": "2025-11-28T10:00:00",
      "money": 1000,
      "discoveries_count": 5,
      "syntheses_count": 42
    }
  },
  "active_save_id": "save_abc123"
}
```

#### 4. Cache de Síntese (synthesis_cache.json)
```json
{
  "save_abc123:m3_1+m3_2": {
    "success": true,
    "result": {...},
    "details": {...}
  }
}
```

### Isolamento por Save
Cada jogador tem:
- ✅ Descobertas próprias
- ✅ Cache de síntese próprio
- ✅ Estatísticas próprias
- ✅ Dinheiro próprio

---

## 🔐 Fluxo de Autenticação

```
1. User abre aplicação
        ↓
2. Router verifica save ativo
        ↓
3. Se não há save → /player-select
        ↓
4. User seleciona/cria save
        ↓
5. Backend define active_save_id
        ↓
6. Todas as operações usam active_save_id
        ↓
7. User pode trocar save (logout)
```

### Implementação
```javascript
// frontend/src/router/index.js
router.beforeEach(async (to, from, next) => {
  if (to.path !== '/player-select') {
    const response = await getCurrentSave()
    
    if (!response.success) {
      next('/player-select')  // Redirecionar
      return
    }
  }
  
  next()
})
```

---

## 🎨 Visualização (PixiJS)

### Estratégia: Render-to-Image
Para evitar limite de contextos WebGL:

```
1. Criar PixiJS app offscreen
2. Renderizar molécula
3. Converter canvas → PNG (base64)
4. Exibir imagem estática
5. Destruir app
```

### Implementação
```javascript
// MoleculeViewer.vue
async renderMoleculeToImage() {
  // 1. Criar canvas offscreen
  const canvas = document.createElement('canvas')
  
  // 2. PixiJS app
  const app = new PIXI.Application({view: canvas, ...})
  
  // 3. Desenhar molécula
  drawMolecule(app.stage, molecule)
  
  // 4. Converter para imagem
  const imageData = canvas.toDataURL('image/png')
  
  // 5. Exibir
  imgElement.src = imageData
  
  // 6. Destruir
  app.destroy(true)
}
```

---

## 📊 Fluxo Completo: Síntese

```
┌─────────────────┐
│  User clicks    │
│  "Sintetizar"   │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Synthesis.vue   │
│ performSynthesis│
└────────┬────────┘
         ↓
┌─────────────────┐
│  api.js         │
│  POST /synthesis│
└────────┬────────┘
         ↓
┌─────────────────┐
│  app.py         │
│  api_synthesize │
└────────┬────────┘
         ↓
┌─────────────────┐
│ synthesis.py    │
│ synthesize()    │
│  1. Annihilate  │
│  2. Merge       │
│  3. Rebond      │
│  4. Reorganize  │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Cache & Return  │
│ synthesis_cache │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Frontend Update │
│ • Show result   │
│ • Update UI     │
│ • Offer save    │
└─────────────────┘
```

---

## 🔧 Configuração de Desenvolvimento

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Portas
- **Backend**: `http://localhost:5000`
- **Frontend**: `http://localhost:5173`
- **CORS**: Habilitado para desenvolvimento

---

## 📈 Escalabilidade

### Limitações Atuais
1. **JSON files**: Não escala para muitos jogadores
2. **Cache em arquivo**: Pode crescer indefinidamente
3. **Sem autenticação real**: Qualquer um pode acessar qualquer save

### Melhorias Futuras

#### Banco de Dados
```
JSON Files → SQLite → PostgreSQL
```

#### Autenticação
```
Simple Save ID → JWT Tokens → OAuth
```

#### Cache
```
JSON File → Redis → Memcached
```

#### API
```
REST → GraphQL (consultas flexíveis)
```

---

## 🧪 Testes

### Estrutura (Futuro)
```
backend/
├── tests/
│   ├── test_synthesis.py
│   ├── test_validator.py
│   ├── test_molecules.py
│   └── test_api.py

frontend/
├── tests/
│   ├── unit/
│   │   └── moleculeComparison.test.js
│   └── e2e/
│       └── synthesis.test.js
```

### Comandos
```bash
# Backend
pytest backend/tests/

# Frontend
npm run test:unit
npm run test:e2e
```

---

## 🔍 Monitoramento

### Logs (Futuro)
```python
# Backend
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Synthesis: {mol_a_id} + {mol_b_id}")
logger.error(f"Synthesis failed: {reason}")
```

### Métricas (Futuro)
- Taxa de sucesso de sínteses
- Tempo médio de síntese
- Moléculas mais usadas
- Descobertas por jogador

---

## 🚀 Deploy (Futuro)

### Backend
```
Flask App → Gunicorn → Nginx → Cloud (AWS/Heroku)
```

### Frontend
```
Vue Build → Static Files → CDN (Vercel/Netlify)
```

### Database
```
JSON Files → PostgreSQL (Cloud)
```

---

## 💡 Decisões de Design

### Por Que Vue 3?
- ✅ Reatividade simples
- ✅ Composition API
- ✅ Bom ecossistema
- ✅ Performance

### Por Que Flask?
- ✅ Simples e direto
- ✅ Python (fácil algoritmos)
- ✅ Extensível
- ✅ Bom para prototipação

### Por Que JSON Files?
- ✅ Simplicidade
- ✅ Sem setup de BD
- ✅ Fácil debug
- ✅ Git-friendly
- ⚠️ Não escala (OK para protótipo)

### Por Que PixiJS?
- ✅ Performance WebGL
- ✅ API simples
- ✅ Fallback para Canvas
- ✅ Bom para 2D

---

## 📚 Referências

- **Vue 3**: https://vuejs.org/
- **Flask**: https://flask.palletsprojects.com/
- **PixiJS**: https://pixijs.com/
- **REST API Design**: https://restfulapi.net/

---

**Diagramas e documentação completa no diretório `modelagem/`**




