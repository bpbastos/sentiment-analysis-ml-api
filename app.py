from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS

import re


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
review_tag = Tag(name="Review", description="Adição, visualização, remoção e análise de sentimentos de avaliações de aplicativos.")

def sanitize_input(input_data):
    """
    Sanitiza os dados de entrada para prevenir SQL Injection e escapar caracteres especiais.
    
    Args:
        input_data (str): Os dados de entrada a serem sanitizados.
        
    Returns:
        str: Os dados de entrada sanitizados.
    """
    if isinstance(input_data, str):
        # Remove quaisquer caracteres especiais de SQL
        sanitized_data = re.sub(r"[;'\"]", "", input_data)
        # Escapa quaisquer caracteres especiais restantes
        sanitized_data = re.escape(sanitized_data)
        return sanitized_data
    return input_data


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
    #filtro condicional por titulo, id da tarefa e por id da categoria
    filtros = []
    if query.texto:
        filtros.append(Review.texto.ilike(f'%{sanitize_input(query.texto)}%'))
    if query.id:
        filtros.append(Review.id == sanitize_input(query.id))    
    if query.sentimento:
        filtros.append(Review.sentimento == sanitize_input(query.sentimento))       


    logger.debug("Coletando dados sobre todos os reviews")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os reviews utilizando filtros, se informados.
    reviews = session.query(Review).filter(*filtros).all() 
    
    if not reviews:
        # Se não houver reviews, retorna uma lista vazia
        return {"reviews": []}, 200
    else:
        logger.debug(f"%d reviews econtrados" % len(reviews))
        print(reviews)
        return apresenta_reviews(reviews), 200


# Rota de adição de review
@app.post('/review', tags=[review_tag],
          responses={"200": ReviewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: ReviewSchema):
    """Adiciona um novo review à base de dados
    Retorna o tom emocional associado ao texto (sentimento).
    
    Args:
        texto (str): texto do review
        
    Returns:
        dict: representação do review com o tom emocional do texto (sentimento)
    """
    # TODO: Instanciar classes

    # Recuperando os dados do formulário
    #texto = sanitize_input(form.texto)
    texto = form.texto        
    # Preparando os dados para o modelo
    pre_processador = PreProcessador()
    X_input = pre_processador.preparar_form(form)
    # Carregando modelo
    model_path = './machine-learning/pipelines/et_sentiment_pipeline.pkl'
    # modelo = Model.carrega_modelo(ml_path)
    modelo = Pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    sentimento = int(Model.preditor(modelo, X_input)[0])
    
    review = Review(
        texto=texto,
        sentimento=sentimento
    )

    logger.debug(f"Adicionando review : '{review.texto}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se review já existe na base
        if session.query(Review).filter(Review.texto == form.texto).first():
            error_msg = "Review já existente na base :/"
            logger.warning(f"Erro ao adicionar review '{review.texto}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando review
        session.add(review)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado review: '{review.texto}'")
        return apresenta_review(review), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo review :/"
        logger.warning(f"Erro ao adicionar review '{review.texto}', {error_msg}")
        return {"message": error_msg}, 400
    
    
# Rota de remoção de review por nome
@app.delete('/review', tags=[review_tag],responses={"200": ReviewDelSchema, "404": ErrorSchema})
def delete_review(query: ReviewDelSchema):
    """Remove um review cadastrado na base a partir do nome

    Args:
        nome (str): nome do review
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    review_id = sanitize_input(query.id)
    logger.debug(f"Deletando dados do review #{review_id}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando review
    review = session.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        error_msg = "Review não encontrado na base :/"
        logger.warning(f"Erro ao deletar review '{review_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(review_id)
        session.commit()
        logger.debug(f"Deletado review #{review_id}")
        return {"message": f"Review {review_id} removido com sucesso!"}, 200
    
if __name__ == '__main__':
    app.run(debug=True)