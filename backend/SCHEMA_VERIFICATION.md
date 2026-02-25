# Schema Verification Guide

## Quick Schema Check

### 1. Check all tables
```bash
docker compose exec database psql -U admin -d senior_checkin -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
```

Expected tables:
- `alembic_version`
- `alerts`
- `checkins`
- `relationships`
- `users`

### 2. Check checkins table structure
```bash
docker compose exec database psql -U admin -d senior_checkin -t -A -F',' -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'checkins' ORDER BY ordinal_position;"
```

Expected columns:
- `status,character varying`
- `created_at,timestamp without time zone`
- `id,uuid`
- `senior_id,uuid` ← **KEY: This changed from relationship_id**

### 3. Check foreign keys
```bash
docker compose exec database psql -U admin -d senior_checkin -t -c "SELECT tc.constraint_name, kcu.column_name, ccu.table_name, ccu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'checkins';"
```

Expected:
```
checkins_senior_id_fkey | senior_id | users | id
```

## Full Test

Run the comprehensive test script:
```bash
cd backend
./test_schema.sh
```

This creates test data and demonstrates that:
- ✓ One senior can have multiple caregivers (relationships)
- ✓ One check-in for a senior reaches all their caregivers
- ✓ No need for multiple check-ins per relationship

## Manual SQL Test

You can also test manually:

```bash
docker compose exec database psql -U admin -d senior_checkin
```

Then run SQL:
```sql
-- See all relationships for a senior
SELECT 
    (SELECT first_name || ' ' || last_name FROM users WHERE id = r.senior_id) AS senior,
    (SELECT first_name || ' ' || last_name FROM users WHERE id = r.caregiver_id) AS caregiver
FROM relationships r
WHERE r.senior_id IN (SELECT id FROM users WHERE email LIKE '%@test.com')
ORDER BY r.senior_id, r.caregiver_id;

-- See which caregivers get notified for a check-in
SELECT 
    c.id AS checkin_id,
    (SELECT first_name || ' ' || last_name FROM users WHERE id = c.senior_id) AS senior,
    u.first_name || ' ' || u.last_name AS caregiver_notified,
    u.email AS caregiver_email
FROM checkins c
JOIN relationships r ON c.senior_id = r.senior_id
JOIN users u ON r.caregiver_id = u.id
WHERE c.senior_id IN (SELECT id FROM users WHERE email LIKE '%@test.com')
ORDER BY c.id, u.email;
```

## Clean Up Test Data

To remove test data:
```bash
docker compose exec database psql -U admin -d senior_checkin -c "
DELETE FROM checkins WHERE senior_id IN (SELECT id FROM users WHERE email LIKE '%@test.com');
DELETE FROM relationships WHERE senior_id IN (SELECT id FROM users WHERE email LIKE '%@test.com');
DELETE FROM users WHERE email LIKE '%@test.com';
"
```

## Migration History

Check applied migrations:
```bash
docker compose exec database psql -U admin -d senior_checkin -c "SELECT * FROM alembic_version;"
```

Current version should be: `a3f8d2e1b7c9` (drop priority from relationships)
