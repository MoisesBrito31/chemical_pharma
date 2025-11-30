<template>
  <div class="builder-container">
    <div class="header">
      <h1>🔧 Montador de Moléculas</h1>
      <p class="subtitle">Teste e lapide os algoritmos com moléculas customizadas</p>
    </div>

    <!-- Tabs: JSON Editor | Visual Editor -->
    <div class="tabs">
      <button 
        @click="activeTab = 'json'" 
        :class="['tab', { active: activeTab === 'json' }]"
      >
        📝 Editor JSON
      </button>
      <button 
        @click="activeTab = 'visual'" 
        :class="['tab', { active: activeTab === 'visual' }]"
      >
        🎨 Editor Visual
      </button>
    </div>

    <div class="builder-layout">
      <!-- Painel Esquerdo: Editor -->
      <div class="editor-panel">
        <!-- Tab JSON -->
        <div v-if="activeTab === 'json'" class="tab-content">
          <div class="panel-header">
            <h2>📝 Editor JSON</h2>
            <div class="editor-actions">
              <button @click="loadExample" class="btn-example">📋 Exemplo</button>
              <button @click="clearEditor" class="btn-clear">🗑️ Limpar</button>
              <button @click="loadFromVisual" class="btn-load">⬇️ Carregar do Visual</button>
            </div>
          </div>
          
          <textarea
            v-model="moleculeJson"
            class="json-editor"
            placeholder='Cole aqui o JSON da molécula...'
            spellcheck="false"
            @input="updateFromJson"
          ></textarea>
        </div>

        <!-- Tab Visual -->
        <div v-if="activeTab === 'visual'" class="tab-content">
          <div class="panel-header">
            <h2>🎨 Editor Visual</h2>
            <button @click="loadFromJson" class="btn-load">⬇️ Carregar do JSON</button>
          </div>

          <!-- Gerenciar Partículas -->
          <div class="section">
            <div class="section-header">
              <h3>⚛️ Partículas ({{ moleculeData.particles.length }})</h3>
              <button @click="showAddParticle = !showAddParticle" class="btn-add">
                ➕ Adicionar
              </button>
            </div>

            <!-- Formulário Adicionar Partícula -->
            <div v-if="showAddParticle" class="form-card visual-form">
              <div class="visual-selector">
                <label class="selector-label">Tipo:</label>
                <div class="type-buttons">
                  <button 
                    @click="newParticle.type = 'circle'"
                    :class="['type-btn', { active: newParticle.type === 'circle' }]"
                    title="Círculo"
                  >
                    <span class="type-icon">○</span>
                    <span class="type-name">Círculo</span>
                  </button>
                  <button 
                    @click="newParticle.type = 'square'"
                    :class="['type-btn', { active: newParticle.type === 'square' }]"
                    title="Quadrado"
                  >
                    <span class="type-icon">□</span>
                    <span class="type-name">Quadrado</span>
                  </button>
                  <button 
                    @click="newParticle.type = 'triangle'"
                    :class="['type-btn', { active: newParticle.type === 'triangle' }]"
                    title="Triângulo"
                  >
                    <span class="type-icon">△</span>
                    <span class="type-name">Triângulo</span>
                  </button>
                  <button 
                    @click="newParticle.type = 'pentagon'"
                    :class="['type-btn', { active: newParticle.type === 'pentagon' }]"
                    title="Pentágono"
                  >
                    <span class="type-icon">⬠</span>
                    <span class="type-name">Pentágono</span>
                  </button>
                </div>
              </div>

              <div class="visual-selector">
                <label class="selector-label">Polaridade:</label>
                <div class="polarity-buttons">
                  <button 
                    @click="newParticle.polarity = '+'"
                    :class="['polarity-btn', 'positive', { active: newParticle.polarity === '+' }]"
                  >
                    <span class="polarity-icon">+</span>
                    <span class="polarity-name">Positiva</span>
                  </button>
                  <button 
                    @click="newParticle.polarity = '-'"
                    :class="['polarity-btn', 'negative', { active: newParticle.polarity === '-' }]"
                  >
                    <span class="polarity-icon">-</span>
                    <span class="polarity-name">Negativa</span>
                  </button>
                </div>
              </div>

              <div class="form-actions">
                <button @click="addParticle" class="btn-save">💾 Adicionar</button>
                <button @click="showAddParticle = false" class="btn-cancel">❌ Cancelar</button>
              </div>
            </div>

            <!-- Lista de Partículas -->
            <div class="list-container">
              <div 
                v-for="(particle, index) in moleculeData.particles" 
                :key="particle.id || index"
                class="list-item"
              >
                <div class="item-info">
                  <span class="item-id">{{ particle.id }}</span>
                  <span class="item-type">{{ getTypeLabel(particle.type) }}</span>
                  <span :class="['item-polarity', particle.polarity === '+' ? 'positive' : 'negative']">
                    {{ particle.polarity }}
                  </span>
                  <span class="item-position">({{ particle.x }}, {{ particle.y }})</span>
                </div>
                <div class="item-actions">
                  <button @click="editParticle(index)" class="btn-edit">✏️</button>
                  <button @click="removeParticle(index)" class="btn-remove">🗑️</button>
                </div>
              </div>
              <div v-if="moleculeData.particles.length === 0" class="empty-state">
                Nenhuma partícula. Clique em "Adicionar" para começar.
              </div>
            </div>
          </div>

          <!-- Gerenciar Bonds -->
          <div class="section">
            <div class="section-header">
              <h3>🔗 Ligações ({{ moleculeData.bonds.length }})</h3>
              <button @click="showAddBond = !showAddBond" class="btn-add">
                ➕ Adicionar
              </button>
            </div>

            <!-- Formulário Adicionar Bond -->
            <div v-if="showAddBond" class="form-card">
              <div class="form-row">
                <label>De:</label>
                <select v-model="newBond.from">
                  <option value="">Selecione...</option>
                  <option v-for="p in moleculeData.particles" :key="p.id" :value="p.id">
                    {{ p.id }} ({{ getTypeLabel(p.type) }})
                  </option>
                </select>
              </div>
              <div class="form-row">
                <label>Para:</label>
                <select v-model="newBond.to">
                  <option value="">Selecione...</option>
                  <option v-for="p in moleculeData.particles" :key="p.id" :value="p.id">
                    {{ p.id }} ({{ getTypeLabel(p.type) }})
                  </option>
                </select>
              </div>
              <div class="form-row">
                <label>Multiplicidade:</label>
                <select v-model.number="newBond.multiplicity">
                  <option :value="1">1 (Simples)</option>
                  <option :value="2">2 (Dupla)</option>
                  <option :value="3">3 (Tripla)</option>
                </select>
              </div>
              <div class="form-actions">
                <button @click="addBond" class="btn-save">💾 Adicionar</button>
                <button @click="showAddBond = false" class="btn-cancel">❌ Cancelar</button>
              </div>
            </div>

            <!-- Lista de Bonds -->
            <div class="list-container">
              <div 
                v-for="(bond, index) in moleculeData.bonds" 
                :key="index"
                class="list-item"
              >
                <div class="item-info">
                  <span class="bond-from">{{ bond.from }}</span>
                  <span class="bond-arrow">→</span>
                  <span class="bond-to">{{ bond.to }}</span>
                  <span class="bond-multiplicity">×{{ bond.multiplicity }}</span>
                </div>
                <div class="item-actions">
                  <button @click="removeBond(index)" class="btn-remove">🗑️</button>
                </div>
              </div>
              <div v-if="moleculeData.bonds.length === 0" class="empty-state">
                Nenhuma ligação. Clique em "Adicionar" para criar.
              </div>
            </div>
          </div>
        </div>

        <!-- Botões de Ação -->
        <div class="action-buttons">
          <button @click="validateMolecule" class="btn-action" :disabled="isProcessing">
            ✅ Validar
          </button>
          <button @click="reorganizeMolecule" class="btn-action" :disabled="isProcessing">
            🔄 Reorganizar
          </button>
          <button @click="analyzeMolecule" class="btn-action" :disabled="isProcessing">
            🔍 Analisar
          </button>
          <button @click="testRebond" class="btn-action" :disabled="isProcessing">
            🔗 Rebond
          </button>
          <button @click="runAll" class="btn-action btn-primary" :disabled="isProcessing">
            ⚡ Executar Tudo
          </button>
        </div>
      </div>

      <!-- Painel Direito: Visualização e Resultados -->
      <div class="results-panel">
        <!-- Visualização da Molécula -->
        <div class="visualization-section">
          <h2>👁️ Visualização</h2>
          <div class="molecule-display">
            <div v-if="currentMolecule" class="molecule-viewer-container">
              <MoleculeViewer :molecule="currentMolecule" :size="300" />
            </div>
            <div v-else class="placeholder">
              <p>Nenhuma molécula carregada</p>
            </div>
          </div>
        </div>

        <!-- Resultados -->
        <div class="results-section" v-if="results">
          <h2>📊 Resultados</h2>
          
          <!-- Validação -->
          <div v-if="results.validation" class="result-card">
            <h3>✅ Validação</h3>
            <div :class="['validation-result', results.validation.valid ? 'valid' : 'invalid']">
              <span v-if="results.validation.valid">✓ Válida</span>
              <span v-else>✗ Inválida: {{ results.validation.reason }}</span>
            </div>
            <pre v-if="results.validation.details">{{ JSON.stringify(results.validation.details, null, 2) }}</pre>
          </div>

          <!-- Estrutura -->
          <div v-if="results.structure" class="result-card">
            <h3>🔍 Análise Estrutural</h3>
            <div v-if="moleculeToCheck && moleculeToCheck.particles" class="discovery-status">
              <span v-if="isMoleculeKnown" class="status-badge known">✓ Já Conhecida</span>
              <span v-else class="status-badge new">✨ Nova Descoberta</span>
            </div>
            <div class="structure-info">
              <div class="info-row">
                <span class="label">Cadeia Circular:</span>
                <span :class="['value', results.structure.has_cycle ? 'cycle-yes' : 'cycle-no']">
                  {{ results.structure.has_cycle ? 'Sim ○' : 'Não ━' }}
                </span>
              </div>
              <div class="info-row">
                <span class="label">Topologia:</span>
                <span class="value topology">{{ getTopologyLabel(results.structure.topology) }}</span>
              </div>
              <div class="info-row">
                <span class="label">Ramificações:</span>
                <span class="value">{{ results.structure.branch_count }}</span>
              </div>
              <div class="info-row">
                <span class="label">Grau Máximo:</span>
                <span class="value">{{ results.structure.max_degree }}</span>
              </div>
              <div class="info-row">
                <span class="label">Conectada:</span>
                <span class="value">{{ results.structure.is_connected ? 'Sim' : 'Não' }}</span>
              </div>
            </div>
          </div>

          <!-- Reorganizada -->
          <div v-if="results.reorganized" class="result-card">
            <h3>🔄 Molécula Reorganizada</h3>
            <div v-if="moleculeToCheck && moleculeToCheck.particles" class="discovery-status">
              <span v-if="isMoleculeKnown" class="status-badge known">✓ Já Conhecida</span>
              <span v-else class="status-badge new">✨ Nova Descoberta</span>
            </div>
            <div class="molecule-viewer-container">
              <MoleculeViewer :molecule="results.reorganized" :size="300" />
            </div>
            <div class="reorganized-actions">
              <button @click="copyReorganized" class="btn-copy">📋 Copiar JSON Reorganizado</button>
              <button 
                @click="saveToLibrary" 
                class="btn-save-library" 
                :disabled="!results.reorganized || isMoleculeKnown"
                :title="isMoleculeKnown ? 'Esta molécula já foi descoberta' : 'Adicionar à biblioteca'"
              >
                📚 Adicionar à Biblioteca
              </button>
            </div>
          </div>

          <!-- Rebond Result -->
          <div v-if="results.rebond" class="result-card">
            <h3>🔗 Resultado do Rebond</h3>
            <div :class="['rebond-result', results.rebond.success ? 'success' : 'failed']">
              <p v-if="results.rebond.success">
                ✓ {{ results.rebond.message }}
                <span v-if="results.rebond.all_stable"> (Todas estáveis)</span>
                <span v-else> (Algumas instáveis)</span>
              </p>
              <p v-else>
                ✗ {{ results.rebond.message || results.rebond.error }}
              </p>
            </div>
            <div v-if="results.rebond.molecule" class="molecule-viewer-container">
              <MoleculeViewer :molecule="results.rebond.molecule" :size="300" />
            </div>
            <button v-if="results.rebond.molecule" @click="loadRebondResult" class="btn-copy">
              📋 Carregar Resultado
            </button>
          </div>

          <!-- Erros -->
          <div v-if="results.reorganize_error || results.analyze_error" class="result-card error">
            <h3>❌ Erros</h3>
            <div v-if="results.reorganize_error" class="error-message">
              <strong>Reorganização:</strong> {{ results.reorganize_error }}
            </div>
            <div v-if="results.analyze_error" class="error-message">
              <strong>Análise:</strong> {{ results.analyze_error }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch, onMounted, computed } from 'vue';
