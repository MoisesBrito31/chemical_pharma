<template>
  <div class="auto-synthesis">
    <header class="auto-synthesis-header">
      <button class="back-btn" @click="voltarHome">
        ← Voltar
      </button>
      <h1>⚗️ Laboratório de Síntese Automático</h1>
      <div class="stats">
        <span>💰 ${{ money }}</span>
        <span>🧪 {{ knownMolecules.length }} conhecidas</span>
      </div>
    </header>

    <div class="auto-synthesis-content">
      <!-- Configuração -->
      <div class="config-panel">
        <div class="config-row">
          <div class="config-section">
            <h2>🔬 Molécula Base</h2>
            <MoleculeSelector
              title="Molécula A (Base)"
              :available-molecules="knownMolecules"
              v-model="moleculeA"
            />
          </div>

          <div class="config-section">
            <h2>📦 Grupo de Moléculas</h2>
          <div class="group-selector">
            <div class="filter-options">
              <label>
                <input 
                  type="radio" 
                  v-model="groupMode" 
                  value="mass"
                  @change="clearGroupSelection"
                />
                Filtrar por Massa
              </label>
              <label>
                <input 
                  type="radio" 
                  v-model="groupMode" 
                  value="specific"
                  @change="clearGroupSelection"
                />
                Selecionar Moléculas Específicas
              </label>
            </div>

            <!-- Filtro por Massa -->
            <div v-if="groupMode === 'mass'" class="mass-filter">
              <label for="target-mass">Massa das Moléculas B:</label>
              <select 
                id="target-mass" 
                v-model.number="filterMass"
                class="form-control"
              >
                <option :value="null">Selecione uma massa...</option>
                <option v-for="mass in availableMasses" :key="mass" :value="mass">
                  Massa {{ mass }}
                </option>
              </select>
              <p v-if="filterMass" class="info-text">
                Encontradas: {{ getMoleculesByMass(filterMass).length }} molécula(s)
              </p>
            </div>

            <!-- Seleção Específica -->
            <div v-if="groupMode === 'specific'" class="specific-selector">
              <label>Selecione as moléculas:</label>
              <div class="molecules-checklist">
                <label 
                  v-for="mol in knownMolecules" 
                  :key="mol.id"
                  class="checkbox-label"
                >
                  <input 
                    type="checkbox" 
                    :value="mol.id"
                    v-model="selectedMoleculeIds"
                  />
                  <span>{{ mol.name || mol.formula || mol.id }} (Massa: {{ mol.particles?.length || 0 }})</span>
                </label>
              </div>
              <p class="info-text">
                Selecionadas: {{ selectedMoleculeIds.length }} molécula(s)
              </p>
            </div>
          </div>
        </div>
        </div>

        <!-- Botão de Execução -->
        <div class="action-panel">
          <button 
            class="execute-btn"
            :disabled="!canExecute || executing"
            @click="executeAutoSynthesis"
          >
            <span v-if="executing">⏳ Executando Sínteses...</span>
            <span v-else>🚀 Executar Sínteses Automáticas</span>
          </button>
        </div>
      </div>

      <!-- Resultados -->
      <div v-if="results && !executing" class="results-panel">
        <div class="results-header">
          <h2>📊 Resultados das Sínteses</h2>
          <div class="results-stats">
            <span class="stat-badge total">
              Total: {{ results.total_tested }}
            </span>
            <span class="stat-badge success">
              Sucesso: {{ results.total_successful }}
            </span>
            <span class="stat-badge failed">
              Falhas: {{ results.total_tested - results.total_successful }}
            </span>
            <span class="stat-badge unknown">
              Desconhecidas: {{ countUnknownMolecules }}
            </span>
            <span class="stat-badge known">
              Conhecidas: {{ countKnownMolecules }}
            </span>
          </div>
        </div>

        <div class="results-list">
          <div 
            v-for="(result, index) in results.results" 
            :key="index"
            class="result-item"
            :class="{
              'success': result.result.success,
              'failure': !result.result.success
            }"
          >
            <div class="result-header">
              <div class="result-formula">
                <span class="base-formula">{{ results.molecule_a.formula }}</span>
                <span class="plus">+</span>
                <span class="target-formula">{{ result.molecule_b.formula }}</span>
                <span class="arrow">→</span>
                <span 
                  v-if="result.result.success && !result.result.multiple"
                  class="result-formula-text"
                >
                  {{ getResultFormula(result.result.result) }}
                </span>
                <span v-else-if="result.result.success && result.result.multiple" class="result-formula-text">
                  {{ result.result.details.molecules_count }} moléculas
                </span>
                <span v-else class="failed-text">✗ Falhou</span>
              </div>
              
              <span 
                v-if="result.result.success && result.status"
                :class="['status-badge', getStatusClass(result.status)]"
              >
                {{ result.status }}
              </span>
            </div>

            <!-- Visualização das moléculas: A, B e Resultante -->
            <div v-if="result.result.success && !result.result.multiple" class="molecules-comparison">
              <div class="molecule-item">
                <h4 class="molecule-label">Molécula A (Base)</h4>
                <div class="molecule-view-wrapper">
                  <MoleculeViewer 
                    v-if="results.molecule_a.molecule" 
                    :molecule="results.molecule_a.molecule" 
                    :size="200" 
                  />
                  <div v-else class="molecule-placeholder">
                    <span>{{ results.molecule_a.formula }}</span>
                  </div>
                </div>
                <p class="molecule-formula">{{ results.molecule_a.formula }}</p>
              </div>
              
              <div class="plus-arrow">
                <span>+</span>
              </div>
              
              <div class="molecule-item">
                <h4 class="molecule-label">Molécula B</h4>
                <div class="molecule-view-wrapper">
                  <MoleculeViewer 
                    v-if="result.molecule_b.molecule" 
                    :molecule="result.molecule_b.molecule" 
                    :size="200" 
                  />
                  <div v-else class="molecule-placeholder">
                    <span>{{ result.molecule_b.formula }}</span>
                  </div>
                </div>
                <p class="molecule-formula">{{ result.molecule_b.formula }}</p>
              </div>
              
              <div class="equals-arrow">
                <span>→</span>
              </div>
              
                <div class="molecule-item">
                  <h4 class="molecule-label">Resultado</h4>
                  <div class="molecule-view-wrapper">
                    <MoleculeViewer :molecule="result.result.result" :size="200" />
                  </div>
                  <p class="molecule-formula">{{ getResultFormula(result.result.result) }}</p>
                  
                  <div class="observable-props-wrapper">
                    <ObservableProperties v-if="result.result.result.observableProperties" :properties="result.result.result.observableProperties" />
                  </div>
                </div>
            </div>

            <!-- Resultados múltiplos -->
            <div v-if="result.result.success && result.result.multiple" class="multiple-results-view">
              <!-- Mostrar moléculas A e B que participaram -->
              <div class="molecules-comparison">
                <div class="molecule-item">
                  <h4 class="molecule-label">Molécula A (Base)</h4>
                  <div class="molecule-view-wrapper">
                    <MoleculeViewer 
                      v-if="results.molecule_a.molecule" 
                      :molecule="results.molecule_a.molecule" 
                      :size="200" 
                    />
                    <div v-else class="molecule-placeholder">
                      <span>{{ results.molecule_a.formula }}</span>
                    </div>
                  </div>
                  <p class="molecule-formula">{{ results.molecule_a.formula }}</p>
                </div>
                
                <div class="plus-arrow">
                  <span>+</span>
                </div>
                
                <div class="molecule-item">
                  <h4 class="molecule-label">Molécula B</h4>
                  <div class="molecule-view-wrapper">
                    <MoleculeViewer 
                      v-if="result.molecule_b.molecule" 
                      :molecule="result.molecule_b.molecule" 
                      :size="200" 
                    />
                    <div v-else class="molecule-placeholder">
                      <span>{{ result.molecule_b.formula }}</span>
                    </div>
                  </div>
                  <p class="molecule-formula">{{ result.molecule_b.formula }}</p>
                </div>
                
                <div class="equals-arrow">
                  <span>→</span>
                </div>
                
                <div class="molecule-item">
                  <h4 class="molecule-label">Resultado ({{ result.result.details.molecules_count }} moléculas)</h4>
                  <div class="molecule-view-wrapper multiple-indicator">
                    <span class="multiple-count-badge">{{ result.result.details.molecules_count }}</span>
                  </div>
                </div>
              </div>
              
              <h4 class="multiple-results-title">Moléculas Resultantes:</h4>
              
              <div class="multiple-molecules-grid">
                <div 
                  v-for="(mol, molIndex) in result.result.result" 
                  :key="molIndex"
                  class="multiple-molecule-item"
                >
                  <MoleculeViewer :molecule="mol" :size="150" />
                  <div class="multiple-molecule-info">
                    <span>{{ getResultFormula(mol) }}</span>
                    
                    <ObservableProperties v-if="mol.observableProperties" :properties="mol.observableProperties" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Detalhes do resultado -->
            <div class="result-details">
              <div v-if="result.result.success" class="success-details">
                <p><strong>Partículas iniciais:</strong> {{ result.result.details.initial_count }}</p>
                <p><strong>Pares anulados:</strong> {{ result.result.details.annihilated_pairs }}</p>
                <p><strong>Partículas finais:</strong> {{ result.result.details.remaining_particles }}</p>
              </div>
              <div v-else class="failure-details">
                <p><strong>Motivo:</strong> {{ getFailureReason(result.result) }}</p>
              </div>
            </div>

            <!-- Ações para salvar descobertas -->
            <div 
              v-if="result.result.success && result.status === 'Desconhecida' && !result.result.multiple"
              class="result-actions"
            >
              <div class="save-actions">
                <input 
                  v-model="discoveryNames[index]"
                  type="text"
                  placeholder="Nome (opcional)..."
                  class="name-input"
                  @keyup.enter="saveDiscovery(result.result.result, index)"
                />
                <button 
                  class="btn-save"
                  @click="saveDiscovery(result.result.result, index)"
                  :disabled="savingIndices.includes(index)"
                >
                  <span v-if="savingIndices.includes(index)">⏳</span>
                  <span v-else>💾 Salvar</span>
                </button>
              </div>
              <div v-if="savedIndices.includes(index)" class="saved-message">
                ✅ Salva!
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="executing" class="loading-state">
        <div class="spinner"></div>
        <p>Executando {{ currentProgress || 0 }} / {{ totalProgress || 0 }} sínteses...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MoleculeSelector from '../components/MoleculeSelector.vue'
