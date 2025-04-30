import json
import time
import jwt
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.auth import credentials
from google.oauth2 import service_account

def generate_jwt(service_account_json_path, audience):
    try:
        # Load the service account JSON file
        with open(service_account_json_path) as f:
            service_account_info = json.load(f)

        # Get the private key and client email from the service account info
        private_key = service_account_info['private_key']
        client_email = service_account_info['client_email']

        # Define JWT header and payload
        headers = {
            "alg": "RS256",
            "typ": "JWT"
        }
        
        # Prepare JWT payload
        now = int(time.time())
        payload = {
            "iss": client_email,  # Issuer is the service account email
            "sub": client_email,  # Subject is the service account email
            "aud": audience,      # Audience (your Google Cloud API)
            "iat": now,           # Issued at time
            "exp": now + 3600     # Expiry time (1 hour from issued time)
        }

        # Generate the JWT token
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256', headers=headers)

        return jwt_token
    except exceptions.GoogleAuthError as e:
        print(f"Error generating JWT: {e}")
        return None

# Example usage
service_account_json_path = 'your-service-account-file.json'
audience = 'https://language.googleapis.com/'  # Example for Google Cloud NLP API
jwt_token = generate_jwt(service_account_json_path, audience)

if jwt_token:
    print("Generated JWT Token: ")
    print(jwt_token)
