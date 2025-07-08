#requests y endpoints

from fastapi import FastAPI, Body, Depends, HTTPException, status

from app.auth.auth_bearier import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.model import PostSchema, UserSchema, UserLoginSchema

import mysql.connector
import hashlib

#Conexxion a DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="fastApi2"
)
# Create a cursor object
cursor = mydb.cursor()

app = FastAPI()

#API
#listas de ejemplo
posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    },
    {
        "id": 2,
        "title": "Waffle",
        "content": "Lorem Ipsum ..."
    },
    {
        "id": 4,
        "title": "Sandvic",
        "content": "Lorem Ipsum ..."
    }
]

#Arreglo para los posts
users = []

#Arreglo para los querys
queryUser=[]
#funcion para pasar el arreglo users al formato de queryUser
#mejor manejarlo como json
def userToQuery():
    temp=[]
    for x in users:
        for y in x:
            temp.append(y)
    print(temp)
    for a in temp:
        queryUser.append(a)
        

#Que me actualize mi arreglo local de la tabla Usuario
def select_users():
    select_query = "SELECT NAME_USUARIO, EMAIL_USUARIO, CONTRASEÑA FROM usuario"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results
queryUser=select_users()
print(queryUser)

#primer endpoint
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}

#ver los posts
@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "data": posts }


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    #si el id que se manda en la url corresponde al id de nuestra lista ejemplo
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    #si no, significa que no es el mismo id. Esto solo funciona en casos especificos, esta mal
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

#FUncion para mandar post en este endpoint   
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }

#funcion para hacer un registro
@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    #arreglo para manejar las keys
    users.append(user) # replace with db call, making sure to hash the password first
    #print(users)
    print(users)
    #arreglo a medias para hacer el query
    userToQuery()
    
    print(queryUser)
    return sign_jwt(user.email)

#revisar si el usuario existe
def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

#endpoint para el logeo
@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_jwt(user.email)
    return {
        "error": "Wrong login details!"
    }

