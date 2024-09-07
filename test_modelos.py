from model import *
import torch


# To run: pytest -v test_modelos.py

# Parâmetros    
url_dados = "./machine-learning/data/android_app_reviews.csv"

# Carga dos dados
dataset = Carregador.carregar_dados(url_dados)

# Método para testar o pipeline do Extra Trees + Max Abs Scaler
def test_modelo_et():  
    pp_et = PreProcessadorFactory.cria_preprocessador(TipoModelo.MODEL_SCIKIT_LEARN)
    model_et = ModelFactory.cria_modelo(TipoModelo.MODEL_SCIKIT_LEARN)    

    X = dataset['content']
    y = dataset['sentiment']

    # Divide os dados em treino e teste
    X_train, X_test, y_train, y_test = PreProcessador.separa_teste_treino(X, y, percentual_teste=0.2, seed=7)

    # Vetoriza e limpa os textos
    X_vec = pp_et.preparar_textos(X_test.tolist())

    # Obtendo as métricas do modelo Extra Trees
    acuracia_model_et = Avaliador.avaliar(model_et, X_vec, y_test)

    # Testando as métricas do pipeline do Extra Trees  
    assert acuracia_model_et >= 0.78, f"Acurácia do modelo abaixo do esperado: {acuracia_model_et}"

# Método para testar o pipeline do Extra Trees + Max Abs Scaler
def test_pipeline_et():  
    pp_et = PreProcessadorFactory.cria_preprocessador(TipoModelo.PIPELINE_SCIKIT_LEARN)
    pipeline_et = ModelFactory.cria_modelo(TipoModelo.PIPELINE_SCIKIT_LEARN)    

    X = dataset['content']
    y = dataset['sentiment']

    # Divide os dados em treino e teste
    X_train, X_test, y_train, y_test = PreProcessador.separa_teste_treino(X, y, percentual_teste=0.2, seed=7)

    # Vetoriza e limpa os textos
    X_vec = pp_et.preparar_textos(X_test.tolist())

    # Obtendo as métricas do pipeline do Extra Trees + Max Abs Scaler
    acuracia_pipeline_et = Avaliador.avaliar(pipeline_et, X_vec, y_test)

    # Testando as métricas do pipeline do Extra Trees + Max Abs Scaler 
    assert acuracia_pipeline_et >= 0.85, f"Acurácia do modelo abaixo do esperado: {acuracia_pipeline_et}" 

# Método para testar o modelo distilbert (deep learning) (!!!Tenha uma GPU disponível!!!)
def test_modelo_tf():  
    model_tf = ModelFactory.cria_modelo(TipoModelo.MODEL_TRANSFORMERS)
    pp_model_tf = PreProcessadorFactory.cria_preprocessador(TipoModelo.MODEL_TRANSFORMERS)

    X = dataset['content']
    y = dataset['sentiment']    

    # Divide os dados em treino e teste
    X_train, X_test, y_train, y_test = PreProcessador.separa_teste_treino(X, y, percentual_teste=0.2, seed=7)

    X_tf = pp_model_tf.preparar_textos(X_test) 

    # Obtendo as métricas do pipeline do Extra Trees + Max Abs Scaler
    acuracia_model_tf = Avaliador.avaliar(model_tf, X_tf, y_test)

    # Testando as métricas do pipeline do Extra Trees  
    assert acuracia_model_tf >= 0.88, f"Acurácia do modelo abaixo do esperado: {acuracia_model_tf}"    