import MoleculeViewer from '../components/MoleculeViewer.vue';
import { saveDiscovery as saveDiscoveryAPI, calculateMolecularFormula, getAllDiscoveries } from '../services/api.js';
import { moleculeExistsInList } from '../utils/moleculeComparison.js';

export default {
  name: 'MoleculeBuilder',
  components: {
    MoleculeViewer
  },
  setup() {
    const activeTab = ref('visual');
    const moleculeJson = ref('');
    const currentMolecule = ref(null);
    const results = ref(null);
    const isProcessing = ref(false);
    const showAddParticle = ref(false);
    const showAddBond = ref(false);
    const knownMolecules = ref([]);

    const moleculeData = reactive({
      particles: [],
      bonds: []
    });

    const newParticle = reactive({
      type: 'circle',
      polarity: '+'
    });

    const newBond = reactive({
      from: '',
      to: '',
      multiplicity: 1
    });

    // Sincronizar moleculeData com currentMolecule
    watch(() => moleculeData, () => {
      updateCurrentMolecule();
      updateJsonFromData();
    }, { deep: true });

    const updateCurrentMolecule = () => {
      if (moleculeData.particles.length > 0) {
        currentMolecule.value = {
          particles: [...moleculeData.particles],
          bonds: [...moleculeData.bonds]
        };
      } else {
        currentMolecule.value = null;
      }
    };

    const updateJsonFromData = () => {
      moleculeJson.value = JSON.stringify({
        particles: moleculeData.particles,
        bonds: moleculeData.bonds
      }, null, 2);
    };

    const updateFromJson = () => {
      try {
        const parsed = JSON.parse(moleculeJson.value);
        if (parsed.particles && parsed.bonds) {
          moleculeData.particles = [...parsed.particles];
          moleculeData.bonds = [...parsed.bonds];
          updateCurrentMolecule();
        }
      } catch (e) {
        // JSON inválido, ignorar
      }
    };

    const loadFromJson = () => {
      updateFromJson();
      activeTab.value = 'visual';
    };

    const loadFromVisual = () => {
      updateJsonFromData();
      activeTab.value = 'json';
    };

    const loadExample = () => {
      moleculeData.particles = [
        { id: 'p0', type: 'circle', polarity: '+', x: 0, y: 0 },
        { id: 'p1', type: 'square', polarity: '-', x: 2, y: 0 },
        { id: 'p2', type: 'triangle', polarity: '+', x: 4, y: 0 }
      ];
      moleculeData.bonds = [
        { from: 'p0', to: 'p1', multiplicity: 1 },
        { from: 'p1', to: 'p2', multiplicity: 1 }
      ];
      updateJsonFromData();
    };

    const clearEditor = () => {
      moleculeData.particles = [];
      moleculeData.bonds = [];
      moleculeJson.value = '';
      currentMolecule.value = null;
      results.value = null;
    };

    const getTypeLabel = (type) => {
      const labels = {
        circle: '○',
        square: '□',
        triangle: '△',
        pentagon: '⬠'
      };
      return labels[type] || type;
    };

    const addParticle = () => {
      // Gerar ID automático
      const newId = `p${moleculeData.particles.length}`;
      
      // Gerar posição automática (em grid simples)
      const count = moleculeData.particles.length;
      const x = (count % 5) * 3; // 0, 3, 6, 9, 12...
      const y = Math.floor(count / 5) * 3; // 0, 0, 0, 0, 0, 3, 3, 3...

      moleculeData.particles.push({
        id: newId,
        type: newParticle.type,
        polarity: newParticle.polarity,
        x: x,
        y: y
      });

      // Reset form (mantém tipo e polaridade para facilitar adicionar várias)
      showAddParticle.value = false;
    };

    const removeParticle = (index) => {
      const particle = moleculeData.particles[index];
      
      // Remover bonds relacionados
      moleculeData.bonds = moleculeData.bonds.filter(
        b => b.from !== particle.id && b.to !== particle.id
      );

      moleculeData.particles.splice(index, 1);
    };

    const editParticle = (index) => {
      const particle = moleculeData.particles[index];
      const newX = prompt(`X atual: ${particle.x}\nNovo X:`, particle.x);
      const newY = prompt(`Y atual: ${particle.y}\nNovo Y:`, particle.y);
      
      if (newX !== null && newY !== null) {
        particle.x = parseInt(newX) || 0;
        particle.y = parseInt(newY) || 0;
      }
    };

    const addBond = () => {
      if (!newBond.from || !newBond.to) {
        alert('Selecione partículas de origem e destino!');
        return;
      }

      if (newBond.from === newBond.to) {
        alert('Uma partícula não pode se ligar com ela mesma!');
        return;
      }

      // Verificar se bond já existe
      const exists = moleculeData.bonds.some(
        b => (b.from === newBond.from && b.to === newBond.to) ||
             (b.from === newBond.to && b.to === newBond.from)
      );

      if (exists) {
        alert('Ligação já existe!');
        return;
      }

      moleculeData.bonds.push({
        from: newBond.from,
        to: newBond.to,
        multiplicity: newBond.multiplicity
      });

      // Reset form
      newBond.from = '';
      newBond.to = '';
      newBond.multiplicity = 1;
      showAddBond.value = false;
    };

    const removeBond = (index) => {
      moleculeData.bonds.splice(index, 1);
    };

    const processMolecule = async (actions) => {
      if (!currentMolecule.value) {
        alert('Nenhuma molécula para processar!');
        return;
      }

      isProcessing.value = true;

      try {
        const response = await fetch('http://localhost:5000/api/molecule/validate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            molecule: currentMolecule.value,
            actions: actions
          })
        });

        const data = await response.json();

        if (data.success) {
          results.value = data.results;
          
          if (data.results.reorganized) {
            currentMolecule.value = data.results.reorganized;
            // Atualizar moleculeData com resultado reorganizado
            moleculeData.particles = [...data.results.reorganized.particles];
            moleculeData.bonds = [...data.results.reorganized.bonds];
          } else if (currentMolecule.value) {
            // Se não há reorganização, manter a molécula atual
            // currentMolecule já está definido
          }
          
          // Recarregar descobertas para verificação atualizada
          await loadKnownMolecules();
        } else {
          alert(`Erro: ${data.error}`);
        }
      } catch (error) {
        alert(`Erro ao processar: ${error.message}`);
      } finally {
        isProcessing.value = false;
      }
    };

    const validateMolecule = () => processMolecule(['validate']);
    const reorganizeMolecule = () => processMolecule(['reorganize']);
    const analyzeMolecule = () => processMolecule(['analyze']);
    const runAll = () => processMolecule(['validate', 'reorganize', 'analyze']);

    const testRebond = async () => {
      if (!currentMolecule.value || moleculeData.particles.length === 0) {
        alert('Adicione partículas primeiro!');
        return;
      }

      isProcessing.value = true;

      try {
        const response = await fetch('http://localhost:5000/api/molecule/rebond', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            particles: moleculeData.particles
          })
        });

        const data = await response.json();

        if (!results.value) {
          results.value = {};
        }

        results.value.rebond = data;

        if (data.success && data.molecule) {
          // Mostrar resultado na visualização
          currentMolecule.value = data.molecule;
        }
      } catch (error) {
        alert(`Erro ao testar rebond: ${error.message}`);
      } finally {
        isProcessing.value = false;
      }
    };

    const loadRebondResult = () => {
      if (results.value?.rebond?.molecule) {
        moleculeData.particles = [...results.value.rebond.molecule.particles];
        moleculeData.bonds = [...results.value.rebond.molecule.bonds];
        updateJsonFromData();
        alert('✅ Resultado do rebond carregado!');
      }
    };

    const copyReorganized = () => {
      if (results.value?.reorganized) {
        const json = JSON.stringify(results.value.reorganized, null, 2);
        navigator.clipboard.writeText(json).then(() => {
          alert('✅ JSON copiado para área de transferência!');
        });
      }
    };

    const loadKnownMolecules = async () => {
      try {
        const response = await getAllDiscoveries();
        if (response.success) {
          // Extrair apenas as moléculas das descobertas
          knownMolecules.value = (response.data || []).map(d => d.molecule || d);
        }
      } catch (error) {
        console.error('Erro ao carregar descobertas:', error);
      }
    };

    const saveToLibrary = async () => {
      const molecule = moleculeToCheck.value;
      
      if (!molecule) {
        alert('Nenhuma molécula para salvar! Execute a análise primeiro.');
        return;
      }
      
      // Validar molécula antes de salvar
      if (!molecule.particles || molecule.particles.length === 0) {
        alert('Molécula inválida: sem partículas!');
        return;
      }

      // Verificar se já existe nas descobertas
      if (moleculeExistsInList(molecule, knownMolecules.value)) {
        alert('❌ Esta molécula já foi descoberta! Não é possível adicioná-la novamente.');
        return;
      }

      try {
        // Calcular fórmula molecular
        const formula = calculateMolecularFormula(molecule);
        
        if (!formula) {
          alert('Erro ao calcular fórmula molecular!');
          return;
        }

        // Pedir nome (opcional)
        const name = prompt('Digite um nome para esta descoberta (ou deixe em branco):');
        const moleculeName = name && name.trim() ? name.trim() : null;

        // Salvar descoberta
        const response = await saveDiscoveryAPI(molecule, formula, moleculeName);

        if (response.success) {
          alert('✅ Molécula adicionada à biblioteca de descobertas!');
          // Recarregar lista de descobertas
          await loadKnownMolecules();
        } else {
          // Verificar se é erro de duplicata
          const errorMsg = response.error || 'Erro desconhecido';
          if (errorMsg.includes('já foi descoberta') || errorMsg.includes('já existe')) {
            alert('❌ Esta molécula já foi descoberta! Não é possível adicioná-la novamente.');
            // Recarregar lista para garantir sincronização
            await loadKnownMolecules();
          } else {
            alert(`❌ Erro ao salvar: ${errorMsg}`);
          }
        }
      } catch (error) {
        console.error('Erro ao salvar descoberta:', error);
        alert(`❌ Erro ao salvar descoberta: ${error.message}`);
      }
    };

    const getTopologyLabel = (topology) => {
      const labels = {
        'single': '● Única',
        'linear': '━ Linear',
        'Y': 'Y Ramificação',
        'X': 'X Cruzamento',
        'tree': '⋈ Árvore',
        'cycle': '○ Ciclo',
        'mista': '◈ Mista'
      };
      return labels[topology] || topology;
    };

    // Obter a molécula a ser verificada (reorganizada se existir, senão a atual)
    const moleculeToCheck = computed(() => {
      // Prioridade 1: Molécula reorganizada
      if (results.value?.reorganized) {
        return results.value.reorganized;
      }
      // Prioridade 2: Molécula atual
      if (currentMolecule.value && currentMolecule.value.particles && currentMolecule.value.particles.length > 0) {
        return currentMolecule.value;
      }
      return null;
    });

    // Verificar se a molécula já é conhecida
    const isMoleculeKnown = computed(() => {
      const molecule = moleculeToCheck.value;
      if (!molecule || !molecule.particles || molecule.particles.length === 0) {
        return false;
      }
      if (!knownMolecules.value || knownMolecules.value.length === 0) {
        return false;
      }
      try {
        const exists = moleculeExistsInList(molecule, knownMolecules.value);
        return exists;
      } catch (error) {
        console.error('Erro ao verificar se molécula é conhecida:', error);
        return false;
      }
    });

    return {
      activeTab,
      moleculeJson,
      currentMolecule,
      results,
      isProcessing,
      moleculeData,
      newParticle,
      newBond,
      showAddParticle,
      showAddBond,
      loadExample,
      clearEditor,
      loadFromJson,
      loadFromVisual,
      updateFromJson,
      getTypeLabel,
      addParticle,
      removeParticle,
      editParticle,
      addBond,
      removeBond,
      validateMolecule,
      reorganizeMolecule,
      analyzeMolecule,
      testRebond,
      runAll,
      copyReorganized,
      saveToLibrary,
      loadRebondResult,
      getTopologyLabel,
      isMoleculeKnown
    };

    // Carregar descobertas ao montar componente
    onMounted(async () => {
      await loadKnownMolecules();
    });

    return {
      activeTab,
      moleculeJson,
      currentMolecule,
      results,
      isProcessing,
      moleculeData,
      newParticle,
      newBond,
      showAddParticle,
      showAddBond,
      loadExample,
      clearEditor,
      loadFromJson,
      loadFromVisual,
      updateFromJson,
      getTypeLabel,
      addParticle,
      removeParticle,
      editParticle,
      addBond,
      removeBond,
      validateMolecule,
      reorganizeMolecule,
      analyzeMolecule,
      testRebond,
      runAll,
      copyReorganized,
      saveToLibrary,
      loadRebondResult,
      getTopologyLabel,
      isMoleculeKnown,
      moleculeToCheck
    };
  }
};
</script>

