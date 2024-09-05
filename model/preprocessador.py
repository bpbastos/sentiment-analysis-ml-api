from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
import pickle
import spacy
import re
from abc import abstractmethod
import numpy as np
import pandas as pd

from model.modelo import TipoModelo

class PreProcessador:
    """ Classe para cuidar do pré-processamento dos dados. """

    tokenizer = None
    tokenizer_path = None
    scaler_path = None    

    def __init__(self, tokenizer_path:str, scaler_path:str):
        self.tokenizer_path = tokenizer_path
        self.scaler_path = scaler_path

    @abstractmethod
    def preparar_textos(self, textos):
        """ Prepara os dados recebidos do front para serem usados no modelo. """
        pass

    @abstractmethod
    def scaler(self, X_train):
        """ Normaliza os dados. """
        pass

    @abstractmethod
    def separa_teste_treino(X, y, percentual_teste, seed=7):
        """ Separa os dados em treino e teste. """
        # divisão em treino e teste
        return train_test_split(X, y, test_size=percentual_teste, shuffle=True, random_state=seed, stratify=y)  # holdout com estratificação
    

class PreProcessadorFactory:
    @staticmethod
    def cria_preprocessador(tipo_modelo: str) -> PreProcessador:
        if tipo_modelo == TipoModelo.MODEL_SCIKIT_LEARN or tipo_modelo == TipoModelo.PIPELINE_SCIKIT_LEARN:
            return PreProcessadorScikitLearn()
        elif tipo_modelo == TipoModelo.MODEL_TRANSFORMERS:
            return PreProcessadorTransformers()
        else:
            raise ValueError(f"Tipo de modelo desconhecido: {tipo_modelo}")
        
class PreProcessadorTransformers(PreProcessador):
    """ Classe para cuidar do pré-processamento dos dados. """
    def __init__(self):

        super().__init__('./machine-learning/models/tf_sentiment_classifier/', None)

        # Carrega o tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)

        if self.tokenizer is None:
            raise Exception('Vetorizador não encontrado')          

    def preparar_textos(self, textos):
        """ Prepara os dados recebidos do front para serem usados no modelo. """

        if isinstance(textos, pd.Series):
            textos = textos.tolist()
        elif isinstance(textos, str):
            textos = [textos]
        elif not isinstance(textos, list):
            raise ValueError('Tipo de dado inválido. Esperado str, list ou pd.Series.')
                
        X_input = self.tokenizer(textos, max_length=40, add_special_tokens=True, truncation=True, padding='max_length', return_attention_mask=True, return_tensors='pt')
        return  X_input

    def scaler(self, X_train):
        return False

