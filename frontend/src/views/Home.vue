<template>
  <div class="home">
    <!-- Header com info do jogador -->
    <header class="player-header">
      <div class="player-info">
        <h2>👤 {{ playerName }}</h2>
        <span class="money">💰 ${{ money }}</span>
      </div>
      <div class="header-actions">
        <button class="btn-secondary" @click="changePlayer">Trocar Jogador</button>
        <button class="btn-danger" @click="confirmDeleteSave">Apagar Save</button>
      </div>
    </header>
    
    <!-- Conteúdo principal -->
    <div class="content">
      <h1>⚗️ Chemical Pharma</h1>
      <p class="welcome">Bem-vindo ao laboratório!</p>
      
      <!-- Estatísticas -->
      <div class="stats-card">
        <h3>📊 Estatísticas</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-icon">🧪</span>
            <div class="stat-info">
              <span class="stat-value">{{ discoveriesCount }}</span>
              <span class="stat-label">Descobertas</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">⚗️</span>
            <div class="stat-info">
              <span class="stat-value">{{ synthesesCount }}</span>
              <span class="stat-label">Sínteses</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">💰</span>
            <div class="stat-info">
              <span class="stat-value">${{ money }}</span>
              <span class="stat-label">Dinheiro</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Menu principal -->
      <div class="menu-grid">
        <div class="menu-card" @click="goToLibrary">
          <div class="card-icon">📚</div>
          <h2>Biblioteca de Moléculas</h2>
          <p>Explore todas as moléculas conhecidas e descobertas</p>
        </div>
        
        <div class="menu-card" @click="goToSynthesis">
          <div class="card-icon">⚗️</div>
          <h2>Laboratório de Síntese</h2>
          <p>Combine moléculas para criar novas descobertas</p>
        </div>
        
        <div class="menu-card" @click="goToAutoSynthesis">
          <div class="card-icon">🔬</div>
          <h2>Síntese Automática</h2>
          <p>Teste múltiplas sínteses de uma vez com uma molécula base</p>
        </div>
        
        <div class="menu-card" @click="goToSimulation">
          <div class="card-icon">🧪</div>
          <h2>Simulação de Moléculas</h2>
          <p>Gere todas as moléculas possíveis com características específicas</p>
        </div>
        
        <div class="menu-card" @click="goToBuilder">
          <div class="card-icon">🔧</div>
          <h2>Montador de Moléculas</h2>
          <p>Teste e lapide algoritmos com moléculas customizadas</p>
        </div>
        
        <div class="menu-card disabled">
          <div class="card-icon">🎮</div>
          <h2>Modo Jogo</h2>
          <p>Em desenvolvimento...</p>
        </div>
      </div>
    </div>
    
    <!-- Modal de confirmação de delete -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDelete">
      <div class="modal" @click.stop>
        <h3>⚠️ Confirmar Exclusão do Save</h3>
        <p>Tem certeza que deseja apagar seu save?</p>
        <p class="warning">Todas as descobertas e progresso serão perdidos!</p>
        <div class="modal-actions">
          <button class="btn-secondary" @click="cancelDelete">Cancelar</button>
          <button class="btn-danger" @click="deleteSave">Confirmar Exclusão</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentSave, deleteSave as deleteSaveAPI } from '../services/api.js'

const router = useRouter()

const playerName = ref('')
const money = ref(0)
const discoveriesCount = ref(0)
const synthesesCount = ref(0)
const currentSaveId = ref(null)
const showDeleteConfirm = ref(false)

onMounted(async () => {
  await loadPlayerData()
})

async function loadPlayerData() {
  try {
    const response = await getCurrentSave()
    
    if (response.success) {
      const save = response.data
      playerName.value = save.player_name
      money.value = save.money
      discoveriesCount.value = save.discoveries_count || 0
      synthesesCount.value = save.syntheses_count || 0
      currentSaveId.value = save.id
    }
  } catch (error) {
    console.error('Erro ao carregar dados do jogador:', error)
    router.push('/player-select')
  }
}

function goToLibrary() {
  router.push('/molecules')
}

function goToSynthesis() {
  router.push('/synthesis')
}

function goToAutoSynthesis() {
  router.push('/auto-synthesis')
}

function goToSimulation() {
  router.push('/simulation')
}

function goToBuilder() {
  router.push('/builder')
}

function changePlayer() {
  router.push('/player-select')
}

function confirmDeleteSave() {
  showDeleteConfirm.value = true
}

function cancelDelete() {
  showDeleteConfirm.value = false
}

async function deleteSave() {
  if (!currentSaveId.value) return
  
  try {
    const response = await deleteSaveAPI(currentSaveId.value)
    
    if (response.success) {
      router.push('/player-select')
    }
  } catch (error) {
    console.error('Erro ao apagar save:', error)
    alert('Erro ao apagar save!')
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.player-header {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #444;
}

.player-info {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.player-info h2 {
  color: #fff;
  margin: 0;
  font-size: 1.3rem;
}

.money {
  color: #10b981;
  font-size: 1.2rem;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.content {
  padding: 3rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #fff;
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.welcome {
  text-align: center;
  color: #aaa;
  font-size: 1.2rem;
  margin-bottom: 3rem;
}

.stats-card {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 3rem;
}

.stats-card h3 {
  color: #fff;
  margin-bottom: 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  color: #fff;
  font-size: 1.8rem;
  font-weight: 700;
}

.stat-label {
  color: #aaa;
  font-size: 0.9rem;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.menu-card {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  border: 2px solid transparent;
  text-align: center;
}

.menu-card:not(.disabled):hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  border-color: #646cff;
}

.menu-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.card-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.menu-card h2 {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.menu-card p {
  color: #aaa;
  font-size: 1rem;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background-color: #444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #555;
}

.btn-danger {
  padding: 0.75rem 1.5rem;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-danger:hover {
  background-color: #dc2626;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
}

.modal h3 {
  color: #fff;
  margin-bottom: 1rem;
}

.modal p {
  color: #ccc;
  margin-bottom: 0.5rem;
}

.modal .warning {
  color: #f59e0b;
  font-weight: 600;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
</style>

