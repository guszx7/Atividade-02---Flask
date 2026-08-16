from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

out='/mnt/data/Atividade_CRUD_Ecommerce_Flask.pdf'
doc=SimpleDocTemplate(out,pagesize=A4,rightMargin=2*cm,leftMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CenterTitle', parent=styles['Title'], alignment=TA_CENTER, fontSize=16, leading=20))
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=9, leading=12))
story=[]
story.append(Paragraph('ATIVIDADE – IMPLEMENTAÇÃO DOS CRUDs NO FLASK', styles['CenterTitle']))
story.append(Spacer(1,12))
story.append(Paragraph('<b>Plataforma de E-commerce</b>', styles['Heading2']))
story.append(Paragraph('Esta etapa complementa a estrutura inicial apresentada na Trilha 1, implementando persistência de dados e operações CRUD (Create, Read, Update e Delete) para todas as entidades previstas no MER: Usuário, Categoria, Anúncio, Pergunta, Compra e Favorito. O projeto utiliza Flask, SQLite e Flask-SQLAlchemy.', styles['BodyText']))
story.append(Spacer(1,12))
story.append(Paragraph('1. Entidades e CRUDs implementados', styles['Heading1']))
data=[['Entidade','Create','Read','Update','Delete','Observação'],['USUÁRIO','✓','✓','✓','✓','Cadastro e gerenciamento de usuários'],['CATEGORIA','✓','✓','✓','✓','Organização dos anúncios'],['ANÚNCIO','✓','✓','✓','✓','Relaciona usuário e categoria'],['PERGUNTA','✓','✓','✓','✓','Edição também permite registrar resposta'],['COMPRA','✓','✓','✓','✓','Valor calculado conforme anúncio e quantidade'],['FAVORITO','✓','✓','✓','✓','Chave composta usuário + anúncio']]
t=Table(data,colWidths=[2.3*cm,1.2*cm,1.2*cm,1.2*cm,1.2*cm,8.0*cm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#333333')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.5,colors.grey),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('FONTSIZE',(0,0),(-1,-1),8),('ALIGN',(1,1),(4,-1),'CENTER')]))
story.append(t)
story.append(Spacer(1,14))
story.append(Paragraph('2. Operações e validações', styles['Heading1']))
for x in ['As listagens exibem os registros cadastrados por entidade.', 'Os formulários permitem criar novos registros.', 'Os registros existentes podem ser editados por rotas específicas.', 'As exclusões são realizadas por POST e utilizam confirmação no navegador.', 'Relacionamentos são representados por chaves estrangeiras e relacionamentos do SQLAlchemy.', 'O sistema impede exclusões que deixariam categorias ou usuários com vínculos incompatíveis, quando aplicável.', 'A entidade FAVORITO utiliza chave primária composta, evitando duplicidade do mesmo favorito.']:
    story.append(Paragraph('• '+x, styles['BodyText']))
story.append(Spacer(1,10))
story.append(Paragraph('3. Principais rotas CRUD', styles['Heading1']))
routes=[['Entidade','Listar','Cadastrar','Editar','Excluir'],['Usuários','/usuarios','/usuarios/novo','/usuarios/<id>/editar','/usuarios/<id>/excluir'],['Categorias','/categorias','/categorias/novo','/categorias/<id>/editar','/categorias/<id>/excluir'],['Anúncios','/anuncios','/anuncios/novo','/anuncios/<id>/editar','/anuncios/<id>/excluir'],['Perguntas','/perguntas','/perguntas/novo','/perguntas/<id>/editar','/perguntas/<id>/excluir'],['Compras','/compras','/compras/novo','/compras/<id>/editar','/compras/<id>/excluir'],['Favoritos','/favoritos','/favoritos/novo','/favoritos/<usuario_id>/<anuncio_id>/editar','/favoritos/<usuario_id>/<anuncio_id>/excluir']]
t2=Table(routes,colWidths=[2.5*cm,3.1*cm,3.1*cm,4.1*cm,4.1*cm],repeatRows=1)
t2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#333333')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.4,colors.grey),('FONTSIZE',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
story.append(t2)
story.append(PageBreak())
story.append(Paragraph('4. Estrutura do projeto', styles['Heading1']))
story.append(Paragraph('ecommerce_crud/<br/>├── app.py<br/>├── requirements.txt<br/>├── README.md<br/>├── ecommerce.db (gerado ao executar)<br/>├── static/css/style.css<br/>└── templates/ (páginas de cada entidade, formulários e relatórios)', styles['BodyText']))
story.append(Spacer(1,12))
story.append(Paragraph('5. Justificativa das ações', styles['Heading1']))
story.append(Paragraph('A utilização do padrão CRUD atende diretamente ao ciclo de persistência trabalhado na disciplina: criar, consultar, alterar e excluir registros. O SQLite foi adotado por ser um banco relacional simples e adequado para uma aplicação acadêmica, enquanto o Flask-SQLAlchemy facilita o mapeamento entre as classes Python e as tabelas do banco. As chaves estrangeiras preservam os relacionamentos definidos no MER, enquanto a chave composta de FAVORITO representa corretamente a associação entre usuário e anúncio. A confirmação antes da exclusão reduz o risco de remoções acidentais. A separação das rotas por entidade mantém a aplicação organizada e facilita a evolução futura.', styles['BodyText']))
story.append(Spacer(1,12))
story.append(Paragraph('6. Menu e navegação', styles['Heading1']))
story.append(Paragraph('O menu mantém acesso direto às operações de usuários, categorias, anúncios, perguntas, compras, favoritos e relatórios. Cada listagem oferece acesso ao cadastro e às ações de edição e exclusão, mantendo o fluxo de navegação simples e consistente.', styles['BodyText']))
try: story.append(Image('/mnt/data/ecommerce_crud/docs/menu_navegacao.png', width=15*cm, height=9*cm))
except: pass
story.append(PageBreak())
story.append(Paragraph('7. Modelo Entidade-Relacionamento', styles['Heading1']))
try: story.append(Image('/mnt/data/ecommerce_crud/docs/MER_ecommerce.png', width=16*cm, height=10*cm))
except: pass
story.append(Spacer(1,10))
story.append(Paragraph('8. Publicação no GitHub', styles['Heading1']))
story.append(Paragraph('<b>Repositório:</b> INSIRA AQUI O LINK DO MESMO REPOSITÓRIO UTILIZADO NA TRILHA 1.', styles['BodyText']))
story.append(Paragraph('Antes da entrega, o código deve ser enviado ao repositório público e devem existir commits que registrem a implementação dos CRUDs até a data limite da atividade.', styles['BodyText']))
story.append(Spacer(1,14))
story.append(Paragraph('9. Conclusão', styles['Heading1']))
story.append(Paragraph('Com esta etapa, a aplicação deixa de utilizar somente dados temporários e passa a possuir persistência relacional. As seis entidades do MER possuem operações CRUD, formulários e listagens, permitindo demonstrar na prática os conceitos de integração entre aplicação Flask e banco de dados.', styles['BodyText']))
doc.build(story)
print(out)
