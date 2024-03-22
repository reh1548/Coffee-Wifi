FROM python:3.9-slim

WORKDIR /flask_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest

COPY app/main.py .

COPY tests/ app/tests/

EXPOSE 5008 

CMD [ "python", "main.py" ]