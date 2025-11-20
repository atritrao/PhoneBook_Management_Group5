FROM python:3.13-slim

WORKDIR /app

COPY SourceCode/ .

RUN pip install pytest

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]