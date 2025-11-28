/**
 * Gerencia fila de criação de contextos WebGL do PixiJS
 * Para evitar o erro "Too many active WebGL contexts"
 */

const MAX_ACTIVE_CONTEXTS = 3

// Fila de tarefas de renderização pendentes
const renderQueue = []

// Contextos ativos
const activeContexts = new Map()

// Contador de contextos sendo processados
let processing = 0

/**
 * Adiciona uma tarefa de renderização à fila
 * @param {Object} task - { id, canvas, renderFn }
 */
export function addToQueue(task) {
  // Verificar se já existe na fila
  const existingIndex = renderQueue.findIndex(t => t.id === task.id)
  if (existingIndex !== -1) {
    // Remover tarefa antiga
    renderQueue.splice(existingIndex, 1)
  }
  
  // Sempre adicionar nova tarefa
  renderQueue.push(task)
  
  // Processar imediatamente
  setTimeout(() => processQueue(), 0)
}

/**
 * Processa a fila de renderização
 */
async function processQueue() {
  // Se já está processando ou fila vazia, sair
  if (processing >= MAX_ACTIVE_CONTEXTS || renderQueue.length === 0) {
    return
  }
  
  // Pegar próxima tarefa
  const task = renderQueue.shift()
  
  if (!task) return
  
  processing++
  
  try {
    // Executar renderização
    const app = await task.renderFn()
    
    // Armazenar referência ao contexto ativo
    if (app) {
      activeContexts.set(task.id, app)
    }
  } catch (error) {
    console.error('Erro ao renderizar:', error)
  } finally {
    processing--
    
    // Processar próxima tarefa
    processQueue()
  }
}

/**
 * Remove uma tarefa da fila
 * @param {string} id - ID da tarefa
 */
export function removeFromQueue(id) {
  const index = renderQueue.findIndex(t => t.id === id)
  if (index !== -1) {
    renderQueue.splice(index, 1)
  }
  
  // Também destruir contexto se existir
  destroyContext(id)
}

/**
 * Destrói um contexto WebGL específico
 * @param {string} id - ID do contexto
 */
export function destroyContext(id) {
  const app = activeContexts.get(id)
  
  if (app) {
    try {
      // Destruir aplicação PixiJS completamente
      app.destroy(true, {
        children: true,
        texture: true,
        baseTexture: true
      })
      
      activeContexts.delete(id)
    } catch (error) {
      console.error('Erro ao destruir contexto:', error)
    }
  }
}

/**
 * Limpa toda a fila
 */
export function clearQueue() {
  renderQueue.length = 0
  
  // Destruir todos os contextos ativos
  activeContexts.forEach((app, id) => {
    destroyContext(id)
  })
  
  activeContexts.clear()
}

/**
 * Retorna informações sobre o estado da fila
 */
export function getQueueStatus() {
  return {
    pending: renderQueue.length,
    active: activeContexts.size,
    processing
  }
}

