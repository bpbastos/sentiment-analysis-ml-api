# Sentiment Analysis API 

<img src="screenshot/swagger.jpg" alt="Swagger">

> API Restful para Análise de Sentimentos. Este backend foi desenvolvido para criar, remover, visualizar e realizar a análise de sentimentos em textos. A aplicação foi construída com Python 3 e o microframework Flask, com SQLAlchemy como ORM e SQLite3 como banco de dados.

> Para a modelagem, treinamento e teste do modelo de machine learning responsável pela análise de sentimentos, foram utilizadas as seguintes bibliotecas:

* Scikit-learn: Para tarefas de machine learning tradicionais, como pré-processamento de dados, modelagem de algoritmos e avaliação do modelo.
* Transformers da Hugging Face: Para o uso de modelos de deep learning baseados em modelos pré-treinados na lingua portuguesa (BERT e DistilBERT), otimizados para tarefas de processamento de linguagem natural (NLP).
* PyTorch: Para o backend do treinamento de modelos de deep learning.
* spaCy: Para o pré-processamento de texto e tokenização.
* Pandas e NumPy: Para manipulação de dados, análise e cálculos numéricos.
* Matplotlib: Para visualização de resultados e métricas de desempenho.

> Você pode acessar o Jupyter Notebook, responsável pela construção do modelo de análise de sentimentos em textos, que inclui toda a modelagem, treinamento e teste, clicando aqui: [SentimentAnalysis.ipynb](https://github.com/bpbastos/sentiment-analysis-ml-api/blob/main/machine-learning/notebooks/SentimentAnalysis.ipynb).

## 🛠️ TODO

- [ ] Implementar Autenticação OAuth 2.0
- [ ] Implementar testes de integração

## 📋 Pré-requisitos

Antes de começar, verifique se o seu ambiente atende aos seguintes requisitos:

> ATENÇÃO, este backend foi desenvolvido para rodar em conjunto com o frontend [Sentiment Analysis Frontend](https://github.com/bpbastos/sentiment-analysis-ml-front). 

* `Docker`

> Instalação do docker: https://docs.docker.com/engine/install/

* `Git Lfs`
  
`Primeiro instale o pacote git-fls:`
```
sudo apt-get install git-lfs
```

`Depois habilite usando o comando:`
```
git lfs install
```

> Como os modelos ficaram maiores que 100mb foi necessario fazer uso do git lfs.


## 📦 Rodando com docker

Faça clone do projeto:
```
git clone https://github.com/bpbastos/sentiment-analysis-ml-api
```

Acesse o diretório do projeto com:
```
cd sentiment-analysis-ml-api
```

Crie o diretório database e log:
```
mkdir database log
```

Para construir a imagem docker do projeto, execute:
```sh
docker compose build
```

Para rodar o projeto, execute:
```sh
docker compose up -d
```

Abra o endereço http://localhost:5000 no seu navegador.

## 🚀 Rodando sem docker 

Clone ou faça download do projeto :
```
git clone https://github.com/bpbastos/sentiment-analysis-ml-api
```

Acesse o diretório do projeto com:
```
cd sentiment-analysis-ml-api
```

Após clonar o repositório, será necessário fazer a instalação das dependencias da aplicação.
> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
pip install -r requirements.txt
```

No terminal execute o comando descrito abaixo baixar as stop words spacy:

```
python -m spacy download pt_core_news_sm
```


No terminal execute o comando descrito abaixo para executar a API:

```
flask run --host 0.0.0.0 --port 5000

```
Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução.

## ⚙️ Testando

No terminal execute o comando descrito abaixo para executar fazer os testes nos modelos/pipelines:

```
pytest -v
```