import MoleculeViewer from '../components/MoleculeViewer.vue'
import ObservableProperties from '../components/ObservableProperties.vue'
import { 
  getAllMolecules, 
  getAllDiscoveries,
  saveDiscovery as saveDiscoveryAPI,
  calculateMolecularFormula,
  getCurrentSave,
  getObservableProperties
} from '../services/api.js'

const router = useRouter()

const moleculeA = ref(null)
const knownMolecules = ref([])
const groupMode = ref('mass')
const filterMass = ref(null)
const selectedMoleculeIds = ref([])
const executing = ref(false)
const results = ref(null)
const money = ref(0)
const discoveryNames = ref({})
const savingIndices = ref([])
const savedIndices = ref([])
const currentProgress = ref(0)
const totalProgress = ref(0)

const availableMasses = computed(() => {
  const masses = new Set()
  knownMolecules.value.forEach(mol => {
    const mass = mol.particles?.length || 0
    if (mass > 0) masses.add(mass)
  })
  return Array.from(masses).sort((a, b) => a - b)
})

const canExecute = computed(() => {
  if (!moleculeA.value) return false
  
  if (groupMode.value === 'mass') {
    return filterMass.value !== null
  } else {
    return selectedMoleculeIds.value.length > 0
  }
})

const getMoleculesByMass = (mass) => {
  return knownMolecules.value.filter(mol => (mol.particles?.length || 0) === mass)
}

