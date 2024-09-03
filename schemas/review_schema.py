from pydantic import BaseModel
from typing import List
from model.review import Review

class ReviewSchema(BaseModel):
    """ Define como um novo review a ser inserido deve ser representado
    """
    texto: str = "Excelente app! A entrega foi super rápida, e a comida chegou quentinha. Adorei a variedade de restaurantes disponíveis. Super recomendo para quem gosta de praticidade!"
    sentimento: int = 1
    
class ReviewViewSchema(BaseModel):
    """Define como um review será retornado
    """
    texto: str = "Excelente app! A entrega foi super rápida, e a comida chegou quentinha. Adorei a variedade de restaurantes disponíveis. Super recomendo para quem gosta de praticidade!"
    sentimento: int = 1
    
class ListaReviewsSchema(BaseModel):
    """Define como uma lista de reviews será representada
    """
    reviews: List[ReviewViewSchema]

    
class ReviewDelSchema(BaseModel):
    """Define como um review para deleção será representado
    """
    id:int = None
    
# Apresenta apenas os dados de um paciente    
def apresenta_review(review: Review):
    """ Retorna uma representação do review seguindo o schema definido em
        ReviewViewSchema.
    """
    return {
        "id": review.id,
        "texto": review.texto,
        "setimento": review.sentimento
    }
    
# Apresenta uma lista de pacientes
def apresenta_reviews(reviews: List[Review]):
    """ Retorna uma representação do review seguindo o schema definido em
        ReviewViewSchema.
    """
    result = []
    for review in reviews:
        result.append({
            "id": review.id,
            "texto": review.texto,
            "sentimento": review.sentimento,
        })

    return {"reviews": result}

