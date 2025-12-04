from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import copy
import json
from data.molecules import (
    get_molecules_by_mass, 
    get_all_molecules, 
    get_molecule_by_id,
    calculate_molecule_properties,
    get_available_masses,
    PARTICLE_TYPES,
    find_molecule
)
from core.synthesis import synthesize, reorganize_positions, rebond_molecule, calculate_connections
from core.validator import validate_molecule
from core.generator import generate_molecules
from core.analyzer import get_molecule_properties
from core.molecule_analyzer import analyze_molecule_structure
from core.molecule_comparison import are_molecules_identical
from data.synthesis_results import (
    get_synthesis_result,
    save_synthesis_result,
    get_all_results,
    get_stats,
    clear_cache
)
from data.discovered_molecules import (
    add_discovery,
    get_all_discoveries,
    get_discovery,
    clear_discoveries,
    delete_discovery,
    get_stats as get_discovery_stats
)
from data.saves import (
    get_all_saves,
    create_save,
    get_save,
    delete_save,
    set_active_save,
    get_active_save_id,
    get_active_save,
    update_save_stats,
    add_discovery_to_save
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chemical-pharma-secret-key'
CORS(app)

# Inicializar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# ============================================
# ROTAS HTTP (REST API)
# ============================================

# Rota principal - serve o HTML de teste
@app.route('/')
def index():
    return render_template('test.html')

# API: Listar todas as moléculas
@app.route('/api/molecules', methods=['GET'])
def api_get_all_molecules():
    molecules = get_all_molecules()
    return jsonify({
        'success': True,
        'data': molecules
    })

# API: Listar moléculas por massa
@app.route('/api/molecules/mass/<int:mass>', methods=['GET'])
def api_get_molecules_by_mass(mass):
    molecules = get_molecules_by_mass(mass)
    return jsonify({
        'success': True,
        'mass': mass,
        'count': len(molecules),
        'data': molecules
    })

# API: Obter massas disponíveis
@app.route('/api/molecules/masses', methods=['GET'])
def api_get_available_masses():
    masses = get_available_masses()
    return jsonify({
        'success': True,
        'data': masses
    })

# API: Validar molécula
@app.route('/api/molecules/validate', methods=['POST'])
def api_validate_molecule():
    molecule = request.json
    is_valid, errors = validate_molecule(molecule)
    
    return jsonify({
        'success': True,
        'valid': is_valid,
        'errors': errors
    })

# API: Calcular propriedades de molécula
@app.route('/api/molecules/properties', methods=['POST'])
def api_calculate_properties():
    molecule = request.json
    properties = calculate_molecule_properties(molecule)
    
    return jsonify({
        'success': True,
        'data': properties
    })

# ============================================
# SYNTHESIS ROUTES
# ============================================

@app.route('/api/synthesis/mix', methods=['POST'])
def api_synthesize():
    """Realiza síntese de duas moléculas"""
    data = request.json
    mol_a_id = data.get('molecule_a_id')
    mol_b_id = data.get('molecule_b_id')
    
    if not mol_a_id or not mol_b_id:
        return jsonify({
            'success': False,
            'error': 'IDs das moléculas são obrigatórios'
        }), 400
    
    # Buscar moléculas no banco de dados (predefinidas) ou descobertas
    molecule_a = find_molecule(mol_a_id)
    molecule_b = find_molecule(mol_b_id)
    
    if not molecule_a:
        return jsonify({
            'success': False,
            'error': f'Molécula A ({mol_a_id}) não encontrada'
        }), 404
    
    if not molecule_b:
        return jsonify({
            'success': False,
            'error': f'Molécula B ({mol_b_id}) não encontrada'
        }), 404
    
    # Verificar se já existe no cache
    cache_key = f"{mol_a_id}+{mol_b_id}"
    cached = get_synthesis_result(cache_key)
    if cached:
        return jsonify(cached)
    
    # Realizar síntese
    result = synthesize(molecule_a, molecule_b)
    
    # Salvar no cache
    save_synthesis_result(cache_key, result)
    
    # Se síntese foi bem-sucedida, incrementar contador do save
    if result.get('success'):
        save_id = get_active_save_id()
        if save_id:
            update_save_stats(save_id, syntheses_increment=1)
    
    return jsonify(result)

@app.route('/api/synthesis/validate', methods=['POST'])
def api_validate_synthesis():
    """Valida se uma síntese é possível"""
    data = request.json
    molecule_a = data.get('molecule_a')
    molecule_b = data.get('molecule_b')
    
    if not molecule_a or not molecule_b:
        return jsonify({
            'success': False,
            'error': 'Ambas as moléculas são obrigatórias'
        }), 400
    
    result = synthesize(molecule_a, molecule_b)
    
    return jsonify({
        'success': True,
        'can_synthesize': result['success'],
        'reason': result.get('details', {}).get('reason', 'unknown')
    })

@app.route('/api/synthesis/results', methods=['GET'])
def api_get_synthesis_results():
    """Retorna todos os resultados de síntese armazenados"""
    results = get_all_results()
    return jsonify({
        'success': True,
        'count': len(results),
        'data': results
    })

@app.route('/api/synthesis/stats', methods=['GET'])
def api_get_synthesis_stats():
    """Retorna estatísticas sobre sínteses realizadas"""
    stats = get_stats()
    return jsonify({
        'success': True,
        'data': stats
    })

@app.route('/api/synthesis/cache/clear', methods=['DELETE'])
def api_clear_synthesis_cache():
    """Limpa o cache de sínteses"""
    clear_cache()
    return jsonify({
        'success': True,
        'message': 'Cache de sínteses limpo com sucesso'
    })

@app.route('/api/synthesis/auto', methods=['POST'])
def api_auto_synthesis():
    """
    Realiza sínteses automáticas entre uma molécula e um grupo de moléculas.
    
    Body: {
        'molecule_a_id': str,  # ID da molécula base
        'molecule_ids': [str] | null,  # Lista de IDs ou null para filtrar por massa
        'filter_mass': int | null  # Se fornecido, filtra moléculas por esta massa
    }
    """
    data = request.json
    mol_a_id = data.get('molecule_a_id')
    molecule_ids = data.get('molecule_ids')  # Lista específica de IDs
    filter_mass = data.get('filter_mass')  # Filtrar por massa
    
    if not mol_a_id:
        return jsonify({
            'success': False,
            'error': 'ID da molécula A é obrigatório'
        }), 400
    
    # Buscar molécula A
    molecule_a = find_molecule(mol_a_id)
    if not molecule_a:
        return jsonify({
            'success': False,
            'error': f'Molécula A ({mol_a_id}) não encontrada'
        }), 404
    
    # Determinar lista de moléculas B
    molecules_b = []
    
    if molecule_ids:
        # Usar lista específica fornecida
        for mol_id in molecule_ids:
            mol_b = find_molecule(mol_id)
            if mol_b:
                molecules_b.append(mol_b)
    elif filter_mass:
        # Filtrar por massa
        molecules_by_mass = get_molecules_by_mass(filter_mass)
        molecules_b = molecules_by_mass.copy()
        
        # Adicionar descobertas da mesma massa
        save_id = get_active_save_id()
        if save_id:
            discoveries = get_all_discoveries(save_id)
            for disc in discoveries:
                mol = disc.get('molecule')
                if mol and len(mol.get('particles', [])) == filter_mass:
                    molecules_b.append(mol)
    else:
        return jsonify({
            'success': False,
            'error': 'É necessário fornecer molecule_ids ou filter_mass'
        }), 400
    
    if not molecules_b:
        return jsonify({
            'success': False,
            'error': 'Nenhuma molécula encontrada para síntese'
        }), 404
    
    # Realizar todas as sínteses
    results = []
    known_molecules = get_all_molecules()
    save_id = get_active_save_id()
    discovered_molecules = []
    if save_id:
        discoveries = get_all_discoveries(save_id)
        discovered_molecules = [d.get('molecule') for d in discoveries if d.get('molecule')]
    
    all_known_molecules = known_molecules + discovered_molecules
    
    for mol_b in molecules_b:
        mol_b_id = mol_b.get('id', 'unknown')
        
        # Cache key para verificar resultado já calculado
        cache_key = f"{mol_a_id}+{mol_b_id}"
        cached = get_synthesis_result(cache_key)
        
        if cached:
            result = cached
        else:
            # Realizar síntese
            result = synthesize(molecule_a, mol_b)
            save_synthesis_result(cache_key, result)
        
        # Determinar status do resultado (se houver)
        result_status = None
        if result.get('success'):
            result_molecule = result.get('result')
            is_multiple = result.get('multiple', False)
            
            if result_molecule:
                # Se for resultado múltiplo, a lista contém várias moléculas
                # Para múltiplas, não definimos status único (cada uma teria seu próprio)
                if is_multiple and isinstance(result_molecule, list):
                    # Resultado múltiplo - não definir status único
                    result_status = None
                elif not is_multiple and isinstance(result_molecule, dict):
                    # Resultado único - verificar status
                    # Verificar se é conhecida (base)
                    is_base = False
                    for base_mol in known_molecules:
                        if are_molecules_identical(result_molecule, base_mol):
                            is_base = True
                            break
                    
                    # Verificar se já foi descoberta
                    is_discovered = False
                    if not is_base:
                        for disc_mol in discovered_molecules:
                            if are_molecules_identical(result_molecule, disc_mol):
                                is_discovered = True
                                break
                    
                    if is_base:
                        result_status = 'Base'
                    elif is_discovered:
                        result_status = 'Descoberta'
                    else:
                        result_status = 'Desconhecida'
        
        results.append({
            'molecule_b': {
                'id': mol_b_id,
                'formula': calculate_molecule_properties(mol_b).get('formula', '?'),
                'mass': len(mol_b.get('particles', [])),
                'molecule': copy.deepcopy(mol_b)  # Incluir molécula completa
            },
            'result': result,
            'status': result_status
        })
    
    # Incrementar contador de sínteses bem-sucedidas
    successful_count = sum(1 for r in results if r['result'].get('success'))
    if successful_count > 0:
        save_id = get_active_save_id()
        if save_id:
            update_save_stats(save_id, syntheses_increment=successful_count)
    
    return jsonify({
        'success': True,
        'molecule_a': {
            'id': mol_a_id,
            'formula': calculate_molecule_properties(molecule_a).get('formula', '?'),
            'mass': len(molecule_a.get('particles', [])),
            'molecule': copy.deepcopy(molecule_a)  # Incluir molécula completa
        },
        'total_tested': len(results),
        'total_successful': successful_count,
        'results': results
    })

# ============================================
# DISCOVERIES ROUTES
# ============================================

@app.route('/api/discoveries', methods=['GET'])
def api_get_all_discoveries():
    """Retorna todas as descobertas do save ativo"""
    save_id = get_active_save_id()
    if not save_id:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 400
    
    discoveries = get_all_discoveries(save_id)
    return jsonify({
        'success': True,
        'count': len(discoveries),
        'data': discoveries
    })

@app.route('/api/discoveries', methods=['POST'])
def api_save_discovery():
    """Salva uma nova descoberta no save ativo"""
    save_id = get_active_save_id()
    if not save_id:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 400
    
    data = request.json
    molecule = data.get('molecule')
    formula = data.get('formula')
    name = data.get('name')
    
    if not molecule:
        return jsonify({
            'success': False,
            'error': 'Molécula é obrigatória'
        }), 400
    
    # Verificar se já existe
    from data.discovered_molecules import molecule_exists_in_discoveries
    if molecule_exists_in_discoveries(save_id, molecule):
        return jsonify({
            'success': False,
            'error': 'Esta molécula já foi descoberta!'
        }), 400
    
    discovery_id = add_discovery_to_save(save_id, molecule, formula, name)
    
    if discovery_id is None:
        return jsonify({
            'success': False,
            'error': 'Esta molécula já foi descoberta!'
        }), 400
    
    return jsonify({
        'success': True,
        'discovery_id': discovery_id,
        'message': 'Descoberta salva com sucesso!'
    })

@app.route('/api/discoveries/<string:discovery_id>', methods=['DELETE'])
def api_delete_discovery(discovery_id):
    """Deleta uma descoberta específica"""
    save_id = get_active_save_id()
    if not save_id:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 400
    
    success = delete_discovery(save_id, discovery_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Descoberta deletada com sucesso'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Descoberta não encontrada'
        }), 404

