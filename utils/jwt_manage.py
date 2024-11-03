from jwt import encode, decode

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    print("validate_token_")
    data: dict = decode(token, key="my_secret_key", algorithms=["HS256"])
    return data