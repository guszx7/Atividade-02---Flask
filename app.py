from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'atividade-flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    anuncios = db.relationship('Anuncio', backref='usuario', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    anuncios = db.relationship('Anuncio', backref='categoria', lazy=True)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    perguntas = db.relationship('Pergunta', backref='anuncio', cascade='all, delete-orphan')
    compras = db.relationship('Compra', backref='anuncio', cascade='all, delete-orphan')

class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'), nullable=False)
    usuario = db.relationship('Usuario')

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=date.today)
    quantidade = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    comprador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'), nullable=False)
    comprador = db.relationship('Usuario')

class Favorito(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'), primary_key=True)
    usuario = db.relationship('Usuario')
    anuncio = db.relationship('Anuncio')

with app.app_context():
    db.create_all()
    if not Usuario.query.first():
        db.session.add(Usuario(nome='Administrador', email='admin@exemplo.com', senha='1234'))
    if not Categoria.query.first():
        db.session.add_all([Categoria(nome='Eletrônicos'), Categoria(nome='Informática'), Categoria(nome='Esportes')])
    db.session.commit()
    if not Anuncio.query.first():
        db.session.add(Anuncio(titulo='Notebook usado', descricao='Notebook para estudos e trabalho.', preco=2500, usuario_id=1, categoria_id=2))
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html', anuncios=Anuncio.query.all())

# USUARIOS
@app.route('/usuarios')
def usuarios_index():
    return render_template('usuarios/index.html', usuarios=Usuario.query.all())

@app.route('/usuarios/novo', methods=['GET','POST'])
def usuario_novo():
    if request.method == 'POST':
        u = Usuario(nome=request.form['nome'], email=request.form['email'], senha=request.form['senha'])
        db.session.add(u); db.session.commit(); flash('Usuário cadastrado.')
        return redirect(url_for('usuarios_index'))
    return render_template('usuarios/form.html', usuario=None)

@app.route('/usuarios/<int:id>/editar', methods=['GET','POST'])
def usuario_editar(id):
    u = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        u.nome=request.form['nome']; u.email=request.form['email']; u.senha=request.form['senha']
        db.session.commit(); flash('Usuário atualizado.')
        return redirect(url_for('usuarios_index'))
    return render_template('usuarios/form.html', usuario=u)

@app.route('/usuarios/<int:id>/excluir', methods=['POST'])
def usuario_excluir(id):
    u=Usuario.query.get_or_404(id)
    if u.anuncios:
        flash('Não é possível excluir usuário com anúncios cadastrados.')
    else:
        db.session.delete(u); db.session.commit(); flash('Usuário excluído.')
    return redirect(url_for('usuarios_index'))

# CATEGORIAS
@app.route('/categorias')
def categorias_index():
    return render_template('categorias/index.html', categorias=Categoria.query.all())

@app.route('/categorias/novo', methods=['GET','POST'])
def categoria_novo():
    if request.method=='POST':
        db.session.add(Categoria(nome=request.form['nome'])); db.session.commit(); flash('Categoria cadastrada.')
        return redirect(url_for('categorias_index'))
    return render_template('categorias/form.html', categoria=None)

@app.route('/categorias/<int:id>/editar', methods=['GET','POST'])
def categoria_editar(id):
    c=Categoria.query.get_or_404(id)
    if request.method=='POST':
        c.nome=request.form['nome']; db.session.commit(); flash('Categoria atualizada.')
        return redirect(url_for('categorias_index'))
    return render_template('categorias/form.html', categoria=c)

@app.route('/categorias/<int:id>/excluir', methods=['POST'])
def categoria_excluir(id):
    c=Categoria.query.get_or_404(id)
    if c.anuncios: flash('Não é possível excluir categoria com anúncios vinculados.')
    else: db.session.delete(c); db.session.commit(); flash('Categoria excluída.')
    return redirect(url_for('categorias_index'))

# ANUNCIOS
@app.route('/anuncios')
def anuncios_index():
    return render_template('anuncios/index.html', anuncios=Anuncio.query.all())

@app.route('/anuncios/novo', methods=['GET','POST'])
def anuncio_novo():
    if request.method=='POST':
        a=Anuncio(titulo=request.form['titulo'], descricao=request.form['descricao'], preco=float(request.form['preco']), usuario_id=int(request.form['usuario_id']), categoria_id=int(request.form['categoria_id']))
        db.session.add(a); db.session.commit(); flash('Anúncio cadastrado.')
        return redirect(url_for('anuncios_index'))
    return render_template('anuncios/form.html', anuncio=None, usuarios=Usuario.query.all(), categorias=Categoria.query.all())

@app.route('/anuncios/<int:id>/editar', methods=['GET','POST'])
def anuncio_editar(id):
    a=Anuncio.query.get_or_404(id)
    if request.method=='POST':
        a.titulo=request.form['titulo']; a.descricao=request.form['descricao']; a.preco=float(request.form['preco']); a.usuario_id=int(request.form['usuario_id']); a.categoria_id=int(request.form['categoria_id'])
        db.session.commit(); flash('Anúncio atualizado.'); return redirect(url_for('anuncios_index'))
    return render_template('anuncios/form.html', anuncio=a, usuarios=Usuario.query.all(), categorias=Categoria.query.all())

@app.route('/anuncios/<int:id>/excluir', methods=['POST'])
def anuncio_excluir(id):
    a=Anuncio.query.get_or_404(id); db.session.delete(a); db.session.commit(); flash('Anúncio excluído.')
    return redirect(url_for('anuncios_index'))

@app.route('/anuncios/<int:id>')
def anuncio_detalhe(id):
    return render_template('anuncios/detalhe.html', anuncio=Anuncio.query.get_or_404(id))

# PERGUNTAS
@app.route('/perguntas')
def perguntas_index():
    return render_template('perguntas/index.html', perguntas=Pergunta.query.all())

@app.route('/perguntas/novo', methods=['GET','POST'])
def pergunta_novo():
    if request.method=='POST':
        p=Pergunta(texto=request.form['texto'], resposta=request.form.get('resposta') or None, usuario_id=int(request.form['usuario_id']), anuncio_id=int(request.form['anuncio_id']))
        db.session.add(p); db.session.commit(); flash('Pergunta cadastrada.'); return redirect(url_for('perguntas_index'))
    return render_template('perguntas/form.html', pergunta=None, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@app.route('/perguntas/<int:id>/editar', methods=['GET','POST'])
def pergunta_editar(id):
    p=Pergunta.query.get_or_404(id)
    if request.method=='POST':
        p.texto=request.form['texto']; p.resposta=request.form.get('resposta') or None; p.usuario_id=int(request.form['usuario_id']); p.anuncio_id=int(request.form['anuncio_id']); db.session.commit(); flash('Pergunta atualizada.'); return redirect(url_for('perguntas_index'))
    return render_template('perguntas/form.html', pergunta=p, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@app.route('/perguntas/<int:id>/excluir', methods=['POST'])
def pergunta_excluir(id):
    db.session.delete(Pergunta.query.get_or_404(id)); db.session.commit(); flash('Pergunta excluída.'); return redirect(url_for('perguntas_index'))

# COMPRAS
@app.route('/compras')
def compras_index():
    return render_template('compras/index.html', compras=Compra.query.all())

@app.route('/compras/novo', methods=['GET','POST'])
def compra_novo():
    if request.method=='POST':
        a=Anuncio.query.get_or_404(int(request.form['anuncio_id']))
        qtd=int(request.form['quantidade'])
        c=Compra(data=date.fromisoformat(request.form['data']), quantidade=qtd, valor=a.preco*qtd, comprador_id=int(request.form['comprador_id']), anuncio_id=a.id)
        db.session.add(c); db.session.commit(); flash('Compra registrada.'); return redirect(url_for('compras_index'))
    return render_template('compras/form.html', compra=None, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@app.route('/compras/<int:id>/editar', methods=['GET','POST'])
def compra_editar(id):
    c=Compra.query.get_or_404(id)
    if request.method=='POST':
        a=Anuncio.query.get_or_404(int(request.form['anuncio_id'])); c.data=date.fromisoformat(request.form['data']); c.quantidade=int(request.form['quantidade']); c.valor=a.preco*c.quantidade; c.comprador_id=int(request.form['comprador_id']); c.anuncio_id=a.id; db.session.commit(); flash('Compra atualizada.'); return redirect(url_for('compras_index'))
    return render_template('compras/form.html', compra=c, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@app.route('/compras/<int:id>/excluir', methods=['POST'])
def compra_excluir(id):
    db.session.delete(Compra.query.get_or_404(id)); db.session.commit(); flash('Compra excluída.'); return redirect(url_for('compras_index'))

# FAVORITOS
@app.route('/favoritos')
def favoritos_index():
    return render_template('favoritos/index.html', favoritos=Favorito.query.all(), usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@app.route('/favoritos/novo', methods=['GET','POST'])
def favorito_novo():
    if request.method=='POST':
        uid=int(request.form['usuario_id']); aid=int(request.form['anuncio_id'])
        if not Favorito.query.get((uid, aid)):
            db.session.add(Favorito(usuario_id=uid, anuncio_id=aid)); db.session.commit(); flash('Favorito cadastrado.')
        else: flash('Esse favorito já existe.')
        return redirect(url_for('favoritos_index'))
    return render_template('favoritos/form.html', favorito=None, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@app.route('/favoritos/<int:usuario_id>/<int:anuncio_id>/editar', methods=['GET','POST'])
def favorito_editar(usuario_id, anuncio_id):
    f=Favorito.query.get_or_404((usuario_id, anuncio_id))
    if request.method=='POST':
        novo_uid=int(request.form['usuario_id']); novo_aid=int(request.form['anuncio_id'])
        if (novo_uid, novo_aid)!=(usuario_id, anuncio_id) and Favorito.query.get((novo_uid, novo_aid)): flash('Esse favorito já existe.')
        else:
            f.usuario_id=novo_uid; f.anuncio_id=novo_aid; db.session.commit(); flash('Favorito atualizado.')
        return redirect(url_for('favoritos_index'))
    return render_template('favoritos/form.html', favorito=f, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@app.route('/favoritos/<int:usuario_id>/<int:anuncio_id>/excluir', methods=['POST'])
def favorito_excluir(usuario_id, anuncio_id):
    db.session.delete(Favorito.query.get_or_404((usuario_id, anuncio_id))); db.session.commit(); flash('Favorito excluído.'); return redirect(url_for('favoritos_index'))

# RELATORIOS
@app.route('/relatorios/vendas')
def relatorio_vendas():
    vendas=Compra.query.join(Anuncio).all(); return render_template('relatorios/vendas.html', vendas=vendas)

@app.route('/relatorios/compras')
def relatorio_compras():
    return render_template('relatorios/compras.html', compras=Compra.query.all())

@app.errorhandler(404)
def erro_404(e): return render_template('erro.html', codigo=404, mensagem='Página não encontrada.'), 404

@app.errorhandler(405)
def erro_405(e): return render_template('erro.html', codigo=405, mensagem='Método HTTP não permitido.'), 405

if __name__ == '__main__':
    app.run(debug=True)
