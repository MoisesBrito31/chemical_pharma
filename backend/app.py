from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from data.molecules import (
    get_molecules_by_mass, 
    get_all_molecules, 
    get_molecule_by_id,
    calculate_molecule_properties,
    get_available_masses,
    PARTICLE_TYPES,
    find_molecule
)
from core.synthesis import synthesize
from core.validator import validate_molecule
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
    
    discovery_id = add_discovery_to_save(save_id, molecule, formula, name)
    
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

   
    
    
    
    
 