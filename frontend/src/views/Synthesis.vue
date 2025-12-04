<template>
  <div class="synthesis">
    <header class="synthesis-header">
      <button class="back-btn" @click="voltarHome">
        ← Voltar
      </button>
      <h1>⚗️ Laboratório de Síntese</h1>
      <div class="stats">
        <span>💰 ${{ money }}</span>
        <span>🧪 {{ knownMolecules.length }} conhecidas</span>
      </div>
    </header>

    <div class="synthesis-content">
      <!-- Seleção de Moléculas -->
      <div class="selection-panel">
        <MoleculeSelector
          title="Molécula A"
          :available-molecules="knownMolecules"
          v-model="moleculeA"
        />
        
        <div class="plus-icon">
          <span>+</span>
        </div>
        
        <MoleculeSelector
          title="Molécula B"
          :available-molecules="knownMolecules"
          v-model="moleculeB"
        />
      </div>

      <!-- Botão de Síntese -->
      <div class="action-panel">
        <button 
          class="synthesize-btn"
          :disabled="!canSynthesize || synthesizing"
          @click="performSynthesis"
        >
          <span v-if="synthesizing">⏳ Sintetizando...</span>
          <span v-else>🧪 Sintetizar</span>
        </button>
      </div>

      <!-- Resultado -->
      <div v-if="lastResult" class="result-panel">
        <div v-if="lastResult.success" class="result-success">
          <h2>✅ Síntese Bem-Sucedida!</h2>
          
          <!-- Resultado Múltiplo -->
          <div v-if="lastResult.multiple" class="multiple-results">
            <div class="multiple-header">
              <p>🔬 A síntese produziu <strong>{{ lastResult.details.molecules_count }} moléculas separadas</strong></p>
            </div>
            
            <div class="molecules-grid">
              <div 
                v-for="(molecule, index) in lastResult.result" 
                :key="index"
                class="result-molecule"
              >
                <div class="result-header">
                  <span class="molecule-number">Molécula {{ index + 1 }}</span>
                  <span class="formula">{{ getFormula(molecule) }}</span>
                  <span v-if="isNewDiscoveryMultiple(molecule)" class="badge new">✨ Nova!</span>
                  <span v-else class="badge known">Conhecida</span>
                </div>
                
                <!-- Visualização da molécula -->
                <div class="result-visualization">
                  <MoleculeViewer :molecule="molecule" />
                </div>
                
                <div class="result-details">
                  <p><strong>Massa:</strong> {{ molecule.particles.length }}</p>
                  <p><strong>Carga:</strong> {{ getMoleculeCharge(molecule) }}</p>
                  
                  <ObservableProperties v-if="molecule.observableProperties" :properties="molecule.observableProperties" />
                </div>

                <!-- Ações para nova descoberta -->
                <div v-if="isNewDiscoveryMultiple(molecule) && !multipleSaved[index]" class="result-actions">
                  <div class="name-input-group">
                    <input 
                      v-model="multipleNames[index]" 
                      type="text" 
                      placeholder="Nome (opcional)..."
                      class="name-input"
                      @keyup.enter="saveMultipleDiscovery(molecule, index)"
                    />
                  </div>
                  <button class="btn-primary" @click="saveMultipleDiscovery(molecule, index)">
                    💾 Salvar
                  </button>
                </div>

                <!-- Mensagem de salvo -->
                <div v-if="multipleSaved[index]" class="saved-message">
                  ✅ Salva!
                </div>
              </div>
            </div>
            
            <div class="result-details">
              <p><strong>Partículas iniciais:</strong> {{ lastResult.details.initial_count }}</p>
              <p><strong>Pares anulados:</strong> {{ lastResult.details.annihilated_pairs }}</p>
              <p><strong>Partículas finais:</strong> {{ lastResult.details.remaining_particles }}</p>
            </div>
          </div>
          
          <!-- Resultado Único -->
          <div v-else class="result-molecule">
            <div class="result-header">
              <span class="formula">{{ resultFormula }}</span>
              <span v-if="isNewDiscovery" class="badge new">✨ Nova Descoberta!</span>
              <span v-else class="badge known">Já conhecida</span>
            </div>
            
            <!-- Visualização da molécula resultante -->
            <div class="result-visualization">
              <div ref="resultCanvas" class="result-canvas"></div>
            </div>
            
            <div class="result-details">
              <p><strong>Massa:</strong> {{ lastResult.result.particles.length }}</p>
              <p><strong>Partículas iniciais:</strong> {{ lastResult.details.initial_count }}</p>
              <p><strong>Pares anulados:</strong> {{ lastResult.details.annihilated_pairs }}</p>
              <p><strong>Partículas finais:</strong> {{ lastResult.details.remaining_particles }}</p>
              
              <ObservableProperties v-if="lastResult.result.observableProperties" :properties="lastResult.result.observableProperties" />
            </div>

            <!-- Ações para nova descoberta -->
            <div v-if="isNewDiscovery && !discoverySaved" class="result-actions">
              <div class="name-input-group">
                <input 
                  v-model="discoveryName" 
                  type="text" 
                  placeholder="Nome da descoberta (opcional)..."
                  class="name-input"
                  @keyup.enter="saveDiscovery"
                />
              </div>
              <button class="btn-primary" @click="saveDiscovery">
                💾 Salvar na Biblioteca
              </button>
            </div>

            <!-- Mensagem de descoberta salva -->
            <div v-if="discoverySaved" class="saved-message">
              ✅ Descoberta salva com sucesso!
            </div>
          </div>
        </div>

        <div v-else class="result-failure">
          <h2>❌ Síntese Falhou</h2>
          
          <div class="failure-details">
            <p v-if="lastResult.details.reason === 'complete_annihilation'">
              <strong>Motivo:</strong> Todas as partículas foram anuladas.
            </p>
            <p v-else-if="lastResult.details.reason === 'no_reaction'">
              <strong>Motivo:</strong> {{ lastResult.details.message }}
            </p>
            <p v-else-if="lastResult.details.reason === 'cannot_rebond'">
              <strong>Motivo:</strong> Não foi possível estabilizar as partículas restantes.
            </p>
            <p v-else>
              <strong>Motivo:</strong> Síntese inválida.
            </p>
            
            <div class="failure-stats">
              <p>Partículas iniciais: {{ lastResult.details.initial_count }}</p>
              <p v-if="lastResult.details.annihilated_pairs !== undefined">
                Pares anulados: {{ lastResult.details.annihilated_pairs }}
              </p>
              <p v-if="lastResult.details.remaining_particles">
                Partículas restantes: {{ lastResult.details.remaining_particles }}
              </p>
            </div>

            <div class="tip">
              💡 <strong>Dica:</strong> Moléculas precisam ter partículas com polaridades opostas para reagir!
            </div>
          </div>
        </div>
      </div>

      <!-- Histórico -->
      <div class="history-panel">
        <h3>📜 Histórico Recente</h3>
        <div v-if="history.length === 0" class="empty-history">
          Nenhuma síntese realizada ainda
        </div>
        <div v-else class="history-list">
          <div 
            v-for="(entry, idx) in history" 
            :key="idx"
            class="history-item"
            :class="{ success: entry.success }"
          >
            <span class="formulas">
              {{ getFormula(entry.molA) }} + {{ getFormula(entry.molB) }}
            </span>
            <span class="arrow">→</span>
            <span v-if="entry.success" class="result-formula">
              {{ entry.resultFormula }}
            </span>
            <span v-else class="failed">✗</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import MoleculeSelector from '../components/MoleculeSelector.vue'
