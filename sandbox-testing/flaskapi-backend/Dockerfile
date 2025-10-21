FROM python:3.13-slim-bookworm AS pythonflaskbuilder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

FROM python:3.13.9-alpine3.21

WORKDIR /app

COPY --from=pythonflaskbuilder /app/app.py .
COPY --from=pythonflaskbuilder /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

ENV FLASK_APP=/app/app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]