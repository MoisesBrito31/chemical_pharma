/**
 * Funções para comparar moléculas considerando estrutura completa
 * (partículas + ligações)
 */

/**
 * Compara duas moléculas verificando se são idênticas estruturalmente
 * Considera: tipos de partículas, polaridades E estrutura de ligações
 */
export function areMoleculesIdentical(mol1, mol2) {
  if (!mol1 || !mol2) return false
  
  // Verificar quantidade de partículas
  if (mol1.particles.length !== mol2.particles.length) return false
  
  // Verificar quantidade de ligações
  if (mol1.bonds.length !== mol2.bonds.length) return false
  
  // Criar "impressão digital" molecular (fingerprint)
  const fingerprint1 = createMolecularFingerprint(mol1)
  const fingerprint2 = createMolecularFingerprint(mol2)
  
  return fingerprint1 === fingerprint2
}

/**
 * Cria uma "impressão digital" única da molécula
 * baseada na estrutura completa (partículas + ligações)
 */
function createMolecularFingerprint(molecule) {
  // 1. Criar representação das partículas (ordenada)
  const particlesSignature = molecule.particles
    .map(p => `${p.type}${p.polarity}`)
    .sort()
    .join(',')
  
  // 2. Criar representação das ligações (normalizada)
  // Cada ligação é representada pelos tipos/polaridades conectados
  const bondsSignature = molecule.bonds
    .map(bond => {
      const particleFrom = molecule.particles.find(p => p.id === bond.from)
      const particleTo = molecule.particles.find(p => p.id === bond.to)
      
      if (!particleFrom || !particleTo) return ''
      
      const from = `${particleFrom.type}${particleFrom.polarity}`
      const to = `${particleTo.type}${particleTo.polarity}`
      const mult = `x${bond.multiplicity}`
      
      // Ordenar para que A-B seja igual a B-A
      const [first, second] = [from, to].sort()
      return `${first}-${second}${mult}`
    })
    .filter(b => b) // Remover vazios
    .sort()
    .join('|')
  
  // 3. Combinar tudo em uma única string
  return `${particlesSignature}::${bondsSignature}`
}

/**
 * Verifica se uma molécula já existe numa lista
 */
export function moleculeExistsInList(molecule, moleculeList) {
  return moleculeList.some(mol => areMoleculesIdentical(molecule, mol))
}