@app.route('/api/discoveries/clear', methods=['DELETE'])
def api_clear_discoveries():
    """Limpa todas as descobertas do save ativo"""
    save_id = get_active_save_id()
    if not save_id:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 400
    
    clear_discoveries(save_id)
    return jsonify({
        'success': True,
        'message': 'Todas as descobertas foram apagadas'
    })

@app.route('/api/discoveries/stats', methods=['GET'])
def api_get_discovery_stats():
    """Retorna estatísticas sobre descobertas do save ativo"""
    save_id = get_active_save_id()
    if not save_id:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 400
    
    stats = get_discovery_stats(save_id)
    return jsonify({
        'success': True,
        'data': stats
    })

# ============================================
# SAVES/PLAYER ROUTES
# ============================================

@app.route('/api/saves', methods=['GET'])
def api_get_all_saves():
    """Retorna todos os saves"""
    saves = get_all_saves()
    return jsonify({
        'success': True,
        'count': len(saves),
        'data': saves
    })

@app.route('/api/saves', methods=['POST'])
def api_create_save():
    """Cria um novo save"""
    data = request.json
    player_name = data.get('player_name')
    
    if not player_name:
        return jsonify({
            'success': False,
            'error': 'Nome do jogador é obrigatório'
        }), 400
    
    save_id = create_save(player_name)
    
    return jsonify({
        'success': True,
        'save_id': save_id,
        'message': f'Save criado para {player_name}!'
    })

