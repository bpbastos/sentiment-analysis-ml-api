from pydantic import BaseModel
from typing import List, Optional
from model.review import Review

class ReviewSchema(BaseModel):
    """ Define como um novo review a ser inserido deve ser representado
    """
    modelo: str = None
    texto: str = None
    
class ReviewViewSchema(BaseModel):
    """Define como um review será retornado
    """
    id: str = "c303282d-f2e6-46ca-a04a-35d3d873712d"
    texto: str = "Excelente app! A entrega foi super rápida, e a comida chegou quentinha. Adorei a variedade de restaurantes disponíveis. Super recomendo para quem gosta de praticidade!"
    sentimento: int = 1
    
class ListaReviewsSchema(BaseModel):
    """Define como uma lista de reviews será representada
    """
    reviews: List[ReviewViewSchema]

class BuscaReviewSchema(BaseModel):
    """ Define como representação dos parametros de busca do Review
    """
    id:Optional[str] = None
    texto: Optional[str] = None
    sentimento: Optional[int] = None
    modelo: Optional[str] = None
    
class ReviewDelSchema(BaseModel):
    """Define como um review para deleção será representado
    """
    id:str = None
    
# Apresenta apenas os dados de um paciente    
def apresenta_review(review: Review):
    """ Retorna uma representação do review seguindo o schema definido em
        ReviewViewSchema.
    """
    return {
        "id": review.uid,
        "texto": review.texto,
        "sentimento": review.sentimento,
        "modelo": review.modelo,  
        "data_criacao": review.data_criacao.strftime("%d/%m/%Y %H:%M:%S")    
    }
    
# Apresenta uma lista de pacientes
def apresenta_reviews(reviews: List[Review]):
    """ Retorna uma representação do review seguindo o schema definido em
        ReviewViewSchema.
    """
    result = [apresenta_review(review) for review in reviews]
    return result

