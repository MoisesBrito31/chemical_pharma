<template>
  <div class="molecule-viewer" ref="container">
    <div v-if="!imageReady" class="placeholder">
      <span>⚛️</span>
    </div>
    <img v-if="imageReady" :src="imageData" class="molecule-image" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as PIXI from 'pixi.js'

const props = defineProps({
  molecule: {
    type: Object,
    required: true
  },
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 300
  }
})

const container = ref(null)
const isVisible = ref(false)
const imageReady = ref(false)
const imageData = ref('')
const moleculeId = `mol-${props.molecule.id || Math.random()}`

let observer = null

onMounted(() => {
  setupIntersectionObserver()
  
  // Se o componente já estiver visível ao montar, renderizar imediatamente
  // (útil quando usado em modais ou áreas sempre visíveis)
  setTimeout(() => {
    if (isVisible.value || !observer) {
      renderMoleculeToImage()
    }
  }, 50)
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})

// Watch para visibilidade - renderizar só quando entra em vista
watch(isVisible, (newValue, oldValue) => {
  if (newValue && !oldValue && !imageReady.value) {
    // Molécula entrou em vista - renderizar uma vez
    renderMoleculeToImage()
  }
})

// Watch para mudanças na molécula - re-renderizar quando trocar
watch(() => props.molecule, () => {
  // Resetar estado e re-renderizar
  imageReady.value = false
  imageData.value = ''
  
  // Se estiver visível, renderizar imediatamente
  if (isVisible.value) {
    renderMoleculeToImage()
  }
}, { deep: true })

function setupIntersectionObserver() {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        isVisible.value = entry.isIntersecting
      })
    },
    {
      root: null,
      rootMargin: '50px',
      threshold: 0.1
    }
  )
  
  if (container.value) {
    observer.observe(container.value)
  }
}

async function renderMoleculeToImage() {
  if (imageReady.value) return
  
  try {
    // Criar canvas offscreen
    const offscreenCanvas = document.createElement('canvas')
    
    // Criar app PixiJS temporário
    const app = new PIXI.Application({
      view: offscreenCanvas,
      width: props.width,
      height: props.height,
      backgroundColor: 0x1a1a1a,
      antialias: true,
      resolution: 1,
      preserveDrawingBuffer: true // Necessário para extrair imagem
    })
    
    // Desenhar molécula
    drawMolecule(app)
    
    // Aguardar próximo frame para garantir renderização
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Extrair imagem do canvas
    imageData.value = offscreenCanvas.toDataURL('image/png')
    imageReady.value = true
    
    // Destruir app PixiJS (libera contexto WebGL)
    app.destroy(true, {
      children: true,
      texture: true,
      baseTexture: true
    })
  } catch (error) {
    console.error('Erro ao renderizar molécula:', error)
  }
}

function drawMolecule(app) {
  const stage = app.stage
  
  const particles = props.molecule.particles || []
  const bonds = props.molecule.bonds || []
  
  if (particles.length === 0) return
  
  // Fator de espaçamento visual (transforma coordenadas lógicas em visuais)
  const spacingFactor = 2
  
  // Calcular escala e offset para centralizar
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
  
  const scaleX = (props.width * 0.7) / molWidth
  const scaleY = (props.height * 0.7) / molHeight
  const scale = Math.min(scaleX, scaleY, 40)
  
  const offsetX = props.width / 2 - ((minX + maxX) / 2) * scale
  const offsetY = props.height / 2 - ((minY + maxY) / 2) * scale
  
  // Desenhar bonds primeiro (para ficarem atrás)
  bonds.forEach(bond => {
    const pFrom = particles.find(p => p.id === bond.from)
    const pTo = particles.find(p => p.id === bond.to)
    
    if (!pFrom || !pTo) return
    
    const x1 = (pFrom.x || 0) * spacingFactor * scale + offsetX
    const y1 = (pFrom.y || 0) * spacingFactor * scale + offsetY
    const x2 = (pTo.x || 0) * spacingFactor * scale + offsetX
    const y2 = (pTo.y || 0) * spacingFactor * scale + offsetY
    
    const multiplicity = bond.multiplicity || 1
    
    // Desenhar linhas baseado na multiplicidade
    for (let i = 0; i < multiplicity; i++) {
      const graphics = new PIXI.Graphics()
      
      // Offset perpendicular para ligações múltiplas
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
    let color = particle.polarity === '+' ? 0xef4444 : 0x3b82f6 // vermelho (+) ou azul (-)
    let radius = 20
    
    switch (particle.type) {
      case 'circle':
        radius = 18
        break
      case 'square':
        radius = 20
        break
      case 'triangle':
        radius = 22
        break
      case 'pentagon':
        radius = 24
        break
    }
    
    // Desenhar forma
    if (particle.type === 'circle') {
      graphics.beginFill(color)
      graphics.drawCircle(x, y, radius)
      graphics.endFill()
    } else if (particle.type === 'square') {
      graphics.beginFill(color)
      graphics.drawRect(x - radius, y - radius, radius * 2, radius * 2)
      graphics.endFill()
    } else if (particle.type === 'triangle') {
      graphics.beginFill(color)
      graphics.moveTo(x, y - radius)
      graphics.lineTo(x + radius, y + radius)
      graphics.lineTo(x - radius, y + radius)
      graphics.lineTo(x, y - radius)
      graphics.endFill()
    } else if (particle.type === 'pentagon') {
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
    }
    
    // Símbolo de polaridade
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
</script>

<style scoped>
.molecule-viewer {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background-color: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  min-height: 300px;
  font-size: 48px;
  opacity: 0.3;
}

.molecule-image {
  display: block;
  max-width: 100%;
  height: auto;
}
</style>

