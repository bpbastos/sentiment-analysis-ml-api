from sklearn.metrics import accuracy_score

class Avaliador:
    """ Classe que avalia um modelo de Machine Learning
    """

    @staticmethod
    def avaliar(model, X_test, y_test):
        """ Faz uma predição e avalia o modelo. Poderia parametrizar o tipo de
        avaliação, entre outros.
        """
        sentimentos = model.realizar_predicao(X_test)
        
        return accuracy_score(y_test, sentimentos)
                
