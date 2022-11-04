FROM python:3.10

COPY . /VkAnalyzing
WORKDIR /VkAnalyzing

RUN pip install --upgrade pip &&  pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