<style scoped>
.builder-container {
  max-width: 1600px;
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

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.tab {
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  font-size: 1rem;
  font-weight: 600;
  color: #7f8c8d;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
}

.tab:hover {
  color: #2c3e50;
}

.tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.builder-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  min-height: 600px;
}

.editor-panel {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow-y: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.panel-header h2 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin: 0;
}

.editor-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-example, .btn-clear, .btn-load {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-example {
  background: #e3f2fd;
  color: #1976d2;
}

.btn-example:hover {
  background: #bbdefb;
}

.btn-clear {
  background: #ffebee;
  color: #c62828;
}

.btn-clear:hover {
  background: #ffcdd2;
}

.btn-load {
  background: #f3e5f5;
  color: #7b1fa2;
}

.btn-load:hover {
  background: #e1bee7;
}

.json-editor {
  flex: 1;
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  resize: none;
  min-height: 400px;
}

.json-editor:focus {
  outline: none;
  border-color: #667eea;
}

.section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.section:last-of-type {
  border-bottom: none;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  font-size: 1.1rem;
  color: #2c3e50;
  margin: 0;
}

.btn-add {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
}

.btn-add:hover {
  background: #5568d3;
}

.form-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.form-card.visual-form {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.75rem;
}

.form-row label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-row input, .form-row select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
}