import MoleculeViewer from '../components/MoleculeViewer.vue'
import ObservableProperties from '../components/ObservableProperties.vue'
import { 
  getAllMolecules, 
  getAllDiscoveries,
  saveDiscovery as saveDiscoveryAPI,
  calculateMolecularFormula,
  synthesizeMolecules,
  getCurrentSave,
  getObservableProperties
} from '../services/api.js'
import { moleculeExistsInList } from '../utils/moleculeComparison.js'
import * as PIXI from 'pixi.js'

const router = useRouter()

const moleculeA = ref(null)
const moleculeB = ref(null)
const knownMolecules = ref([])
const synthesizing = ref(false)
const lastResult = ref(null)
const history = ref([])
const resultCanvas = ref(null)
const discoveryName = ref('')
const discoverySaved = ref(false)
const money = ref(0)

// Para resultados múltiplos
const multipleNames = ref({})
const multipleSaved = ref({})

let resultPixiApp = null

const canSynthesize = computed(() => {
  return moleculeA.value && moleculeB.value && !synthesizing.value
})

const resultFormula = computed(() => {
  if (!lastResult.value || !lastResult.value.success || lastResult.value.multiple) return ''
  return calculateMolecularFormula(lastResult.value.result)
})

const isNewDiscovery = computed(() => {
  if (!lastResult.value || !lastResult.value.success || lastResult.value.multiple) return false
  
  // Verificar se a molécula resultante já existe estruturalmente
  // (não apenas pela fórmula, mas pela estrutura completa de ligações)
  return !moleculeExistsInList(lastResult.value.result, knownMolecules.value)
})

