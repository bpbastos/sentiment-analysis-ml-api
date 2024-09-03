from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from  model import Base

# colunas = Texto, Sentimento - 0 ou 1

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    texto = Column("texto", String(250))
    sentimento = Column("sentimento", Integer)
    data_insercao = Column(DateTime, default=datetime.now(), nullable=False)
    
    def __init__(self, texto:str, sentimento:str): 
        """
        Cria um Review

        Arguments:
        texto: texto do review
        sentimento: emoção expressa no texto do review
        data_insercao: data de quando o review foi inserido à base
        """
        self.texto = texto
        self.sentimento = sentimento