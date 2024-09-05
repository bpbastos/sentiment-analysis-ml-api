import pandas as pd

class Carregador:

    def __to_sentiment(rating) -> int:
        rating = int(rating)
        if rating <= 2:
            return 0
        elif rating > 3:
            return 1    

    @staticmethod
    def carregar_dados(url: str) -> pd.DataFrame:
        """ Carrega e retorna um DataFrame. Há diversos parâmetros 
        no read_csv que poderiam ser utilizados para dar opções 
        adicionais.
        """
        # Carregando os dados
        dt = pd.read_csv(url, delimiter=',', encoding='utf-8')
        # Desprezando os comentários com score 3 (neutro)
        dt = dt[dt['score'] != 3]
        dt['sentiment'] = dt['score'].apply(Carregador.__to_sentiment)

        return dt[['content', 'sentiment']]