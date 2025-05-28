from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secure_key'

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pedidos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redireciona para login se não estiver logado

# Modelos
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    sabor = db.Column(db.String(100), nullable=False)

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

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
@login_required
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
        username = request.form.get('username')
        senha = request.form['senha']
        user = Usuario.query.filter_by(username=username, password=senha).first()
        if user:
            session['logged_in'] = True
            login_user(user)
            flash("✅ Login bem-sucedido!")
            return redirect(url_for('index'))
        else:
            flash("❌ Nome de usuário ou senha inválidos.")
    return render_template('login.html')


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("👋 Você saiu do sistema.")
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form['senha']
        if Usuario.query.filter_by(username=username).first():
            flash("⚠️ Nome de usuário já existe.")
            return redirect(url_for('registro'))
        novo_usuario = Usuario(username=username, password=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash("✅ Registro realizado com sucesso!")
        return redirect(url_for('login'))
    return render_template('registro.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
