import json
import os

DATA_FILE = "app/data/users.json"

def get_users():
    """Load users from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def create_user(user_data):
    """Save user to JSON file"""
    users = get_users()
    user_data['id'] = len(users) + 1
    users.append(user_data)
    
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return user_data
