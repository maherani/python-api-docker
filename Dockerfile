
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#RUN pip install psycopg2-binary

COPY app/ /app/

RUN useradd -m appuser

USER appuser

EXPOSE 5000


# If using python directly
CMD ["python", "app.py"]

# OR if using flask CLI
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
