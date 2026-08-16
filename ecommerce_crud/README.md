# Plataforma de E-commerce — CRUD Flask

Projeto da atividade de CRUD. A aplicação implementa persistência com SQLite e Flask-SQLAlchemy para as entidades do MER: Usuário, Categoria, Anúncio, Pergunta, Compra e Favorito.

## Executar
```bash
python -m venv venv
# Windows: venv\\Scripts\\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Acesse `http://127.0.0.1:5000`.

## CRUDs
Todas as entidades possuem listagem, cadastro, edição e exclusão com confirmação. Perguntas também permitem registrar/alterar respostas. Relatórios de vendas e compras são consultas derivadas das compras.

## GitHub
Publique este projeto no mesmo repositório utilizado na Trilha 1 e mantenha commits que registrem a evolução do CRUD.
