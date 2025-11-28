<template>
  <div class="molecule-selector">
    <h3>{{ title }}</h3>
    
    <div class="selector-content">
      <!-- Filtros -->
      <div class="filters">
        <div class="filter-group">
          <label>Massa:</label>
          <select v-model="filterMass" class="filter-select">
            <option value="all">Todas</option>
            <option v-for="mass in availableMasses" :key="mass" :value="mass">
              {{ mass }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Carga:</label>
          <select v-model="filterCharge" class="filter-select">
            <option value="all">Todas</option>
            <option value="positive">Positiva (+)</option>
            <option value="neutral">Neutra (0)</option>
            <option value="negative">Negativa (-)</option>
          </select>
        </div>
      </div>
      
      <select v-model="selectedId" @change="handleSelection" class="molecule-select">
        <option value="">Selecione uma molécula...</option>
        <optgroup 
          v-for="(group, massLabel) in filteredGroupedMolecules" 
          :key="massLabel" 
          :label="massLabel"
        >
          <option 
            v-for="mol in group" 
            :key="mol.id" 
            :value="mol.id"
          >
            {{ mol.name || mol.formula || mol.id }}
          </option>
        </optgroup>
      </select>
      
      <div v-if="selectedMolecule" class="selected-info">
        <div class="info-row">
          <span class="label">Fórmula:</span>
          <span class="value">{{ formula }}</span>
        </div>
        <div class="info-row">
          <span class="label">Massa:</span>
          <span class="value">{{ selectedMolecule.particles.length }}</span>
        </div>
        
        <!-- Visualização da molécula -->
        <div class="molecule-preview">
          <MoleculeViewer :molecule="selectedMolecule" :width="300" :height="200" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { calculateMolecularFormula } from '../services/api.js'
import MoleculeViewer from './MoleculeViewer.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Selecione Molécula'
  },
  availableMolecules: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const selectedId = ref('')
const selectedMolecule = ref(null)
const filterMass = ref('all')
const filterCharge = ref('all')

// Função para calcular carga da molécula
function calculateCharge(molecule) {
  let charge = 0
  molecule.particles.forEach(p => {
    charge += p.polarity === '+' ? 1 : -1
  })
  return charge
}

// Função para obter polaridade
function getPolarity(molecule) {
  const charge = calculateCharge(molecule)
  if (charge > 0) return 'positive'
  if (charge < 0) return 'negative'
  return 'neutral'
}

// Massas disponíveis
const availableMasses = computed(() => {
  const masses = new Set(props.availableMolecules.map(m => m.particles.length))
  return Array.from(masses).sort((a, b) => a - b)
})

// Moléculas filtradas
const filteredMolecules = computed(() => {
  let filtered = props.availableMolecules
  
  // Filtro por massa
  if (filterMass.value !== 'all') {
    filtered = filtered.filter(m => m.particles.length === parseInt(filterMass.value))
  }
  
  // Filtro por carga
  if (filterCharge.value !== 'all') {
    filtered = filtered.filter(m => getPolarity(m) === filterCharge.value)
  }
  
  return filtered
})

// Agrupar moléculas filtradas por massa
const filteredGroupedMolecules = computed(() => {
  const groups = {}
  
  filteredMolecules.value.forEach(mol => {
    const mass = mol.particles.length
    const label = `Massa ${mass}`
    
    if (!groups[label]) {
      groups[label] = []
    }
    
    groups[label].push({
      ...mol,
      formula: calculateMolecularFormula(mol)
    })
  })
  
  return groups
})

const formula = computed(() => {
  if (!selectedMolecule.value) return ''
  return calculateMolecularFormula(selectedMolecule.value)
})

function handleSelection() {
  if (!selectedId.value) {
    selectedMolecule.value = null
    emit('update:modelValue', null)
    return
  }
  
  const molecule = props.availableMolecules.find(m => m.id === selectedId.value)
  selectedMolecule.value = molecule
  emit('update:modelValue', molecule)
}

// Watch para mudanças externas no modelValue
watch(() => props.modelValue, (newValue) => {
  if (!newValue) {
    selectedId.value = ''
    selectedMolecule.value = null
  } else if (newValue.id !== selectedId.value) {
    selectedId.value = newValue.id
    selectedMolecule.value = newValue
  }
})
</script>

<style scoped>
.molecule-selector {
  padding: 1.5rem;
  background-color: #2a2a2a;
  border-radius: 12px;
  min-width: 350px;
}

h3 {
  margin: 0 0 1rem 0;
  color: #fff;
  font-size: 1.2rem;
}

.selector-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.molecule-select {
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 2px solid #444;
  background-color: #1a1a1a;
  color: #fff;
  cursor: pointer;
  transition: border-color 0.2s;
}

.molecule-select:hover {
  border-color: #646cff;
}

.molecule-select:focus {
  outline: none;
  border-color: #646cff;
}

.selected-info {
  padding: 1rem;
  background-color: #1a1a1a;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #aaa;
  font-size: 0.9rem;
}

.value {
  color: #fff;
  font-weight: 600;
  font-size: 1.1rem;
}

.molecule-preview {
  margin-top: 0.5rem;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #444;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.filter-group label {
  color: #aaa;
  font-size: 0.85rem;
  font-weight: 500;
}

.filter-select {
  padding: 0.5rem;
  font-size: 0.9rem;
  border-radius: 6px;
  border: 2px solid #444;
  background-color: #1a1a1a;
  color: #fff;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-select:hover {
  border-color: #646cff;
}

.filter-select:focus {
  outline: none;
  border-color: #646cff;
}
</style>

