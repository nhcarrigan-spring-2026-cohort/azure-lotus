FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Note: @T-Pushyamitra used pyproject.toml instead of requirements.txt
# We can install dependencies directly from the root
COPY pyproject.toml ./
RUN pip install . 

COPY . .
EXPOSE 8000
# Updated to point to his src.main:app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]