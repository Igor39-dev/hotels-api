FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

# CMD ["python", "src/main.py"]
CMD ["sh", "-c", "alembic upgrade head && python src/main.py"]
