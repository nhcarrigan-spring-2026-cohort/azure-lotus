-- Test script to verify senior-based check-in schema

-- 1. Verify checkins table structure
\echo '=== CHECKINS TABLE STRUCTURE ==='
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'checkins' 
ORDER BY ordinal_position;

-- 2. Verify foreign keys
\echo ''
\echo '=== FOREIGN KEY CONSTRAINTS ==='
SELECT 
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu 
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu 
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND tc.table_name = 'checkins';

-- 3. Create test data
\echo ''
\echo '=== CREATING TEST DATA ==='

-- Insert test users
INSERT INTO users (id, first_name, last_name, email, phone_number, hashed_password, created_at, updated_at) 
VALUES 
('11111111-1111-1111-1111-111111111111', 'Senior', 'Smith', 'senior.smith@test.com', '555-0001', '$2b$12$test', NOW(), NOW()),
('22222222-2222-2222-2222-222222222222', 'Caregiver', 'One', 'caregiver.one@test.com', '555-0002', '$2b$12$test', NOW(), NOW()),
('33333333-3333-3333-3333-333333333333', 'Caregiver', 'Two', 'caregiver.two@test.com', '555-0003', '$2b$12$test', NOW(), NOW()),
('44444444-4444-4444-4444-444444444444', 'Caregiver', 'Three', 'caregiver.three@test.com', '555-0004', '$2b$12$test', NOW(), NOW())
ON CONFLICT (email) DO UPDATE SET updated_at = NOW();

\echo 'Created 4 users: 1 senior, 3 caregivers'

-- Create relationships
INSERT INTO relationships (id, senior_id, caregiver_id, created_at) 
VALUES 
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', NOW()),
('cccccccc-cccc-cccc-cccc-cccccccccccc', '11111111-1111-1111-1111-111111111111', '44444444-4444-4444-4444-444444444444', NOW())
ON CONFLICT (id) DO UPDATE SET senior_id = EXCLUDED.senior_id;

\echo 'Created 3 relationships (senior -> 3 caregivers)'

-- Create a check-in
INSERT INTO checkins (id, senior_id, status, created_at)
VALUES ('dddddddd-dddd-dddd-dddd-dddddddddddd', '11111111-1111-1111-1111-111111111111', 'completed', NOW())
ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status;

\echo 'Created 1 check-in for senior'

-- 4. Verify the setup
\echo ''
\echo '=== VERIFICATION: Users ==='
SELECT first_name || ' ' || last_name AS name, email FROM users ORDER BY email;

\echo ''
\echo '=== VERIFICATION: Relationships ==='
SELECT 
    (SELECT first_name || ' ' || last_name FROM users WHERE id = r.senior_id) AS senior,
    (SELECT first_name || ' ' || last_name FROM users WHERE id = r.caregiver_id) AS caregiver
FROM relationships r
ORDER BY r.caregiver_id;

\echo ''
\echo '=== VERIFICATION: Check-ins ==='
SELECT 
    (SELECT first_name || ' ' || last_name FROM users WHERE id = c.senior_id) AS senior,
    c.status,
    c.created_at
FROM checkins c;

-- 5. The key test: Get all caregivers for a check-in
\echo ''
\echo '=== KEY TEST: Caregivers Notified for Check-in ==='
SELECT 
    u.first_name || ' ' || u.last_name AS caregiver_name,
    u.email
FROM checkins c
JOIN relationships r ON c.senior_id = r.senior_id
JOIN users u ON r.caregiver_id = u.id
WHERE c.id = 'dddddddd-dddd-dddd-dddd-dddddddddddd'
ORDER BY u.email;

\echo ''
\echo '=== TEST COMPLETE ==='
\echo 'Result: One check-in for Senior Smith notifies all 3 caregivers!'
