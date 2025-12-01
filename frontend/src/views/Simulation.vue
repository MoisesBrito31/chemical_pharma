<template>
  <div class="simulation-container">
    <div class="header">
      <h1>🧪 Simulação de Moléculas</h1>
      <p class="subtitle">Gere todas as moléculas possíveis com características específicas</p>
    </div>

    <!-- Formulário de Entrada -->
    <div class="input-panel">
      <div class="form-group">
        <label for="particle-type">Tipo de Partícula:</label>
        <select id="particle-type" v-model.number="particleType" class="form-control">
          <option :value="0">Qualquer</option>
          <option :value="1">Círculo</option>
          <option :value="2">Quadrado</option>
          <option :value="3">Triângulo</option>
          <option :value="4">Pentágono</option>
        </select>
      </div>

      <div class="form-group">
        <label for="target-mass">Massa Total Desejada:</label>
        <input 
          id="target-mass" 
          type="number" 
          v-model.number="targetMass" 
          min="1" 
          max="40"
          class="form-control"
          placeholder="Ex: 10"
        />
      </div>

      <button 
        @click="generateMolecules" 
        :disabled="isLoading || !isValid"
        class="btn-generate"
      >
        <span v-if="!isLoading">🔬 Gerar Moléculas</span>
        <span v-else>⏳ Gerando...</span>
      </button>
    </div>

    <!-- Mensagem de Erro -->
    <div v-if="error" class="error-message">
      ⚠️ {{ error }}
    </div>

    <!-- Resultados -->
    <div v-if="results && !isLoading" class="results-section">
      <div class="results-header">
        <h2>📊 Resultados</h2>
        <div class="stats">
          <span class="stat-badge">
            <strong>{{ results.count }}</strong> molécula(s) encontrada(s)
          </span>
          <span class="stat-badge">
            <strong>{{ results.details.attempted }}</strong> estrutura(s) testada(s)
          </span>
        </div>
      </div>

      <div v-if="results.count === 0" class="no-results">
        😔 Nenhuma molécula válida encontrada com esses parâmetros.
      </div>

      <div v-else class="molecules-grid">
        <div 
          v-for="(molecule, index) in results.molecules" 
          :key="index"
          class="molecule-card"
          @click="showMoleculeJson(molecule)"
          title="Clique para ver o JSON (debug)"
        >
          <div class="molecule-header">
            <span class="molecule-index">#{{ index + 1 }}</span>
            <span 
              v-if="molecule.status" 
              :class="['status-badge', getStatusClass(molecule.status)]"
            >
              {{ molecule.status }}
            </span>
          </div>
          
          <div class="molecule-viewer-container">
            <MoleculeViewer :molecule="molecule" :size="200" />
          </div>

          <div class="molecule-info">
            <div class="info-row">
              <span class="label">Partículas:</span>
              <span class="value">{{ molecule.particles.length }}</span>
            </div>
            <div class="info-row">
              <span class="label">Ligações:</span>
              <span class="value">{{ molecule.bonds.length }}</span>
            </div>
            <div class="info-row">
              <span class="label">Carga:</span>
              <span class="value" :class="getChargeClass(molecule)">
                {{ calculateCharge(molecule) }}
              </span>
            </div>
            <div v-if="molecule.structure" class="info-row structure-info">
              <span class="label">Cadeia Circular:</span>
              <span class="value" :class="molecule.structure.has_cycle ? 'cycle-yes' : 'cycle-no'">
                {{ molecule.structure.has_cycle ? 'Sim ○' : 'Não ━' }}
              </span>
            </div>
            <div v-if="molecule.structure" class="info-row structure-info">
              <span class="label">Topologia:</span>
              <span class="value topology">
                {{ getTopologyLabel(molecule.structure.topology) }}
              </span>
            </div>
            
            <ObservableProperties v-if="molecule.observableProperties" :properties="molecule.observableProperties" />
          </div>
          
          <!-- Botão para salvar molécula desconhecida -->
          <div v-if="molecule.status === 'Desconhecida'" class="molecule-actions">
            <button 
              @click.stop="saveDiscovery(molecule, index)"
              :disabled="savingIndex === index"
              class="btn-save-discovery"
            >
              <span v-if="savingIndex !== index">💾 Salvar na Biblioteca</span>
              <span v-else>⏳ Salvando...</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Gerando moléculas... Isso pode levar alguns segundos.</p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import MoleculeViewer from '../components/MoleculeViewer.vue';
import ObservableProperties from '../components/ObservableProperties.vue';
import { saveDiscovery as saveDiscoveryAPI, calculateMolecularFormula, getObservableProperties } from '../services/api.js';

