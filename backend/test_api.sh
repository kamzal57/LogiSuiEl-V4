#!/bin/bash
# Integration test script for LogiSuiEl-V4 API

BASE_URL="http://localhost:8000"

echo "======================================"
echo "LogiSuiEl-V4 API Integration Tests"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local expected_code=$5
    
    echo -n "Testing: $name... "
    
    if [ "$method" == "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" == "$expected_code" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected HTTP $expected_code, got $http_code)"
        echo "Response: $body"
        ((FAILED++))
    fi
}

# Test 1: Health check
test_endpoint "Health Check" "GET" "/health" "" "200"

# Test 2: Root endpoint
test_endpoint "Root Endpoint" "GET" "/" "" "200"

# Test 3: Login with admin credentials
echo -n "Testing: Admin Login... "
response=$(curl -s -X POST "$BASE_URL/api/auth/token" -d "username=admin&password=admin")
TOKEN=$(echo $response | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('access_token', ''))" 2>/dev/null)

if [ ! -z "$TOKEN" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "Response: $response"
    ((FAILED++))
fi

# Test 4: Get current user
if [ ! -z "$TOKEN" ]; then
    echo -n "Testing: Get Current User... "
    response=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/auth/me")
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected HTTP 200, got $http_code)"
        ((FAILED++))
    fi
fi

# Test 5: List students (should be empty initially)
if [ ! -z "$TOKEN" ]; then
    echo -n "Testing: List Students... "
    response=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/students/")
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected HTTP 200, got $http_code)"
        ((FAILED++))
    fi
fi

# Test 6: Get dashboard
if [ ! -z "$TOKEN" ]; then
    echo -n "Testing: Dashboard... "
    response=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/dashboard/")
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected HTTP 200, got $http_code)"
        ((FAILED++))
    fi
fi

# Test 7: List configuration
if [ ! -z "$TOKEN" ]; then
    echo -n "Testing: Configuration... "
    response=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/config/")
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected HTTP 200, got $http_code)"
        ((FAILED++))
    fi
fi

echo ""
echo "======================================"
echo "Test Results"
echo "======================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "Total: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
