# Check-In History Endpoint

## Overview

`GET /relationships/{relationship_id}/checkins/history`

Returns a paginated list of check-ins for the senior in a given relationship, sorted by most recent first.

Only the **senior** or a **caregiver** that is part of the relationship may call this endpoint.

---

## Authentication

All requests require a valid JWT access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Obtain a token via `POST /auth/login`.

---

## Query Parameters

| Parameter | Type    | Default | Constraints | Description           |
|-----------|---------|---------|-------------|-----------------------|
| `page`    | integer | `1`     | `>= 1`      | Page number (1-based) |
| `limit`   | integer | `10`    | `1 – 100`   | Items per page        |

---

## Response

**200 OK**

```json
{
  "success": true,
  "message": "Check-in history retrieved",
  "data": {
    "items": [
      {
        "id": "dddddddd-dddd-dddd-dddd-dddddddddddd",
        "senior_id": "11111111-1111-1111-1111-111111111111",
        "status": "completed",
        "created_at": "2026-02-24T12:00:00Z"
      }
    ],
    "page": 1,
    "limit": 10,
    "total": 1
  }
}
```

If there are no check-ins, `items` will be an empty list and `total` will be `0`.

---

## Error Responses

| Status | Reason |
|--------|--------|
| `401`  | Missing or invalid token |
| `403`  | Authenticated user is not the senior or caregiver in this relationship |
| `404`  | Relationship ID does not exist |

---

## Manual Testing Guide

### 1. Start the stack

```bash
docker compose up -d
docker compose exec app alembic upgrade head
```

### 2. Register and log in

```bash
curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "phone_number": "555-0000",
    "password": "Password1"
  }'

curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Password1"}'
```

Copy the `access_token` from the login response and export it:

```bash
export TOKEN=<access_token>
```

### 3. Seed test data (optional — skip if already done)

```bash
cd backend && ./test_schema.sh
```

This creates a senior (`11111111-…`), three caregivers, a relationship (`aaaaaaaa-…`), and one completed check-in.

### 4. Test: 404 — relationship not found

```bash
curl -s "http://localhost:8000/relationships/00000000-0000-0000-0000-000000000000/checkins/history" \
  -H "Authorization: Bearer $TOKEN"
```

Expected:
```json
{"detail": "Relationship 00000000-0000-0000-0000-000000000000 not found"}
```

### 5. Test: 403 — user not in relationship

Using an account that is **not** the senior or caregiver in relationship `aaaaaaaa-…`:

```bash
curl -s "http://localhost:8000/relationships/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/checkins/history" \
  -H "Authorization: Bearer $TOKEN"
```

Expected:
```json
{"detail": "You do not have access to this relationship"}
```

### 6. Test: 200 — authorized user, with check-ins

First insert a relationship that includes your logged-in user as caregiver:

```bash
docker compose exec database psql -U admin -d senior_checkin -c "
INSERT INTO relationships (id, senior_id, caregiver_id, created_at)
VALUES (
  'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
  '11111111-1111-1111-1111-111111111111',
  '<your-user-uuid>',
  NOW()
) ON CONFLICT DO NOTHING;
"
```

Then call the endpoint:

```bash
curl -s "http://localhost:8000/relationships/eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee/checkins/history" \
  -H "Authorization: Bearer $TOKEN"
```

Expected:
```json
{
  "success": true,
  "message": "Check-in history retrieved",
  "data": {
    "items": [{ "id": "...", "senior_id": "...", "status": "completed", "created_at": "..." }],
    "page": 1,
    "limit": 10,
    "total": 1
  }
}
```

### 7. Test: pagination

```bash
# Page 1, 1 item per page
curl -s "http://localhost:8000/relationships/eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee/checkins/history?page=1&limit=1" \
  -H "Authorization: Bearer $TOKEN"

# Page 2 (empty if only 1 check-in exists)
curl -s "http://localhost:8000/relationships/eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee/checkins/history?page=2&limit=1" \
  -H "Authorization: Bearer $TOKEN"
```

### 8. Test: 200 — no check-ins (empty list)

Create a fresh senior with no check-ins, add a relationship, then call the endpoint.
`items` should be `[]` and `total` should be `0`.

---

## Interactive Docs

With the stack running, the full Swagger UI is available at:

```
http://localhost:8000/docs
```

Navigate to **relationships → GET /relationships/{relationship_id}/checkins/history**.
