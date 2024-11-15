from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from flask import Flask

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)

# Instanciando o objeto OpenAPI
info = Info(title="API de Análise de sentimentos em textos.", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
review_tag = Tag(name="Review", description="Adição, visualização, remoção e análise de sentimentos em textos.")

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de reviews
@app.get('/review', tags=[review_tag], responses={"200": ListaReviewsSchema, "404": ErrorSchema})
def get_reviews(query: BuscaReviewSchema):
    """Faz a busca por todos os reviews ou filtra dependendo dos parametros passados
    Retorna uma representação da listagem de reviews.
    """     
    #filtro condicional por id,texto,sentimento e modelo do review 
    filtros = []
    if query.id:
        filtros.append(Review.id == query.id)    
    if query.texto:
        filtros.append(Review.texto.ilike(f'%{query.texto}%'))
    if query.sentimento:
        filtros.append(Review.sentimento == query.sentimento)       
    if query.modelo:
        filtros.append(Review.modelo == query.modelo)       
        
    logger.debug("Coletando dados sobre todos os reviews")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os reviews utilizando filtros, se informados.
    reviews = session.query(Review).filter(*filtros).order_by(desc(Review.data_criacao)).all() 
    # Fechando a conexão
    session.close()
    
    if not reviews:
        # Se não houver reviews, retorna uma lista vazia
        return {}, 200
    else:
        logger.debug(f"%d reviews econtrados" % len(reviews))
        return jsonify(apresenta_reviews(reviews)), 200


# Rota de adição de review
@app.post('/review', tags=[review_tag],
          responses={"200": ReviewSchema, "400": ErrorSchema})
def add_review(form: ReviewSchema):
    """Adiciona um novo review à base de dados
    Retorna o tom emocional associado ao texto (sentimento).
    
    Args:
        texto (str): texto do review
        modelo (str): tipo de modelo a ser utilizado para análise de sentimento
        
    Returns:
        dict: representação do review com o tom emocional do texto (sentimento)
    """

    # Recuperando os dados do formulário
    texto = form.texto  
    tipo_modelo = form.modelo

    if tipo_modelo not in [TipoModelo.PIPELINE_SCIKIT_LEARN, TipoModelo.MODEL_SCIKIT_LEARN, TipoModelo.MODEL_TRANSFORMERS]:
        error_msg = "Tipo de modelo não suportado"
        logger.warning(f"Erro ao selecionar o tipo de modelo do review '{tipo_modelo}', {error_msg}")
        return {"error": error_msg}, 200  
    
    if not texto:
        error_msg = "Texto do review não informado"
        logger.warning(f"Erro ao adicionar review '{texto}', {error_msg}")
        return {"error": error_msg}, 200    
    
    # Vetorizando e limpando o texto
    preprocessador = PreProcessadorFactory.cria_preprocessador(tipo_modelo)    
    X_input = preprocessador.preparar_textos(texto)
    
    # Carregando modelo 
    model = ModelFactory.cria_modelo(tipo_modelo)

    # Realizando a predição
    sentimento = int(model.realizar_predicao(X_input)[0])
    
    review = Review(
        texto=texto,
        sentimento=sentimento,
        modelo=tipo_modelo,
        data_criacao=datetime.now()
    )

    logger.debug(f"Adicionando review : '{review.texto}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se review já existe na base
        filtros = []
        filtros.append(Review.texto == texto)
        filtros.append(Review.modelo == tipo_modelo)
        if session.query(Review).filter(*filtros).first():
            error_msg = "Review já existente na base :/"
            logger.warning(f"Erro ao adicionar review '{review.texto}', {error_msg}")
            return {"error": error_msg}, 200
        
        # Adicionando review
        session.add(review)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado review: '{review.uid}'")
        return jsonify(apresenta_review(review)), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo review :/"
        logger.warning(f"Erro ao adicionar review '{review.uid}', {error_msg}")
        return {"error": error_msg}, 200
    
    finally:
        # Fechando a conexão
        session.close()
    
    
# Rota de remoção de review por nome
@app.delete('/review', tags=[review_tag],responses={"200": ReviewDelSchema, "404": ErrorSchema})
def delete_review(query: ReviewDelSchema):
    """Remove um review cadastrado na base a partir do ID

    Args:
        ID (str): nome do review
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    

    # Criando conexão com a base
    session = Session()
    
    # Buscando review
    review = session.query(Review).filter(Review.uid == query.id).first()
    
    if not review:
        error_msg = "Review não encontrado na base :/"
        logger.warning(f"Erro ao deletar review '{query.id}', {error_msg}")
        return {"error": error_msg}, 200
    else:
        session.delete(review)
        session.commit()
        session.close()
        logger.debug(f"Deletado review #{query.id}")
        return {"message": f"Review {query.id} removido com sucesso!"}, 200
    
if __name__ == '__main__':
    app.run()