FROM python:3.10

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv install --system --deploy

COPY src/ /app/src/
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "src.app.app:app", "--host", "0.0.0.0", "--port", "8000"]
