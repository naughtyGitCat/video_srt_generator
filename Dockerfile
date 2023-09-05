FROM python:3.11-alpine
RUN pip install -r requirements.txt
WORKDIR /app

COPY . .

CMD python main.py