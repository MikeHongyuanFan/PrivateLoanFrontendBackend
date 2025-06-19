import requests
import json

# API endpoint
login_url = "http://localhost:8000/api/token/"

# Login data - using the superuser credentials
login_data = {
    "email": "fanhongyuan897@gmail.com",
    "password": "admin"  # Try with a common default password
}

# Try to login
try:
    login_response = requests.post(login_url, json=login_data)
    print(f"Login response status: {login_response.status_code}")
    print(f"Login response: {login_response.text}")
    
    if login_response.status_code == 200:
        token = login_response.json().get("access")
        print(f"Access token: {token}")
    else:
        print("Login failed. Please check credentials.")
except Exception as e:
    print(f"Error: {str(e)}")
