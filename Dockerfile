FROM python:3.11.4

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD [ "/bin/bash" ]
