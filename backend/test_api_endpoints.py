"""Test API endpoints directly"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api"

# First, login to get token
login_data = {
    "username": "allanbruno",
    "password": "senha123"
}

print("1. Testing Login...")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"✅ Login successful! Token: {token[:20]}...")
else:
    print(f"❌ Login failed: {response.status_code} - {response.text}")
    exit(1)

# Headers with token
headers = {
    "Authorization": f"Bearer {token}"
}

print("\n2. Testing /suggestions endpoint...")
params = {
    "status": "pending",
    "category": "all",
    "dateRange": "all"
}
response = requests.get(f"{BASE_URL}/suggestions", headers=headers, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    suggestions = response.json()
    print(f"✅ Found {len(suggestions)} suggestions")
    for i, s in enumerate(suggestions[:3]):
        print(f"  - {s['type']}: {s['content'][:60]}...")
else:
    print(f"❌ Error: {response.text}")

print("\n3. Testing /suggestions/stats endpoint...")
response = requests.get(f"{BASE_URL}/suggestions/stats", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    stats = response.json()
    print("✅ Stats:")
    print(f"  - Total suggestions: {stats.get('total_suggestions')}")
    print(f"  - Days active: {stats.get('days_active')}")
    print(f"  - Total actions: {stats.get('total_actions')}")
    print(f"  - Acceptance rate: {stats.get('acceptance_rate', 0)*100:.1f}%")
else:
    print(f"❌ Error: {response.text}")

print("\n4. Testing /users/me endpoint...")
response = requests.get(f"{BASE_URL}/users/me", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    user_data = response.json()
    print(f"✅ User: {user_data.get('username')}")
    print(f"  - Created: {user_data.get('created_at')}")
else:
    print(f"❌ Error: {response.text}")