const getResultFormula = (molecule) => {
  if (!molecule) return '?'
  return calculateMolecularFormula(molecule)
}

const getStatusClass = (status) => {
  const classes = {
    'Base': 'base',
    'Descoberta': 'discovered',
    'Desconhecida': 'unknown'
  }
  return classes[status] || 'unknown'
}

const countUnknownMolecules = computed(() => {
  if (!results.value || !results.value.results) return 0
  
  return results.value.results.filter(r => {
    return r.result.success && r.status === 'Desconhecida'
  }).length
})

const countKnownMolecules = computed(() => {
  if (!results.value || !results.value.results) return 0
  
  return results.value.results.filter(r => {
    return r.result.success && (r.status === 'Base' || r.status === 'Descoberta')
  }).length
})

const getFailureReason = (result) => {
  if (!result.details) return 'Erro desconhecido'
  
  const reason = result.details.reason
  if (reason === 'complete_annihilation') return 'Todas as partículas foram anuladas'
  if (reason === 'no_reaction') return result.details.message || 'Sem reação'
  if (reason === 'cannot_rebond') return 'Não foi possível estabilizar as partículas'
  return 'Erro na síntese'
}

const clearGroupSelection = () => {
  filterMass.value = null
  selectedMoleculeIds.value = []
}