@app.route('/api/saves/<string:save_id>/select', methods=['POST'])
def api_select_save(save_id):
    """Seleciona um save como ativo"""
    success = set_active_save(save_id)
    
    if success:
        save_data = get_save(save_id)
        return jsonify({
            'success': True,
            'save': save_data,
            'message': 'Save selecionado com sucesso!'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Save não encontrado'
        }), 404

@app.route('/api/saves/current', methods=['GET'])
def api_get_current_save():
    """Retorna o save atualmente ativo"""
    save_data = get_active_save()
    
    if save_data:
        return jsonify({
            'success': True,
            'data': save_data
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 404

@app.route('/api/saves/<string:save_id>', methods=['DELETE'])
def api_delete_save(save_id):
    """Deleta um save"""
    success = delete_save(save_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Save deletado com sucesso!'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Save não encontrado'
        }), 404

# ============================================
# PROPERTIES ROUTES
# ============================================

@app.route('/api/properties/profile', methods=['GET'])
def api_get_property_profile():
    """Retorna o perfil de propriedades do save ativo (sabores, cores, efeitos)"""
    from core.property_profiles import get_or_create_profile
    
    save_id = get_active_save_id()
    if not save_id:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 400
    
    profile = get_or_create_profile(save_id)
    
    # Retornar apenas os mapeamentos (não incluir dados sensíveis)
    # Converter tuplas para strings JSON-friendly para chaves de dicionário
    multiplicity_color_map = {}
    for key, value in profile.get('multiplicity_color_map', {}).items():
        # Converter tupla para string JSON-friendly
        if isinstance(key, tuple):
            key_str = json.dumps(sorted(key))
        elif isinstance(key, list):
            key_str = json.dumps(sorted(key))
        else:
            key_str = str(key)
        multiplicity_color_map[key_str] = value
    
    # Converter padrões de efeitos (tuplas) para listas
    effect_patterns = {}
    for effect_name, patterns in profile.get('effect_patterns', {}).items():
        effect_patterns[effect_name] = [
            list(pattern) if isinstance(pattern, tuple) else pattern
            for pattern in patterns
        ]
    
    return jsonify({
        'success': True,
        'data': {
            'topology_flavor_map': profile.get('topology_flavor_map', {}),
            'multiplicity_color_map': multiplicity_color_map,
            'effect_patterns': effect_patterns
        }
    })

@app.route('/api/properties/profile/regenerate', methods=['POST'])
def api_regenerate_property_profile():
    """Força a regeneração do perfil de propriedades do save ativo"""
    from core.property_profiles import get_or_create_profile, delete_profile
    
    save_id = get_active_save_id()
    if not save_id:
        return jsonify({
            'success': False,
            'error': 'Nenhum save ativo'
        }), 400
    
    try:
        # Deletar perfil antigo
        delete_profile(save_id)
        
        # Gerar novo perfil
        profile = get_or_create_profile(save_id)
        
        return jsonify({
            'success': True,
            'message': 'Perfil regenerado com sucesso'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/molecules/observable-properties', methods=['POST'])
def api_get_observable_properties():
    """Retorna as propriedades observáveis de uma molécula (sabor, aparência, efeitos)"""
    from core.molecule_properties import calculate_molecule_observable_properties
    from core.property_profiles import get_or_create_profile
    
    data = request.json
    molecule = data.get('molecule')
    
    if not molecule:
        return jsonify({
            'success': False,
            'error': 'Molécula é obrigatória'
        }), 400
    
    try:
        # Obter perfil do save para calcular efeitos
        save_id = get_active_save_id()
        profile = get_or_create_profile(save_id) if save_id else None
        
        # Calcular todas as propriedades observáveis
        observable_props = calculate_molecule_observable_properties(molecule, profile)
        
        return jsonify({
            'success': True,
            'data': observable_props
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# SIMULATION ROUTES
# ============================================

@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    """
    Gera todas as moléculas possíveis com um tipo de partícula e massa específicos.
    
    Body: {
        'particle_type': int (1, 2, 3, 4),
        'mass': int
    }
    """
    data = request.json
    particle_type = data.get('particle_type')
    target_mass = data.get('mass')
    
    if particle_type is None or target_mass is None:
        return jsonify({
            'success': False,
            'error': 'Parâmetros particle_type e mass são obrigatórios'
        }), 400
    
    # Validar inputs (0 = qualquer tipo)
    if particle_type not in [0, 1, 2, 3, 4]:
        return jsonify({
            'success': False,
            'error': 'particle_type deve ser 0 (qualquer), 1, 2, 3 ou 4'
        }), 400
    
    if target_mass <= 0:
        return jsonify({
            'success': False,
            'error': 'mass deve ser maior que 0'
        }), 400
    
    # Gerar moléculas
    result = generate_molecules(particle_type, target_mass)
    
    # Buscar todas as moléculas conhecidas do banco de dados base
    known_molecules = get_all_molecules()
    
    # Buscar todas as descobertas do save ativo
    save_id = get_active_save_id()
    discovered_molecules = []
    if save_id:
        discoveries = get_all_discoveries(save_id)
        discovered_molecules = [d.get('molecule') for d in discoveries if d.get('molecule')]
    
    # Adicionar propriedades estruturais e verificar status de cada molécula
    if result['success'] and result['molecules']:
        for molecule in result['molecules']:
            props = get_molecule_properties(molecule)
            molecule['properties'] = props
            
            # Verificar se a molécula está no banco de dados base
            is_base = False
            for base_mol in known_molecules:
                if are_molecules_identical(molecule, base_mol):
                    is_base = True
                    break
            
            # Verificar se a molécula já foi descoberta pelo jogador
            is_discovered = False
            if not is_base:
                for disc_mol in discovered_molecules:
                    if are_molecules_identical(molecule, disc_mol):
                        is_discovered = True
                        break
            
            # Definir status
            if is_base:
                molecule['status'] = 'Base'
                molecule['is_known'] = True
                molecule['is_base'] = True
                molecule['is_discovered'] = False
            elif is_discovered:
                molecule['status'] = 'Descoberta'
                molecule['is_known'] = True
                molecule['is_base'] = False
                molecule['is_discovered'] = True
            else:
                molecule['status'] = 'Desconhecida'
                molecule['is_known'] = False
                molecule['is_base'] = False
                molecule['is_discovered'] = False
    
    return jsonify(result)

# ============================================
# MOLECULE BUILDER ROUTES
# ============================================

@app.route('/api/molecule/validate', methods=['POST'])
def api_builder_validate():
    """
    Valida e processa uma molécula customizada (JSON).
    Pode aplicar algoritmos de reorganização e análise.
    
    Body: {
        'molecule': {...},  # Molécula em JSON
        'actions': ['validate', 'reorganize', 'analyze']  # Ações a executar
    }
    """
    data = request.json
    molecule = data.get('molecule')
    actions = data.get('actions', ['validate'])
    
    if not molecule:
        return jsonify({
            'success': False,
            'error': 'Molécula não fornecida'
        }), 400
    
    result = {
        'success': True,
        'molecule': molecule,
        'results': {}
    }
    
    # Ação: Validar
    if 'validate' in actions:
        is_valid, errors = validate_molecule(molecule)
        result['results']['validation'] = {
            'valid': is_valid,
            'reason': '; '.join(errors) if errors else 'Molécula válida',
            'details': errors if errors else []
        }
    
    # Ação: Reorganizar posições
    if 'reorganize' in actions:
        try:
            molecule_copy = copy.deepcopy(molecule)
            reorganize_positions(molecule_copy)
            result['results']['reorganized'] = molecule_copy
        except Exception as e:
            result['results']['reorganize_error'] = str(e)
    
    # Ação: Analisar estrutura
    if 'analyze' in actions:
        try:
            structure = analyze_molecule_structure(molecule)
            result['results']['structure'] = structure
        except Exception as e:
            result['results']['analyze_error'] = str(e)
    
    return jsonify(result)

@app.route('/api/molecule/rebond', methods=['POST'])
def api_builder_rebond():
    """
    Testa a função rebond: recebe apenas partículas e tenta criar ligações válidas.
    
    Body: {
        'particles': [...]  # Apenas partículas, sem bonds
    }
    
    Returns: {
        'success': bool,
        'molecule': {...} ou None,
        'message': str
    }
    """
    data = request.json
    particles = data.get('particles', [])
    
    if not particles:
        return jsonify({
            'success': False,
            'error': 'Partículas não fornecidas'
        }), 400
    
    # Criar molécula com bonds vazios
    molecule = {
        'particles': copy.deepcopy(particles),
        'bonds': []
    }
    
    # Tentar criar ligações com rebond
    try:
        result = rebond_molecule(molecule)
        
        if result is None:
            return jsonify({
                'success': False,
                'molecule': None,
                'message': 'Não foi possível criar ligações válidas para estabilizar todas as partículas'
            })
        
        # Verificar se todas as partículas estão estáveis
        from data.molecules import PARTICLE_TYPES
        
        connection_count = calculate_connections(result)
        all_stable = True
        
        for particle in result['particles']:
            pid = particle['id']
            ptype = particle['type']
            max_conn = PARTICLE_TYPES[ptype]['connections']
            current_conn = connection_count.get(pid, 0)
            
            if current_conn != max_conn:
                all_stable = False
                break
        
        return jsonify({
            'success': True,
            'molecule': result,
            'all_stable': all_stable,
            'message': 'Ligações criadas com sucesso!' if all_stable else 'Ligações criadas, mas algumas partículas ainda instáveis'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'molecule': None,
            'error': str(e)
        }), 500

# ============================================
# WEBSOCKET EVENTS
# ============================================

@socketio.on('connect')
def handle_connect():
    print('✅ Cliente conectado!')
    emit('resposta', {'message': '✅ Conectado ao Servidor Flask+SocketIO'})

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Cliente desconectado!')

@socketio.on('enviar_mensagem')
def handle_message(data):
    mensagem_recebida = data.get('message', '')
    print(f'📩 Mensagem recebida: {mensagem_recebida}')
    
    resposta = f'Servidor recebeu: "{mensagem_recebida}"'
    emit('resposta', {'message': resposta})

# ============================================
# INICIAR SERVIDOR
# ============================================

if __name__ == '__main__':
    print('🚀 Servidor Flask iniciando...')
    print('📡 WebSocket habilitado')
    print('🌐 Acesse: http://localhost:5000')
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

  
 
   
 
   
 
   
 
   
 
 