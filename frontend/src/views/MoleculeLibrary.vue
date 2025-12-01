<template>
  <div class="molecule-library">
    <!-- Header -->
    <header class="library-header">
      <button class="back-btn" @click="voltarHome">← Voltar</button>
      <h1>📚 Biblioteca de Moléculas</h1>
      <div class="stats">
        <span>Total: {{ filteredMolecules.length }}</span>
      </div>
    </header>

    <!-- Filtros -->
    <div class="filters">
      <div class="filter-group">
        <label>Massa:</label>
        <select v-model="selectedMass" class="filter-select">
          <option value="all">Todas</option>
          <option v-for="mass in availableMasses" :key="mass" :value="mass">
            Massa {{ mass }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label>Tipo:</label>
        <select v-model="selectedType" class="filter-select">
          <option value="all">Todos</option>
          <option value="predefined">Predefinidas</option>
          <option value="discoveries">Descobertas</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Polaridade:</label>
        <select v-model="selectedPolarity" class="filter-select">
          <option value="all">Todas</option>
          <option value="positive">Positiva</option>
          <option value="neutral">Neutra</option>
          <option value="negative">Negativa</option>
        </select>
      </div>

      <div class="filter-group search-group">
        <label>Buscar:</label>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Nome ou fórmula..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Lista de moléculas -->
    <div class="molecules-grid">
      <div
        v-for="molecule in filteredMolecules"
        :key="molecule.id"
        class="molecule-card"
      >
        <div class="card-header">
          <h3>{{ molecule.name || molecule.formula || molecule.id }}</h3>
          <span v-if="molecule.isDiscovery" class="badge discovery">✨ Descoberta</span>
          <span v-else class="badge predefined">📖 Predefinida</span>
        </div>

        <div class="molecule-visualization">
          <MoleculeViewer :molecule="molecule" :width="350" :height="250" />
        </div>

        <div class="molecule-info">
          <div class="info-row">
            <span class="label">Fórmula:</span>
            <span class="value">{{ molecule.formula }}</span>
          </div>
          <div class="info-row">
            <span class="label">Massa:</span>
            <span class="value">{{ molecule.particles.length }}</span>
          </div>
          <div class="info-row">
            <span class="label">Polaridade:</span>
            <span class="value" :class="`polarity-${molecule.polarity}`">
              {{ getPolarityLabel(molecule.polarity) }}
            </span>
          </div>
          <div class="info-row">
            <span class="label">Carga:</span>
            <span class="value">{{ molecule.charge > 0 ? '+' : '' }}{{ molecule.charge }}</span>
          </div>
          
          <ObservableProperties v-if="molecule.observableProperties" :properties="molecule.observableProperties" />
        </div>
      </div>
    </div>

    <div v-if="filteredMolecules.length === 0" class="empty-state">
      <p>Nenhuma molécula encontrada com os filtros selecionados.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MoleculeViewer from '../components/MoleculeViewer.vue'
import ObservableProperties from '../components/ObservableProperties.vue'
import { getAllMolecules, getAllDiscoveries, calculateMoleculeProperties, getObservableProperties } from '../services/api.js'

const router = useRouter()

const allMolecules = ref([])

// Função auxiliar para carregar propriedades observáveis
async function loadObservableProperties(molecule) {
  try {
    const response = await getObservableProperties(molecule)
    if (response.success) {
      return response.data
    }
  } catch (error) {
    console.warn('Erro ao carregar propriedades observáveis:', error)
  }
  return null
}
const selectedMass = ref('all')
const selectedType = ref('all')
const selectedPolarity = ref('all')
const searchQuery = ref('')

onMounted(async () => {
  await loadMolecules()
})

async function loadMolecules() {
  try {
    // Carregar moléculas predefinidas
    const predefinedResponse = await getAllMolecules()
    let molecules = []

    if (predefinedResponse.success) {
      const moleculesWithProps = await Promise.all(
        predefinedResponse.data.map(async mol => {
          const props = calculateMoleculeProperties(mol)
          const observableProps = await loadObservableProperties(mol)
          return {
            ...mol,
            ...props,
            observableProperties: observableProps,
            isDiscovery: false
          }
        })
      )
      molecules = moleculesWithProps
    }

    // Carregar descobertas
    try {
      const discoveriesResponse = await getAllDiscoveries()
      if (discoveriesResponse.success) {
        const discoveriesWithProps = await Promise.all(
          discoveriesResponse.data.map(async disc => {
            const mol = disc.molecule
            const props = calculateMoleculeProperties(mol)
            const observableProps = await loadObservableProperties(mol)
            return {
              ...mol,
              id: disc.id,
              name: disc.name,
              formula: disc.formula || props.formula,
              ...props,
              observableProperties: observableProps,
              isDiscovery: true
            }
          })
        )
        molecules = [...molecules, ...discoveriesWithProps]
      }
    } catch (error) {
      console.warn('Erro ao carregar descobertas:', error)
    }

    allMolecules.value = molecules
  } catch (error) {
    console.error('Erro ao carregar moléculas:', error)
  }
}

const availableMasses = computed(() => {
  const masses = new Set(allMolecules.value.map(m => m.particles.length))
  return Array.from(masses).sort((a, b) => a - b)
})

const filteredMolecules = computed(() => {
  let filtered = allMolecules.value

  // Filtro por massa
  if (selectedMass.value !== 'all') {
    filtered = filtered.filter(m => m.particles.length === parseInt(selectedMass.value))
  }

  // Filtro por tipo
  if (selectedType.value === 'predefined') {
    filtered = filtered.filter(m => !m.isDiscovery)
  } else if (selectedType.value === 'discoveries') {
    filtered = filtered.filter(m => m.isDiscovery)
  }

  // Filtro por polaridade
  if (selectedPolarity.value !== 'all') {
    filtered = filtered.filter(m => m.polarity === selectedPolarity.value)
  }

  // Busca por nome ou fórmula
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(m => {
      const name = (m.name || '').toLowerCase()
      const formula = (m.formula || '').toLowerCase()
      const id = (m.id || '').toLowerCase()
      return name.includes(query) || formula.includes(query) || id.includes(query)
    })
  }

  return filtered
})

