import requests
from flask import current_app

def login_user(username, password):
    """Authenticate user with the backend API"""
    try:
        response = requests.post(
            f"{current_app.config['API_BASE_URL']}/login",
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                return True, data['token'], None
        
        return False, None, "Invalid credentials"
    
    except requests.RequestException as e:
        return False, None, f"Connection error: {str(e)}"

def get_acceleration_data(token):
    """Fetch user's acceleration data from the API"""
    try:
        response = requests.get(
            f"{current_app.config['API_BASE_URL']}/health/acceleration_data",
            headers={'Authorization': f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            return False, None, "Authentication failed or session expired"
        
        data = response.json()
        if data['status'] != 'success' or not data.get('data'):
            return False, None, data.get('message', 'No data available')
        
        return True, data['data'], None
    
    except requests.RequestException as e:
        return False, None, f"Connection error: {str(e)}"