from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    adicionar_usuario(nome)
    return "Usuário cadastrado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