function getPolarityLabel(polarity) {
  const labels = {
    positive: 'Positiva (+)',
    negative: 'Negativa (-)',
    neutral: 'Neutra (0)'
  }
  return labels[polarity] || polarity
}

function voltarHome() {
  router.push('/')
}
</script>

<style scoped>
.molecule-library {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding-bottom: 2rem;
}

.library-header {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  border-bottom: 2px solid #444;
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  padding: 0.5rem 1rem;
  background-color: #444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
}

.back-btn:hover {
  background-color: #555;
}

.library-header h1 {
  flex: 1;
  color: #fff;
  margin: 0;
  font-size: 2rem;
}

.stats {
  color: #aaa;
  font-size: 1.1rem;
}

.filters {
  display: flex;
  gap: 1.5rem;
  padding: 2rem;
  background-color: rgba(0, 0, 0, 0.2);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 150px;
}

.search-group {
  flex: 1;
  min-width: 250px;
}

.filter-group label {
  color: #aaa;
  font-size: 0.9rem;
  font-weight: 600;
}

.filter-select,
.search-input {
  padding: 0.5rem;
  border-radius: 6px;
  border: 2px solid #444;
  background-color: #2a2a2a;
  color: #fff;
  font-size: 1rem;
}

.filter-select:focus,
.search-input:focus {
  outline: none;
  border-color: #646cff;
}

.molecules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.molecule-card {
  background-color: #2a2a2a;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: transform 0.2s, border-color 0.2s;
}

.molecule-card:hover {
  transform: translateY(-4px);
  border-color: #646cff;
}

.card-header {
  padding: 1rem 1.5rem;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.card-header h3 {
  color: #fff;
  margin: 0;
  font-size: 1.2rem;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge.discovery {
  background-color: #f59e0b;
  color: #1a1a1a;
}

.badge.predefined {
  background-color: #3b82f6;
  color: white;
}

.molecule-visualization {
  background-color: #1a1a1a;
  display: flex;
  align-items: center;
  justify-content: center;
}

.molecule-info {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-row .label {
  color: #aaa;
  font-size: 0.9rem;
}

.info-row .value {
  color: #fff;
  font-weight: 600;
  font-size: 1.1rem;
}

.polarity-positive {
  color: #ef4444 !important;
}

.polarity-negative {
  color: #3b82f6 !important;
}

.polarity-neutral {
  color: #aaa !important;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #aaa;
  font-size: 1.2rem;
}
</style>

