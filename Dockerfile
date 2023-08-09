FROM python:3.11.4

WORKDIR /workspace
COPY requirements.txt .
# COPY app.py .
# COPY static .
# COPY worker.py .

RUN pip install -r requirements.txt

CMD [ "gunicorn", "app:app" ]