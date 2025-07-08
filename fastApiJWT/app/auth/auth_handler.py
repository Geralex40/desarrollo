import time #a;adir expiracion a los tokens
from typing import Dict 

import jwt #codificar los tokens
from decouple import config #

#el arreglo de usuarios para hacer query
#from api import queryUser 


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

#me regresa el token generado
def token_response(token: str):
    
    return {
        "access_token": token
    }

#firmar el JWT
#no esta encriptado, cualquiera lo puede ver, pero el servidor asi garantisa con su firma que es suyo
def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

#decodificar el token
#asi sabemos que en efecto nosotros lo hicimos en primer lugar
def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
