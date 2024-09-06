from model.modelo import TipoModelo
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
import uuid

from  model import Base

# colunas = Texto, Sentimento - 0 ou 1

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False, default=lambda: str(uuid.uuid4()))
    texto = Column("texto", String(250), nullable=False)
    sentimento = Column("sentimento", Integer, nullable=False)
    modelo =  Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.now(), nullable=False)
    
    def __init__(self, texto:str, sentimento:str, modelo:str, data_criacao:datetime = datetime.now()): 
        """
        Cria um Review

        Arguments:
        texto: texto do review
        sentimento: emoção expressa no texto do review
        data_insercao: data de quando o review foi inserido à base
        """
        self.uid = str(uuid.uuid4())
        self.texto = texto
        self.sentimento = sentimento
        self.modelo = modelo
        self.data_criacao = data_criacao