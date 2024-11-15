from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.review import Review
from model.modelo import Model
from model.modelo import TipoModelo
from model.modelo import ModelFactory
from model.modelo import ModelSciKitLearn
from model.modelo import ModelTransformers
from model.modelo import PipelineSciKitLearn
from model.preprocessador import PreProcessador
from model.preprocessador import PreProcessadorFactory
from model.preprocessador import PreProcessadorScikitLearn
from model.preprocessador import PreProcessadorTransformers
from model.avaliador import Avaliador
from model.carregador import Carregador

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/reviews.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(
    db_url, 
    echo=False,
    pool_size=10,  # tamanho do pool conforme necessário
    max_overflow=20,  # número máximo de conexões extras
    pool_timeout=30,  # Tempo limite para obter uma conexão do pool
    pool_recycle=1800  # Tempo de reciclagem das conexões (em segundos)    
)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)