const executeAutoSynthesis = async () => {
  if (!canExecute.value) return
  
  executing.value = true
  results.value = null
  discoveryNames.value = {}
  savingIndices.value = []
  savedIndices.value = []
  currentProgress.value = 0
  
  try {
    const payload = {
      molecule_a_id: moleculeA.value.id
    }
    
    if (groupMode.value === 'mass') {
      payload.filter_mass = filterMass.value
    } else {
      payload.molecule_ids = selectedMoleculeIds.value
    }
    
    // Simular progresso
    const moleculesToTest = groupMode.value === 'mass' 
      ? getMoleculesByMass(filterMass.value).length
      : selectedMoleculeIds.value.length
    
    totalProgress.value = moleculesToTest
    
    const response = await fetch('http://localhost:5000/api/synthesis/auto', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    
    const data = await response.json()
    
    if (data.success) {
      // Carregar propriedades observáveis para cada resultado
      if (data.results && Array.isArray(data.results)) {
        const resultsWithProps = await Promise.all(
          data.results.map(async (result) => {
            if (result.result.success) {
              if (result.result.multiple && Array.isArray(result.result.result)) {
                // Resultado múltiplo: carregar propriedades para cada molécula
                const moleculesWithProps = await Promise.all(
                  result.result.result.map(async (mol) => {
                    try {
                      const propsResponse = await getObservableProperties(mol)
                      if (propsResponse.success) {
                        return { ...mol, observableProperties: propsResponse.data }
                      }
                    } catch (err) {
                      console.warn('Erro ao carregar propriedades observáveis:', err)
                    }
                    return mol
                  })
                )
                result.result.result = moleculesWithProps
              } else if (result.result.result) {
                // Resultado único: carregar propriedades
                try {
                  const propsResponse = await getObservableProperties(result.result.result)
                  if (propsResponse.success) {
                    result.result.result.observableProperties = propsResponse.data
                  }
                } catch (err) {
                  console.warn('Erro ao carregar propriedades observáveis:', err)
                }
              }
            }
            return result
          })
        )
        data.results = resultsWithProps
      }
      
      results.value = data
    } else {
      alert('Erro: ' + (data.error || 'Erro desconhecido'))
    }
  } catch (error) {
    console.error('Erro ao executar sínteses:', error)
    alert('Erro ao conectar com o servidor: ' + error.message)
  } finally {
    executing.value = false
    currentProgress.value = 0
    totalProgress.value = 0
  }
}

const saveDiscovery = async (molecule, index) => {
  if (savingIndices.value.includes(index)) return
  
  savingIndices.value.push(index)
  
  try {
    const formula = calculateMolecularFormula(molecule)
    const name = discoveryNames.value[index]?.trim() || null
    
    const response = await saveDiscoveryAPI(molecule, formula, name)
    
    if (response.success) {
      savedIndices.value.push(index)
      
      // Atualizar o status do resultado
      if (results.value && results.value.results[index]) {
        results.value.results[index].status = 'Descoberta'
      }
      
      // Recarregar moléculas conhecidas
      await loadKnownMolecules()
      await loadPlayerData()
    }
  } catch (error) {
    console.error('Erro ao salvar descoberta:', error)
  } finally {
    savingIndices.value = savingIndices.value.filter(i => i !== index)
  }
}

const voltarHome = () => {
  router.push('/')
}

async function loadKnownMolecules() {
  try {
    const response = await getAllMolecules()
    if (response.success) {
      knownMolecules.value = response.data
      
      // Carregar descobertas
      await loadDiscoveries()
    }
  } catch (error) {
    console.error('Erro ao carregar moléculas:', error)
  }
}

async function loadDiscoveries() {
  try {
    const response = await getAllDiscoveries()
    if (response.success) {
      const discoveries = response.data.map(disc => ({
        ...disc.molecule,
        id: disc.id,
        name: disc.name,
        formula: disc.formula
      }))
      knownMolecules.value = [...knownMolecules.value, ...discoveries]
    }
  } catch (error) {
    console.warn('Erro ao carregar descobertas:', error)
  }
}

async function loadPlayerData() {
  try {
    const response = await getCurrentSave()
    if (response.success) {
      money.value = response.data.money
    }
  } catch (error) {
    console.error('Erro ao carregar dados do jogador:', error)
  }
}

onMounted(async () => {
  await loadKnownMolecules()
  await loadPlayerData()
})
</script>

<style scoped>
.auto-synthesis {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding-bottom: 2rem;
}

.auto-synthesis-header {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  border-bottom: 2px solid #444;
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

.auto-synthesis-header h1 {
  flex: 1;
  color: #fff;
  margin: 0;
  font-size: 2rem;
}

.stats {
  display: flex;
  gap: 2rem;
  color: #aaa;
  font-size: 1.1rem;
}

.auto-synthesis-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 2rem;
}

.config-panel {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

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

.config-section {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.config-section h2 {
  color: #fff;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.group-selector {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1.5rem;
}

.filter-options {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.filter-options label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ccc;
  cursor: pointer;
}

.mass-filter {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mass-filter label {
  color: #ccc;
  font-weight: 600;
}

.form-control {
  padding: 0.75rem;
  border-radius: 8px;
  border: 2px solid #444;
  background-color: #1a1a1a;
  color: #fff;
  font-size: 1rem;
}

.info-text {
  color: #aaa;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.specific-selector {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.molecules-checklist {
  max-height: 300px;
  overflow-y: auto;
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ccc;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.checkbox-label:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.action-panel {
  text-align: center;
  margin-top: 2rem;
}

.execute-btn {
  padding: 1rem 3rem;
  font-size: 1.3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.execute-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.execute-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.results-panel {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.results-header h2 {
  color: #fff;
  margin: 0;
}

.results-stats {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.stat-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.stat-badge.total {
  background-color: #3b82f6;
  color: white;
}

.stat-badge.success {
  background-color: #10b981;
  color: white;
}

.stat-badge.failed {
  background-color: #ef4444;
  color: white;
}

.stat-badge.unknown {
  background-color: #f59e0b;
  color: white;
}

.stat-badge.known {
  background-color: #10b981;
  color: white;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.result-item {
  background-color: #1a1a1a;
  border-radius: 12px;
  padding: 1.5rem;
  border-left: 4px solid #666;
}

.result-item.success {
  border-left-color: #10b981;
}

.result-item.failure {
  border-left-color: #ef4444;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.result-formula {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.base-formula,
.target-formula,
.result-formula-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #fff;
}

.plus,
.arrow {
  color: #646cff;
  font-size: 1.2rem;
}

.failed-text {
  color: #ef4444;
  font-weight: 600;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
}

.status-badge.base {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.status-badge.discovered {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.status-badge.unknown {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.molecules-comparison {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 1.5rem 0;
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 2rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .molecules-comparison {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .plus-arrow,
  .equals-arrow {
    transform: rotate(90deg);
  }
}

.molecule-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 200px;
  max-width: 300px;
}

.molecule-label {
  color: #ccc;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  text-align: center;
}

.molecule-view-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
  width: 100%;
  min-height: 200px;
}

.molecule-formula {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  text-align: center;
}

.plus-arrow,
.equals-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #646cff;
  font-weight: bold;
  min-width: 50px;
}

.plus-arrow span {
  color: #646cff;
}

.equals-arrow span {
  color: #10b981;
}

.molecule-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #aaa;
  font-size: 1.2rem;
  font-weight: 600;
}

.multiple-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.multiple-count-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 2rem;
  font-weight: bold;
  padding: 1.5rem 2rem;
  border-radius: 50%;
  min-width: 100px;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.multiple-results-view {
  margin: 1.5rem 0;
}

.multiple-results-title {
  color: #fff;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 2rem 0 1rem 0;
  text-align: center;
}

.multiple-molecules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.multiple-molecule-item {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.multiple-molecule-info {
  color: #ccc;
  font-size: 0.9rem;
}

.result-details {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #444;
}

.result-details p {
  color: #ccc;
  margin-bottom: 0.5rem;
}

.result-actions {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #444;
}

.save-actions {
  display: flex;
  gap: 0.5rem;
}

.name-input {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  border: 2px solid #444;
  background-color: #1a1a1a;
  color: #fff;
  font-size: 0.95rem;
}

.name-input:focus {
  outline: none;
  border-color: #646cff;
}

.btn-save {
  padding: 0.75rem 1.5rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.btn-save:hover:not(:disabled) {
  background-color: #059669;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.saved-message {
  margin-top: 0.5rem;
  color: #10b981;
  font-weight: 600;
  text-align: center;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  background-color: #2a2a2a;
  border-radius: 12px;
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1rem;
  border: 4px solid #f0f0f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #ccc;
  font-size: 1.1rem;
}
</style>