class PreProcessadorScikitLearn(PreProcessador):
    """ Classe para cuidar do pré-processamento dos dados. """
    npl = None
    def __init__(self):

        super().__init__('./machine-learning/vectorizer/count_vectorizer.pkl', './machine-learning/scalers/maxabs_scaler_sentiment.pkl')

        # Carrega o vetorizador
        with open(self.tokenizer_path, 'rb') as file:
            self.tokenizer = pickle.load(file)

        if self.tokenizer is None:
            raise Exception('Vetorizador não encontrado')  
        
        with open(self.scaler_path, 'rb') as file:
            self.scaler = pickle.load(file)

        if self.scaler is None:
            raise Exception('Scaler não encontrado')
        
        self.__carrega_stop_words()
            

    def __carrega_stop_words(self):        
        # Stop words em português
        novas_stop_words = [ 'a', 'à', 'adeus', 'agora', 'aí', 'ainda', 'além', 'algo', 'alguém', 'algum', 'alguma', 'algumas', 'alguns', 'ali', 'ampla', 'amplas', 'amplo', 'amplos', 'ano', 'anos', 'ante', 'antes', 'ao', 'aos', 'apenas', 'apoio', 'após', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', 'área', 'as', 'às', 'assim', 'até', 'atrás', 'através', 'baixo', 'bastante', 'bem', 'boa', 'boas', 'bom', 'bons', 'breve', 'cá', 'cada', 'catorze', 'cedo', 'cento', 'certamente', 'certeza', 'cima', 'cinco', 'coisa', 'coisas', 'com', 'como', 'conselho', 'contra', 'contudo', 'custa', 'da', 'dá', 'dão', 'daquela', 'daquelas', 'daquele', 'daqueles', 'dar', 'das', 'de', 'debaixo', 'dela', 'delas', 'dele', 'deles', 'demais', 'dentro', 'depois', 'desde', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'destes', 'deve', 'devem', 'devendo', 'dever', 'deverá', 'deverão', 'deveria', 'deveriam', 'devia', 'deviam', 'dez', 'dezanove', 'dezasseis', 'dezassete', 'dezoito', 'dia', 'diante', 'disse', 'disso', 'disto', 'dito', 'diz', 'dizem', 'dizer', 'do', 'dois', 'dos', 'doze', 'duas', 'dúvida', 'e', 'é', 'ela', 'elas', 'ele', 'eles', 'em', 'embora', 'enquanto', 'entre', 'era', 'eram', 'éramos', 'és', 'essa', 'essas', 'esse', 'esses', 'esta', 'está', 'estamos', 'estão', 'estar', 'estas', 'estás', 'estava', 'estavam', 'estávamos', 'este', 'esteja', 'estejam', 'estejamos', 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera', 'estiveram', 'estivéramos', 'estiverem', 'estivermos', 'estivesse', 'estivessem', 'estivéssemos', 'estiveste', 'estivestes', 'estou', 'etc', 'eu', 'exemplo', 'faço', 'falta', 'favor', 'faz', 'fazeis', 'fazem', 'fazemos', 'fazendo', 'fazer', 'fazes', 'feita', 'feitas', 'feito', 'feitos', 'fez', 'fim', 'final', 'foi', 'fomos', 'for', 'fora', 'foram', 'fôramos', 'forem', 'forma', 'formos', 'fosse', 'fossem', 'fôssemos', 'foste', 'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'há', 'haja', 'hajam', 'hajamos', 'hão', 'havemos', 'havia', 'hei', 'hoje', 'hora', 'horas', 'houve', 'houvemos', 'houver', 'houvera', 'houverá', 'houveram', 'houvéramos', 'houverão', 'houverei', 'houverem', 'houveremos', 'houveria', 'houveriam', 'houveríamos', 'houvermos', 'houvesse', 'houvessem', 'houvéssemos', 'isso', 'isto', 'já', 'la', 'lá', 'lado', 'lhe', 'lhes', 'lo', 'local', 'logo', 'longe', 'lugar', 'maior', 'maioria', 'mais', 'mal', 'mas', 'máximo', 'me', 'meio', 'menor', 'menos', 'mês', 'meses', 'mesma', 'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'mil', 'minha', 'minhas', 'momento', 'muita', 'muitas', 'muito', 'muitos', 'na', 'nada', 'não', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas', 'nem', 'nenhum', 'nenhuma', 'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes', 'ninguém', 'nível', 'no', 'noite', 'nome', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'nova', 'novas', 'nove', 'novo', 'novos', 'num', 'numa', 'número', 'nunca', 'o', 'obra', 'obrigada', 'obrigado', 'oitava', 'oitavo', 'oito', 'onde', 'ontem', 'onze', 'os', 'ou', 'outra', 'outras', 'outro', 'outros', 'para', 'parece', 'parte', 'partir', 'paucas', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas', 'pequeno', 'pequenos', 'per', 'perante', 'perto', 'pode', 'pude', 'pôde', 'podem', 'podendo', 'poder', 'poderia', 'poderiam', 'podia', 'podiam', 'põe', 'põem', 'pois', 'ponto', 'pontos', 'por', 'porém', 'porque', 'porquê', 'posição', 'possível', 'possivelmente', 'posso', 'pouca', 'poucas', 'pouco', 'poucos', 'primeira', 'primeiras', 'primeiro', 'primeiros', 'própria', 'próprias', 'próprio', 'próprios', 'próxima', 'próximas', 'próximo', 'próximos', 'pude', 'puderam', 'quais', 'quáis', 'qual', 'quando', 'quanto', 'quantos', 'quarta', 'quarto', 'quatro', 'que', 'quê', 'quem', 'quer', 'quereis', 'querem', 'queremas', 'queres', 'quero', 'questão', 'quinta', 'quinto', 'quinze', 'relação', 'sabe', 'sabem', 'são', 'se', 'segunda', 'segundo', 'sei', 'seis', 'seja', 'sejam', 'sejamos', 'sem', 'sempre', 'sendo', 'ser', 'será', 'serão', 'serei', 'seremos', 'seria', 'seriam', 'seríamos', 'sete', 'sétima', 'sétimo', 'seu', 'seus', 'sexta', 'sexto', 'si', 'sido', 'sim', 'sistema', 'só', 'sob', 'sobre', 'sois', 'somos', 'sou', 'sua', 'suas', 'tal', 'talvez', 'também', 'tampouco', 'tanta', 'tantas', 'tanto', 'tão', 'tarde', 'te', 'tem', 'tém', 'têm', 'temos', 'tendes', 'tendo', 'tenha', 'tenham', 'tenhamos', 'tenho', 'tens', 'ter', 'terá', 'terão', 'terceira', 'terceiro', 'terei', 'teremos', 'teria', 'teriam', 'teríamos', 'teu', 'teus', 'teve', 'ti', 'tido', 'tinha', 'tinham', 'tínhamos', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram', 'tivéramos', 'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéssemos', 'tiveste', 'tivestes', 'toda', 'todas', 'todavia', 'todo', 'todos', 'trabalho', 'três', 'treze', 'tu', 'tua', 'tuas', 'tudo', 'última', 'últimas', 'último', 'últimos', 'um', 'uma', 'umas', 'uns', 'vai', 'vais', 'vão', 'vários', 'vem', 'vêm', 'vendo', 'vens', 'ver', 'vez', 'vezes', 'viagem', 'vindo', 'vinte', 'vir', 'você', 'vocês', 'vos', 'vós', 'vossa', 'vossas', 'vosso', 'vossos', 'zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_' ]

        # Carrega stop words em português
        self.nlp = spacy.load("pt_core_news_sm")

        # Adiciona cada palavra da lista às stop words do spaCy
        for word in novas_stop_words:
            self.nlp.Defaults.stop_words.add(word)
            # Marca como stop word no vocabulário
            self.nlp.vocab[word].is_stop = True


    def __clean_text(self, text):
        # Converte o texto para string
        text = str(text)
        # Remove caracteres especiais
        text = re.sub(r'[^\w\s]', '', text)  
        # Converte para minúsculas
        text = text.lower()             
        # Processa o texto com spaCy
        doc = self.nlp(text)        
       # Remove stopwords, pontuação e lematiza o texto
        cleaned_text = ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
        return cleaned_text   
      
    def preparar_textos(self, textos):
        """ Prepara os dados recebidos do front para serem usados no modelo. """
        textos_limpos = []
        if isinstance(textos, (list, np.ndarray)):
            textos_limpos= [self.__clean_text(texto) for texto in textos]
        elif isinstance(textos, str):
           textos_limpos = [self.__clean_text(textos)]   
        else:
            raise ValueError('Tipo de dado inválido')   

        return self.tokenizer.transform(textos_limpos)
       
    def scaler(self, X_train):
        """ Normaliza os dados. """
        # normalização/padronização
        reescaled_X_train = self.scaler.transform(X_train)
        return reescaled_X_train
