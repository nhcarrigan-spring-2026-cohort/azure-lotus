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

---

## API Endpoints

The backend runs at `http://localhost:8000` (Docker) or `http://localhost:8000` (local uvicorn).  
Interactive docs: **http://localhost:8000/docs**

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

---

### Auth — `/auth`

#### Register
```
POST /auth/register
```
**Body:**
```json
{
  "email": "user@example.com",
  "password": "Password1!",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone_number": "1234567890"
}
```
**Returns:** `201` with user object.

---

#### Login
```
POST /auth/login
```
**Body:**
```json
{
  "email": "user@example.com",
  "password": "Password1!"
}
```
**Returns:** `200` with `access_token` and sets `refresh_token` httponly cookie.

**Response shape:**
```json
{
  "user_info": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "Jane",
    "phone_number": "1234567890"
  },
  "access_token": "<jwt>"
}
```

---

#### Logout
```
POST /auth/logout
```
**Header:** `Authorization: Bearer <token>`  
**Returns:** `200`, clears the `refresh_token` cookie.

---

#### Refresh Access Token
```
POST /auth/refresh
```
Requires the `refresh_token` cookie (set automatically on login).  
**Returns:** `200` with a new `access_token`.

---

### Relationships — `/relationships`

A **relationship** links a **caregiver** (the authenticated user who creates it) to a **senior** (looked up by email).

#### Add a Relationship (caregiver adds senior)
```
POST /relationships
```
**Header:** `Authorization: Bearer <caregiver_token>`  
**Body:**
```json
{
  "email": "senior@example.com"
}
```
**Returns:** `201`
```json
{
  "success": true,
  "message": "Relationship created",
  "data": { "id": "uuid", "senior_id": "uuid" }
}
```
**Errors:** `404` senior not found · `409` already exists / self-monitoring

---

#### View Seniors I Monitor (caregiver POV)
```
GET /relationships/monitoring
```
**Header:** `Authorization: Bearer <caregiver_token>`  
**Returns:** `200` list of seniors the authenticated caregiver is monitoring.

---

#### View Caregivers Monitoring Me (senior POV)
```
GET /relationships/monitors
```
**Header:** `Authorization: Bearer <senior_token>`  
**Returns:** `200` list of caregivers monitoring the authenticated senior.

---

#### Delete a Relationship
```
DELETE /relationships/{relationship_id}
```
**Header:** `Authorization: Bearer <token>`  
**Returns:** `200`  
**Errors:** `404` not found · `403` not authorized

---

#### Get Check-in History for a Relationship
```
GET /relationships/{relationship_id}/checkins/history
```
**Header:** `Authorization: Bearer <token>`  
**Query params (optional):**
| Param | Default | Description |
|-------|---------|-------------|
| `offset` | `0` | Pagination offset |
| `limit` | `10` | Max results |
| `from_date` | — | `YYYY-MM-DD` start date filter |
| `to_date` | — | `YYYY-MM-DD` end date filter |

**Returns:** `200` paginated list of check-ins.  
**Errors:** `404` relationship not found · `403` not authorized

---

#### Get Missing Check-ins for a Relationship
```
GET /relationships/{relationship_id}/checkins/missing
```
Same auth and query params as history above.  
**Returns:** `200` list of dates where check-ins were missed.

---

#### Submit a Check-in for a Relationship (senior POV)
```
POST /relationships/{relationship_id}/checkins
```
**Header:** `Authorization: Bearer <senior_token>`  
**Body:**
```json
{
  "status": "ok",
  "notes": "Feeling great today!"
}
```
**Returns:** `201`  
**Errors:** `404` relationship not found · `403` you are not the senior in this relationship

---

### Check-ins — `/check_in`

These endpoints are scoped to the **authenticated senior** (no relationship ID needed).

#### Create Today's Check-in
```
POST /check_in
```
**Header:** `Authorization: Bearer <senior_token>`  
**Returns:** `201`
```json
{
  "success": true,
  "message": "Check-in created successfully",
  "data": { "id": "uuid", "senior_id": "uuid", "status": "pending", "created_at": "..." }
}
```
**Errors:** `400` check-in already exists for today

---

#### Get Today's Check-in
```
GET /check_in/today
```
**Header:** `Authorization: Bearer <senior_token>`  
**Returns:** `200` with today's check-in object, or `null` if none exists yet.

---

#### Mark a Check-in Complete
```
PUT /check_in/{checkin_id}/complete
```
**Header:** `Authorization: Bearer <senior_token>`  
**Returns:** `200` with updated check-in (status → `completed`, `completed_at` timestamp set).  
**Errors:** `404` not found · `403` you don't own this check-in

---

#### Trigger Emergency Alert
```
PUT /check_in/{checkin_id}/alert
```
**Header:** `Authorization: Bearer <senior_token>`  
**Returns:** `200` — sets check-in status to `alerted` and creates `Alert` records for all caregivers.  
**Errors:** `404` not found · `403` not your check-in · `400` already alerted

---

### Quick Test Flow

```bash
# 1. Register two users
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"senior@test.com","password":"Test1234!","first_name":"Senior","last_name":"Test","phone_number":"1111111111"}'

curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"caregiver@test.com","password":"Test1234!","first_name":"Care","last_name":"Giver","phone_number":"2222222222"}'

# 2. Login as caregiver, capture token
CAREGIVER_TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"caregiver@test.com","password":"Test1234!"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('access_token') or r['user_info']['access_token'])")

# 3. Caregiver adds senior as monitored
RELATIONSHIP=$(curl -s -X POST http://localhost:8000/relationships \
  -H "Authorization: Bearer $CAREGIVER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"senior@test.com"}')
echo $RELATIONSHIP
REL_ID=$(echo $RELATIONSHIP | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 4. Login as senior, capture token
SENIOR_TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"senior@test.com","password":"Test1234!"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('access_token') or r['user_info']['access_token'])")

# 5. Senior creates today's check-in
curl -s -X POST http://localhost:8000/check_in \
  -H "Authorization: Bearer $SENIOR_TOKEN"

# 6. Senior marks it complete
CHECKIN_ID=$(curl -s http://localhost:8000/check_in/today \
  -H "Authorization: Bearer $SENIOR_TOKEN" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

curl -s -X PUT http://localhost:8000/check_in/$CHECKIN_ID/complete \
  -H "Authorization: Bearer $SENIOR_TOKEN"

# 7. View check-in history (caregiver POV)
curl -s http://localhost:8000/relationships/$REL_ID/checkins/history \
  -H "Authorization: Bearer $CAREGIVER_TOKEN"
```

