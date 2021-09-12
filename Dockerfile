FROM python:3.7-slim-bullseye

WORKDIR /code/stock-market-analysis

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]