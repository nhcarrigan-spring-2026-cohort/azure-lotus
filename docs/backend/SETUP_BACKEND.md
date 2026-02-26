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

#### 6.1 Verify Database Schema

##### Quick verification of table structure:

```bash
docker compose exec database psql -U admin -d senior_checkin -c "
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND (
    (table_name = 'users' AND column_name IN ('id')) OR
    (table_name = 'relationships' AND column_name IN ('id','senior_id','caregiver_id')) OR
    (table_name = 'checkins' AND column_name IN ('id','senior_id')) OR
    (table_name = 'alerts' AND column_name IN ('id','checkin_id'))
  )
ORDER BY table_name, column_name;
"
```

Expected: all listed IDs should show `data_type = uuid`.

#### 6.2 Seed baseline data

```bash
docker compose exec -e PYTHONPATH=/app app python src/scripts/seed.py
```

#### 6.3 Verify seeded data

```bash
docker compose exec database psql -U admin -d senior_checkin -c "SELECT COUNT(*) AS users_count FROM users;"
docker compose exec database psql -U admin -d senior_checkin -c "SELECT COUNT(*) AS relationships_count FROM relationships;"
docker compose exec database psql -U admin -d senior_checkin -c "SELECT COUNT(*) AS checkins_count FROM checkins;"
docker compose exec database psql -U admin -d senior_checkin -c "SELECT COUNT(*) AS alerts_count FROM alerts;"
```

Expected: `users_count >= 2`, and other counts `>= 1`.


##### Comprehensive schema test:

Run the test script to verify the senior-based check-in schema:

```bash
cd backend
./test_schema.sh
```

This will:
1. ✓ Verify `checkins` table has `senior_id` column (not `relationship_id`)
2. ✓ Verify foreign key: `checkins.senior_id` → `users.id`
3. ✓ Create test data: 1 senior with 3 caregivers
4. ✓ Create 1 check-in for the senior
5. ✓ Demonstrate that ONE check-in notifies ALL caregivers

**Expected output:**
```
=== KEY TEST: Caregivers Notified ===
For Senior Smith's check-in, these caregivers are notified:
 Caregiver One   | caregiver.one@test.com
 Caregiver Three | caregiver.three@test.com
 Caregiver Two   | caregiver.two@test.com

✓ Test Complete!
Result: ONE check-in notifies ALL 3 caregivers!
```

##### Manual verification of checkins table:

```bash
docker compose exec database psql -U admin -d senior_checkin -c "\d checkins"
```

Expected columns:
- `id` (uuid, primary key)
- `senior_id` (uuid, foreign key to users.id)
- `status` (character varying)
- `created_at` (timestamp)

[More About Migration](
    https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

#### 7. Run the Backend (FastAPI)

```
uvicorn src.main:app --reload
```
