<template>
  <div class="properties-library">
    <!-- Header -->
    <header class="library-header">
      <button class="back-btn" @click="voltarHome">← Voltar</button>
      <h1>📖 Biblioteca de Propriedades e Efeitos</h1>
      <div class="stats">
        <span>Guia de Referência</span>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Carregando perfil de propriedades...</p>
    </div>

    <!-- Content -->
    <div v-else-if="profile" class="content">
      <!-- Seção: Sabores por Topologia -->
      <section class="properties-section">
        <h2>👅 Sabores por Topologia</h2>
        <p class="section-description">
          Cada topologia estrutural corresponde a um sabor específico nesta partida.
        </p>
        <div class="flavor-grid">
          <div
            v-for="(flavor, topology) in profile.topology_flavor_map"
            :key="topology"
            class="flavor-card"
          >
            <div class="topology-icon">{{ getTopologyEmoji(topology) }}</div>
            <div class="topology-name">{{ getTopologyName(topology) }}</div>
            <div class="flavor-name">{{ flavor }}</div>
          </div>
        </div>
      </section>

      <!-- Seção: Cores por Multiplicidades -->
      <section class="properties-section">
        <h2>🎨 Cores por Multiplicidades de Ligação</h2>
        <p class="section-description">
          Cada combinação de multiplicidades de ligações produz uma cor específica.
        </p>
        <div class="color-grid">
          <div
            v-for="(appearance, multKey) in profile.multiplicity_color_map"
            :key="multKey"
            class="color-card"
          >
            <div
              class="color-preview"
              :style="{ backgroundColor: appearance.color }"
            ></div>
            <div class="color-info">
              <div class="color-name">{{ appearance.name }}</div>
              <div class="color-description">{{ appearance.description }}</div>
              <div class="multiplicities">
                Multiplicidades: {{ formatMultiplicities(multKey) }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Seção: Efeitos -->
      <section class="properties-section">
        <h2>⚡ Efeitos Moleculares</h2>
        <p class="section-description">
          Cada efeito requer padrões específicos de ligação entre partículas.
          A molécula precisa ter <strong>TODOS</strong> os padrões listados para ter o efeito.
        </p>
        
        <!-- Filtros de efeitos -->
        <div class="effect-filters">
          <button
            v-for="category in effectCategories"
            :key="category.value"
            :class="['filter-btn', { active: selectedCategory === category.value }]"
            @click="selectedCategory = category.value"
          >
            {{ category.label }}
          </button>
        </div>

        <!-- Lista de Efeitos Terapêuticos -->
        <div v-if="selectedCategory === 'all' || selectedCategory === 'therapeutic'" class="effects-group">
          <h3>💚 Efeitos Terapêuticos</h3>
          <div class="effects-grid">
            <div
              v-for="(patterns, effectName) in therapeuticEffects"
              :key="effectName"
              class="effect-card"
            >
              <div class="effect-header">
                <span class="effect-name">{{ effectName }}</span>
                <span class="pattern-count">{{ patterns.length }} padrão(ões)</span>
              </div>
              <div class="effect-patterns">
                <div
                  v-for="(pattern, idx) in patterns"
                  :key="idx"
                  class="pattern-item"
                >
                  <span class="pattern-bond">
                    {{ formatParticleType(pattern[0]) }} ↔ {{ formatParticleType(pattern[1]) }}
                  </span>
                  <span class="pattern-multiplicity">×{{ pattern[2] }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Lista de Efeitos Colaterais -->
        <div v-if="selectedCategory === 'all' || selectedCategory === 'side'" class="effects-group">
          <h3>💔 Efeitos Colaterais</h3>
          <div class="effects-grid">
            <div
              v-for="(patterns, effectName) in sideEffects"
              :key="effectName"
              class="effect-card side-effect"
            >
              <div class="effect-header">
                <span class="effect-name">{{ effectName }}</span>
                <span class="pattern-count">{{ patterns.length }} padrão(ões)</span>
              </div>
              <div class="effect-patterns">
                <div
                  v-for="(pattern, idx) in patterns"
                  :key="idx"
                  class="pattern-item"
                >
                  <span class="pattern-bond">
                    {{ formatParticleType(pattern[0]) }} ↔ {{ formatParticleType(pattern[1]) }}
                  </span>
                  <span class="pattern-multiplicity">×{{ pattern[2] }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button class="btn-primary" @click="loadProfile">Tentar Novamente</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getPropertyProfile } from '../services/api.js'

const router = useRouter()

const loading = ref(true)
const profile = ref(null)
const error = ref(null)
const selectedCategory = ref('all')

const effectCategories = [
  { value: 'all', label: 'Todos' },
  { value: 'therapeutic', label: 'Terapêuticos' },
  { value: 'side', label: 'Colaterais' }
]

const therapeuticEffects = computed(() => {
  if (!profile.value || !profile.value.effect_patterns) return {}
  
  const therapeutic = [
    'Analgésico', 'Anti-inflamatório', 'Antibiótico', 'Regenerativo',
    'Antioxidante', 'Imunomodulador', 'Vasodilatador', 'Hepatoprotetor',
    'Cardioprotetor', 'Neuroprotetor'
  ]
  
  const result = {}
  therapeutic.forEach(effect => {
    if (profile.value.effect_patterns[effect]) {
      result[effect] = profile.value.effect_patterns[effect]
    }
  })
  return result
})

const sideEffects = computed(() => {
  if (!profile.value || !profile.value.effect_patterns) return {}
  
  const side = [
    'Hepatotóxico', 'Nefrotóxico', 'Neurotóxico', 'Carcinogênico',
    'Teratogênico', 'Mutagênico', 'Cardiotóxico', 'Alergênico',
    'Hemorrágico', 'Sedativo-excessivo'
  ]
  
  const result = {}
  side.forEach(effect => {
    if (profile.value.effect_patterns[effect]) {
      result[effect] = profile.value.effect_patterns[effect]
    }
  })
  return result
})

onMounted(() => {
  loadProfile()
})

async function loadProfile() {
  loading.value = true
  error.value = null
  
  try {
    const response = await getPropertyProfile()
    if (response.success) {
      profile.value = response.data
    } else {
      error.value = response.error || 'Erro ao carregar perfil'
    }
  } catch (err) {
    error.value = 'Erro ao conectar com o servidor'
    console.error('Erro ao carregar perfil:', err)
  } finally {
    loading.value = false
  }
}

function voltarHome() {
  router.push('/')
}

function getTopologyEmoji(topology) {
  const emojiMap = {
    'linear': '━',
    'Y': 'Y',
    'X': 'X',
    'tree': '⋈',
    'cycle': '○',
    'mista': '◈'
  }
  return emojiMap[topology] || '?'
}

function getTopologyName(topology) {
  const nameMap = {
    'linear': 'Linear',
    'Y': 'Ramificação Y',
    'X': 'Ramificação X',
    'tree': 'Árvore',
    'cycle': 'Ciclo',
    'mista': 'Mista'
  }
  return nameMap[topology] || topology
}

function formatMultiplicities(multKey) {
  // multKey pode ser array ou string JSON
  if (Array.isArray(multKey)) {
    return multKey.join(', ')
  }
  if (typeof multKey === 'string') {
    try {
      const parsed = JSON.parse(multKey)
      return Array.isArray(parsed) ? parsed.join(', ') : multKey
    } catch {
      return multKey
    }
  }
  return String(multKey)
}

function formatParticleType(type) {
  const typeMap = {
    'circle': '○',
    'square': '□',
    'triangle': '△',
    'pentagon': '⬠'
  }
  return typeMap[type] || type
}
</script>

<style scoped>
.properties-library {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding-bottom: 2rem;
}

.library-header {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #444;
}

.library-header h1 {
  color: #fff;
  margin: 0;
  font-size: 1.8rem;
}

.back-btn {
  background-color: #444;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.back-btn:hover {
  background-color: #555;
}

.stats {
  color: #aaa;
  font-size: 0.9rem;
}

.content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.loading-container,
.error-container {
  text-align: center;
  padding: 4rem 2rem;
  color: #aaa;
}

.loading-spinner {
  border: 4px solid #444;
  border-top: 4px solid #646cff;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.properties-section {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.properties-section h2 {
  color: #fff;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.section-description {
  color: #aaa;
  margin: 0 0 1.5rem 0;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Sabores */
.flavor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.flavor-card {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  border: 2px solid #444;
  transition: border-color 0.2s;
}

.flavor-card:hover {
  border-color: #646cff;
}

.topology-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.topology-name {
  color: #aaa;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.flavor-name {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
}

/* Cores */
.color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.color-card {
  background-color: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #444;
  transition: border-color 0.2s;
}

.color-card:hover {
  border-color: #646cff;
}

.color-preview {
  height: 80px;
  width: 100%;
}

.color-info {
  padding: 1rem;
}

.color-name {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.color-description {
  color: #aaa;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.multiplicities {
  color: #888;
  font-size: 0.8rem;
  font-family: monospace;
}

/* Efeitos */
.effect-filters {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  background-color: #444;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-btn:hover {
  background-color: #555;
}

.filter-btn.active {
  background-color: #646cff;
}

.effects-group {
  margin-bottom: 2rem;
}

.effects-group h3 {
  color: #fff;
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
}

.effects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.effect-card {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1.5rem;
  border: 2px solid #444;
  transition: border-color 0.2s;
}

.effect-card:hover {
  border-color: #646cff;
}

.effect-card.side-effect {
  border-color: #666;
}

.effect-card.side-effect:hover {
  border-color: #ff4444;
}

.effect-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #444;
}

.effect-name {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
}

.pattern-count {
  color: #aaa;
  font-size: 0.85rem;
}

.effect-patterns {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.pattern-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #0a0a0a;
  padding: 0.75rem;
  border-radius: 6px;
}

.pattern-bond {
  color: #fff;
  font-size: 1rem;
  font-family: monospace;
}

.pattern-multiplicity {
  color: #646cff;
  font-weight: 600;
  font-size: 0.9rem;
}

.error-message {
  color: #ff4444;
  margin-bottom: 1rem;
}

.btn-primary {
  background-color: #646cff;
  color: #fff;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #535bf2;
}

@media (max-width: 768px) {
  .flavor-grid,
  .color-grid,
  .effects-grid {
    grid-template-columns: 1fr;
  }
  
  .library-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>

