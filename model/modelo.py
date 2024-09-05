import pickle
import numpy as np
from abc import abstractmethod
from transformers import AutoModelForSequenceClassification

class TipoModelo:
    PIPELINE_SCIKIT_LEARN = "pipeline-et"
    MODEL_SCIKIT_LEARN = "model-et"
    MODEL_TRANSFORMERS = "model-distilbert"

class Model:
    path: str = None
    model = None
    def __init__(self, path: str):
        self.path = path
        self.model = self.carrega_modelo()

    @abstractmethod    
    def carrega_modelo(self, path):
        pass

    @abstractmethod   
    def realizar_predicao(self, X_input):
        pass

class ModelFactory:
    @staticmethod
    def cria_modelo(tipo_modelo: str) -> Model:
        if tipo_modelo == TipoModelo.MODEL_SCIKIT_LEARN:
            return ModelSciKitLearn()
        elif tipo_modelo == TipoModelo.MODEL_TRANSFORMERS:
            return ModelTransformers('cpu')
        elif tipo_modelo == TipoModelo.PIPELINE_SCIKIT_LEARN:
            return PipelineSciKitLearn()
        else:
            raise ValueError(f"Tipo de modelo desconhecido: {tipo_modelo}")
        
class PipelineSciKitLearn(Model):
    def __init__(self):
        super().__init__('./machine-learning/pipelines/et_sentiment_pipeline.pkl')

    def carrega_modelo(self):
        """Carregamos o pipeline construindo durante a fase de treinamento
        """
        model = None
        if self.model is None:        
            if self.path.endswith('.pkl'):
                with open(self.path, 'rb') as file:
                    model = pickle.load(file)
            else:
                raise Exception('Formato de arquivo não suportado')
        return model
    
    def realizar_predicao(self, X_input):
        """Realiza a análise de sentimento com base no modelo treinado
        """
        sentimento = self.model.predict(X_input)
        return sentimento
        
class ModelSciKitLearn(Model):
    def __init__(self):
        super().__init__('./machine-learning/models/et_sentiment_classifier.pkl')
    
    def carrega_modelo(self):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra
        """
        model = None
        if self.model is None:        
            if self.path.endswith('.pkl'):
                with open(self.path, 'rb') as file:
                    model = pickle.load(file)
            else:
                raise Exception('Formato de arquivo não suportado')
        return model
    
    def realizar_predicao(self, X_input):
        """Realiza a análise de sentimento com base no modelo treinado
        """
        sentimento = self.model.predict(X_input)
        return sentimento
    
class ModelTransformers(Model):
    device = None
    def __init__(self, device):
        super().__init__('./machine-learning/models/tf_sentiment_classifier/')
        self.device =  device
    
    def carrega_modelo(self):
        """Carrega o modelo pré-treinado
        """
        model = None

        if self.model is None:
            model = AutoModelForSequenceClassification.from_pretrained(self.path)
        else:
            model = self.model

        return model
    
    def realizar_predicao(self, X_input):
        """Realiza a análise de sentimento com base no modelo treinado
        """
        inputs = {key: value.to(self.device) for key, value in X_input.items()}
        outputs = self.model(**inputs)
        predictions = np.argmax(outputs.logits.detach().cpu().numpy(), axis=-1)
        return predictions