.form-row input:focus, .form-row select:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-save {
  padding: 0.5rem 1rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-save:hover {
  background: #45a049;
}

.btn-cancel {
  padding: 0.5rem 1rem;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-cancel:hover {
  background: #da190b;
}

.list-container {
  max-height: 300px;
  overflow-y: auto;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.item-id {
  font-weight: 700;
  color: #667eea;
}

.item-type {
  font-size: 1.2rem;
}

.item-polarity {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
}

.item-polarity.positive {
  background: #ffebee;
  color: #c62828;
}

.item-polarity.negative {
  background: #e3f2fd;
  color: #1976d2;
}

.item-position {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.bond-from, .bond-to {
  font-weight: 700;
  color: #667eea;
}

.bond-arrow {
  color: #7f8c8d;
}

.bond-multiplicity {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-remove {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-edit {
  background: #fff3e0;
  color: #e65100;
}

.btn-edit:hover {
  background: #ffe0b2;
}

.btn-remove {
  background: #ffebee;
  color: #c62828;
}

.btn-remove:hover {
  background: #ffcdd2;
}

.empty-state {
  text-align: center;
  color: #95a5a6;
  padding: 2rem;
  font-style: italic;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid #e0e0e0;
}

.btn-action {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  background: #f0f0f0;
  color: #333;
}

.btn-action:hover:not(:disabled) {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.btn-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-action.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  grid-column: 1 / -1;
}

.btn-action.btn-primary:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.results-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-height: 90vh;
  overflow-y: auto;
}

.visualization-section, .results-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.visualization-section h2, .results-section h2 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.molecule-display {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.molecule-viewer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
}

.placeholder {
  text-align: center;
  color: #95a5a6;
}

.result-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.result-card h3 {
  font-size: 1.1rem;
  color: #2c3e50;
  margin-bottom: 0.75rem;
}

.result-card.error {
  background: #fee;
  border: 2px solid #fcc;
}

.validation-result {
  padding: 0.5rem;
  border-radius: 6px;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.validation-result.valid {
  background: #d4edda;
  color: #155724;
}

.validation-result.invalid {
  background: #f8d7da;
  color: #721c24;
}

.result-card pre {
  background: white;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  overflow-x: auto;
  margin-top: 0.5rem;
}

.structure-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: white;
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

.info-row .value.cycle-yes {
  color: #667eea;
}

.info-row .value.cycle-no {
  color: #95a5a6;
}

.info-row .value.topology {
  color: #2c3e50;
}

.error-message {
  color: #721c24;
  margin-bottom: 0.5rem;
}

.btn-copy {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-copy:hover {
  background: #5568d3;
}

.reorganized-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.btn-save-library {
  padding: 0.5rem 1rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-save-library:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
}

.btn-save-library:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.discovery-status {
  margin-bottom: 1rem;
  text-align: center;
}

.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.status-badge.known {
  background: #e3f2fd;
  color: #1976d2;
  border: 2px solid #1976d2;
}

.status-badge.new {
  background: #fff3e0;
  color: #e65100;
  border: 2px solid #ff9800;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.visual-selector {
  margin-bottom: 1.5rem;
}

.selector-label {
  display: block;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.type-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 80px;
}

.type-btn:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.type-btn.active {
  border-color: #667eea;
  background: #f3f4ff;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.type-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.type-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #2c3e50;
}

.polarity-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.polarity-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  border: 3px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 100px;
}

.polarity-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.polarity-btn.positive {
  border-color: #ffcdd2;
}

.polarity-btn.positive:hover {
  border-color: #ef5350;
  background: #ffebee;
}

.polarity-btn.positive.active {
  border-color: #c62828;
  background: #ffebee;
  box-shadow: 0 2px 8px rgba(198, 40, 40, 0.3);
}

.polarity-btn.negative {
  border-color: #bbdefb;
}

.polarity-btn.negative:hover {
  border-color: #42a5f5;
  background: #e3f2fd;
}

.polarity-btn.negative.active {
  border-color: #1976d2;
  background: #e3f2fd;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);
}

.polarity-icon {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.polarity-btn.positive .polarity-icon {
  color: #c62828;
}

.polarity-btn.negative .polarity-icon {
  color: #1976d2;
}

.polarity-name {
  font-size: 1rem;
  font-weight: 600;
}

.polarity-btn.positive .polarity-name {
  color: #c62828;
}

.polarity-btn.negative .polarity-name {
  color: #1976d2;
}

.rebond-result {
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.rebond-result.success {
  background: #d4edda;
  color: #155724;
}

.rebond-result.failed {
  background: #f8d7da;
  color: #721c24;
}
</style>
