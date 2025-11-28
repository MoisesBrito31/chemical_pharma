<template>
  <div class="player-select">
    <div class="container">
      <h1>⚗️ Chemical Pharma</h1>
      <p class="subtitle">Selecione ou crie um jogador</p>
      
      <!-- Lista de saves existentes -->
      <div v-if="saves.length > 0" class="saves-list">
        <h2>Saves Existentes</h2>
        <div class="saves-grid">
          <div 
            v-for="save in saves" 
            :key="save.id"
            class="save-card"
            @click="selectPlayer(save.id)"
          >
            <div class="save-header">
              <h3>{{ save.player_name }}</h3>
              <button 
                class="delete-btn"
                @click.stop="confirmDelete(save)"
                title="Apagar save"
              >
                🗑️
              </button>
            </div>
            <div class="save-stats">
              <div class="stat">
                <span class="label">💰 Dinheiro:</span>
                <span class="value">${{ save.money }}</span>
              </div>
              <div class="stat">
                <span class="label">🧪 Descobertas:</span>
                <span class="value">{{ save.discoveries_count }}</span>
              </div>
              <div class="stat">
                <span class="label">⚗️ Sínteses:</span>
                <span class="value">{{ save.syntheses_count }}</span>
              </div>
            </div>
            <div class="save-date">
              Última jogada: {{ formatDate(save.last_played) }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-message">
        <p>Nenhum save encontrado. Crie um novo jogador!</p>
      </div>
      
      <!-- Formulário para criar novo jogador -->
      <div class="create-new">
        <h2>Novo Jogador</h2>
        <div class="create-form">
          <input 
            v-model="newPlayerName"
            type="text"
            placeholder="Digite o nome do jogador..."
            @keyup.enter="createPlayer"
            class="player-input"
          />
          <button 
            @click="createPlayer"
            :disabled="!newPlayerName.trim() || creating"
            class="btn-primary"
          >
            {{ creating ? '⏳ Criando...' : '➕ Criar Novo Jogador' }}
          </button>
        </div>
      </div>
      
      <!-- Modal de confirmação de delete -->
      <div v-if="deleteConfirm" class="modal-overlay" @click="cancelDelete">
        <div class="modal" @click.stop>
          <h3>⚠️ Confirmar Exclusão</h3>
          <p>Tem certeza que deseja apagar o save de <strong>{{ deleteConfirm.player_name }}</strong>?</p>
          <p class="warning">Esta ação não pode ser desfeita!</p>
          <div class="modal-actions">
            <button class="btn-secondary" @click="cancelDelete">Cancelar</button>
            <button class="btn-danger" @click="deletePlayer">Confirmar Exclusão</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAllSaves, createSave, selectSave, deleteSave } from '../services/api.js'

const router = useRouter()

const saves = ref([])
const newPlayerName = ref('')
const creating = ref(false)
const deleteConfirm = ref(null)

onMounted(async () => {
  await loadSaves()
})

async function loadSaves() {
  try {
    const response = await getAllSaves()
    if (response.success) {
      saves.value = response.data
    }
  } catch (error) {
    console.error('Erro ao carregar saves:', error)
  }
}

async function createPlayer() {
  if (!newPlayerName.value.trim() || creating.value) return
  
  creating.value = true
  
  try {
    const response = await createSave(newPlayerName.value.trim())
    
    if (response.success) {
      // Selecionar automaticamente o novo save
      await selectPlayer(response.save_id)
    }
  } catch (error) {
    console.error('Erro ao criar save:', error)
    alert('Erro ao criar jogador!')
  } finally {
    creating.value = false
  }
}

async function selectPlayer(saveId) {
  try {
    const response = await selectSave(saveId)
    
    if (response.success) {
      // Redirecionar para a home
      router.push('/')
    }
  } catch (error) {
    console.error('Erro ao selecionar save:', error)
    alert('Erro ao selecionar jogador!')
  }
}

function confirmDelete(save) {
  deleteConfirm.value = save
}

function cancelDelete() {
  deleteConfirm.value = null
}

async function deletePlayer() {
  if (!deleteConfirm.value) return
  
  try {
    const response = await deleteSave(deleteConfirm.value.id)
    
    if (response.success) {
      // Recarregar lista de saves
      await loadSaves()
      deleteConfirm.value = null
    }
  } catch (error) {
    console.error('Erro ao deletar save:', error)
    alert('Erro ao apagar save!')
  }
}

function formatDate(isoString) {
  const date = new Date(isoString)
  return date.toLocaleString('pt-BR')
}
</script>

<style scoped>
.player-select {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  width: 100%;
  max-width: 1200px;
}

h1 {
  text-align: center;
  color: #fff;
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  color: #aaa;
  font-size: 1.2rem;
  margin-bottom: 3rem;
}

.saves-list {
  margin-bottom: 3rem;
}

.saves-list h2,
.create-new h2 {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.saves-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.save-card {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
}

.save-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  border-color: #646cff;
}

.save-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.save-header h3 {
  color: #fff;
  font-size: 1.3rem;
  margin: 0;
}

.delete-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.delete-btn:hover {
  opacity: 1;
}

.save-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stat {
  display: flex;
  justify-content: space-between;
}

.stat .label {
  color: #aaa;
}

.stat .value {
  color: #fff;
  font-weight: 600;
}

.save-date {
  color: #777;
  font-size: 0.85rem;
  text-align: right;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #444;
}

.empty-message {
  text-align: center;
  padding: 3rem;
  color: #aaa;
  font-size: 1.1rem;
}

.create-new {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
}

.create-form {
  display: flex;
  gap: 1rem;
}

.player-input {
  flex: 1;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 2px solid #444;
  background-color: #1a1a1a;
  color: #fff;
  transition: border-color 0.2s;
}

.player-input:focus {
  outline: none;
  border-color: #646cff;
}

.btn-primary {
  padding: 0.75rem 2rem;
  background-color: #646cff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.btn-primary:hover:not(:disabled) {
  background-color: #5458e8;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background-color: #444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
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
}

.btn-danger:hover {
  background-color: #dc2626;
}
</style>

