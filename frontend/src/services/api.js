/**
 * API Service - Comunicação com o backend Flask
 */

const API_BASE_URL = 'http://localhost:5000/api'

// ============================================
// MOLECULES
// ============================================

export async function getAllMolecules() {
  const response = await fetch(`${API_BASE_URL}/molecules`)
  return response.json()
}

export async function getMoleculesByMass(mass) {
  const response = await fetch(`${API_BASE_URL}/molecules/mass/${mass}`)
  return response.json()
}

export async function getAvailableMasses() {
  const response = await fetch(`${API_BASE_URL}/molecules/masses`)
  return response.json()
}

export async function validateMolecule(molecule) {
  const response = await fetch(`${API_BASE_URL}/molecules/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(molecule)
  })
  return response.json()
}

export async function calculateProperties(molecule) {
  const response = await fetch(`${API_BASE_URL}/molecules/properties`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(molecule)
  })
  return response.json()
}

export async function getObservableProperties(molecule) {
  const response = await fetch(`${API_BASE_URL}/molecules/observable-properties`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ molecule })
  })
  return response.json()
}

// ============================================
// SYNTHESIS
// ============================================

export async function synthesizeMolecules(moleculeAId, moleculeBId) {
  const response = await fetch(`${API_BASE_URL}/synthesis/mix`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      molecule_a_id: moleculeAId,
      molecule_b_id: moleculeBId
    })
  })
  return response.json()
}

export async function validateSynthesis(moleculeA, moleculeB) {
  const response = await fetch(`${API_BASE_URL}/synthesis/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      molecule_a: moleculeA,
      molecule_b: moleculeB
    })
  })
  return response.json()
}

export async function getAllSynthesisResults() {
  const response = await fetch(`${API_BASE_URL}/synthesis/results`)
  return response.json()
}

export async function getSynthesisStats() {
  const response = await fetch(`${API_BASE_URL}/synthesis/stats`)
  return response.json()
}

export async function clearSynthesisCache() {
  const response = await fetch(`${API_BASE_URL}/synthesis/cache/clear`, {
    method: 'DELETE'
  })
  return response.json()
}

// ============================================
// DISCOVERIES
// ============================================

export async function getAllDiscoveries() {
  const response = await fetch(`${API_BASE_URL}/discoveries`)
  return response.json()
}

export async function saveDiscovery(molecule, formula, name = null) {
  const response = await fetch(`${API_BASE_URL}/discoveries`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      molecule,
      formula,
      name
    })
  })
  return response.json()
}

export async function deleteDiscovery(discoveryId) {
  const response = await fetch(`${API_BASE_URL}/discoveries/${discoveryId}`, {
    method: 'DELETE'
  })
  return response.json()
}

export async function clearAllDiscoveries() {
  const response = await fetch(`${API_BASE_URL}/discoveries/clear`, {
    method: 'DELETE'
  })
  return response.json()
}

export async function getDiscoveryStats() {
  const response = await fetch(`${API_BASE_URL}/discoveries/stats`)
  return response.json()
}

// ============================================
// SAVES/PLAYERS
// ============================================

export async function getAllSaves() {
  const response = await fetch(`${API_BASE_URL}/saves`)
  return response.json()
}

export async function createSave(playerName) {
  const response = await fetch(`${API_BASE_URL}/saves`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ player_name: playerName })
  })
  return response.json()
}

export async function selectSave(saveId) {
  const response = await fetch(`${API_BASE_URL}/saves/${saveId}/select`, {
    method: 'POST'
  })
  return response.json()
}

export async function getCurrentSave() {
  const response = await fetch(`${API_BASE_URL}/saves/current`)
  return response.json()
}

export async function deleteSave(saveId) {
  const response = await fetch(`${API_BASE_URL}/saves/${saveId}`, {
    method: 'DELETE'
  })
  return response.json()
}

// ============================================
// PROPERTIES
// ============================================

export async function getPropertyProfile() {
  const response = await fetch(`${API_BASE_URL}/properties/profile`)
  return response.json()
}

// ============================================
// UTILITIES
// ============================================

export function calculateMolecularFormula(molecule) {
  if (!molecule || !molecule.particles) return ''
  
  const particles = molecule.particles
  const bonds = molecule.bonds || []
  
  // Contar conexões de cada partícula
  const connectionCount = {}
  particles.forEach(p => {
    connectionCount[p.id] = 0
  })
  
  bonds.forEach(bond => {
    connectionCount[bond.from] += bond.multiplicity || 1
    connectionCount[bond.to] += bond.multiplicity || 1
  })
  
  // Mapear tipos para letras
  const typeToLetter = {
    'circle': 'C',
    'square': 'Q',
    'triangle': 'T',
    'pentagon': 'P'
  }
  
  // Agrupar partículas por número de conexões
  const particlesByConnections = {}
  particles.forEach(p => {
    const conn = connectionCount[p.id]
    if (!particlesByConnections[conn]) {
      particlesByConnections[conn] = []
    }
    particlesByConnections[conn].push(p.type)
  })
  
  // Ordenar por número de conexões (crescente)
  const sortedConnections = Object.keys(particlesByConnections)
    .map(Number)
    .sort((a, b) => a - b)
  
  // Construir fórmula
  let formula = ''
  sortedConnections.forEach(conn => {
    const types = particlesByConnections[conn]
    
    // Contar ocorrências de cada tipo
    const typeCounts = {}
    types.forEach(type => {
      typeCounts[type] = (typeCounts[type] || 0) + 1
    })
    
    // Ordenar tipos por ordem padrão: C, Q, T, P
    const typeOrder = ['circle', 'square', 'triangle', 'pentagon']
    typeOrder.forEach(type => {
      if (typeCounts[type]) {
        const letter = typeToLetter[type]
        const count = typeCounts[type]
        
        if (count === 1) {
          formula += letter
        } else {
          formula += letter + convertToSuperscript(count)
        }
      }
    })
  })
  
  return formula
}

function convertToSuperscript(number) {
  const superscripts = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
  }
  return String(number)
    .split('')
    .map(digit => superscripts[digit] || digit)
    .join('')
}

export function calculateMoleculeProperties(molecule) {
  const mass = molecule.particles.length
  
  // Calcular carga (soma das polaridades)
  let charge = 0
  molecule.particles.forEach(p => {
    charge += p.polarity === '+' ? 1 : -1
  })
  
  let polarity = 'neutral'
  if (charge > 0) polarity = 'positive'
  if (charge < 0) polarity = 'negative'
  
  const formula = calculateMolecularFormula(molecule)
  
  return {
    mass,
    charge,
    polarity,
    formula
  }
}

