FROM python:3.7-slim-bullseye

WORKDIR /code/stock-market-analysis

# Install vim
RUN apt-get update && apt-get install apt-file -y && apt-file update && apt-get install vim -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]