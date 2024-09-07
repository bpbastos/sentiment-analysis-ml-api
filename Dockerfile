FROM python:3.10.12-slim 

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download pt_core_news_sm
RUN mkdir database
RUN mkdir log

COPY . .

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]