### SETUP BACKEND

#### 1. Clone the repository

```
git clone https://github.com/nhcarrigan-spring-2026-cohort/azure-lotus.git
cd azure-lotus
```

#### 2. Create a Virtual Environment

macOS/Linux
```
python -m venv .venv
source .venv/bin/activate
```

windows
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### 3. Install Dependencies

```
pip install -e ".[dev]"
```

#### 4. Create .env file
```
cp .sample.env .env
```

#### 5. Run Docker

```
docker compose up -d database
```

#### 6. Run migration

```
alembic upgrade head
```

[More Abour Migration](
    https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

#### 7. Run the Backend (FastAPI)

```
uvicorn src.main:app --reload
```
