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

> Você pode acessar o Jupyter Notebook, responsável pela construção do modelo de análise de sentimentos em textos, que inclui toda a análise exploratória de dados, modelagem, treinamento e teste, clicando aqui: [SentimentAnalysis.ipynb](https://github.com/bpbastos/sentiment-analysis-ml-api/blob/main/machine-learning/notebooks/SentimentAnalysis.ipynb).

> Esta API foi desenvolvida como uma parte do trabalho de conclusão do último módulo - Qualidade de Software, Segurança e Sistemas Inteligentes - da Pós-Graduação em Engenharia de Software da PUC-RIO. 

## 📋 Pré-requisitos

Antes de começar, verifique se o seu ambiente atende aos seguintes requisitos:

> ATENÇÃO, este backend foi desenvolvido para rodar em conjunto com o frontend [Sentiment Analysis Frontend](https://github.com/bpbastos/sentiment-analysis-frontend).
 Recomendo seguir as instruções contidas no README do repositório de implantação [Sentiment Analysis Deploy](https://github.com/bpbastos/sentiment-analysis-deploy) para garantir uma configuração adequada.

* `Docker`

> Instalação do docker: https://docs.docker.com/engine/install/

## 📦 Rodando com docker

Faça clone do projeto:
```
git clone https://github.com/bpbastos/sentiment-analysis-ml-api
```

Acesse o diretório do projeto com:
```
cd sentiment-analysis-ml-api
```

Para construir a imagem docker do projeto, execute:
```sh
docker build -t sentiment-analysis-ml-api:1.0 .
```

Para rodar o projeto, execute:
```sh
docker run -d -p 5000:5000 --name data sentiment-analysis-ml-api:1.0 
```

Abra o endereço http://localhost:5000 no seu navegador.

## 🚀 Rodando sem docker 

Clone ou faça download do projeto :
```
git clone https://github.com/bpbastos/sentiment-analysis-ml-api
```

Após clonar o repositório, será necessário fazer a instalação das dependencias da aplicação.
> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

No terminal execute o comando descrito abaixo para executar a API:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```
Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução.

## ⚙️ Testando

No terminal execute o comando descrito abaixo para executar fazer os testes nos modelos/pipelines:

```
(env)$ pytest
```




