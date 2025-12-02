FROM python:3.13-slim

# Install Poetry
RUN pip install poetry

# Do not create virtualenv inside container
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Copy only dependency files first (cache optimization)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-interaction --no-root --no-ansi

# Copy the rest of your project
COPY . .

# Expose FastAPI port
EXPOSE 80

# Run the app
# poetry run uvicorn app.main:app --host 0.0.0.0 --port 80
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]