const isNewDiscoveryMultiple = (molecule) => {
  return !moleculeExistsInList(molecule, knownMolecules.value)
}

const getMoleculeCharge = (molecule) => {
  const charge = molecule.particles.reduce((sum, p) => {
    return sum + (p.polarity === '+' ? 1 : -1)
  }, 0)
  
  if (charge > 0) return `+${charge} (positiva)`
  if (charge < 0) return `${charge} (negativa)`
  return '0 (neutra)'
}

const voltarHome = () => {
  router.push('/')
}

const getFormula = (molecule) => {
  if (!molecule) return '?'
  return calculateMolecularFormula(molecule)
}

// Carregar moléculas conhecidas
async function loadKnownMolecules() {
  try {
    const response = await getAllMolecules()
    if (response.success) {
      knownMolecules.value = response.data
      
      // Carregar descobertas do backend
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

async function performSynthesis() {
  if (!canSynthesize.value) return
  
  synthesizing.value = true
  discoverySaved.value = false
  discoveryName.value = ''
  multipleNames.value = {}
  multipleSaved.value = {}
  
  try {
    const result = await synthesizeMolecules(moleculeA.value.id, moleculeB.value.id)
    
    // Carregar propriedades observáveis se a síntese foi bem-sucedida
    if (result.success) {
      if (result.multiple && Array.isArray(result.result)) {
        // Carregar propriedades para cada molécula em resultado múltiplo
        const moleculesWithProps = await Promise.all(
          result.result.map(async (mol) => {
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
        result.result = moleculesWithProps
      } else if (result.result) {
        // Carregar propriedades para resultado único
        try {
          const propsResponse = await getObservableProperties(result.result)
          if (propsResponse.success) {
            result.result.observableProperties = propsResponse.data
          }
        } catch (err) {
          console.warn('Erro ao carregar propriedades observáveis:', err)
        }
      }
    }
    
    lastResult.value = result
    
    // Adicionar ao histórico
    const resultFormula = result.success && !result.multiple 
      ? calculateMolecularFormula(result.result)
      : result.success && result.multiple 
        ? `${result.details.molecules_count} moléculas`
        : null
    
    history.value.unshift({
      molA: moleculeA.value,
      molB: moleculeB.value,
      success: result.success,
      resultFormula
    })
    
    // Limitar histórico a 10 itens
    if (history.value.length > 10) {
      history.value = history.value.slice(0, 10)
    }
    
    // Se sucesso e molécula única, renderizar molécula resultado
    if (result.success && !result.multiple) {
      await renderResultMolecule(result.result)
    }
  } catch (error) {
    console.error('Erro ao sintetizar:', error)
  } finally {
    synthesizing.value = false
  }
}

async function renderResultMolecule(molecule) {
  // Aguardar próximo tick para garantir que o canvas existe
  await new Promise(resolve => setTimeout(resolve, 100))
  
  if (!resultCanvas.value) return
  
  // Destruir app anterior se existir
  if (resultPixiApp) {
    resultPixiApp.destroy(true)
    resultPixiApp = null
  }
  
  // Criar novo canvas
  const canvas = document.createElement('canvas')
  resultCanvas.value.innerHTML = ''
  resultCanvas.value.appendChild(canvas)
  
  const app = new PIXI.Application({
    view: canvas,
    width: 500,
    height: 400,
    backgroundColor: 0x1a1a1a,
    antialias: true
  })
  
  resultPixiApp = app
  
  // Desenhar molécula (código similar ao MoleculeViewer)
  const stage = app.stage
  const particles = molecule.particles || []
  const bonds = molecule.bonds || []
  
  if (particles.length === 0) return
  
  // Fator de espaçamento visual (transforma coordenadas lógicas em visuais)
  const spacingFactor = 2
  
  // Calcular escala
  const positions = particles.map(p => ({ 
    x: (p.x || 0) * spacingFactor, 
    y: (p.y || 0) * spacingFactor 
  }))
  const minX = Math.min(...positions.map(p => p.x))
  const maxX = Math.max(...positions.map(p => p.x))
  const minY = Math.min(...positions.map(p => p.y))
  const maxY = Math.max(...positions.map(p => p.y))
  
  const molWidth = maxX - minX || 1
  const molHeight = maxY - minY || 1
  
  const scaleX = (500 * 0.7) / molWidth
  const scaleY = (400 * 0.7) / molHeight
  const scale = Math.min(scaleX, scaleY, 40)
  
  const offsetX = 250 - ((minX + maxX) / 2) * scale
  const offsetY = 200 - ((minY + maxY) / 2) * scale
  
  // Desenhar bonds
  bonds.forEach(bond => {
    const pFrom = particles.find(p => p.id === bond.from)
    const pTo = particles.find(p => p.id === bond.to)
    
    if (!pFrom || !pTo) return
    
    const x1 = (pFrom.x || 0) * spacingFactor * scale + offsetX
    const y1 = (pFrom.y || 0) * spacingFactor * scale + offsetY
    const x2 = (pTo.x || 0) * spacingFactor * scale + offsetX
    const y2 = (pTo.y || 0) * spacingFactor * scale + offsetY
    
    const multiplicity = bond.multiplicity || 1
    
    for (let i = 0; i < multiplicity; i++) {
      const graphics = new PIXI.Graphics()
      
      const dx = x2 - x1
      const dy = y2 - y1
      const length = Math.sqrt(dx * dx + dy * dy)
      const perpX = -dy / length
      const perpY = dx / length
      
      const offset = (i - (multiplicity - 1) / 2) * 5
      
      graphics.lineStyle(2, 0xcccccc, 1)
      graphics.moveTo(x1 + perpX * offset, y1 + perpY * offset)
      graphics.lineTo(x2 + perpX * offset, y2 + perpY * offset)
      
      stage.addChild(graphics)
    }
  })
  
  // Desenhar partículas
  particles.forEach(particle => {
    const x = (particle.x || 0) * spacingFactor * scale + offsetX
    const y = (particle.y || 0) * spacingFactor * scale + offsetY
    
    const graphics = new PIXI.Graphics()
    
    // Cor baseada na polaridade
    const color = particle.polarity === '+' ? 0xef4444 : 0x3b82f6 // vermelho (+) ou azul (-)
    let radius = 20
    
    switch (particle.type) {
      case 'circle':
        radius = 18
        graphics.beginFill(color)
        graphics.drawCircle(x, y, radius)
        graphics.endFill()
        break
      case 'square':
        radius = 20
        graphics.beginFill(color)
        graphics.drawRect(x - radius, y - radius, radius * 2, radius * 2)
        graphics.endFill()
        break
      case 'triangle':
        radius = 22
        graphics.beginFill(color)
        graphics.moveTo(x, y - radius)
        graphics.lineTo(x + radius, y + radius)
        graphics.lineTo(x - radius, y + radius)
        graphics.lineTo(x, y - radius)
        graphics.endFill()
        break
      case 'pentagon':
        radius = 24
        graphics.beginFill(color)
        const sides = 5
        for (let i = 0; i < sides; i++) {
          const angle = (i / sides) * Math.PI * 2 - Math.PI / 2
          const px = x + Math.cos(angle) * radius
          const py = y + Math.sin(angle) * radius
          if (i === 0) {
            graphics.moveTo(px, py)
          } else {
            graphics.lineTo(px, py)
          }
        }
        graphics.closePath()
        graphics.endFill()
        break
    }
    
    const text = new PIXI.Text(particle.polarity, {
      fontSize: 16,
      fill: 0xffffff,
      fontWeight: 'bold'
    })
    text.anchor.set(0.5)
    text.x = x
    text.y = y
    
    stage.addChild(graphics)
    stage.addChild(text)
  })
}

async function saveMultipleDiscovery(molecule, index) {
  try {
    const formula = calculateMolecularFormula(molecule)
    const name = multipleNames.value[index]?.trim() || null
    
    const response = await saveDiscoveryAPI(molecule, formula, name)
    
    if (response.success) {
      multipleSaved.value = { ...multipleSaved.value, [index]: true }
      
      // Recarregar moléculas conhecidas
      await loadKnownMolecules()
      await loadPlayerData()
    }
  } catch (error) {
    console.error('Erro ao salvar descoberta:', error)
    alert('Erro ao salvar descoberta!')
  }
}

async function saveDiscovery() {
  if (!lastResult.value || !lastResult.value.success || !isNewDiscovery.value) return
  
  try {
    const response = await saveDiscoveryAPI(
      lastResult.value.result,
      resultFormula.value,
      discoveryName.value.trim() || null
    )
    
    if (response.success) {
      discoverySaved.value = true
      
      // Recarregar moléculas conhecidas
      await loadKnownMolecules()
      await loadPlayerData()
    }
  } catch (error) {
    console.error('Erro ao salvar descoberta:', error)
    alert('Erro ao salvar descoberta!')
  }
}

onMounted(async () => {
  await loadKnownMolecules()
  await loadPlayerData()
})

onUnmounted(() => {
  if (resultPixiApp) {
    resultPixiApp.destroy(true)
  }
})
</script>

<style scoped>
.synthesis {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding-bottom: 2rem;
}

.synthesis-header {
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

.synthesis-header h1 {
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

.synthesis-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.selection-panel {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 2rem;
  align-items: start;
  margin-bottom: 2rem;
}

.plus-icon {
  font-size: 3rem;
  color: #646cff;
  font-weight: bold;
  align-self: center;
  margin-top: 2rem;
}

.action-panel {
  text-align: center;
  margin-bottom: 2rem;
}

.synthesize-btn {
  padding: 1rem 3rem;
  font-size: 1.3rem;
  background-color: #646cff;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s, transform 0.2s;
}

.synthesize-btn:hover:not(:disabled) {
  background-color: #5458e8;
  transform: scale(1.05);
}

.synthesize-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.result-panel {
  margin-bottom: 3rem;
}

.result-success,
.result-failure {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
}

.result-success h2 {
  color: #10b981;
  margin-bottom: 1.5rem;
  text-align: center;
}

.result-failure h2 {
  color: #ef4444;
  margin-bottom: 1.5rem;
  text-align: center;
}

.result-molecule {
  max-width: 600px;
  margin: 0 auto;
}

.multiple-results {
  max-width: 1000px;
  margin: 0 auto;
}

.multiple-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  border: 2px solid #3b82f6;
}

.multiple-header p {
  color: #fff;
  font-size: 1.1rem;
  margin: 0;
}

.molecules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.molecules-grid .result-molecule {
  max-width: 100%;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 12px;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.molecule-number {
  font-size: 0.9rem;
  color: #a0a0a0;
  font-weight: 600;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.result-header .formula {
  font-size: 1.5rem;
  color: #fff;
  font-weight: 700;
}

.badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.badge.new {
  background-color: #f59e0b;
  color: #1a1a1a;
}

.badge.known {
  background-color: #3b82f6;
  color: white;
}

.result-visualization {
  background-color: #1a1a1a;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.result-canvas {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.result-details {
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.result-details p {
  color: #ccc;
  margin-bottom: 0.5rem;
}

.result-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.name-input-group {
  display: flex;
  gap: 1rem;
}

.name-input {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  border: 2px solid #444;
  background-color: #1a1a1a;
  color: #fff;
  font-size: 1rem;
}

.name-input:focus {
  outline: none;
  border-color: #646cff;
}

.btn-primary {
  padding: 0.75rem 2rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #059669;
}

.saved-message {
  text-align: center;
  padding: 1rem;
  background-color: #10b981;
  color: white;
  border-radius: 8px;
  font-weight: 600;
}

.failure-details {
  max-width: 600px;
  margin: 0 auto;
}

.failure-details p {
  color: #ccc;
  margin-bottom: 1rem;
}

.failure-stats {
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.failure-stats p {
  margin-bottom: 0.5rem;
}

.tip {
  background-color: #1a1a1a;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #f59e0b;
}

.history-panel {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
}

.history-panel h3 {
  color: #fff;
  margin-bottom: 1.5rem;
}

.empty-history {
  text-align: center;
  color: #aaa;
  padding: 2rem;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #1a1a1a;
  border-radius: 8px;
  border-left: 4px solid #ef4444;
}

.history-item.success {
  border-left-color: #10b981;
}

.formulas {
  color: #ccc;
}

.arrow {
  color: #646cff;
  font-size: 1.2rem;
}

.result-formula {
  color: #10b981;
  font-weight: 600;
}

.failed {
  color: #ef4444;
  font-size: 1.5rem;
}
</style>

