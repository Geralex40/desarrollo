import time #a;adir expiracion a los tokens
from typing import Dict 

import jwt #codificar los tokens
from decouple import config #

from database.db import conn
from app.model import usersDB

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
def sign_jwt(user_id: str,var1:dict) :
    Dict[str, str]
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token),insertDB(var1,token)
#para que no me lo guarde en la base de datos al ser un Login
def sign_jwtLogin(user_id: str,var1:dict) :
    Dict[str, str]
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
    
#funcion para hacer el insert en mi DB
def insertDB(var1,token:str):
    #guardar el toquen con el propio usuario
    print("el var1: ")
    print(var1)
    var1["TOKEN_USUARIO"]=token

    #hacer el insert
    conn.execute(usersDB.insert().values(var1))
    conn.commit()