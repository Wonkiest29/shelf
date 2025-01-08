import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = 'your_secret_key'

def check_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except ExpiredSignatureError:
        return "Token has expired"
    except InvalidTokenError:
        return "Invalid token"

# Example usage
if __name__ == "__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJpZCI6IjY3N2U0ZmE5ZTA3YTZkZTE3Zjk1NWVmZSIsImV4cCI6MTczNjM1NTk4NH0.GZm-aPcISVrZHv_MeenaampJWq-JJk2g1VbJUfkYqG4"
    result = check_jwt(token)
    print(result)