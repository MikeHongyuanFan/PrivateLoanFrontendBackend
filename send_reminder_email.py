import requests
import json
from datetime import datetime, timedelta

# API endpoint
url = "http://localhost:8000/api/reminders/"

# Email data
data = {
    "recipient_type": "custom",
    "recipient_email": "fanhongyuan897@gmail.com",
    "send_datetime": (datetime.now() + timedelta(minutes=1)).isoformat(),
    "email_body": "This is a test email sent via the reminder API. The email configuration has been updated successfully.",
    "subject": "Test Email from Reminder API",
    "is_sent": False
}

# First, try to create a user if needed
try:
    register_url = "http://localhost:8000/api/users/"
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": "admin"
    }
    register_response = requests.post(register_url, json=register_data)
    print(f"Registration response: {register_response.status_code}")
except Exception as e:
    print(f"Registration error: {str(e)}")

# Try to login
try:
    login_url = "http://localhost:8000/api/token/"
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    login_response = requests.post(login_url, json=login_data)
    print(f"Login response: {login_response.status_code}")
    
    if login_response.status_code == 200:
        token = login_response.json().get("access")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Send POST request with authentication
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("Email reminder created successfully!")
        else:
            print(f"Failed to create reminder: {response.text}")
    else:
        print(f"Login failed: {login_response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
