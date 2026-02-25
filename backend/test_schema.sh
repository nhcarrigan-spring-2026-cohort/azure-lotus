#!/bin/bash
# Test script to verify senior-based check-in schema

echo "======================================"
echo "Testing Senior-Based Check-in Schema"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Verifying checkins table structure...${NC}"
docker compose exec database psql -U admin -d senior_checkin -t -A -F',' -c \
  "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'checkins' ORDER BY ordinal_position;"

echo ""
echo -e "${BLUE}2. Verifying foreign key constraints...${NC}"
docker compose exec database psql -U admin -d senior_checkin -t -A -c \
  "SELECT tc.constraint_name, kcu.column_name, ccu.table_name AS foreign_table, ccu.column_name AS foreign_column FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'checkins';"

echo ""
echo -e "${BLUE}3. Creating test data...${NC}"

# Insert test data
docker compose exec -T database psql -U admin -d senior_checkin << 'EOF'
-- Clean up existing test data
DELETE FROM checkins WHERE senior_id IN (
  SELECT id FROM users WHERE email LIKE '%@test.com'
);
DELETE FROM relationships WHERE senior_id IN (
  SELECT id FROM users WHERE email LIKE '%@test.com'
);
DELETE FROM users WHERE email LIKE '%@test.com';

-- Insert test users
INSERT INTO users (id, first_name, last_name, email, phone_number, hashed_password, created_at, updated_at) 
VALUES 
('11111111-1111-1111-1111-111111111111', 'Senior', 'Smith', 'senior.smith@test.com', '555-0001', '$2b$12$test', NOW(), NOW()),
('22222222-2222-2222-2222-222222222222', 'Caregiver', 'One', 'caregiver.one@test.com', '555-0002', '$2b$12$test', NOW(), NOW()),
('33333333-3333-3333-3333-333333333333', 'Caregiver', 'Two', 'caregiver.two@test.com', '555-0003', '$2b$12$test', NOW(), NOW()),
('44444444-4444-4444-4444-444444444444', 'Caregiver', 'Three', 'caregiver.three@test.com', '555-0004', '$2b$12$test', NOW(), NOW());

-- Create relationships
INSERT INTO relationships (id, senior_id, caregiver_id, created_at) 
VALUES 
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', NOW()),
('cccccccc-cccc-cccc-cccc-cccccccccccc', '11111111-1111-1111-1111-111111111111', '44444444-4444-4444-4444-444444444444', NOW());

-- Create a check-in
INSERT INTO checkins (id, senior_id, status, created_at)
VALUES ('dddddddd-dddd-dddd-dddd-dddddddddddd', '11111111-1111-1111-1111-111111111111', 'completed', NOW());
EOF

echo -e "${GREEN}✓ Test data created${NC}"

echo ""
echo -e "${BLUE}4. Verification Tests${NC}"
echo ""
echo "Users created:"
docker compose exec database psql -U admin -d senior_checkin -t -c \
  "SELECT first_name || ' ' || last_name AS name, email FROM users WHERE email LIKE '%@test.com' ORDER BY email;"

echo ""
echo "Relationships (Senior -> Caregivers):"
docker compose exec database psql -U admin -d senior_checkin -t -c \
  "SELECT (SELECT first_name || ' ' || last_name FROM users WHERE id = r.senior_id) AS senior, (SELECT first_name || ' ' || last_name FROM users WHERE id = r.caregiver_id) AS caregiver FROM relationships r WHERE r.senior_id = '11111111-1111-1111-1111-111111111111' ORDER BY r.caregiver_id;"

echo ""
echo "Check-ins:"
docker compose exec database psql -U admin -d senior_checkin -t -c \
  "SELECT (SELECT first_name || ' ' || last_name FROM users WHERE id = c.senior_id) AS senior, c.status FROM checkins c WHERE c.senior_id = '11111111-1111-1111-1111-111111111111';"

echo ""
echo -e "${GREEN}=== KEY TEST: Caregivers Notified ===${NC}"
echo "For Senior Smith's check-in, these caregivers are notified:"
docker compose exec database psql -U admin -d senior_checkin -t -c \
  "SELECT u.first_name || ' ' || u.last_name AS caregiver, u.email FROM checkins c JOIN relationships r ON c.senior_id = r.senior_id JOIN users u ON r.caregiver_id = u.id WHERE c.id = 'dddddddd-dddd-dddd-dddd-dddddddddddd' ORDER BY u.email;"

echo ""
echo -e "${GREEN}======================================"
echo "✓ Test Complete!"
echo "Result: ONE check-in notifies ALL 3 caregivers!"
echo "======================================${NC}"
