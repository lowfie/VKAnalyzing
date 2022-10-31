FROM python

COPY . /VkAnalyzing
WORKDIR /VkAnalyzing

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