export default {
  name: 'Simulation',
  components: {
    MoleculeViewer,
    ObservableProperties
  },
  setup() {
    const particleType = ref(0); // 0 = Qualquer
    const targetMass = ref(10);
    const isLoading = ref(false);
    const error = ref(null);
    const results = ref(null);
    const savingIndex = ref(null);

    const isValid = computed(() => {
      return particleType.value >= 0 && 
             particleType.value <= 4 && 
             targetMass.value > 0 && 
             targetMass.value <= 40;
    });

    const generateMolecules = async () => {
      if (!isValid.value) return;

      isLoading.value = true;
      error.value = null;
      results.value = null;

      try {
        const response = await fetch('http://localhost:5000/api/simulate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            particle_type: particleType.value,
            mass: targetMass.value
          })
        });

        const data = await response.json();

        if (data.success) {
          // Carregar propriedades observáveis para cada molécula
          if (data.molecules && Array.isArray(data.molecules)) {
            const moleculesWithProps = await Promise.all(
              data.molecules.map(async (mol) => {
                try {
                  const propsResponse = await getObservableProperties(mol);
                  if (propsResponse.success) {
                    return { ...mol, observableProperties: propsResponse.data };
                  }
                } catch (err) {
                  console.warn('Erro ao carregar propriedades observáveis:', err);
                }
                return mol;
              })
            );
            results.value = { ...data, molecules: moleculesWithProps };
          } else {
            results.value = data;
          }
        } else {
          error.value = data.details?.error || data.error || 'Erro desconhecido';
        }
      } catch (err) {
        error.value = `Erro ao conectar com o servidor: ${err.message}`;
      } finally {
        isLoading.value = false;
      }
    };

    const calculateCharge = (molecule) => {
      let charge = 0;
      molecule.particles.forEach(p => {
        charge += p.polarity === '+' ? 1 : -1;
      });
      return charge > 0 ? `+${charge}` : charge.toString();
    };

    const getChargeClass = (molecule) => {
      const charge = molecule.particles.reduce((sum, p) => {
        return sum + (p.polarity === '+' ? 1 : -1);
      }, 0);
      
      if (charge > 0) return 'positive';
      if (charge < 0) return 'negative';
      return 'neutral';
    };

    const showMoleculeJson = (molecule) => {
      // Função de debug: mostra o JSON completo da molécula
      const json = JSON.stringify(molecule, null, 2);
      
      // Mostrar no console (melhor para JSONs grandes)
      console.log('=== JSON COMPLETO DA MOLÉCULA (DEBUG) ===');
      console.log(molecule);
      console.log('=== JSON STRING ===');
      console.log(json);
      
      // Copiar para área de transferência
      navigator.clipboard.writeText(json).then(() => {
        alert('✅ JSON copiado para área de transferência!\n\n' +
              'Verifique também o Console (F12) para ver o JSON completo.\n\n' +
              'Partículas: ' + molecule.particles.length + '\n' +
              'Ligações: ' + molecule.bonds.length);
      }).catch(() => {
        // Se falhar ao copiar, apenas mostrar resumo
        alert('📋 JSON mostrado no Console (F12)\n\n' +
              'Partículas: ' + molecule.particles.length + '\n' +
              'Ligações: ' + molecule.bonds.length + '\n\n' +
              json.substring(0, 500) + '\n...(continua no console)');
      });
    };

    const getTopologyLabel = (topology) => {
      const labels = {
        'linear': '━ Linear',
        'Y': 'Y Ramificação',
        'X': 'X Cruzamento',
        'tree': '⋈ Árvore',
        'cycle': '○ Ciclo',
        'mista': '◈ Mista'
      };
      return labels[topology] || topology;
    };

    const getStatusClass = (status) => {
      const classes = {
        'Base': 'base',
        'Descoberta': 'discovered',
        'Desconhecida': 'unknown'
      };
      return classes[status] || 'unknown';
    };

    const saveDiscovery = async (molecule, index) => {
      if (savingIndex.value !== null) return; // Já está salvando algo
      
      savingIndex.value = index;
      
      try {
        // Calcular fórmula molecular
        const formula = calculateMolecularFormula(molecule);
        
        // Salvar descoberta
        const response = await saveDiscoveryAPI(molecule, formula);
        
        if (response.success) {
          // Atualizar o status da molécula na lista
          if (results.value && results.value.molecules) {
            results.value.molecules[index].status = 'Descoberta';
            results.value.molecules[index].is_discovered = true;
            results.value.molecules[index].is_known = true;
          }
        }
      } catch (err) {
        console.error('Erro ao salvar descoberta:', err);
      } finally {
        savingIndex.value = null;
      }
    };

    return {
      particleType,
      targetMass,
      isLoading,
      error,
      results,
      savingIndex,
      isValid,
      generateMolecules,
      calculateCharge,
      getChargeClass,
      showMoleculeJson,
      getTopologyLabel,
      getStatusClass,
      saveDiscovery
    };
  }
};
</script>

<style scoped>
.simulation-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.input-panel {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  display: flex;
  gap: 1.5rem;
  align-items: flex-end;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
}

.btn-generate {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  white-space: nowrap;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  border: 2px solid #fcc;
  border-radius: 8px;
  padding: 1rem;
  color: #c33;
  margin-bottom: 1rem;
  text-align: center;
}

.results-section {
  margin-top: 2rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.results-header h2 {
  font-size: 1.8rem;
  color: #2c3e50;
}

.stats {
  display: flex;
  gap: 1rem;
}

.stat-badge {
  background: #f0f0f0;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #555;
}

.stat-badge strong {
  color: #667eea;
}

.no-results {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  color: #7f8c8d;
  font-size: 1.2rem;
}

.molecules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.molecule-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.molecule-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  border: 2px solid #667eea;
}

.molecule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.molecule-index {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
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

.molecule-viewer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.molecule-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.info-row .label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.info-row .value {
  font-weight: 600;
  color: #2c3e50;
}

.info-row .value.positive {
  color: #e74c3c;
}

.info-row .value.negative {
  color: #3498db;
}

.info-row .value.neutral {
  color: #95a5a6;
}

.info-row .value.has-cycle {
  color: #e67e22;
  font-weight: 700;
}

.info-row .value.topology-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
}

.info-row.structure-info {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-left: 3px solid #667eea;
}

.info-row .value.cycle-yes {
  color: #667eea;
  font-weight: 700;
}

.info-row .value.cycle-no {
  color: #95a5a6;
}

.info-row .value.topology {
  font-weight: 600;
  color: #2c3e50;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  background: white;
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
  color: #7f8c8d;
  font-size: 1.1rem;
}

.molecule-actions {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.btn-save-discovery {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-save-discovery:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.btn-save-discovery:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

