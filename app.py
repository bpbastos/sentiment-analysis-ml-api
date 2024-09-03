from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
review_tag = Tag(name="Review", description="Adição, visualização, remoção e predição de reviews de aplicativos")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de reviews
@app.get('/reviews', tags=[review_tag], responses={"200": ListaReviewsSchema, "404": ErrorSchema})
def get_reviews():
    """Lista todos os reviews cadastrados na base
    Args:
       none
        
    Returns:
        list: lista de reviews cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os reviews")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os pacientes
    reviews = session.query(Review).all()
    
    if not reviews:
        # Se não houver pacientes
        return {"reviews": []}, 200
    else:
        logger.debug(f"%d reviews econtrados" % len(reviews))
        print(reviews)
        return apresenta_reviews(reviews), 200


# Rota de adição de paciente
@app.post('/review', tags=[review_tag],
          responses={"200": ReviewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: ReviewSchema):
    """Adiciona um novo paciente à base de dados
    Retorna o tom emocional associado ao texto (sentimento).
    
    Args:
        texto (str): nome do paciente
        
    Returns:
        dict: representação do review com o tom emocional do texto (sentimento)
    """
    # TODO: Instanciar classes

    # Recuperando os dados do formulário
    texto = form.texto
        
    # Preparando os dados para o modelo
    X_input = PreProcessador.preparar_form(form)
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
        
        # Checando se paciente já existe na base
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
        logger.warning(f"Erro ao adicionar paciente '{review.texto}', {error_msg}")
        return {"message": error_msg}, 400
    
    
# Rota de remoção de paciente por nome
@app.delete('/paciente', tags=[review_tag],responses={"200": ReviewDelSchema, "404": ErrorSchema})
def delete_paciente(query: ReviewDelSchema):
    """Remove um review cadastrado na base a partir do nome

    Args:
        nome (str): nome do paciente
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    review_id = unquote(query.id)
    logger.debug(f"Deletando dados do review #{review_id}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando paciente
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