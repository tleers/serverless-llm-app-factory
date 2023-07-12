FROM python:3.10
RUN pip install "poetry==1.5.1"

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

COPY apps/todo_extractor app
COPY pyproject.toml pyproject.toml
RUN poetry install --only main

# run the app!
EXPOSE 8080

ENTRYPOINT ["poetry", "run", "uvicorn", "app.todo_fastapi_r8:app", "--host", "0.0.0.0", "--port", "8080"]