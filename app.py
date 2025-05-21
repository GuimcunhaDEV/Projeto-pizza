from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # troque para algo seguro

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pedidos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do banco de dados
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    sabor = db.Column(db.String(100), nullable=False)

# Decorador para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Você precisa estar logado para acessar essa página.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota principal
@app.route('/')
def index():
    pedidos = Pedido.query.all()
    return render_template('index.html', pedidos=pedidos)

# Adicionar pedido
@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['cliente']
    sabor = request.form['sabor']
    novo_pedido = Pedido(cliente=nome, sabor=sabor)
    db.session.add(novo_pedido)
    db.session.commit()
    flash(f"✅ Pedido de {nome} adicionado com sabor {sabor}!")
    return redirect(url_for('index'))

# Entregar (remover) pedido - protegido
@app.route('/entregar/<int:id>')
@login_required
def entregar(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    flash(f"🍕 Pedido #{id} entregue e removido da lista.")
    return redirect(url_for('index'))

# Editar pedido - protegido
@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    pedido = Pedido.query.get_or_404(id)
    if request.method == "POST":
        novo_sabor = request.form["sabor"]
        if novo_sabor:
            pedido.sabor = novo_sabor
            db.session.commit()
            flash(f"Pedido #{id} atualizado para '{novo_sabor}'!")
            return redirect(url_for("index"))
        else:
            flash("⚠️ O sabor não pode ficar vazio.")
    return render_template("editar.html", pedido=pedido)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if user == 'admin' and password == 'admin':
            session['logged_in'] = True
            flash("Login realizado com sucesso!")
            return redirect(url_for('index'))
        else:
            flash("Usuário ou senha inválidos!")
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("Deslogado com sucesso!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
