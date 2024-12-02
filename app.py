from flask import Flask, jsonify, request
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

Livros = [
    {
        'id': 1,
        'Título': 'O Senhor dos Anéis',
        'Autor': 'J.R.R. Tolkien'
    },
    {
        'id': 2,
        'Título': 'Harry Potter e a pedra filosofal',
        'Autor': 'J.K Rowling'
    },
    {
        'id': 3,
        'Título': 'Hábitos Atômicos',
        'Autor': 'James Clear'
    },
]

# Consultar todos os livros
@app.route('/livros', methods=['GET'])
def obter_livros():
    logging.info('Requisição para obter todos os livros.')
    return jsonify(Livros)

# Consultar por ID
@app.route('/livros/<int:id>', methods=['GET'])
def livro_por_id(id):
    logging.info(f'Requisição para obter livro com ID {id}.')
    for livro in Livros:
        if livro.get('id') == id:
            logging.info(f'Livro encontrado: {livro}')
            return jsonify(livro)
    logging.warning(f'Livro com ID {id} não encontrado.')
    return jsonify({'erro': f'Livro com ID {id} não encontrado.'}), 404

# Editar livro
@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_id(id):
    livro_alterado = request.get_json()
    for indice, livro in enumerate(Livros):
        if livro.get('id') == id:
            Livros[indice].update(livro_alterado)
            logging.info(f'Livro com ID {id} atualizado: {Livros[indice]}')
            return jsonify(Livros[indice])
    logging.warning(f'Tentativa de editar livro com ID {id} que não existe.')
    return jsonify({'erro': f'Livro com ID {id} não encontrado.'}), 404

# Criar novo livro
@app.route('/livros', methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()
    logging.info('Requisição para adicionar novo livro.')
    novo_livro['id'] = max([livro['id'] for livro in Livros]) + 1 if Livros else 1
    Livros.append(novo_livro)
    logging.info(f'Novo livro adicionado: {novo_livro}')
    return jsonify(novo_livro), 201

# Excluir livro
@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    for indice, livro in enumerate(Livros):
        if livro.get('id') == id:
            livro_excluido = Livros.pop(indice)
            logging.info(f'Livro com ID {id} excluído: {livro_excluido}')
            return jsonify({'mensagem': f'Livro com ID {id} excluído.'})
    logging.warning(f'Tentativa de excluir livro com ID {id} que não existe.')
    return jsonify({'erro': f'Livro com ID {id} não encontrado.'}), 404

# Inicialização do servidor
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
