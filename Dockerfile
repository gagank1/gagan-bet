FROM python:3.11.4

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "gunicorn", "--log-level=info", "app:app" ]
