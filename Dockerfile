FROM python:3.10

COPY . /VkAnalyzing
WORKDIR /VkAnalyzing

RUN pip install --upgrade pip &&  pip install -r requirements.txt
RUN python -m dostoevsky download fasttext-social-network-model

CMD ["python3", "main.py"]
