from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pedidos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para flash messages

db = SQLAlchemy(app)

# Modelo do banco de dados
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    sabor = db.Column(db.String(100), nullable=False)

# Rota principal (somente GET)
@app.route('/')
def index():
    pedidos = Pedido.query.all()
    return render_template('index.html', pedidos=pedidos)

# Adicionar pedido (POST)
@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['cliente']
    sabor = request.form['sabor']
    if not nome or not sabor:
        flash("⚠️ Nome e sabor são obrigatórios!")
        return redirect(url_for('index'))
    novo_pedido = Pedido(cliente=nome, sabor=sabor)
    db.session.add(novo_pedido)
    db.session.commit()
    flash(f"✅ Pedido de {nome} adicionado!")
    return redirect(url_for('index'))

# Entregar (remover) pedido
@app.route('/entregar/<int:id>')
def entregar(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    flash(f"🍕 Pedido #{id} entregue e removido!")
    return redirect(url_for('index'))

# Editar pedido
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    pedido = Pedido.query.get_or_404(id)
    if request.method == "POST":
        novo_sabor = request.form["sabor"]
        if novo_sabor:
            pedido.sabor = novo_sabor
            db.session.commit()
            flash(f"✏️ Pedido #{id} atualizado para '{novo_sabor}'!")
            return redirect(url_for("index"))
        else:
            flash("⚠️ O sabor não pode ficar vazio.")
    return render_template("editar.html", pedido=pedido)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem
    app.run(debug=True)
