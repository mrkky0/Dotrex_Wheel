import token
import requests

# API URL'leri
REGISTER_URL = 'http://127.0.0.1:8000/api/register/'
LOGIN_URL = 'http://127.0.0.1:8000/api/login/'
LOGOUT_URL = 'http://127.0.0.1:8000/api/logout/'

# Kullanıcı bilgileri
username = 'xxxf'
email = 'xxxf@example.com'
password = 'xxxf'
password2 = 'xxxf'

def register():
    data = {
        'username': username,
        'email': email,
        'password': password,
        'password2': password2,
    }
    response = requests.post(REGISTER_URL, data=data)
    try:
        response.raise_for_status()  # HTTPError varsa raise edilir
        print("Response text:", response.text)
        print("Kayıt başarılı. Token:", response.json().get('token'))
        return response.json().get('token')
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
 
    return None

def login():
    data = {
        'username': username,
        'password': password,
    }
    response = requests.post(LOGIN_URL, data=data)
    try:
        response.raise_for_status()  # HTTPError varsa raise edilir
        print("Response text:", response.text)
        print("Giriş başarılı. Token:", response.json().get('token'))
        return response.json().get('token')
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
 
    return None

def logout(token):
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.post(LOGOUT_URL, headers=headers)
    try:
        response.raise_for_status()  # HTTPError varsa raise edilir
        print("Çıkış başarılı.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
 
if __name__ == "__main__":
    if token:
        logout(token)
        # login()
        # register()
