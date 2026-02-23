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
docker compose up -d
```

#### 6. Run migration

Use Docker Compose:

```bash
docker compose exec app alembic -c alembic.ini upgrade head
```

If running locally (without Docker app container):

```bash
alembic upgrade head
```

> If your local DB is out of sync, reset once and rerun:
```bash
docker compose down -v && docker compose up -d
docker compose exec app alembic -c alembic.ini upgrade head
```

#### 6.1 Verify UUID schema

```bash
docker compose exec database psql -U admin -d senior_checkin -c "
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND (
    (table_name = 'users' AND column_name IN ('id')) OR
    (table_name = 'relationships' AND column_name IN ('id','senior_id','caregiver_id')) OR
    (table_name = 'checkins' AND column_name IN ('id','relationship_id')) OR
    (table_name = 'alerts' AND column_name IN ('id','checkin_id'))
  )
ORDER BY table_name, column_name;
"
```

Expected: all listed IDs should show `data_type = uuid`.


[More Abour Migration](
    https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

#### 7. Run the Backend (FastAPI)

```
uvicorn src.main:app --reload
```
